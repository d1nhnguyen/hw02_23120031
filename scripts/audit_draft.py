#!/usr/bin/env python3
"""Nháp bảng audit (mẫu AI-02, 1 hàng / artifact) từ lịch sử git.

Quy ước commit: `[<FEATURE>][B<n>] …` là output AI của một bước; `[<FEATURE>][B<n>-review] …` là phần sửa sau rà soát.
Commit `[skill]` / `[report]` (artifact không thuộc một bước) mỗi commit một hàng.
Verdict gợi ý: không có commit review → VALID; có commit review → INCOMPLETE (sinh viên xác nhận lại, đổi thành
INVALID nếu artifact bị loại bỏ). Cột lý do (ISTQB / slide) để trống cho sinh viên điền.

Có `--prompt-log`: cột (1) ghi lượt prompt gần nhất trước commit (đọc bảng mục lục của prompt_log.md).

Dùng: python3 audit_draft.py [đường_dẫn_repo] [--prompt-log ai/prompt_log.md] > ai/audit_draft.md
"""
import argparse
import re
import subprocess
from collections import OrderedDict
from pathlib import Path

STEP = {"B1": "Biến Input / Output", "B2": "Lớp tương đương", "B3": "Test case Minimum Set", "B4": "Test case BVA",
        "B5": "Thực thi + script", "B6": "AI gap analysis", "B7": "Nháp bug report"}
OTHER = {"skill": "Agent Skill", "report": "Báo cáo chung"}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def read_prompts(path):
    """[(số lượt, 'YYYY-MM-DD HH:MM', phiên, prompt rút gọn)] từ bảng mục lục của prompt_log.md."""
    rows = re.findall(r"^\| (\d+) \| (\d{4}-\d\d-\d\d \d\d:\d\d) \| `([^`]*)` \| (.*?) \|$",
                      Path(path).read_text(encoding="utf-8"), re.M)
    return [(int(n), when, sess, text.strip()) for n, when, sess, text in rows]


def _fmt_prompt(p):
    n, at, _, text = p
    short = text[:70].rstrip() + ("…" if len(text) > 70 else "")
    return f"lượt #{n} ({at[5:]}): «{short.replace('<', '&lt;')}»"


def prompt_before(prompts, when):
    earlier = [p for p in prompts if p[1] <= when]
    if not earlier:
        return f"xem prompt_log lúc {when}"
    cur = earlier[-1]
    if cur[3].startswith("<pasted_content") and len(earlier) >= 2 and earlier[-2][2] != cur[2]:
        prev = earlier[-2]
        return f"rà soát chéo Antigravity {_fmt_prompt(prev)} → áp dụng ở {_fmt_prompt(cur)}"
    return _fmt_prompt(cur)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--prompt-log")
    args = ap.parse_args()
    prompts = read_prompts(args.prompt_log) if args.prompt_log else []
    log = git(args.repo, "log", "--reverse", "--date=format:%Y-%m-%d %H:%M", "--format=%h|%ad|%s")
    artifacts = OrderedDict()
    for line in log.splitlines():
        sha, date, subject = line.split("|", 2)
        m = re.match(r"\[([^\]]+)\]\[(B\d)(-review)?\]\s*(.*)", subject)
        o = re.match(r"\[(%s)\]\s*(.*)" % "|".join(OTHER), subject)
        if m:
            feature, step, review, title = m.groups()
            key, label = (feature, step), f"{feature} {step} ({STEP.get(step, '')})"
        elif o:
            review, title = None, o.group(2)
            key, label = (sha,), OTHER[o.group(1)]
        else:
            continue
        a = artifacts.setdefault(key, {"label": label, "ai": [], "review": []})
        stat = git(args.repo, "show", "--stat", "--format=", sha).strip().splitlines()
        a["review" if review else "ai"].append((sha, date, title, stat[-1].strip() if stat else ""))
    print("| # | (1) Prompt + Công cụ | (2) Output AI | (3) Verdict gợi ý | (4) Lý do (slide / ISTQB) | (5) Bản sửa sau rà soát |")
    print("| --- | --- | --- | --- | --- | --- |")
    ag_reviews = [p for p in prompts if p[2] == "421e648d" and "fr-01" in p[3].lower()]
    row_num = 0
    for key, a in artifacts.items():
        row_num += 1
        ai = "<br>".join(f"`{s}` {d} – {t} ({st})" for s, d, t, st in a["ai"]) or "–"
        rv = "<br>".join(f"`{s}` {d} – {t} ({st})" for s, d, t, st in a["review"]) or "Không sửa"
        if a["review"] and prompts:
            rv = f"Theo {prompt_before(prompts, a['review'][0][1])}:<br>{rv}"
        verdict = "INCOMPLETE" if a["review"] else "VALID"
        when = a["ai"][0][1] if a["ai"] else a["review"][0][1]
        print(f"| {row_num} | Claude Code – {a['label']}; prompt: {prompt_before(prompts, when)} "
              f"| {ai} | {verdict} | | {rv} |")
        if key == ("FR-01", "B7") and ag_reviews:
            p = ag_reviews[0]
            nxt = next((q for q in prompts if q[0] == p[0] + 1), None)
            apply_ref = f" ở {_fmt_prompt(nxt)}" if nxt else ""
            row_num += 1
            print(f"| {row_num} | Google Antigravity (Gemini 4 Argon) – FR-01 Rà soát chéo (bảng, tên TC, mức chi tiết); "
                  f"prompt: {_fmt_prompt(p)} | Bản nhận xét rà soát FR-01 trong `ai/prompt_log.md` mục #{p[0]} "
                  f"(phát hiện G9–G16, gợi ý kiểm tra chữ có dấu `Đ`, `ă` từ mục 6.3) | VALID | | "
                  f"Sinh viên duyệt và chuyển sang Claude Code áp dụng{apply_ref} (commits `32f8ff9`…`b7b58bf`) |")


if __name__ == "__main__":
    main()
