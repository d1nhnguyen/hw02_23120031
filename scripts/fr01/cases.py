"""Nguồn dữ liệu duy nhất của test case FR-01: thiết kế (mục 3.2, 4.2, 6.2 của report/FR-01_Dang_ky.md)
và dữ liệu cho runner. `report_tables.py` sinh các bảng của báo cáo từ file này.

Chạy trực tiếp để xuất cases.json cho runner Web (Playwright).
"""
import json
from pathlib import Path

PREFIX = "FR01"
NAME, PASSWORD = "Nguyen Van A", "Abcdef1@"
SEED_EMAIL, SEED_PASSWORD = "test@eshop.com", "Test1234!"
SAME = None  # Xác nhận mật khẩu giống Mật khẩu

# Thông báo mong đợi và lớp đầu ra theo lý do từ chối (A7)
REJECT = {
    "name": ("báo thiếu Họ Tên", "EC42"),
    "email_missing": ("báo thiếu Email", "EC42"),
    "email": ("báo email sai định dạng", "EC43"),
    "dup": ("báo email đã tồn tại", "EC44"),
    "password_missing": ("báo thiếu Mật khẩu", "EC42"),
    "password": ("báo mật khẩu không đủ mạnh", "EC45"),
    "confirm_missing": ("báo thiếu Xác nhận mật khẩu hoặc không khớp", "EC42/EC46"),
    "confirm": ("báo xác nhận mật khẩu không khớp", "EC46"),
}


def email(short_id):
    return f"fr01.{short_id.lower().replace('-', '')}@example.com"


def case(short_id, expect, target, title, covers, *, name=NAME, mail=None, password=PASSWORD, confirm=SAME,
         web_only=False, duplicate_of=None, reason=None, note="", show=None, origin="AI", added=False):
    reason = reason or target
    channels = ["web"] if web_only else ["web", "api"]
    if expect == "accept":
        expected = ("Đăng ký thành công: Web chuyển tới trang Đăng nhập"
                    + ("; API trả `200` + `id`" if not web_only else "")
                    + "; đăng nhập được bằng email + mật khẩu vừa nhập (EC41)")
    else:
        message, output = REJECT[reason]
        expected = (f"Từ chối, {message}; không tạo tài khoản"
                    + ("; API trả 4xx" if not web_only else "")
                    + (f"; `{SEED_EMAIL} / {SEED_PASSWORD}` vẫn đăng nhập được" if duplicate_of else "")
                    + f" ({output})")
    if note:
        expected += f"; {note}"
    workaround = target in ("name", "email", "dup", "confirm")
    return {
        "id": f"{PREFIX}-{short_id}",
        "section": "GAP" if added else short_id[:2],  # DT: mục 3.2, BV: mục 4.2, GAP: mục 6.2
        "title": title,
        "covers": covers,
        "expect": expect,  # accept | reject
        # Biến mà test case nhắm tới; với test case reject đây cũng là lý do từ chối mong đợi (A7)
        "target": target,  # all | mixed | name | email | dup | password | confirm
        "expected": expected,
        "origin": origin,
        "name": name,
        "email": email(short_id) if mail is None else mail,
        "password": password,
        "confirm": password if confirm is SAME else confirm,
        "show": show or {},  # cách hiển thị giá trị dài trong báo cáo (công thức tạo chuỗi)
        "channels": channels,
        # Email đã tồn tại: kiểm tra tài khoản gốc không bị ghi đè
        "duplicate_of": duplicate_of,
        # Lượt chạy khảo sát trên Web (không tính verdict): form Web chặn mọi mật khẩu hợp lệ theo đặc tả và chỉ
        # nhận dấu cách làm "ký tự đặc biệt", nên thay "@" bằng dấu cách để quan sát cách Web xử lý các biến khác;
        # chỉ áp dụng cho test case không nhắm vào mật khẩu
        "web_workaround_password": password.replace("@", " ") if workaround else None,
        "web_workaround_confirm": (password.replace("@", " ") if confirm is SAME else confirm) if workaround else None,
    }


LONG_PASSWORD = "Abcdef1@" + "a" * 992
LONG_NAME = "A" * 1000
LONG_EMAIL = "a" * 64 + "@" + "b" * 63 + "." + "c" * 63 + "." + "d" * 57 + ".com"
assert len(LONG_PASSWORD) == 1000 and len(LONG_NAME) == 1000 and len(LONG_EMAIL) == 254

DUP = dict(password="Newpass1@", duplicate_of=SEED_EMAIL)

CASES = [
    # 3.2 – Minimum Set, valid
    case("DT-01", "accept", "all", "Kiểm tra đăng ký thành công với dữ liệu hợp lệ điển hình",
         "EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC29, EC37, EC41"),
    case("DT-02", "accept", "mixed",
         "Kiểm tra đăng ký thành công khi Họ Tên có dấu, Email có khoảng trắng đầu/cuối và Mật khẩu đủ 4 loại kèm thêm ký tự ngoài tập",
         "EC2, EC6, EC14, EC18, EC20, EC22, EC24, EC26, EC30, EC36, EC37, EC41", name="Nguyễn Thị Ánh", mail=" fr01.dt02@example.com ", password="Abc#def1$",
         note="email được lưu là `fr01.dt02@example.com` (A4)", origin="AI-sửa"),
    case("DT-03", "accept", "password", "Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất của Mật khẩu là `!`",
         "EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC31, EC37, EC41", password="Abcdef1!"),
    case("DT-04", "accept", "password", "Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất của Mật khẩu là `%`",
         "EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC32, EC37, EC41", password="Abcdef1%"),
    case("DT-05", "accept", "password", "Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất của Mật khẩu là `*`",
         "EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC33, EC37, EC41", password="Abcdef1*"),
    case("DT-06", "accept", "password", "Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất của Mật khẩu là `?`",
         "EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC34, EC37, EC41", password="Abcdef1?"),
    case("DT-07", "accept", "password", "Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất của Mật khẩu là `&`",
         "EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC35, EC37, EC41", password="Abcdef1&"),
    # 3.2 – Minimum Set, invalid
    case("DT-08", "reject", "name", "Kiểm tra đăng ký bị từ chối khi bỏ trống Họ Tên", "EC3, EC42", name=""),
    case("DT-09", "reject", "name", "Kiểm tra đăng ký bị từ chối khi Họ Tên chỉ gồm khoảng trắng", "EC4, EC42",
         name="   ", note="A4"),
    case("DT-10", "reject", "email", "Kiểm tra đăng ký bị từ chối khi bỏ trống Email", "EC7, EC42", mail="",
         reason="email_missing"),
    case("DT-11", "reject", "email", "Kiểm tra đăng ký bị từ chối khi Email thiếu ký tự `@`", "EC8, EC43",
         mail="fr01.dt11example.com"),
    case("DT-12", "reject", "email", "Kiểm tra đăng ký bị từ chối khi Email thiếu phần trước `@`", "EC9, EC43",
         mail="@example.com"),
    case("DT-13", "reject", "email", "Kiểm tra đăng ký bị từ chối khi Email thiếu phần domain sau `@`", "EC10, EC43",
         mail="fr01.dt13@"),
    case("DT-14", "reject", "email", "Kiểm tra đăng ký bị từ chối khi domain của Email không có dấu `.`", "EC11, EC43",
         mail="fr01.dt14@example", note="A2"),
    case("DT-15", "reject", "email", "Kiểm tra đăng ký bị từ chối khi Email có hai ký tự `@`", "EC12, EC43",
         mail="fr01@dt15@example.com"),
    case("DT-16", "reject", "email", "Kiểm tra đăng ký bị từ chối khi Email có khoảng trắng ở giữa", "EC13, EC43",
         mail="fr01 dt16@example.com"),
    case("DT-17", "reject", "dup", "Kiểm tra đăng ký bị từ chối khi Email đã tồn tại", "EC15, EC44",
         mail=SEED_EMAIL, **DUP),
    case("DT-18", "reject", "dup",
         "Kiểm tra đăng ký bị từ chối khi Email trùng tài khoản có sẵn nhưng khác chữ hoa / thường", "EC16, EC44",
         mail="TEST@eshop.com", note="A3", **DUP),
    case("DT-19", "reject", "password", "Kiểm tra đăng ký bị từ chối khi bỏ trống Mật khẩu", "EC17, EC42",
         password="", reason="password_missing"),
    case("DT-20", "reject", "password", "Kiểm tra đăng ký bị từ chối khi Mật khẩu ngắn hơn 8 ký tự", "EC19, EC45",
         password="Abcd1@"),
    case("DT-21", "reject", "password", "Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ hoa", "EC21, EC45",
         password="abcdef1@"),
    case("DT-22", "reject", "password", "Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ thường", "EC23, EC45",
         password="ABCDEF1@"),
    case("DT-23", "reject", "password", "Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ số", "EC25, EC45",
         password="Abcdefg@"),
    case("DT-24", "reject", "password", "Kiểm tra đăng ký bị từ chối khi Mật khẩu không có ký tự đặc biệt",
         "EC27, EC45", password="Abcdefg1"),
    case("DT-25", "reject", "password",
         "Kiểm tra đăng ký bị từ chối khi ký tự đặc biệt duy nhất của Mật khẩu nằm ngoài tập `@ $ ! % * ? &`",
         "EC28, EC45", password="Abcdef1#", note="A1"),
    case("DT-26", "reject", "confirm", "Kiểm tra đăng ký bị từ chối khi bỏ trống Xác nhận mật khẩu", "EC38, EC42",
         confirm="", web_only=True, reason="confirm_missing"),
    case("DT-27", "reject", "confirm", "Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu khác Mật khẩu", "EC39, EC46",
         confirm="Abcdef2@", web_only=True),
    case("DT-28", "reject", "confirm",
         "Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu chỉ khác Mật khẩu ở chữ hoa / thường", "EC40, EC46",
         confirm="abcdef1@", web_only=True),
    # 4.2 – Boundary Value Test Cases
    case("BV-01", "reject", "password", "Kiểm tra đăng ký bị từ chối khi Mật khẩu dài 1 ký tự",
         "EC17/EC19 – độ dài 1 (LB của EC19)", password="@"),
    case("BV-02", "reject", "password", "Kiểm tra đăng ký bị từ chối khi Mật khẩu dài 2 ký tự",
         "EC19 – độ dài 2 (LB+1)", password="A1"),
    case("BV-03", "reject", "password", "Kiểm tra đăng ký bị từ chối khi Mật khẩu dài 7 ký tự và đủ 4 loại ký tự",
         "EC19/EC18 – độ dài 7 (UB của EC19)", password="Abcde1@"),
    case("BV-04", "accept", "password", "Kiểm tra đăng ký thành công khi Mật khẩu dài 9 ký tự",
         "EC18 – độ dài 9 (LB+1 của EC18)", password="Abcdefg1@"),
    case("BV-05", "accept", "password", "Kiểm tra đăng ký thành công khi Mật khẩu dài 1000 ký tự",
         "EC18 – độ dài 1000 (lớn nhất chọn thử)", password=LONG_PASSWORD, note="A5",
         show={"password": '`"Abcdef1@" + "a" * 992` (1000 ký tự)'}),
    case("BV-06", "accept", "password", "Kiểm tra đăng ký thành công khi Mật khẩu có đúng 1 chữ thường",
         "EC22 – 1 chữ thường (LB)", password="ABCDEa1@"),
    case("BV-07", "accept", "password",
         "Kiểm tra đăng ký thành công khi chữ hoa duy nhất là `Z`, chữ thường duy nhất là `a`, chữ số duy nhất là `9`",
         "`Z` (UB chữ hoa), `a` (LB chữ thường), `9` (UB chữ số)", password="Zaaaaa9@"),
    case("BV-08", "accept", "password",
         "Kiểm tra đăng ký thành công khi chữ hoa duy nhất là `A`, chữ thường duy nhất là `z`, chữ số duy nhất là `0`",
         "`A` (LB chữ hoa), `z` (UB chữ thường), `0` (LB chữ số)", password="Azzzzz0@"),
    case("BV-09", "reject", "password",
         "Kiểm tra đăng ký bị từ chối khi ký tự liền sau `Z` (`[`) thay cho chữ hoa", "`Z`/`[` (UB+1 chữ hoa)",
         password="[bcdef1@"),
    case("BV-10", "reject", "password",
         "Kiểm tra đăng ký bị từ chối khi ký tự liền trước `a` (`` ` ``) thay cho chữ thường",
         "`` ` ``/`a` (LB-1 chữ thường)", password="A`````1@"),
    case("BV-11", "reject", "password",
         "Kiểm tra đăng ký bị từ chối khi ký tự liền sau `z` (`{`) thay cho chữ thường", "`z`/`{` (UB+1 chữ thường)",
         password="A{{{{{1@"),
    case("BV-12", "reject", "password",
         "Kiểm tra đăng ký bị từ chối khi ký tự liền trước `0` (`/`) thay cho chữ số", "`/`/`0` (LB-1 chữ số)",
         password="Abcdef/@"),
    case("BV-13", "reject", "password",
         "Kiểm tra đăng ký bị từ chối khi ký tự liền sau `9` (`:`) thay cho chữ số", "`9`/`:` (UB+1 chữ số)",
         password="Abcdef:@"),
    case("BV-14", "accept", "name", "Kiểm tra đăng ký thành công khi Họ Tên dài 1 ký tự",
         "EC3/EC1 – độ dài 1 (LB của EC1)", name="A"),
    case("BV-15", "accept", "name", "Kiểm tra đăng ký thành công khi Họ Tên có 1 ký tự giữa các khoảng trắng",
         "EC4/EC1 – 1 ký tự khác khoảng trắng (LB)", name=" A ", note="A4"),
    case("BV-16", "accept", "name", "Kiểm tra đăng ký thành công khi Họ Tên dài 1000 ký tự",
         "EC1 – độ dài 1000 (lớn nhất chọn thử)", name=LONG_NAME, note="A5",
         show={"name": '`"A" * 1000`'}),
    case("BV-17", "accept", "email", "Kiểm tra đăng ký thành công với Email ngắn nhất hợp lệ",
         "EC5 – độ dài 5 (LB theo A2)", mail="a@b.c"),
    case("BV-18", "accept", "email", "Kiểm tra đăng ký thành công với Email dài 254 ký tự",
         "EC5 – độ dài 254 (UB theo RFC 5321)", mail=LONG_EMAIL,
         show={"email": '`"a" * 64 + "@" + "b" * 63 + "." + "c" * 63 + "." + "d" * 57 + ".com"` (254 ký tự)'}),
    case("BV-19", "reject", "dup",
         "Kiểm tra đăng ký bị từ chối khi Email đã tồn tại có đúng 1 khoảng trắng ở đầu",
         "Số khoảng trắng đầu email = 1 (LB của EC6) kết hợp EC15", mail=" " + SEED_EMAIL, note="A4",
         origin="AI-sửa", **DUP),
    case("BV-20", "reject", "confirm", "Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu thiếu ký tự cuối",
         "EC37/EC39 – độ dài Mật khẩu - 1", confirm="Abcdef1", web_only=True),
    case("BV-21", "reject", "confirm", "Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu thừa 1 ký tự",
         "EC37/EC39 – độ dài Mật khẩu + 1", confirm="Abcdef1@1", web_only=True),
    # 6.2 – bổ sung sau AI gap analysis
    case("DT-29", "reject", "password",
         "Kiểm tra đăng ký bị từ chối khi ký tự đặc biệt duy nhất của Mật khẩu là dấu cách",
         "EC28 (đại diện thứ hai), EC45", password="Abcdef1 ", note="A1", added=True),
    case("DT-30", "reject", "password",
         "Kiểm tra đăng ký bị từ chối khi chữ hoa duy nhất của Mật khẩu là chữ có dấu `Đ`",
         "EC21 (đại diện thứ hai), EC45", password="Đbcdef1@", note="A10", origin="AI-sửa", added=True),
    case("DT-31", "reject", "password",
         "Kiểm tra đăng ký bị từ chối khi chữ thường duy nhất của Mật khẩu là chữ có dấu `ă`",
         "EC23 (đại diện thứ hai), EC45", password="ABCDEă1@", note="A10", origin="AI-sửa", added=True),
    case("DT-32", "accept", "password",
         "Kiểm tra đăng ký thành công khi Mật khẩu đủ 4 loại kèm thêm chữ có dấu tiếng Việt",
         "EC36 (đại diện thứ hai), EC41", password="Mậtkhẩu1@", note="A1, A10", origin="AI-sửa", added=True),
]

BY_ID = {c["id"]: c for c in CASES}

# Xác nhận mật khẩu ở lượt khảo sát phải giữ đúng quan hệ với mật khẩu "Abcdef1 " như thiết kế
for short_id, confirm in {
    "DT-27": "Abcdef2 ",    # khác mật khẩu
    "DT-28": "abcdef1 ",    # chỉ khác chữ hoa / thường
    "BV-20": "Abcdef1",     # thiếu ký tự cuối
    "BV-21": "Abcdef1 1",   # thừa 1 ký tự
}.items():
    BY_ID[f"{PREFIX}-{short_id}"]["web_workaround_confirm"] = confirm

assert len(CASES) == 53 and len(BY_ID) == 53
assert len(BY_ID["FR01-DT-01"]["password"]) == 8

if __name__ == "__main__":
    out = Path(__file__).with_name("cases.json")
    out.write_text(json.dumps(CASES, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(CASES)} test case -> {out}")
