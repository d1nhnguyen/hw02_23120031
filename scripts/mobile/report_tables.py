"""Sinh các bảng của report/Mobile_Dang_nhap.md từ cases.py và file kết quả trong evidence/Mobile/.
Kênh "Web" của khung báo cáo chung là kênh Mobile app (cột được đổi tên khi sinh bảng).

Dùng: python3 report_tables.py T32 T33   (không truyền mã nào = sinh tất cả; danh sách mã: xem report_lib.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from report_lib import Feature, code  # noqa: E402

from cases import CASES, PREFIX  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

BV_ORDER = [
    ("DT-01", "EC12 – 0 lần sai (LB)"),
    "BV-01", "BV-02",
    ("DT-13", "EC13 – 3 lần sai (LB của EC13)"),
    "BV-03", "BV-04",
    ("DT-13", "EC14 – 0 giây sau khi khóa"),
    "BV-05", "BV-06",
    ("DT-04", "EC15 – 35 giây"),
    ("DT-01", "EC7 – mật khẩu đúng độ dài"),
    "BV-07", "BV-08", "BV-09", "BV-10",
]


def display(c, key):
    if key == "pre":
        if not c["pre"]:
            return "–"
        parts, prev, n = [], None, 0
        for item in c["pre"] + [None]:
            if item == prev:
                n += 1
                continue
            if prev is not None:
                kind = "sai" if prev[1] != "Test1234!" else "đúng"
                parts.append(f"{n} × {kind} ({code(prev[1])})")
            prev, n = item, 1
        return " → ".join(parts)
    if key == "wait":
        return f"{c['wait']} giây" if c["wait"] else "–"
    return None


def bugs_for(c, ch, verdict):
    if verdict != "Fail":
        return []
    if c["email"] != c["email"].strip() or c["email"] != c["email"].lower():
        return ["MOB-B4"]
    if c["wait"] >= 30:
        return ["MOB-B3"]
    return ["MOB-B2"]


def lock_text(r):
    counter = r.get("login_attempts")
    text = f"bộ đếm = {counter}"
    if r.get("locked"):
        text += f", bị khóa đến {r['locked_until'][11:19]} UTC"
    return text


def web_actual(r, c):
    if r["verdict"] == "Blocked":
        return "; ".join(r["notes"])
    if r.get("success"):
        return ("Đăng nhập thành công, thanh tiêu đề hiện “Chào, Test User”, "
                + ("mở được Hồ sơ" if r.get("profile_opens") else "không mở được Hồ sơ") + f"; {lock_text(r)}")
    return f"Ở lại màn hình Đăng nhập, hiện “{r['message']}”; {lock_text(r)}"


def api_actual(r, c):
    if r["verdict"] == "Blocked":
        return "; ".join(r["notes"])
    return f"HTTP {r['status']} “{r['message']}”{', có token' if r.get('token') else ''}; {lock_text(r)}"


FEATURE = Feature(
    prefix=PREFIX, cases=CASES,
    fields=[("email", "Email"), ("password", "Mật khẩu"), ("pre", "Các lần thử trước (tiền điều kiện)"),
            ("wait", "Chờ trước lần thử")],
    report=ROOT / "report" / "Mobile_Dang_nhap.md", evidence=ROOT / "evidence" / "Mobile", n_ec=21,
    bv_order=BV_ORDER, web_actual=web_actual, api_actual=api_actual, bugs_for=bugs_for, display=display,
    web_label="Mobile",
)


def channel(c):
    return "Mobile, API"


FEATURE.channel = channel  # kênh hiển thị: Mobile app thay cho Web

if __name__ == "__main__":
    FEATURE.update(sys.argv[1:])
