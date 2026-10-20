"""Sinh các bảng của report/FR-15_Quan_ly_san_pham.md từ cases.py và file kết quả trong evidence/FR-15/.

Dùng: python3 report_tables.py T32 T33   (không truyền mã nào = sinh tất cả; danh sách mã: xem report_lib.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from report_lib import MISSING, Feature  # noqa: E402

from cases import CASES, PREFIX  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

BV_ORDER = [
    ("DT-05", "EC8 – Tên độ dài 0"),
    "BV-01", "BV-02", "BV-03", "BV-04", "BV-05", "BV-06", "BV-07", "BV-08", "BV-09", "BV-10",
    "BV-11", "BV-12",
    ("DT-08", "EC13 – Giá 0"),
    "BV-13", "BV-14", "BV-15", "BV-16", "BV-17",
    "BV-18", "BV-19",
    ("DT-01", "EC17 – Danh mục id 3 (UB)"),
    "BV-20",
    "BV-21", "BV-22",
    ("DT-15", "EC21 (Sửa) – id 3 (giá trị giữa)"),
    "BV-23", "BV-24", "BV-25", "BV-26",
    ("DT-30", "EC21 (Xóa) – id 5 (UB)"),
    "BV-27",
]


def display(c, key):
    v = c.get(key)
    if key == "op_vn":
        return v
    if key in ("price", "category_id", "pid") and isinstance(v, str) and v != MISSING:
        return f'`"{v}"`'  # chuỗi (khác kiểu số)
    return None


def bugs_for(c, ch, verdict):
    return [] if verdict != "Fail" else ["?"]


def web_actual(r, c):
    return r.get("summary", "")


def api_actual(r, c):
    return r.get("summary", "")


FEATURE = Feature(
    prefix=PREFIX, cases=CASES,
    fields=[("op_vn", "Thao tác"), ("pid", "Sản phẩm (id)"), ("name", "Tên"), ("price", "Giá"),
            ("category_id", "Danh mục")],
    report=ROOT / "report" / "FR-15_Quan_ly_san_pham.md", evidence=ROOT / "evidence" / "FR-15", n_ec=32,
    bv_order=BV_ORDER, web_actual=web_actual, api_actual=api_actual, bugs_for=bugs_for, display=display,
    na_text="Không áp dụng (giao diện không cho nhập giá trị này)",
)

if __name__ == "__main__":
    FEATURE.update(sys.argv[1:])
