"""Nguồn dữ liệu duy nhất của test case FR-10 (Máy trạng thái đơn hàng): thiết kế (mục 3.2, 4.2 của
report/FR-10_Trang_thai_don_hang.md) và dữ liệu cho runner. `report_tables.py` sinh bảng báo cáo từ file này.

Chạy trực tiếp để xuất cases.json cho runner Web (Playwright).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from report_lib import MISSING  # noqa: E402

PREFIX = "FR10"
USER_B = {"name": "User B FR10", "email": "fr10.userb@example.com", "password": "Abcdef1@"}
# Bộ dữ liệu dựng trước mỗi test case: id đơn -> (chủ đơn, trạng thái)
FIXTURE = {1: ("test", "pending"), 2: ("test", "confirmed"), 3: ("test", "shipping"), 4: ("test", "delivered"),
           5: ("test", "canceled"), 6: ("test", "pending"), 7: ("userb", "pending")}
LABEL = {"pending": "Chờ xác nhận", "confirmed": "Đã xác nhận", "shipping": "Đang giao", "delivered": "Đã giao",
         "canceled": "Đã hủy"}
# Nút trên Web Admin ứng với cạnh hợp lệ của sơ đồ (A7)
ADMIN_BUTTONS = {"pending": ["Xác nhận", "Hủy"], "confirmed": ["Giao hàng", "Hủy"], "shipping": ["Hoàn thành"],
                 "delivered": [], "canceled": []}
USER_BUTTONS = {"pending": ["Hủy đơn"], "confirmed": ["Hủy đơn"], "shipping": [], "delivered": [], "canceled": []}
ACTOR_VN = {"admin": "Admin", "user": "User chủ đơn", "other": "User khác (test@eshop.com hủy đơn của User B)"}


def expected_text(expect, action, order, frm, to, api):
    api2 = "; API trả 2xx" if api else ""
    if expect == "accept":
        return f"Đơn #{order} chuyển `{frm}` → `{to}`; các đơn khác giữ nguyên{api2} (EC26)"
    if expect == "reject":
        return (f"Từ chối, báo chuyển đổi không hợp lệ; đơn #{order} giữ `{frm}`; các đơn khác giữ nguyên"
                + ("; API trả 4xx" if api else "") + " (EC27)")
    if expect == "invalid_value":
        return f"Từ chối, báo trạng thái không hợp lệ; đơn #{order} giữ `{frm}`; API trả 4xx (EC28)"
    if expect == "notfound":
        return "Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29)"
    if action == "ui_admin":
        return ("Web Admin hiện: Chờ xác nhận – Xác nhận, Hủy; Đã xác nhận – Giao hàng, Hủy; Đang giao – Hoàn thành; "
                "Đã giao, Đã hủy – không có nút (EC30)")
    return "Trang Hồ sơ hiện nút \"Hủy đơn\" chỉ ở đơn Chờ xác nhận, Đã xác nhận; không có ở Đang giao, Đã giao, Đã hủy (EC30)"


def case(short_id, actor, action, expect, title, covers, *, order=None, status=None, web=False, api=True,
         note="", show=None, origin="AI", added=False):
    frm = FIXTURE[order][1] if isinstance(order, int) and order in FIXTURE else None
    to = status if action == "status" else "canceled" if action == "cancel" else None
    channels = (["web"] if web else []) + (["api"] if api else [])
    expected = expected_text(expect, action, order, frm, to, api)
    if note:
        expected += f"; {note}"
    return {
        "id": f"{PREFIX}-{short_id}",
        "section": "GAP" if added else short_id[:2],
        "title": title,
        "covers": covers,
        "actor": actor,
        "actor_vn": ACTOR_VN[actor],
        "action": action,  # status | cancel | ui_admin | ui_user
        "action_vn": {"status": "Đổi trạng thái", "cancel": "Hủy đơn", "ui_admin": "Xem tab Đơn hàng",
                      "ui_user": "Xem Lịch sử đơn hàng"}[action],
        "order": order,
        "from_state": frm,
        "status": status,  # giá trị gửi trong trường status (Admin), MISSING = không gửi
        "target_state": to,
        "expect": expect,  # accept | reject | invalid_value | notfound | ui
        "expected": expected,
        "origin": origin,
        "show": show or {},
        "channels": channels,
    }


S, C = "status", "cancel"
CASES = [
    # 3.2 – Minimum Set: chuyển đổi hợp lệ
    case("DT-01", "admin", S, "accept", "Kiểm tra Admin xác nhận đơn đang chờ xác nhận thành công",
         "EC1, EC18, EC23, EC26", order=1, status="confirmed", web=True),
    case("DT-02", "admin", S, "accept", "Kiểm tra Admin chuyển đơn đã xác nhận sang đang giao thành công",
         "EC2, EC18, EC23, EC26", order=2, status="shipping", web=True),
    case("DT-03", "admin", S, "accept", "Kiểm tra Admin hoàn tất đơn đang giao thành công",
         "EC3, EC18, EC23, EC26", order=3, status="delivered", web=True),
    case("DT-04", "admin", S, "accept", "Kiểm tra Admin hủy đơn đang chờ xác nhận thành công",
         "EC4, EC18, EC23, EC26", order=1, status="canceled", web=True),
    case("DT-05", "admin", S, "accept", "Kiểm tra Admin hủy đơn đã xác nhận thành công",
         "EC5, EC18, EC23, EC26", order=2, status="canceled", web=True),
    case("DT-06", "user", C, "accept", "Kiểm tra User hủy đơn đang chờ xác nhận của mình thành công",
         "EC6, EC23, EC26", order=1, web=True),
    case("DT-07", "user", C, "accept", "Kiểm tra User hủy đơn đã xác nhận của mình thành công",
         "EC7, EC23, EC26", order=2, web=True),
    # 3.2 – Minimum Set: chuyển đổi không hợp lệ
    case("DT-08", "admin", S, "reject", "Kiểm tra Admin chuyển đơn đã giao sang đã hủy bị từ chối",
         "EC8, EC27", order=4, status="canceled"),
    case("DT-09", "admin", S, "reject", "Kiểm tra Admin chuyển đơn đã hủy sang đã giao bị từ chối",
         "EC9, EC27", order=5, status="delivered", web=True, note="trên Web Admin bấm nút \"Đánh dấu Đã giao\" có sẵn ở đơn đã hủy"),
    case("DT-10", "admin", S, "reject", "Kiểm tra Admin chuyển đơn chờ xác nhận thẳng sang đang giao bị từ chối",
         "EC10, EC27", order=1, status="shipping", note="A3"),
    case("DT-11", "admin", S, "reject", "Kiểm tra Admin chuyển đơn đang giao lùi về đã xác nhận bị từ chối",
         "EC11, EC27", order=3, status="confirmed", note="A3"),
    case("DT-12", "admin", S, "reject", "Kiểm tra Admin chuyển đơn đã xác nhận sang chính trạng thái đã xác nhận bị từ chối",
         "EC12, EC27", order=2, status="confirmed", note="A2"),
    case("DT-13", "admin", S, "reject", "Kiểm tra Admin hủy đơn đang giao bị từ chối",
         "EC13, EC27", order=3, status="canceled", note="A1"),
    case("DT-14", "user", C, "reject", "Kiểm tra User hủy đơn đang giao bị từ chối",
         "EC14, EC27", order=3, web=True, note="trên Web bấm nút \"Hủy đơn\" có sẵn ở đơn đang giao"),
    case("DT-15", "user", C, "reject", "Kiểm tra User hủy đơn đã giao bị từ chối", "EC15, EC27", order=4),
    case("DT-16", "user", C, "reject", "Kiểm tra User hủy đơn đã hủy bị từ chối", "EC16, EC27", order=5),
    case("DT-17", "other", C, "reject", "Kiểm tra User hủy đơn của người dùng khác bị từ chối",
         "EC17, EC27", order=7, note="A6; đơn #7 của User B giữ `pending`"),
    case("DT-18", "admin", S, "invalid_value", "Kiểm tra Admin đổi trạng thái bị từ chối khi status ngoài tập",
         "EC19, EC28", order=1, status="abc"),
    case("DT-19", "admin", S, "invalid_value", "Kiểm tra Admin đổi trạng thái bị từ chối khi status sai chữ hoa / thường",
         "EC20, EC28", order=1, status="Confirmed"),
    case("DT-20", "admin", S, "invalid_value", "Kiểm tra Admin đổi trạng thái bị từ chối khi status rỗng",
         "EC21, EC28", order=1, status=""),
    case("DT-21", "admin", S, "invalid_value", "Kiểm tra Admin đổi trạng thái bị từ chối khi không gửi status",
         "EC22, EC28", order=1, status=MISSING),
    case("DT-22", "admin", S, "notfound", "Kiểm tra Admin đổi trạng thái đơn không tồn tại bị từ chối",
         "EC24 (Admin), EC29", order=9999, status="confirmed"),
    case("DT-23", "admin", S, "notfound", "Kiểm tra Admin đổi trạng thái bị từ chối khi mã đơn không phải số",
         "EC25 (Admin), EC29", order="abc", status="confirmed"),
    case("DT-24", "user", C, "notfound", "Kiểm tra User hủy đơn không tồn tại bị từ chối",
         "EC24 (User), EC29", order=9999),
    case("DT-25", "user", C, "notfound", "Kiểm tra User hủy đơn bị từ chối khi mã đơn không phải số",
         "EC25 (User), EC29", order="abc"),
    case("DT-26", "admin", "ui_admin", "ui", "Kiểm tra Web Admin chỉ hiện thao tác hợp lệ cho từng trạng thái đơn",
         "EC30 (Admin)", web=True, api=False, show={"order": "#1–#5", "status": "–"}),
    case("DT-27", "user", "ui_user", "ui", "Kiểm tra trang Hồ sơ chỉ hiện nút Hủy đơn cho đơn được phép hủy",
         "EC30 (User)", web=True, api=False, show={"order": "#1–#5", "status": "–"}),
    # 4.2 – Boundary Value Test Cases: d = thứ tự đích − thứ tự hiện tại (pending 0 < confirmed 1 < shipping 2 < delivered 3)
    case("BV-01", "admin", S, "reject", "Kiểm tra Admin chuyển đơn chờ xác nhận sang chính nó bị từ chối",
         "`pending`: d = 0 (UB-1)", order=1, status="pending", note="A2"),
    case("BV-02", "admin", S, "reject", "Kiểm tra Admin chuyển đơn chờ xác nhận thẳng sang đã giao bị từ chối",
         "`pending`: d = +3 (lớn nhất)", order=1, status="delivered", note="A3"),
    case("BV-03", "admin", S, "reject", "Kiểm tra Admin chuyển đơn đã xác nhận lùi về chờ xác nhận bị từ chối",
         "`confirmed`: d = −1", order=2, status="pending", note="A3"),
    case("BV-04", "admin", S, "reject", "Kiểm tra Admin chuyển đơn đã xác nhận thẳng sang đã giao bị từ chối",
         "`confirmed`: d = +2 (UB+1)", order=2, status="delivered", note="A3"),
    case("BV-05", "admin", S, "reject", "Kiểm tra Admin chuyển đơn đang giao lùi về chờ xác nhận bị từ chối",
         "`shipping`: d = −2", order=3, status="pending", note="A3"),
    case("BV-06", "admin", S, "reject", "Kiểm tra Admin chuyển đơn đang giao sang chính nó bị từ chối",
         "`shipping`: d = 0", order=3, status="shipping", note="A2"),
    case("BV-07", "admin", S, "reject", "Kiểm tra Admin chuyển đơn đã giao lùi về đang giao bị từ chối",
         "`delivered` (kết thúc): d = −1", order=4, status="shipping"),
    case("BV-08", "admin", S, "reject", "Kiểm tra Admin chuyển đơn đã giao sang chính nó bị từ chối",
         "`delivered` (kết thúc): d = 0", order=4, status="delivered", note="A2"),
    case("BV-09", "admin", S, "reject", "Kiểm tra Admin hủy lại đơn đã hủy bị từ chối",
         "`canceled` (kết thúc) → `canceled`", order=5, status="canceled", note="A2"),
    case("BV-10", "admin", S, "reject", "Kiểm tra Admin khôi phục đơn đã hủy về chờ xác nhận bị từ chối",
         "`canceled` (kết thúc) → `pending`", order=5, status="pending"),
    case("BV-11", "admin", S, "invalid_value", "Kiểm tra Admin đổi trạng thái bị từ chối khi status thừa 1 khoảng trắng đầu",
         "`confirmed` + 1 ký tự ở đầu", order=1, status=" confirmed", note="A4"),
    case("BV-12", "admin", S, "invalid_value", "Kiểm tra Admin đổi trạng thái bị từ chối khi status thừa 1 khoảng trắng cuối",
         "`confirmed` + 1 ký tự ở cuối", order=1, status="confirmed ", note="A4"),
    case("BV-13", "admin", S, "invalid_value", "Kiểm tra Admin đổi trạng thái bị từ chối khi status thiếu 1 ký tự",
         "độ dài `confirmed` − 1", order=1, status="confirme", note="A4"),
    case("BV-14", "admin", S, "invalid_value", "Kiểm tra Admin đổi trạng thái bị từ chối khi status thừa 1 ký tự",
         "độ dài `confirmed` + 1", order=1, status="confirmedd", note="A4"),
    case("BV-15", "admin", S, "notfound", "Kiểm tra Admin đổi trạng thái đơn mã 0 bị từ chối",
         "mã đơn 0 (LB-1)", order=0, status="confirmed"),
    case("BV-16", "admin", S, "accept", "Kiểm tra Admin xác nhận đơn có mã lớn nhất đang tồn tại thành công",
         "mã đơn 7 (UB)", order=7, status="confirmed"),
    case("BV-17", "admin", S, "notfound", "Kiểm tra Admin đổi trạng thái đơn mã 8 bị từ chối",
         "mã đơn 8 (UB+1)", order=8, status="confirmed"),
    case("BV-18", "user", C, "notfound", "Kiểm tra User hủy đơn mã 0 bị từ chối", "mã đơn 0 (LB-1)", order=0),
    case("BV-19", "user", C, "accept", "Kiểm tra User hủy đơn có mã lớn nhất của mình thành công",
         "mã đơn 6 (UB của User)", order=6),
    case("BV-20", "user", C, "notfound", "Kiểm tra User hủy đơn mã 8 bị từ chối", "mã đơn 8 (UB+1)", order=8),
]

BY_ID = {c["id"]: c for c in CASES}
assert len(CASES) == 47 and len(BY_ID) == 47

if __name__ == "__main__":
    out = Path(__file__).with_name("cases.json")
    out.write_text(json.dumps(CASES, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(CASES)} test case -> {out}")
