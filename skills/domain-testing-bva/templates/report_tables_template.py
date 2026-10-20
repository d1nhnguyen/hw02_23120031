"""Sinh bảng của report/<Feature>.md từ cases.py và evidence/<Feature>/*_results.json.
Chép vào scripts/<feature>/report_tables.py.   Dùng: python3 report_tables.py T32 T33 T42 …
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from report_lib import Feature  # noqa: E402

from cases import CASES, PREFIX  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

# Thứ tự bảng BVA: chuỗi = test case BV mới; tuple = điểm biên đã có trong Minimum Set (chỉ dẫn chiếu)
BV_ORDER = [("DT-02", "EC8 – độ dài 0"), "BV-01"]


def bugs_for(c, channel, verdict):
    """Ánh xạ test case Fail sang mã bug (theo điều khoản đặc tả bị vi phạm)."""
    return [] if verdict != "Fail" else ["<PREFIX>-B1"]


def web_actual(r, c):
    """Mô tả kết quả thực tế trên giao diện từ một dòng của web_results.json."""
    return "; ".join(r.get("notes", [])) or r["verdict"]


def api_actual(r, c):
    return f"HTTP {r.get('status')}; " + ("; ".join(r.get("notes", [])) or "đúng như mong đợi")


FEATURE = Feature(
    prefix=PREFIX, cases=CASES,
    fields=[("<field>", "<Nhãn cột>")],
    report=ROOT / "report" / "<Feature>.md", evidence=ROOT / "evidence" / "<Feature>", n_ec=32,
    bv_order=BV_ORDER, web_actual=web_actual, api_actual=api_actual, bugs_for=bugs_for,
)

if __name__ == "__main__":
    FEATURE.update(sys.argv[1:])
