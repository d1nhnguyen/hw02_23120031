#!/usr/bin/env python3
"""Nháp bảng audit (mẫu AI-02, 1 hàng / artifact) từ lịch sử git.

Quy ước commit: `[<FEATURE>][B<n>] …` là output AI của một bước; `[<FEATURE>][B<n>-review] …` là phần sinh viên sửa.
Verdict gợi ý: không có commit review → VALID; có commit review → INCOMPLETE (sinh viên xác nhận lại, đổi thành
INVALID nếu artifact bị loại bỏ). Cột lý do (ISTQB / slide) để trống cho sinh viên điền.

Dùng: python3 audit_draft.py [đường_dẫn_repo] > ai/audit_draft.md
"""
import re
import subprocess
import sys
from collections import OrderedDict

STEP = {"B1": "Biến Input / Output", "B2": "Lớp tương đương", "B3": "Test case Minimum Set", "B4": "Test case BVA",
        "B5": "Thực thi + script", "B6": "AI gap analysis", "B7": "Nháp bug report"}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def main(repo="."):
    log = git(repo, "log", "--reverse", "--date=format:%Y-%m-%d %H:%M", "--format=%h|%ad|%s")
    artifacts = OrderedDict()
    for line in log.splitlines():
        sha, date, subject = line.split("|", 2)
        m = re.match(r"\[([^\]]+)\]\[(B\d)(-review)?\]\s*(.*)", subject)
        if not m:
            continue
        feature, step, review, title = m.groups()
        a = artifacts.setdefault((feature, step), {"ai": [], "review": []})
        stat = git(repo, "show", "--stat", "--format=", sha).strip().splitlines()
        a["review" if review else "ai"].append((sha, date, title, stat[-1].strip() if stat else ""))
    print("| # | (1) Prompt + Công cụ | (2) Output AI | (3) Verdict gợi ý | (4) Lý do (slide / ISTQB) | (5) Bản SV sửa |")
    print("| --- | --- | --- | --- | --- | --- |")
    for i, ((feature, step), a) in enumerate(artifacts.items(), 1):
        ai = "<br>".join(f"`{s}` {d} – {t} ({st})" for s, d, t, st in a["ai"]) or "–"
        rv = "<br>".join(f"`{s}` {d} – {t} ({st})" for s, d, t, st in a["review"]) or "Không sửa"
        verdict = "INCOMPLETE" if a["review"] else "VALID"
        when = a["ai"][0][1] if a["ai"] else ""
        print(f"| {i} | Claude Code – {feature} {step} ({STEP.get(step, '')}); prompt: xem prompt_log lúc {when} "
              f"| {ai} | {verdict} | | {rv} |")


if __name__ == "__main__":
    main(*sys.argv[1:])
