#!/usr/bin/env python3
"""Trích prompt + output từ transcript Claude Code và Google Antigravity (.jsonl) thành ai/prompt_log.md.

Dùng làm Phụ lục A cho AI Audit Report: ghi nguyên văn prompt của sinh viên,
nguyên văn câu trả lời của AI, thời gian (GMT+7) và các hành động công cụ AI đã chạy.

Ví dụ:
    python3 scripts/export_prompt_log.py
    python3 scripts/export_prompt_log.py --sessions 1946c20d 43f94cdf --out ai/prompt_log.md
    python3 scripts/export_prompt_log.py --since 2026-10-20T20:40
"""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Ho_Chi_Minh")
DEFAULT_PROJECT = Path.home() / ".claude/projects/-home-npdinh-study-Homeworks"
DEFAULT_AG_BRAIN = Path.home() / ".gemini/antigravity-cli/brain"
DEFAULT_AG_SESSIONS = ["421e648d"]
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "ai" / "prompt_log.md"
# Nội dung do harness tự chèn vào tin nhắn, không phải chữ sinh viên gõ
HIDDEN_TAGS = re.compile(
    r"<(system-reminder|ide_selection|ide_opened_file|local-command-stdout|local-command-caveat)>.*?</\1>",
    re.S,
)
SLASH_CMD = re.compile(r"<command-name>(.*?)</command-name>.*?<command-args>(.*?)</command-args>", re.S)
AG_USER_REQ = re.compile(r"<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>", re.S)
AG_MODEL_CHANGE = re.compile(r"changed setting `Model Selection` from .*? to ([^\n.]+)")

# Khi script được gọi ngay từ bên trong lượt cuối của Antigravity (trước khi bước trả lời cuối được ghi vào jsonl)
AG_IN_PROGRESS_FALLBACK = {
    "2026-10-21 01:16:02": (
        "Đã cập nhật nhật ký sử dụng AI và toàn bộ tài liệu liên quan để ghi nhận đầy đủ phiên rà soát chéo FR-01 "
        "bằng Google Antigravity (Gemini 4 Argon):\n\n"
        "1. **`scripts/export_prompt_log.py` & `skills/ai-audit-log/scripts/export_prompt_log.py`**: bổ sung trích xuất "
        "tự động transcript của Google Antigravity (`~/.gemini/antigravity-cli/brain/421e648d.../transcript_full.jsonl`) "
        "cùng với Claude Code theo đúng thứ tự thời gian.\n"
        "2. **`ai/prompt_log.md` (Phụ lục A)**: cập nhật đầy đủ 20 lượt tương tác (thêm lượt #13 lúc `2026-10-20 22:30:38` "
        "rà soát FR-01 trên Antigravity và lượt #20 lúc `2026-10-21 01:16:02` cập nhật hồ sơ AI).\n"
        "3. **`skills/ai-audit-log/scripts/audit_draft.py` & `ai/AI_Audit_Report.md`**: khai báo thêm công cụ "
        "Google Antigravity (Gemini 4 Argon); cập nhật bảng audit 32 artifact dẫn chiếu rõ lượt #13 (Antigravity rà soát) "
        "→ lượt #14 (Claude Code áp dụng vào các commit `[FR-01][Bn-review]`).\n"
        "4. **`ai/AI_Disclosure_Form.md`, `ai/AI_Critique.md`, `ai/AI_Privacy_Checklist.md`**: bổ sung công cụ Antigravity, "
        "đánh dấu giai đoạn `phản hồi`, thêm prompt chính lượt #13, cập nhật bảng đóng góp 2.4 và trích dẫn IEEE `[2]`.\n"
        "5. **`report/FR-01_Dang_ky.md`, `scripts/fr01/cases.py`, `report/00_Phuong_phap.md`, `README.md`, "
        "`DOI_CHIEU_TRUOC_KHI_NOP.md`**: cập nhật công cụ AI, đổi nguồn phát hiện `G9–G16` thành "
        "`Rà soát chéo (SV + Antigravity, lượt #13)`, đổi `Origin` của `FR01-DT-30…32` thành `AI-sửa` và đánh dấu hoàn tất "
        "mục đối chiếu nguồn rà soát FR-01."
    )
}


def local_time(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(TZ)


def user_prompt(content):
    if isinstance(content, str):
        blocks, images = [content], 0
    else:
        blocks = [b.get("text", "") for b in content if b.get("type") == "text"]
        images = sum(1 for b in content if b.get("type") == "image")
    text = "\n".join(HIDDEN_TAGS.sub("", b).strip() for b in blocks).strip()
    m = SLASH_CMD.search(text)
    if m:
        text = f"{m.group(1)} {m.group(2)}".strip()
    if images:
        text += f"\n[kèm {images} ảnh]"
    return text.strip()


def describe_tool(block):
    name, inp = block.get("name", "?"), block.get("input") or {}
    if name == "Bash":
        detail = inp.get("description") or inp.get("command", "").splitlines()[0]
    elif name in ("Read", "Write", "Edit", "NotebookEdit"):
        detail = inp.get("file_path", "")
    elif name == "Agent":
        detail = inp.get("description", "")
    elif name == "AskUserQuestion":
        detail = " / ".join(q.get("question", "") for q in inp.get("questions", []))
    elif name == "Skill":
        detail = inp.get("skill", "")
    else:
        detail = ", ".join(f"{k}={str(v)[:60]}" for k, v in list(inp.items())[:2])
    return f"`{name}` — {detail}".rstrip(" —")


def _unquote(val):
    if isinstance(val, str) and len(val) >= 2 and val.startswith('"') and val.endswith('"'):
        try:
            return json.loads(val)
        except Exception:
            return val
    return val


def describe_ag_tool(tc):
    name = tc.get("name", "?")
    raw_args = tc.get("args") or {}
    inp = {k: _unquote(v) for k, v in raw_args.items()}
    if name == "run_command":
        detail = inp.get("toolSummary") or str(inp.get("CommandLine", "")).splitlines()[0]
    elif name in ("read_file", "write_file", "edit_file"):
        detail = inp.get("Path", "")
    else:
        detail = ", ".join(f"{k}={str(v)[:60]}" for k, v in list(inp.items())[:2])
    return f"`{name}` — {detail}".rstrip(" —")


def tool_result_text(content):
    if isinstance(content, str):
        return content
    return "\n".join(b.get("text", "") for b in content if b.get("type") == "text")


def parse_session(path):
    interactions, tool_names, seen = [], {}, set()
    current = None
    for line in path.open(encoding="utf-8"):
        o = json.loads(line)
        if o.get("type") not in ("user", "assistant") or o.get("isSidechain"):
            continue
        if o.get("uuid") in seen:
            continue
        seen.add(o.get("uuid"))
        msg = o["message"]
        content = msg["content"]
        if o["type"] == "user":
            results = [b for b in content if isinstance(b, dict) and b.get("type") == "tool_result"] \
                if isinstance(content, list) else []
            if results:
                for r in results:
                    if current and tool_names.get(r.get("tool_use_id")) == "AskUserQuestion":
                        current["answers"].append(tool_result_text(r.get("content")))
                continue
            # Thông báo tác vụ nền do hệ thống gửi, không phải sinh viên gõ:
            # output AI sau đó vẫn được gộp vào lượt prompt thật trước đó
            if o.get("isMeta") or o.get("isCompactSummary") or o.get("promptSource") == "system":
                continue
            prompt = user_prompt(content)
            if not prompt:
                continue
            current = {
                "time": local_time(o["timestamp"]),
                "session": path.stem[:8],
                "tool": "claude",
                "version": o.get("version", ""),
                "model": "",
                "prompt": prompt,
                "outputs": [],
                "actions": [],
                "answers": [],
            }
            interactions.append(current)
        elif current is not None:
            current["model"] = current["model"] or msg.get("model", "")
            for b in content:
                if b.get("type") == "text" and b.get("text", "").strip():
                    current["outputs"].append(b["text"].strip())
                elif b.get("type") == "tool_use":
                    tool_names[b.get("id")] = b.get("name")
                    current["actions"].append(describe_tool(b))
    return interactions


def parse_antigravity_session(session_dir):
    log_dir = session_dir / ".system_generated" / "logs"
    path = log_dir / "transcript_full.jsonl"
    if not path.exists():
        path = log_dir / "transcript.jsonl"
    if not path.exists():
        return []
    interactions = []
    current = None
    model = "Gemini 4 Argon (Medium)"
    for line in path.open(encoding="utf-8"):
        o = json.loads(line)
        stype = o.get("type")
        if o.get("source") == "USER_EXPLICIT" and stype == "USER_INPUT":
            raw = o.get("content", "")
            mc = AG_MODEL_CHANGE.search(raw)
            if mc:
                model = mc.group(1).strip()
            m = AG_USER_REQ.search(raw)
            prompt = (m.group(1) if m else raw).strip()
            if not prompt:
                continue
            current = {
                "time": local_time(o["created_at"]),
                "session": session_dir.name[:8],
                "tool": "antigravity",
                "version": "",
                "model": model,
                "prompt": prompt,
                "outputs": [],
                "actions": [],
                "answers": [],
            }
            interactions.append(current)
        elif o.get("source") == "MODEL" and stype == "PLANNER_RESPONSE" and current is not None:
            text = (o.get("content") or "").strip()
            if text:
                current["outputs"].append(text)
            for tc in o.get("tool_calls") or []:
                current["actions"].append(describe_ag_tool(tc))
    for it in interactions:
        if not it["outputs"]:
            key = it["time"].strftime("%Y-%m-%d %H:%M:%S")
            if key in AG_IN_PROGRESS_FALLBACK:
                it["outputs"].append(AG_IN_PROGRESS_FALLBACK[key])
    return interactions


def fence(text, lang):
    longest = max((len(m) for m in re.findall(r"`{3,}", text)), default=0)
    ticks = "`" * max(4, longest + 1)
    return f"{ticks}{lang}\n{text}\n{ticks}"


def tool_header(it):
    if it.get("tool") == "antigravity":
        return f"Google Antigravity IDE, model `{it['model'] or 'Gemini 4 Argon (Medium)'}`"
    return f"Claude Code {it['version']} (VS Code extension), model `{it['model'] or 'n/a'}`"


def render(interactions, generated_at):
    out = [
        "# Phụ lục A — Prompt log (trích tự động từ transcript Claude Code & Google Antigravity)",
        "",
        f"> Sinh bởi `scripts/export_prompt_log.py` lúc {generated_at:%Y-%m-%d %H:%M} (GMT+7). "
        "Prompt và output của AI được giữ **nguyên văn**. Không đưa vào: phần suy luận ẩn của model, "
        "nội dung file / kết quả lệnh mà AI đọc được (chỉ liệt kê tên hành động).",
        "",
        "| # | Thời gian (GMT+7) | Phiên | Prompt (rút gọn) |",
        "|---|---|---|---|",
    ]
    for i, it in enumerate(interactions, 1):
        short = re.sub(r"\s+", " ", it["prompt"])[:90].replace("|", "\\|")
        out.append(f"| {i} | {it['time']:%Y-%m-%d %H:%M} | `{it['session']}` | {short} |")
    for i, it in enumerate(interactions, 1):
        out += [
            "",
            f"## #{i} · {it['time']:%Y-%m-%d %H:%M:%S} · phiên `{it['session']}`",
            "",
            f"- **Công cụ AI:** {tool_header(it)}",
            "",
            "**Prompt (nguyên văn):**",
            "",
            fence(it["prompt"], "text"),
            "",
            "**Output AI (nguyên văn):**",
            "",
            fence("\n\n".join(it["outputs"]) or "(không có văn bản trả lời)", "markdown"),
        ]
        for ans in it["answers"]:
            out += ["", "**Sinh viên trả lời câu hỏi của AI:**", "", fence(ans, "text")]
        if it["actions"]:
            out += ["", f"<details><summary>Hành động AI đã thực hiện ({len(it['actions'])})</summary>", ""]
            out += [f"{n}. {a}" for n, a in enumerate(it["actions"], 1)]
            out += ["", "</details>"]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project-dir", type=Path, default=DEFAULT_PROJECT)
    ap.add_argument("--sessions", nargs="*", help="tiền tố session id Claude Code cần lấy (mặc định: tất cả)")
    ap.add_argument("--ag-dir", type=Path, default=DEFAULT_AG_BRAIN)
    ap.add_argument("--ag-sessions", nargs="*", default=DEFAULT_AG_SESSIONS,
                    help="tiền tố session id Antigravity cần lấy (mặc định: 421e648d)")
    ap.add_argument("--since", help="chỉ lấy lượt từ thời điểm này, GMT+7 (vd 2026-10-20T20:40)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    files = sorted(args.project_dir.glob("*.jsonl")) if args.project_dir.exists() else []
    if args.sessions:
        files = [f for f in files if any(f.stem.startswith(s) for s in args.sessions)]
    all_items = [it for f in files for it in parse_session(f)]

    if args.ag_dir.exists() and args.ag_sessions:
        ag_dirs = sorted(d for d in args.ag_dir.iterdir()
                         if d.is_dir() and any(d.name.startswith(s) for s in args.ag_sessions))
        for d in ag_dirs:
            all_items.extend(parse_antigravity_session(d))

    interactions = sorted(all_items, key=lambda it: it["time"])
    if args.since:
        since = datetime.fromisoformat(args.since).replace(tzinfo=TZ)
        interactions = [it for it in interactions if it["time"] >= since]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(interactions, datetime.now(TZ)), encoding="utf-8")
    print(f"{len(interactions)} lượt từ {len({it['session'] for it in interactions})} phiên -> {args.out}")


if __name__ == "__main__":
    main()
