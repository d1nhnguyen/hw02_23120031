"""Nguồn dữ liệu duy nhất của test case Mobile – Đăng nhập: thiết kế (mục 3.2, 4.2 của report/Mobile_Dang_nhap.md)
và dữ liệu cho runner. `report_tables.py` sinh bảng báo cáo từ file này.
"""
import json
from pathlib import Path

PREFIX = "MOB"
EMAIL, PASSWORD, WRONG = "test@eshop.com", "Test1234!", "Sai12345!"
FAIL = [EMAIL, WRONG]  # một lần đăng nhập sai mật khẩu
OK = [EMAIL, PASSWORD]


def expected_text(expect, counter, note):
    if expect == "success":
        text = ("Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; "
                "API trả `200` + `token`; bộ đếm = 0 (EC17)")
    elif expect == "fail":
        text = ("Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx"
                + (f"; bộ đếm = {counter} (EC18, EC19)" if counter is not None else " (EC18)"))
    else:
        text = "Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20)"
    return text + (f"; {note}" if note else "")


def case(short_id, expect, title, covers, *, email=EMAIL, password=PASSWORD, pre=None, wait=0, counter=None,
         same_message_as_pre=False, lock_expected=None, note="", origin="AI", added=False):
    return {
        "id": f"{PREFIX}-{short_id}",
        "section": "GAP" if added else short_id[:2],
        "title": title,
        "covers": covers,
        "email": email,
        "password": password,
        "pre": pre or [],       # các lần đăng nhập trước lần thử được đánh giá [[email, mật khẩu], ...]
        "wait": wait,           # giây chờ tính từ lần thử trước cuối cùng tới lúc bấm đăng nhập lần cuối
        "expect": "accept" if expect == "success" else expect,  # accept | fail | locked
        "counter": counter,     # login_attempts mong đợi sau lần thử cuối (None = không kiểm tra)
        "lock_expected": lock_expected,  # True: lần thử cuối phải làm tài khoản bị khóa
        "same_message_as_pre": same_message_as_pre,  # thông báo phải giống hệt thông báo của lần thử trước
        "expected": expected_text(expect, counter, note),
        "origin": origin,
        "show": {},
        "channels": ["web", "api"],  # "web" = kênh Mobile app (dùng chung khung báo cáo)
    }


CASES = [
    # 3.2 – Minimum Set: valid
    case("DT-01", "success", "Kiểm tra đăng nhập thành công với email và mật khẩu đúng", "EC1, EC7, EC12, EC17"),
    case("DT-02", "success", "Kiểm tra đăng nhập thành công khi email khác chữ hoa / thường",
         "EC2, EC7, EC12, EC17", email="TEST@eshop.com", note="A6"),
    case("DT-03", "success", "Kiểm tra đăng nhập thành công khi email có khoảng trắng đầu / cuối",
         "EC3, EC7, EC12, EC17", email=" test@eshop.com ", note="A6"),
    case("DT-04", "success", "Kiểm tra đăng nhập thành công khi đã hết 30 giây khóa",
         "EC15, EC21", pre=[FAIL] * 3, wait=35, note="tiền điều kiện: 3 lần sai liên tiếp rồi chờ 35 giây"),
    case("DT-05", "success", "Kiểm tra đăng nhập đúng xen giữa làm mới chuỗi sai liên tiếp",
         "EC16, EC12, EC17", pre=[FAIL, FAIL, OK, FAIL, FAIL],
         note="A3; sau lần đúng thứ nhất chuỗi sai bắt đầu lại nên 2 lần sai sau không làm khóa tài khoản"),
    # 3.2 – Minimum Set: invalid
    case("DT-06", "fail", "Kiểm tra đăng nhập bị từ chối khi sai mật khẩu", "EC8, EC18, EC19",
         password=WRONG, counter=1),
    case("DT-07", "fail", "Kiểm tra đăng nhập bị từ chối với cùng thông báo khi email không tồn tại",
         "EC4, EC18", email="khongco@eshop.com", pre=[FAIL], counter=1, same_message_as_pre=True,
         note="A5, A7: thông báo giống hệt lần sai mật khẩu ở tiền điều kiện; bộ đếm của `test@eshop.com` giữ 1"),
    case("DT-08", "fail", "Kiểm tra đăng nhập bị từ chối khi bỏ trống email", "EC5, EC18", email="", counter=0),
    case("DT-09", "fail", "Kiểm tra đăng nhập bị từ chối khi email sai định dạng", "EC6, EC18", email="test@eshop",
         counter=0),
    case("DT-10", "fail", "Kiểm tra đăng nhập bị từ chối khi bỏ trống mật khẩu", "EC9, EC18", password="", counter=1),
    case("DT-11", "fail", "Kiểm tra đăng nhập bị từ chối khi mật khẩu chỉ khác chữ hoa / thường", "EC10, EC18",
         password="test1234!", counter=1),
    case("DT-12", "fail", "Kiểm tra đăng nhập bị từ chối khi mật khẩu thừa khoảng trắng cuối", "EC11, EC18",
         password="Test1234! ", counter=1, note="A6"),
    case("DT-13", "locked", "Kiểm tra đăng nhập bị từ chối dù mật khẩu đúng khi đã sai 3 lần liên tiếp",
         "EC13, EC14, EC20", pre=[FAIL] * 3, note="A2"),
    # 4.2 – Boundary Value Test Cases
    case("BV-01", "success", "Kiểm tra đăng nhập thành công khi trước đó sai 1 lần", "EC12 – 1 lần sai (LB+1)",
         pre=[FAIL]),
    case("BV-02", "success", "Kiểm tra đăng nhập thành công khi trước đó sai 2 lần liên tiếp",
         "EC12/EC13 – 2 lần sai (UB của EC12)", pre=[FAIL] * 2, note="A2"),
    case("BV-03", "locked", "Kiểm tra đăng nhập bị từ chối dù mật khẩu đúng khi trước đó sai 4 lần liên tiếp",
         "EC13 – 4 lần sai (LB+1 của EC13)", pre=[FAIL] * 4),
    case("BV-04", "fail", "Kiểm tra lần sai thứ 3 liên tiếp đưa bộ đếm lên 3 và khóa tài khoản",
         "EC19 – bộ đếm 2 → 3 (biên khóa)", password=WRONG, pre=[FAIL] * 2, counter=3, lock_expected=True,
         note="sau lần này `locked_until` ≈ thời điểm hiện tại + 30 giây"),
    case("BV-05", "locked", "Kiểm tra đăng nhập bị từ chối khi mới qua 28 giây khóa",
         "EC14/EC15 – 28 giây (UB-1 của EC14, sai số thao tác ~1 giây)", pre=[FAIL] * 3, wait=28),
    case("BV-06", "success", "Kiểm tra đăng nhập thành công khi đã qua 32 giây khóa",
         "EC14/EC15 – 32 giây (LB+1 của EC15, sai số thao tác ~1 giây)", pre=[FAIL] * 3, wait=32),
    case("BV-07", "fail", "Kiểm tra đăng nhập bị từ chối khi mật khẩu thiếu 1 ký tự cuối",
         "EC7/EC8 – độ dài mật khẩu − 1", password="Test1234", counter=1),
    case("BV-08", "fail", "Kiểm tra đăng nhập bị từ chối khi mật khẩu thừa 1 ký tự",
         "EC7/EC8 – độ dài mật khẩu + 1", password="Test1234!!", counter=1),
    case("BV-09", "fail", "Kiểm tra đăng nhập bị từ chối khi email thiếu 1 ký tự cuối",
         "EC1/EC4 – độ dài email − 1", email="test@eshop.co", counter=0),
    case("BV-10", "fail", "Kiểm tra đăng nhập bị từ chối khi email thừa 1 ký tự",
         "EC1/EC4 – độ dài email + 1", email="test@eshop.comm", counter=0),
]

BY_ID = {c["id"]: c for c in CASES}
assert len(CASES) == 23 and len(BY_ID) == 23

if __name__ == "__main__":
    out = Path(__file__).with_name("cases.json")
    out.write_text(json.dumps(CASES, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(CASES)} test case -> {out}")
