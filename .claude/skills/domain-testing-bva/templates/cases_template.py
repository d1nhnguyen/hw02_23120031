"""Nguồn dữ liệu duy nhất của test case <FEATURE>: thiết kế (mục 3.2, 4.2, 6.2 của báo cáo) và dữ liệu cho runner.
Chép file này vào scripts/<feature>/cases.py rồi sửa phần đánh dấu <…>.

Chạy trực tiếp để xuất cases.json cho runner Node / Playwright.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from report_lib import MISSING  # noqa: E402,F401  (MISSING = trường không gửi / để trống)

PREFIX = "<PREFIX>"  # vd FR15, MOB – ID có tiền tố feature để không trùng khi gộp báo cáo
# Thông báo mong đợi và lớp đầu ra theo lý do từ chối
REJECT = {
    "<field>": ("báo <Trường> không hợp lệ", "EC<n>"),
}


def expected_text(expect, target, api):
    if expect == "accept":
        return "<Mô tả kết quả thành công kiểm chứng được>" + ("; API trả 2xx" if api else "") + " (EC<n>)"
    message, output = REJECT[target]
    return f"Từ chối, {message}; <dữ liệu giữ nguyên>" + ("; API trả 4xx" if api else "") + f" ({output})"


def case(short_id, expect, target, title, covers, *, api_only=False, web_only=False, note="", show=None,
         origin="AI", added=False, **data):
    channels = ["api"] if api_only else ["web"] if web_only else ["web", "api"]
    expected = expected_text(expect, target, "api" in channels) + (f"; {note}" if note else "")
    return {
        "id": f"{PREFIX}-{short_id}",
        "section": "GAP" if added else short_id[:2],  # DT: mục 3.2 · BV: mục 4.2 · GAP: mục 6.2
        "title": title,                                 # Action + Function + Condition
        "covers": covers,                               # vd "EC1, EC5, EC25" hoặc "EC5/EC10 – độ dài 256 (UB+1)"
        "expect": expect,                               # accept | reject | notfound | ui | …
        "target": target,                               # biến được nhắm tới = lý do từ chối mong đợi
        "expected": expected,
        "origin": origin,                               # AI | AI-sửa | SV
        "show": show or {},                             # hiển thị riêng, vd {"name": '`"A" * 256`'}
        "channels": channels,
        **{"<field_default>": "<giá trị hợp lệ mặc định>", **data},  # dữ liệu cụ thể của test case
    }


LONG = "A" * 256
assert len(LONG) == 256  # dữ liệu dài luôn tính bằng code + assert

CASES = [
    case("DT-01", "accept", "all", "Kiểm tra <chức năng> thành công với dữ liệu hợp lệ điển hình", "EC1, EC5, EC25"),
    case("DT-02", "reject", "<field>", "Kiểm tra <chức năng> bị từ chối khi <điều kiện>", "EC8, EC29", **{"<field>": ""}),
    case("BV-01", "reject", "<field>", "Kiểm tra <chức năng> bị từ chối khi <biến> dài 256 ký tự",
         "EC5/EC10 – độ dài 256 (UB+1)", show={"<field>": '`"A" * 256`'}, **{"<field>": LONG}),
]

BY_ID = {c["id"]: c for c in CASES}
assert len(BY_ID) == len(CASES)

if __name__ == "__main__":
    out = Path(__file__).with_name("cases.json")
    out.write_text(json.dumps(CASES, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(CASES)} test case -> {out}")
