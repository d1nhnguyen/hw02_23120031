"""Dữ liệu test case FR-01 (mục 3.2 và 4.2 của report/FR-01_Dang_ky.md).

Chạy trực tiếp để xuất cases.json cho runner Web (Playwright).
"""
import json
from pathlib import Path

NAME, PASSWORD = "Nguyen Van A", "Abcdef1@"
SEED_EMAIL, SEED_PASSWORD = "test@eshop.com", "Test1234!"
SAME = None  # Xác nhận mật khẩu giống Mật khẩu


def email(tc_id):
    return f"fr01.{tc_id.lower().replace('-', '')}@example.com"


def case(tc_id, expect, target, name=NAME, mail=None, password=PASSWORD, confirm=SAME, web_only=False, duplicate_of=None):
    return {
        "id": tc_id,
        "expect": expect,  # accept | reject
        # Biến mà test case nhắm tới; với test case reject đây cũng là lý do từ chối mong đợi (A7)
        "target": target,  # all | mixed | name | email | dup | password | confirm
        "name": name,
        "email": email(tc_id) if mail is None else mail,
        "password": password,
        "confirm": password if confirm is SAME else confirm,
        "web_workaround_confirm": (password.replace("@", " ") if confirm is SAME else confirm) if target in ("name", "email", "dup", "confirm") else None,
        "channels": ["web"] if web_only else ["web", "api"],
        # Email đã tồn tại: kiểm tra tài khoản gốc không bị ghi đè
        "duplicate_of": duplicate_of,
        # Lần chạy 2 trên Web (khảo sát, không tính verdict): form Web chặn mọi mật khẩu hợp lệ theo đặc tả và
        # chỉ nhận dấu cách làm "ký tự đặc biệt", nên thay "@" bằng dấu cách để quan sát cách Web xử lý các biến
        # khác; chỉ áp dụng cho test case không nhắm vào mật khẩu
        "web_workaround_password": password.replace("@", " ") if target in ("name", "email", "dup", "confirm") else None,
    }


LONG_EMAIL = "a" * 64 + "@" + "b" * 63 + "." + "c" * 63 + "." + "d" * 57 + ".com"
assert len(LONG_EMAIL) == 254

CASES = [
    # 3.2 – Minimum Set, valid
    case("DT-01", "accept", "all"),
    case("DT-02", "accept", "mixed", name="Nguyễn Thị Ánh", mail=f" {email('DT-02')} ", password="Abc#def1$"),
    case("DT-03", "accept", "password", password="Abcdef1!"),
    case("DT-04", "accept", "password", password="Abcdef1%"),
    case("DT-05", "accept", "password", password="Abcdef1*"),
    case("DT-06", "accept", "password", password="Abcdef1?"),
    case("DT-07", "accept", "password", password="Abcdef1&"),
    # 3.2 – Minimum Set, invalid
    case("DT-08", "reject", "name", name=""),
    case("DT-09", "reject", "name", name="   "),
    case("DT-10", "reject", "email", mail=""),
    case("DT-11", "reject", "email", mail="fr01.dt11example.com"),
    case("DT-12", "reject", "email", mail="@example.com"),
    case("DT-13", "reject", "email", mail="fr01.dt13@"),
    case("DT-14", "reject", "email", mail="fr01.dt14@example"),
    case("DT-15", "reject", "email", mail="fr01@dt15@example.com"),
    case("DT-16", "reject", "email", mail="fr01 dt16@example.com"),
    case("DT-17", "reject", "dup", mail=SEED_EMAIL, password="Newpass1@", duplicate_of=SEED_EMAIL),
    case("DT-18", "reject", "dup", mail="TEST@eshop.com", password="Newpass1@", duplicate_of=SEED_EMAIL),
    case("DT-19", "reject", "password", password=""),
    case("DT-20", "reject", "password", password="Abcd1@"),
    case("DT-21", "reject", "password", password="abcdef1@"),
    case("DT-22", "reject", "password", password="ABCDEF1@"),
    case("DT-23", "reject", "password", password="Abcdefg@"),
    case("DT-24", "reject", "password", password="Abcdefg1"),
    case("DT-25", "reject", "password", password="Abcdef1#"),
    case("DT-26", "reject", "confirm", confirm="", web_only=True),
    case("DT-27", "reject", "confirm", confirm="Abcdef2@", web_only=True),
    case("DT-28", "reject", "confirm", confirm="abcdef1@", web_only=True),
    # 4.2 – Boundary Value Test Cases
    case("BV-01", "reject", "password", password="@"),
    case("BV-02", "reject", "password", password="A1"),
    case("BV-03", "reject", "password", password="Abcde1@"),
    case("BV-04", "accept", "password", password="Abcdefg1@"),
    case("BV-05", "accept", "password", password="Abcdef1@" + "a" * 992),
    case("BV-06", "accept", "password", password="ABCDEa1@"),
    case("BV-07", "accept", "password", password="Zaaaaa9@"),
    case("BV-08", "accept", "password", password="Azzzzz0@"),
    case("BV-09", "reject", "password", password="[bcdef1@"),
    case("BV-10", "reject", "password", password="A`````1@"),
    case("BV-11", "reject", "password", password="A{{{{{1@"),
    case("BV-12", "reject", "password", password="Abcdef/@"),
    case("BV-13", "reject", "password", password="Abcdef:@"),
    case("BV-14", "accept", "name", name="A"),
    case("BV-15", "accept", "name", name=" A "),
    case("BV-16", "accept", "name", name="A" * 1000),
    case("BV-17", "accept", "email", mail="a@b.c"),
    case("BV-18", "accept", "email", mail=LONG_EMAIL),
    case("BV-19", "reject", "dup", mail=" " + SEED_EMAIL, password="Newpass1@", duplicate_of=SEED_EMAIL),
    case("BV-20", "reject", "confirm", confirm="Abcdef1", web_only=True),
    case("BV-21", "reject", "confirm", confirm="Abcdef1@1", web_only=True),
]

BY_ID = {c["id"]: c for c in CASES}

# Xác nhận mật khẩu ở lần chạy 2 phải giữ đúng quan hệ với mật khẩu "Abcdef1 " như thiết kế
for tc_id, confirm in {
    "DT-27": "Abcdef2 ",    # khác mật khẩu
    "DT-28": "abcdef1 ",    # chỉ khác chữ hoa / thường
    "BV-20": "Abcdef1",     # thiếu ký tự cuối
    "BV-21": "Abcdef1 1",   # thừa 1 ký tự
}.items():
    BY_ID[tc_id]["web_workaround_confirm"] = confirm
assert len(CASES) == 49 and len(BY_ID) == 49
assert len(BY_ID["DT-01"]["password"]) == 8 and len(BY_ID["BV-05"]["password"]) == 1000
assert len(BY_ID["BV-16"]["name"]) == 1000

if __name__ == "__main__":
    out = Path(__file__).with_name("cases.json")
    out.write_text(json.dumps(CASES, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(CASES)} test case -> {out}")
