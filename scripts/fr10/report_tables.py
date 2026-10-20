"""Sinh các bảng của report/FR-10_Trang_thai_don_hang.md từ cases.py và file kết quả trong evidence/FR-10/.

Dùng: python3 report_tables.py T32 T33   (không truyền mã nào = sinh tất cả; danh sách mã: xem report_lib.py)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from report_lib import Feature  # noqa: E402

from cases import CASES, PREFIX  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

BV_ORDER = [
    "BV-01",
    ("DT-01", "`pending`: d = +1 (UB – cạnh hợp lệ)"),
    ("DT-10", "`pending`: d = +2 (UB+1)"),
    "BV-02", "BV-03",
    ("DT-12", "`confirmed`: d = 0 (UB-1)"),
    ("DT-02", "`confirmed`: d = +1 (UB)"),
    "BV-04", "BV-05",
    ("DT-11", "`shipping`: d = −1 (UB-2)"),
    "BV-06",
    ("DT-03", "`shipping`: d = +1 (UB)"),
    "BV-07", "BV-08",
    ("DT-05", "Vùng được hủy {pending, confirmed} – Admin hủy `confirmed` (UB)"),
    ("DT-13", "Admin hủy `shipping` (UB+1, A1)"),
    ("DT-07", "User hủy `confirmed` (UB)"),
    ("DT-14", "User hủy `shipping` (UB+1)"),
    "BV-09", "BV-10", "BV-11", "BV-12", "BV-13", "BV-14", "BV-15",
    ("DT-01", "mã đơn 1 (LB)"),
    "BV-16", "BV-17", "BV-18", "BV-19", "BV-20",
]


def display(c, key):
    v = c.get(key)
    if key in ("actor_vn", "action_vn"):
        return v
    if key == "order":
        return f"`{v}`" if isinstance(v, str) else f"#{v}" if v is not None else "–"
    if key == "from_state":
        return f"`{v}`" if v else "–"
    if key == "status" and c["action"] != "status":
        return "–"
    return None


def bugs_for(c, ch, verdict):
    return [] if verdict != "Fail" else ["?"]


def web_actual(r, c):
    return r.get("summary", "")


def api_actual(r, c):
    return r.get("summary", "")


FEATURE = Feature(
    prefix=PREFIX, cases=CASES,
    fields=[("actor_vn", "Tác nhân"), ("action_vn", "Thao tác"), ("order", "Đơn"), ("from_state", "Trạng thái hiện tại"),
            ("status", "Giá trị `status`")],
    report=ROOT / "report" / "FR-10_Trang_thai_don_hang.md", evidence=ROOT / "evidence" / "FR-10", n_ec=30,
    bv_order=BV_ORDER, web_actual=web_actual, api_actual=api_actual, bugs_for=bugs_for, display=display,
    na_text="Không áp dụng (giao diện không có thao tác này)",
)

if __name__ == "__main__":
    FEATURE.update(sys.argv[1:])
