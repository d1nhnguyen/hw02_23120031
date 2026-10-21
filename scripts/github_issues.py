#!/usr/bin/env python3
"""Nháp nội dung GitHub issue từ bugs/Bug_Report.md và điền số BUG-NN vào báo cáo sau khi sinh viên tạo issue.

Dùng:
  python3 scripts/github_issues.py draft          # -> bugs/issues/<Mã>.md (nội dung) + bugs/issues/README.md (tiêu đề, thứ tự)
  python3 scripts/github_issues.py fill           # đọc issue trên repo nhóm, điền cột Issue của Bug_Report.md và mục 7 các báo cáo
  python3 scripts/github_issues.py fill --shots   # thêm: chụp trang issue -> bugs/screenshots/BUG-NN_issue.png

Mỗi nội dung issue có dòng đánh dấu "Mã trong báo cáo HW02 (23120031): <Mã>" để `fill` tìm lại đúng issue
kể cả khi tiêu đề bị sửa. Chỉ đọc repo nhóm (gh issue list), không tạo / sửa issue.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "d1nhnguyen/eshop-sut"
BUGS = ROOT / "bugs" / "Bug_Report.md"
OUT = ROOT / "bugs" / "issues"
MARK = "Mã trong báo cáo HW02 (23120031):"
REPORTS = sorted((ROOT / "report").glob("*.md"))


def parse():
    text = BUGS.read_text(encoding="utf-8")
    env = re.search(r"^\*\*Môi trường chung:\*\* (.*)$", text, re.M).group(1)
    summary = {}
    for m in re.finditer(r"^\| (\w+-B\d+) \|[^|]*\| ([^|]*) \| (.*?) \| (Critical|Major|Minor|Trivial) \|", text, re.M):
        code, feature, title, severity = m.groups()
        summary[code] = {"fr": re.search(r"FR-\d+", feature).group(0), "title": title.strip(), "severity": severity}
    details = text[text.index("## Chi tiết"):text.index("## Ảnh trang GitHub Issues")]
    bugs, group_env = [], ""
    for block in re.split(r"^### ", details, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        m = re.match(r"(\w+-B\d+) – ", head)
        if not m:  # tiêu đề nhóm feature: đoạn "Môi trường: …" áp cho các bug phía sau
            note = re.search(r"^Môi trường: (.*)$", body, re.M)
            group_env = re.sub(r"^như FR-\d+; ", "", note.group(1)) if note else ""  # môi trường chung đã ghi ở trên
            group_env = " ".join(s for s in re.split(r"(?<=\.) ", group_env) if "Tiêu đề issue" not in s)
            continue
        code = m.group(1)
        body = re.sub(r"^!\[[^\]]*\]\([^)]*\)\n?", "", body.strip(), flags=re.M).strip()
        evidence = re.search(r"^\*\*Bằng chứng:\*\* .*$", body, re.M).group(0)
        shots = ", ".join(f"`{f}`" for f in re.findall(r"bugs/screenshots/[\w.-]+\.png", evidence))
        body = body.replace(evidence, f"**Bằng chứng:** _(kéo-thả ảnh {shots} vào đây)_")
        bugs.append({"code": code, **summary[code], "env": env + (" " + group_env if group_env else ""), "body": body})
    assert len(bugs) == len(summary), (len(bugs), len(summary))
    return bugs


def gh_issues():
    out = subprocess.run(["gh", "issue", "list", "-R", REPO, "--state", "all", "--limit", "500",
                          "--json", "number,title,body,url"], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def draft():
    bugs = parse()
    used = [int(n) for i in gh_issues() for n in re.findall(r"\[BUG-(\d+)\]", i["title"])]
    nxt = max(used, default=0) + 1
    OUT.mkdir(exist_ok=True)
    lines = [f"# Nội dung {len(bugs)} GitHub issue · repo `{REPO}`", "",
             f"Số BUG đề xuất bắt đầu từ BUG-{nxt:02d} (số lớn nhất trên repo lúc sinh: BUG-{nxt - 1:02d}). "
             "**Kiểm tra lại số mới nhất ngay trước khi tạo** – nếu bạn khác trong nhóm đã dùng, lấy số kế tiếp.", "",
             "Mỗi issue: dán tiêu đề, dán toàn bộ file nội dung vào ô mô tả, kéo-thả ảnh vào dòng **Bằng chứng**. "
             "Giữ nguyên dòng đầu (`" + MARK + " …`) để script điền lại số BUG vào báo cáo.", "",
             "| # | Mã | Mức độ | File nội dung |", "| --- | --- | --- | --- |"]
    titles = []
    for i, b in enumerate(bugs):
        (OUT / f"{b['code']}.md").write_text(
            f"**{MARK}** {b['code']}\n\n**Môi trường:** {b['env']}\n\n{b['body']}\n", encoding="utf-8")
        lines.append(f"| {i + 1} | {b['code']} | {b['severity']} | [{b['code']}.md]({b['code']}.md) |")
        titles.append(f"[BUG-{nxt + i:02d}] [{b['fr']}] {b['title']}")
    lines += ["", "Tiêu đề (theo đúng thứ tự bảng trên):", "", "```text", *titles, "```", ""]
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(bugs)} issue -> {OUT}")


def set_issue_cell(path, code, link, col):
    """Ghi link issue vào cột `col` (0-based, -1 = cột cuối) của dòng bảng bắt đầu bằng `| <code> |`."""
    text = path.read_text(encoding="utf-8")
    out = []
    for line in text.split("\n"):
        if line.startswith(f"| {code} |"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]  # ô bảng không chứa "|"
            cells[col] = link
            line = "| " + " | ".join(cells) + " |"
        out.append(line)
    path.write_text("\n".join(out), encoding="utf-8")


def fill(shots=False):
    bugs = parse()
    issues = gh_issues()
    found = {}
    for b in bugs:
        hit = [i for i in issues if re.search(rf"{re.escape(MARK)}\**\s*{b['code']}\b", i["body"] or "")]
        hit = hit or [i for i in issues if i["title"].endswith(b["title"]) and f"[{b['fr']}]" in i["title"]]
        if len(hit) != 1:
            print(f"{b['code']}: {'chưa tìm thấy issue' if not hit else 'nhiều issue khớp: ' + str([i['number'] for i in hit])}")
            continue
        bug = re.search(r"\[BUG-(\d+)\]", hit[0]["title"])
        if not bug:
            print(f"{b['code']}: tiêu đề issue #{hit[0]['number']} thiếu [BUG-NN]")
            continue
        found[b["code"]] = (f"BUG-{bug.group(1)}", hit[0]["url"])
    for code, (bug, url) in found.items():
        set_issue_cell(BUGS, code, f"[{bug}]({url})", 1)
        for report in REPORTS:
            set_issue_cell(report, code, f"[{bug}]({url})", -1)
    print(f"đã điền {len(found)} / {len(bugs)} issue")
    if shots and found:
        targets = [{"bug": bug, "code": code, "url": url} for code, (bug, url) in found.items()]
        subprocess.run(["node", str(ROOT / "scripts" / "issue_shots.mjs"), json.dumps(targets)], check=True)
        text = BUGS.read_text(encoding="utf-8")
        head = text[:text.index("## Ảnh trang GitHub Issues")]
        body = ["## Ảnh trang GitHub Issues", ""]
        for t in targets:
            body += [f"### {t['bug']} ({t['code']})", "", f"![{t['bug']}](screenshots/{t['bug']}_issue.png)", ""]
        BUGS.write_text(head + "\n".join(body), encoding="utf-8")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "draft":
        draft()
    elif cmd == "fill":
        fill(shots="--shots" in sys.argv)
    else:
        sys.exit(__doc__)
