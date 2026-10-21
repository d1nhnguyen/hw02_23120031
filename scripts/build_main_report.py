#!/usr/bin/env python3
"""Gộp báo cáo chính report/Bao_cao_chinh.md từ phần phương pháp + 4 báo cáo feature, kết thúc bằng Mandatory Disclosure.

Nguồn vẫn là các file trong report/ (bảng được sinh bởi report_tables.py); chạy lại script này sau mỗi lần sửa nguồn.
Dùng: python3 scripts/build_main_report.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report"
PARTS = ["00_Phuong_phap.md", "FR-01_Dang_ky.md", "FR-10_Trang_thai_don_hang.md",
         "FR-15_Quan_ly_san_pham.md", "Mobile_Dang_nhap.md"]


def demote(text):
    """Hạ mọi tiêu đề một cấp (# → ##) để báo cáo gộp chỉ có một tiêu đề cấp 1."""
    return re.sub(r"^(#{1,5}) ", r"#\1 ", text, flags=re.M)


def section(md, heading):
    start = md.index(heading)
    end = md.find("\n## ", start + len(heading))
    return md[start + len(heading):end if end != -1 else None].strip()


def main():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    audit = (ROOT / "ai" / "AI_Audit_Report.md").read_text(encoding="utf-8")
    titles = [re.search(r"^# (.+)$", (REPORT / p).read_text(encoding="utf-8"), re.M).group(1) for p in PARTS]
    out = [
        "# Báo cáo chính · HW02 – Domain Testing trên EShop · 23120031",
        "",
        "Báo cáo gộp phần phương pháp và 4 báo cáo feature; mỗi feature gồm báo cáo Domain Testing (bước 1–3) "
        "và Boundary Value Analysis (bước 4), kết quả thực thi, AI gap analysis và bug. "
        "Bug chi tiết: `bugs/Bug_Report.md`; hồ sơ AI: thư mục `ai/`.",
        "",
        "## Mục lục",
        "",
        *[f"{i}. {t}" for i, t in enumerate(titles, 1)],
        f"{len(titles) + 1}. Khai báo sử dụng AI (Mandatory Disclosure)",
        "",
        "## Tổng hợp kết quả",
        "",
        # link trong README tính từ gốc repo; báo cáo gộp nằm trong report/
        demote(section(readme, "## Test summary")).replace("](report/", "](").replace("](bugs/", "](../bugs/"),
        "",
    ]
    for p in PARTS:
        out += [demote((REPORT / p).read_text(encoding="utf-8").strip()), ""]
    out += [
        "## Khai báo sử dụng AI (Mandatory Disclosure)",
        "",
        section(audit, "## 6. Mandatory Disclosure"),
        "",
        "Hồ sơ đi kèm: `ai/AI_Audit_Report.md` (AI Audit Report), `ai/AI_Disclosure_Form.md`, `ai/AI_Critique.md`, "
        "`ai/AI_Privacy_Checklist.md`, `ai/prompt_log.md` (Phụ lục A – prompt log có thời gian).",
        "",
    ]
    (REPORT / "Bao_cao_chinh.md").write_text("\n".join(out), encoding="utf-8")
    print(REPORT / "Bao_cao_chinh.md")


if __name__ == "__main__":
    main()
