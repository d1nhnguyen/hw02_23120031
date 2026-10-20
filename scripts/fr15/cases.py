"""Nguồn dữ liệu duy nhất của test case FR-15 (Quản lý sản phẩm): thiết kế (mục 3.2, 4.2 của
report/FR-15_Quan_ly_san_pham.md) và dữ liệu cho runner. `report_tables.py` sinh bảng báo cáo từ file này.

Chạy trực tiếp để xuất cases.json cho runner Web (Playwright).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from report_lib import MISSING  # noqa: E402

PREFIX = "FR15"
# Dữ liệu seed quan sát qua GET /api/products (mục 1.1): id -> (Tên, Giá, Danh mục)
SEED = {
    1: ("iPhone 15 Pro Max", 30000000, 1),
    2: ("Samsung Galaxy S24 Ultra", 28000000, 1),
    3: ("MacBook Pro M3", 45000000, 2),
    4: ("Tai nghe AirPods Pro 2", 6000000, 3),
    5: ("Bàn phím cơ Keychron Q1", 4000000, 3),
}
ADD = {"name": "Sac nhanh USB-C 20W", "price": 350000, "category_id": 3}
EXTRA = {"description": "Mô tả kiểm thử FR-15", "imageUrl": "https://placehold.co/300x300/png?text=FR15"}
EDIT_TARGET = 2  # sản phẩm dùng cho các test case sửa bị từ chối (Samsung Galaxy S24 Ultra)
REASON = {
    "name": ("báo Tên không hợp lệ", "EC29"),
    "price": ("báo Giá không hợp lệ", "EC30"),
    "category": ("báo Danh mục không hợp lệ", "EC31"),
}
OP_VN = {"add": "Thêm", "edit": "Sửa", "delete": "Xóa"}


def expected_text(op, expect, target, pid, api):
    api_ok = "; API trả 2xx" if api else ""
    if expect == "accept":
        if op == "add":
            return (f"Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá "
                    f"/ Danh mục{api_ok} (EC25)")
        if op == "edit":
            return (f"Sửa thành công: sản phẩm id {pid} mang Tên / Giá / Danh mục như cột dữ liệu, Mô tả / Ảnh giữ "
                    f"nguyên; các sản phẩm khác giữ nguyên{api_ok} (EC26, EC28)")
        return f"Xóa thành công: sản phẩm id {pid} không còn trong danh sách; các sản phẩm khác giữ nguyên{api_ok} (EC27, EC28)"
    if expect == "notfound":
        return "Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32)"
    message, output = REASON[target]
    kept = "không tạo sản phẩm; danh sách sản phẩm không đổi" if op == "add" else \
        f"sản phẩm id {pid} và các sản phẩm khác giữ nguyên"
    return f"Từ chối, {message}; {kept}" + ("; API trả 4xx" if api else "") + f" ({output})"


def case(short_id, op, expect, target, title, covers, *, pid=None, name=None, price=None, category_id=None,
         api_only=False, web_only=False, note="", show=None, origin="AI", added=False, pre=None, check=None,
         touch=None):
    if op == "add":
        values = {**ADD}
    elif isinstance(pid, int) and pid in SEED:
        values = dict(zip(("name", "price", "category_id"), SEED[pid]))
    else:
        values = {"name": "San pham sua thu", "price": 1000000, "category_id": 1}
    for key, v in (("name", name), ("price", price), ("category_id", category_id)):
        if v is not None:
            values[key] = v
    if op == "delete":
        values = {"name": None, "price": None, "category_id": None}
    channels = ["api"] if api_only else ["web"] if web_only else ["web", "api"]
    expected = expected_text(op, expect, target, pid, "api" in channels)
    if note:
        expected += f"; {note}"
    return {
        "id": f"{PREFIX}-{short_id}",
        "section": "GAP" if added else short_id[:2],
        "title": title,
        "covers": covers,
        "op": op,
        "op_vn": OP_VN[op],
        "pid": pid,
        **values,
        "expect": expect,  # accept | reject | notfound
        "target": target,  # all | name | price | category | id
        "expected": expected,
        "origin": origin,
        "show": show or {},
        "channels": channels,
        "pre": pre or [],    # tiền điều kiện, vd [["delete", 5]]
        "check": check,      # kiểm tra thêm, vd "html_display"
        "touch": touch,      # Web: chỉ nhập vào các ô này, các ô khác để nguyên giá trị form điền sẵn
    }


def chars(ch, n):
    return ch * n


N300, A254, A255, A256 = "B" * 300, chars("A", 254), chars("A", 255), chars("A", 256)
VN255, VN256 = chars("Ố", 255), chars("Ố", 256)
MAX_SAFE = 9007199254740991
SHOW = {
    "N300": {"name": '`"B" * 300`'}, "A254": {"name": '`"A" * 254`'}, "A255": {"name": '`"A" * 255`'},
    "A256": {"name": '`"A" * 256`'}, "VN255": {"name": '`"Ố" * 255`'}, "VN256": {"name": '`"Ố" * 256`'},
}
T = EDIT_TARGET

CASES = [
    # 3.2 – Minimum Set: Thêm
    case("DT-01", "add", "accept", "all", "Kiểm tra thêm sản phẩm thành công với dữ liệu hợp lệ điển hình",
         "EC1, EC2, EC5, EC11, EC17, EC25"),
    case("DT-02", "add", "accept", "name", "Kiểm tra thêm sản phẩm thành công khi Tên có chữ tiếng Việt có dấu",
         "EC1, EC2, EC6, EC11, EC17, EC25", name="Ốp lưng chống sốc iPhone 15", price=150000),
    case("DT-03", "add", "accept", "name",
         "Kiểm tra thêm sản phẩm thành công và Tên hiển thị nguyên văn khi Tên có ký tự HTML",
         "EC1, EC2, EC7, EC11, EC17, EC25", name="<b>Loa Bluetooth</b> Mini", price=500000,
         note="danh sách Admin hiển thị đúng chuỗi `<b>Loa Bluetooth</b> Mini`, không in đậm (A8)", check="html_display"),
    case("DT-04", "add", "accept", "price", "Kiểm tra thêm sản phẩm thành công khi Giá là số thập phân dương",
         "EC1, EC2, EC5, EC12, EC17, EC25", price=99999.5, note="A3"),
    case("DT-05", "add", "reject", "name", "Kiểm tra thêm sản phẩm bị từ chối khi bỏ trống Tên", "EC8 (Thêm), EC29",
         name=""),
    case("DT-06", "add", "reject", "name", "Kiểm tra thêm sản phẩm bị từ chối khi Tên chỉ gồm khoảng trắng",
         "EC9 (Thêm), EC29", name="   ", note="A2"),
    case("DT-07", "add", "reject", "name", "Kiểm tra thêm sản phẩm bị từ chối khi Tên dài hơn 255 ký tự",
         "EC10 (Thêm), EC29", name=N300, show=SHOW["N300"]),
    case("DT-08", "add", "reject", "price", "Kiểm tra thêm sản phẩm bị từ chối khi Giá bằng 0", "EC13 (Thêm), EC30",
         price=0),
    case("DT-09", "add", "reject", "price", "Kiểm tra thêm sản phẩm bị từ chối khi Giá âm", "EC14 (Thêm), EC30",
         price=-50000),
    case("DT-10", "add", "reject", "price", "Kiểm tra thêm sản phẩm bị từ chối khi bỏ trống Giá", "EC15 (Thêm), EC30",
         price=MISSING),
    case("DT-11", "add", "reject", "price", "Kiểm tra thêm sản phẩm bị từ chối khi Giá không phải số",
         "EC16 (Thêm), EC30", price="abc", api_only=True, note="A4"),
    case("DT-12", "add", "reject", "category", "Kiểm tra thêm sản phẩm bị từ chối khi không có Danh mục",
         "EC18 (Thêm), EC31", category_id=MISSING, api_only=True),
    case("DT-13", "add", "reject", "category", "Kiểm tra thêm sản phẩm bị từ chối khi Danh mục không có trong danh sách",
         "EC19 (Thêm), EC31", category_id=99, api_only=True),
    case("DT-14", "add", "reject", "category", "Kiểm tra thêm sản phẩm bị từ chối khi Danh mục không phải số",
         "EC20 (Thêm), EC31", category_id="abc", api_only=True),
    # 3.2 – Minimum Set: Sửa
    case("DT-15", "edit", "accept", "price", "Kiểm tra sửa Giá sản phẩm thành công và các sản phẩm khác giữ nguyên",
         "EC2, EC3, EC5, EC11, EC17, EC21, EC26, EC28", pid=3, price=42000000),
    case("DT-16", "edit", "accept", "name",
         "Kiểm tra sửa Tên và Danh mục sản phẩm thành công và các sản phẩm khác giữ nguyên",
         "EC2, EC3, EC6, EC11, EC17, EC21, EC26, EC28", pid=4, name="Tai nghe AirPods Pro 2 – bản 2026", category_id=1),
    case("DT-17", "edit", "reject", "name", "Kiểm tra sửa sản phẩm bị từ chối khi bỏ trống Tên", "EC8 (Sửa), EC29",
         pid=T, name=""),
    case("DT-18", "edit", "reject", "name", "Kiểm tra sửa sản phẩm bị từ chối khi Tên chỉ gồm khoảng trắng",
         "EC9 (Sửa), EC29", pid=T, name="   ", note="A2"),
    case("DT-19", "edit", "reject", "name", "Kiểm tra sửa sản phẩm bị từ chối khi Tên dài hơn 255 ký tự",
         "EC10 (Sửa), EC29", pid=T, name=N300, show=SHOW["N300"]),
    case("DT-20", "edit", "reject", "price", "Kiểm tra sửa sản phẩm bị từ chối khi Giá bằng 0", "EC13 (Sửa), EC30",
         pid=T, price=0),
    case("DT-21", "edit", "reject", "price", "Kiểm tra sửa sản phẩm bị từ chối khi Giá âm", "EC14 (Sửa), EC30",
         pid=T, price=-50000),
    case("DT-22", "edit", "reject", "price", "Kiểm tra sửa sản phẩm bị từ chối khi bỏ trống Giá", "EC15 (Sửa), EC30",
         pid=T, price=MISSING),
    case("DT-23", "edit", "reject", "price", "Kiểm tra sửa sản phẩm bị từ chối khi Giá không phải số",
         "EC16 (Sửa), EC30", pid=T, price="abc", api_only=True, note="A4"),
    case("DT-24", "edit", "reject", "category", "Kiểm tra sửa sản phẩm bị từ chối khi không có Danh mục",
         "EC18 (Sửa), EC31", pid=T, category_id=MISSING, api_only=True),
    case("DT-25", "edit", "reject", "category", "Kiểm tra sửa sản phẩm bị từ chối khi Danh mục không có trong danh sách",
         "EC19 (Sửa), EC31", pid=T, category_id=99, api_only=True),
    case("DT-26", "edit", "reject", "category", "Kiểm tra sửa sản phẩm bị từ chối khi Danh mục không phải số",
         "EC20 (Sửa), EC31", pid=T, category_id="abc", api_only=True),
    case("DT-27", "edit", "notfound", "id", "Kiểm tra sửa sản phẩm bị từ chối khi sản phẩm không tồn tại",
         "EC22 (Sửa), EC32", pid=9999, api_only=True),
    case("DT-28", "edit", "notfound", "id", "Kiểm tra sửa sản phẩm bị từ chối khi id sản phẩm không phải số",
         "EC23 (Sửa), EC32", pid="abc", api_only=True),
    case("DT-29", "edit", "notfound", "id", "Kiểm tra sửa sản phẩm bị từ chối khi sản phẩm vừa bị xóa",
         "EC24 (Sửa), EC32", pid=5, api_only=True, pre=[["delete", 5]],
         show={"pid": "`5` (đã xóa ở tiền điều kiện)"}),
    # 3.2 – Minimum Set: Xóa
    case("DT-30", "delete", "accept", "all", "Kiểm tra xóa sản phẩm thành công và các sản phẩm khác giữ nguyên",
         "EC2, EC4, EC21, EC27, EC28", pid=5),
    case("DT-31", "delete", "notfound", "id", "Kiểm tra xóa sản phẩm bị từ chối khi sản phẩm không tồn tại",
         "EC22 (Xóa), EC32", pid=9999, api_only=True),
    case("DT-32", "delete", "notfound", "id", "Kiểm tra xóa sản phẩm bị từ chối khi id sản phẩm không phải số",
         "EC23 (Xóa), EC32", pid="abc", api_only=True),
    case("DT-33", "delete", "notfound", "id", "Kiểm tra xóa sản phẩm bị từ chối khi sản phẩm đã bị xóa trước đó",
         "EC24 (Xóa), EC32", pid=5, api_only=True, pre=[["delete", 5]],
         show={"pid": "`5` (đã xóa ở tiền điều kiện)"}),
    # 4.2 – Boundary Value Test Cases
    case("BV-01", "add", "accept", "name", "Kiểm tra thêm sản phẩm thành công khi Tên dài 1 ký tự",
         "EC8/EC5 – độ dài 1 (LB)", name="A"),
    case("BV-02", "add", "accept", "name", "Kiểm tra thêm sản phẩm thành công khi Tên dài 2 ký tự",
         "EC5 – độ dài 2 (LB+1)", name="AB"),
    case("BV-03", "add", "accept", "name", "Kiểm tra thêm sản phẩm thành công khi Tên dài 254 ký tự",
         "EC5 – độ dài 254 (UB-1)", name=A254, show=SHOW["A254"]),
    case("BV-04", "add", "accept", "name", "Kiểm tra thêm sản phẩm thành công khi Tên dài 255 ký tự",
         "EC5/EC10 – độ dài 255 (UB)", name=A255, show=SHOW["A255"]),
    case("BV-05", "add", "reject", "name", "Kiểm tra thêm sản phẩm bị từ chối khi Tên dài 256 ký tự",
         "EC5/EC10 – độ dài 256 (UB+1)", name=A256, show=SHOW["A256"]),
    case("BV-06", "add", "accept", "name", "Kiểm tra thêm sản phẩm thành công khi Tên dài 255 ký tự có dấu",
         "EC6/EC10 – 255 ký tự có dấu (UB, A1)", name=VN255, show=SHOW["VN255"], note="A1"),
    case("BV-07", "add", "reject", "name", "Kiểm tra thêm sản phẩm bị từ chối khi Tên dài 256 ký tự có dấu",
         "EC6/EC10 – 256 ký tự có dấu (UB+1, A1)", name=VN256, show=SHOW["VN256"], note="A1"),
    case("BV-08", "add", "accept", "name", "Kiểm tra thêm sản phẩm thành công khi Tên có 1 ký tự giữa các khoảng trắng",
         "EC9/EC5 – 1 ký tự khác khoảng trắng (LB, A2)", name=" A ", note="A2"),
    case("BV-09", "edit", "accept", "name", "Kiểm tra sửa sản phẩm thành công khi Tên mới dài 255 ký tự",
         "EC5/EC10 (Sửa) – độ dài 255 (UB)", pid=T, name=A255, show=SHOW["A255"]),
    case("BV-10", "edit", "reject", "name", "Kiểm tra sửa sản phẩm bị từ chối khi Tên mới dài 256 ký tự",
         "EC5/EC10 (Sửa) – độ dài 256 (UB+1)", pid=T, name=A256, show=SHOW["A256"]),
    case("BV-11", "add", "reject", "price", "Kiểm tra thêm sản phẩm bị từ chối khi Giá bằng -1",
         "EC14/EC13 – Giá -1 (bước 1)", price=-1),
    case("BV-12", "add", "reject", "price", "Kiểm tra thêm sản phẩm bị từ chối khi Giá bằng -0.01",
         "EC14/EC13 – Giá -0.01 (bước 0.01, A3)", price=-0.01, note="A3"),
    case("BV-13", "add", "accept", "price", "Kiểm tra thêm sản phẩm thành công khi Giá bằng 0.01",
         "EC13/EC12 – Giá 0.01 (LB thập phân, A3)", price=0.01, note="A3"),
    case("BV-14", "add", "accept", "price", "Kiểm tra thêm sản phẩm thành công khi Giá bằng 1",
         "EC13/EC11 – Giá 1 (LB nguyên)", price=1),
    case("BV-15", "add", "accept", "price", "Kiểm tra thêm sản phẩm thành công khi Giá bằng 9007199254740991",
         "EC11 – giá trị lớn nhất biểu diễn chính xác (2^53 - 1, A3)", price=MAX_SAFE, note="A3"),
    case("BV-16", "edit", "accept", "price", "Kiểm tra sửa sản phẩm thành công khi Giá mới bằng 1",
         "EC13/EC11 (Sửa) – Giá 1 (LB)", pid=T, price=1),
    case("BV-17", "edit", "reject", "price", "Kiểm tra sửa sản phẩm bị từ chối khi Giá mới bằng -1",
         "EC14/EC13 (Sửa) – Giá -1", pid=T, price=-1),
    case("BV-18", "add", "reject", "category", "Kiểm tra thêm sản phẩm bị từ chối khi Danh mục bằng 0",
         "EC19/EC17 – id 0 (LB-1)", category_id=0, api_only=True),
    case("BV-19", "add", "accept", "category", "Kiểm tra thêm sản phẩm thành công khi Danh mục bằng 1",
         "EC17 – id 1 (LB)", category_id=1),
    case("BV-20", "add", "reject", "category", "Kiểm tra thêm sản phẩm bị từ chối khi Danh mục bằng 4",
         "EC17/EC19 – id 4 (UB+1)", category_id=4, api_only=True),
    case("BV-21", "edit", "notfound", "id", "Kiểm tra sửa sản phẩm bị từ chối khi id sản phẩm bằng 0",
         "EC22/EC21 (Sửa) – id 0 (LB-1)", pid=0, api_only=True),
    case("BV-22", "edit", "accept", "price", "Kiểm tra sửa sản phẩm id 1 thành công",
         "EC21 (Sửa) – id 1 (LB)", pid=1, price=31000000),
    case("BV-23", "edit", "accept", "price", "Kiểm tra sửa sản phẩm id 5 thành công",
         "EC21 (Sửa) – id 5 (UB)", pid=5, price=4100000),
    case("BV-24", "edit", "notfound", "id", "Kiểm tra sửa sản phẩm bị từ chối khi id sản phẩm bằng 6",
         "EC21/EC22 (Sửa) – id 6 (UB+1)", pid=6, api_only=True),
    case("BV-25", "delete", "notfound", "id", "Kiểm tra xóa sản phẩm bị từ chối khi id sản phẩm bằng 0",
         "EC22/EC21 (Xóa) – id 0 (LB-1)", pid=0, api_only=True),
    case("BV-26", "delete", "accept", "all", "Kiểm tra xóa sản phẩm id 1 thành công",
         "EC21 (Xóa) – id 1 (LB)", pid=1),
    case("BV-27", "delete", "notfound", "id", "Kiểm tra xóa sản phẩm bị từ chối khi id sản phẩm bằng 6",
         "EC21/EC22 (Xóa) – id 6 (UB+1)", pid=6, api_only=True),
]

# 6.2 – bổ sung sau AI gap analysis
CASES.append(case(
    "DT-34", "edit", "accept", "price",
    "Kiểm tra sửa chỉ Giá sản phẩm thành công mà Danh mục do form điền sẵn được giữ nguyên",
    "EC3, EC11, EC17, EC21, EC26 (A9 – form Sửa điền sẵn đúng Danh mục khác giá trị mặc định 1)",
    pid=3, price=43000000, web_only=True, added=True, touch=["price"], note="A9",
    show={"name": "`MacBook␣Pro␣M3` (không chạm vào ô)", "category_id": "`2` (không chạm vào ô)"}))

BY_ID = {c["id"]: c for c in CASES}
assert len(CASES) == 61 and len(BY_ID) == 61
assert len(A255) == 255 and len(VN256) == 256

if __name__ == "__main__":
    out = Path(__file__).with_name("cases.json")
    out.write_text(json.dumps(CASES, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(CASES)} test case -> {out}")
