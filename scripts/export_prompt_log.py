#!/usr/bin/env python3
"""Trích prompt + output từ transcript Claude Code (.jsonl) thành ai/prompt_log.md.

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
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "ai" / "prompt_log.md"
# Nội dung do harness tự chèn vào tin nhắn, không phải chữ sinh viên gõ
HIDDEN_TAGS = re.compile(
    r"<(system-reminder|ide_selection|ide_opened_file|local-command-stdout|local-command-caveat)>.*?</\1>",
    re.S,
)
SLASH_CMD = re.compile(r"<command-name>(.*?)</command-name>.*?<command-args>(.*?)</command-args>", re.S)


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
            if o.get("isMeta") or o.get("isCompactSummary"):
                continue
            prompt = user_prompt(content)
            if not prompt:
                continue
            current = {
                "time": local_time(o["timestamp"]),
                "session": path.stem[:8],
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


def fence(text, lang):
    longest = max((len(m) for m in re.findall(r"`{3,}", text)), default=0)
    ticks = "`" * max(4, longest + 1)
    return f"{ticks}{lang}\n{text}\n{ticks}"


def render(interactions, generated_at):
    out = [
        "# Phụ lục A — Prompt log (trích tự động từ transcript Claude Code)",
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
            f"- **Công cụ AI:** Claude Code {it['version']} (VS Code extension), model `{it['model'] or 'n/a'}`",
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
    ap.add_argument("--sessions", nargs="*", help="tiền tố session id cần lấy (mặc định: tất cả)")
    ap.add_argument("--since", help="chỉ lấy lượt từ thời điểm này, GMT+7 (vd 2026-10-20T20:40)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    files = sorted(args.project_dir.glob("*.jsonl"))
    if args.sessions:
        files = [f for f in files if any(f.stem.startswith(s) for s in args.sessions)]
    interactions = sorted((it for f in files for it in parse_session(f)), key=lambda it: it["time"])
    if args.since:
        since = datetime.fromisoformat(args.since).replace(tzinfo=TZ)
        interactions = [it for it in interactions if it["time"] >= since]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(interactions, datetime.now(TZ)), encoding="utf-8")
    print(f"{len(interactions)} lượt từ {len({it['session'] for it in interactions})} phiên -> {args.out}")


if __name__ == "__main__":
    main()
