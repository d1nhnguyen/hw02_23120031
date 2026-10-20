"""Sinh các bảng của report/FR-01_Dang_ky.md từ cases.py và file kết quả trong evidence/FR-01/.

Dùng: python3 report_tables.py T32 T33   (không truyền mã nào = sinh tất cả; danh sách mã: xem report_lib.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from report_lib import Feature  # noqa: E402

from cases import CASES, PREFIX  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FIELD_VN = {"name": "Họ Tên", "email": "Email", "password": "Mật khẩu", "confirm": "Xác nhận mật khẩu"}

# Thứ tự bảng BVA: test case BV mới xen với các điểm biên đã có trong Minimum Set (dẫn chiếu, không chạy lại)
BV_ORDER = [
    ("DT-19", "EC17 – độ dài 0"),
    "BV-01", "BV-02",
    ("DT-20", "EC19 – độ dài 6 (UB-1)"),
    "BV-03",
    ("DT-01", "EC19/EC18 – độ dài 8 (LB của EC18); EC20, EC24, EC26 – đúng 1 chữ hoa, 1 chữ số, 1 ký tự đặc biệt (LB); "
              "số khoảng trắng đầu email = 0"),
    "BV-04", "BV-05",
    ("DT-21", "EC21 – 0 chữ hoa; `@`/`A` (`@` là ký tự liền trước `A`, LB-1 chữ hoa)"),
    ("DT-22", "EC23 – 0 chữ thường"),
    ("DT-23", "EC25 – 0 chữ số"),
    ("DT-24", "EC27 – 0 ký tự đặc biệt"),
    "BV-06", "BV-07", "BV-08", "BV-09", "BV-10", "BV-11", "BV-12", "BV-13",
    ("DT-08", "EC3 – Họ Tên độ dài 0"),
    "BV-14", "BV-15", "BV-16", "BV-17", "BV-18", "BV-19", "BV-20", "BV-21",
]


def display(c, key):
    # Xác nhận mật khẩu dài: hiển thị cùng công thức với Mật khẩu
    if key == "confirm" and c["confirm"] == c["password"] and "password" in c["show"]:
        return c["show"]["password"]
    return None


def bugs_for(c, ch, verdict):
    if verdict != "Fail":
        return []
    t = c["target"]
    if ch == "web":
        if t == "confirm":
            return ["FR01-B2"]
        return ["FR01-B1"] if c["expect"] == "accept" or t == "password" else ["?"]
    if t == "name":
        return ["FR01-B3"] if c["name"] == "" else ["FR01-B9"]
    if t == "email":
        return ["FR01-B3"] if c["email"] == "" else ["FR01-B4"]
    if t == "dup":
        return ["FR01-B6"] + (["FR01-B8"] if c["email"] != c["email"].strip() else [])
    if t == "password" and c["expect"] == "reject":
        return ["FR01-B3"] if c["password"] == "" else ["FR01-B5"]
    if t == "mixed":
        return ["FR01-B8"]
    return ["?"]


def first_sentence(text):
    return text.split("!")[0] + "!" if "!" in text else text


def web_actual(r, c):
    parts = []
    if r["target"] == "confirm" and not r["confirm_field"]:
        parts.append("không có ô Xác nhận mật khẩu")
    if r["request_sent"]:
        parts.append(f"form gửi request, HTTP {r['status']}, chuyển tới `{r['url_after']}`")
    else:
        native = [m for m in r["messages"] if m["source"].startswith("native")]
        page = [m for m in r["messages"] if m["source"] == "page"]
        if native:
            parts.append(f"trình duyệt chặn ô {FIELD_VN[native[0]['reason']]}: “{native[0]['text']}”")
        elif page:
            parts.append(f"form báo “{first_sentence(page[0]['text'])}”, không gửi request")
        else:
            parts.append("không gửi request, không có thông báo")
    parts.append("tạo tài khoản" if r["created"] else "không tạo tài khoản")
    if r.get("login_ok") is not None and r["created"]:
        parts.append("đăng nhập được" if r["login_ok"] else "không đăng nhập được")
    text = "; ".join(parts)
    if r["verdict"] == "Blocked":
        text += " – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra"
    return text[0].upper() + text[1:]


def api_actual(r, c):
    body = r["body"]
    msg = (body.get("message") or body.get("error")) if isinstance(body, dict) else str(body)
    parts = [f"HTTP {r['status']} “{msg}”"]
    if r["created"]:
        parts.append(f"tạo thêm tài khoản trùng email (có {r['matching_accounts_after']} tài khoản cùng email)"
                     if c["duplicate_of"] else "tạo tài khoản")
    elif r["status"] == 200:
        parts.append("tài khoản lưu với email chưa bỏ khoảng trắng")
    else:
        parts.append("không tạo tài khoản")
    if r.get("login_ok") is not None:
        parts.append("đăng nhập được" if r["login_ok"] else "không đăng nhập được bằng email đã bỏ khoảng trắng")
    if r.get("seed_login_ok"):
        parts.append("tài khoản gốc vẫn đăng nhập được")
    return "; ".join(parts)


FEATURE = Feature(
    prefix=PREFIX, cases=CASES,
    fields=[("name", "Họ Tên"), ("email", "Email"), ("password", "Mật khẩu"), ("confirm", "Xác nhận")],
    report=ROOT / "report" / "FR-01_Dang_ky.md", evidence=ROOT / "evidence" / "FR-01", n_ec=46, bv_order=BV_ORDER,
    web_actual=web_actual, api_actual=api_actual, bugs_for=bugs_for, display=display,
    na_text="Không áp dụng (A8)", na_note=" (biến Xác nhận mật khẩu, A8)",
)

if __name__ == "__main__":
    FEATURE.update(sys.argv[1:])
