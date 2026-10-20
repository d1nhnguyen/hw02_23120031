# Kế hoạch & quy ước làm bài HW02

## Phạm vi

| Pool | Feature | Kênh kiểm thử |
| --- | --- | --- |
| A | FR-01 Đăng ký tài khoản | Web (`/register`) + API `POST /api/register` |
| B | FR-10 Máy trạng thái đơn hàng | Web Admin (tab Đơn hàng) + Web (hủy đơn ở Hồ sơ) + API `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel` |
| C | FR-15 Quản lý sản phẩm (CRUD) | Web Admin (tab Sản phẩm) + API `/api/products` |
| D | Mobile – Đăng nhập (FR-20) | App mobile (Expo Go trên Android Emulator); đặc tả kế thừa FR-02, FR-20, FR-22 |

Thiết kế test theo hướng hộp đen, chỉ dựa trên đặc tả (`README.md` của SUT, `api_specification.md`). Không đọc mã nguồn SUT để thiết kế test.

## Quy trình cho mỗi feature (mỗi bước = 1 commit)

| Bước | Nội dung | Sản phẩm |
| --- | --- | --- |
| B1 | Phân tích đặc tả: biến Input/Output, ràng buộc, giả định | `report/<FR>.md` mục 1 |
| B2 | Xác định lớp tương đương (valid / invalid) | mục 2 |
| B3 | Chọn test case Domain Testing (valid gộp nhiều lớp, invalid mỗi TC đúng 1 lớp) | mục 3 |
| B4 | Boundary Value Analysis cho các biến có thứ tự | mục 4 |
| B5 | Chạy test trên SUT, ghi Actual / Status, chụp bằng chứng | mục 5, `evidence/<FR>/` |
| B6 | AI gap analysis: so bản AI gốc (`ai/raw/`) với bản cuối | mục 6 |
| B7 | Báo cáo bug (Markdown + GitHub Issue có ảnh) | `bugs/` |

- Sinh viên tự viết prompt cho từng bước. Output AI nguyên gốc được lưu ở `ai/raw/<FR>_B<n>.md` **trước** khi chỉnh sửa.
- Mỗi test case có cột **Origin**: `AI` (dùng nguyên) / `AI-sửa` / `SV` (sinh viên tự thêm).
- Template test case: ID | Tiêu đề (Action + Function + Condition) | Lớp/biên phủ | Tiền điều kiện | Các bước | Dữ liệu | Kết quả mong đợi | Kết quả thực tế | Trạng thái | Bug ID | Origin.

## Quy ước

- **Commit:** `[<FR>][B<n>] <mô tả>`, ví dụ `[FR-15][B2] Xác định lớp tương đương cho tên, giá, danh mục`; feature mobile dùng `[Mobile]`. Việc chung dùng `[setup]`, `[skill]`, `[report]`, `[ai-log]`.
- **Issue:** `[BUG-NN] [FR-xx] <tóm tắt>`, trong đó NN là số kế tiếp trên repo nhóm tại thời điểm tạo. Bug mobile dùng `[FR-20]` như nhóm đang làm, phần thân dẫn chiếu FR-02. Nội dung bug do AI nháp, sinh viên duyệt và tự viết lên GitHub.
- **Prompt log:** chạy `python3 scripts/export_prompt_log.py --since 2026-10-20T20:40` sau mỗi phiên làm việc rồi commit với `[ai-log]`.

## Môi trường

| Thành phần | Địa chỉ |
| --- | --- |
| Backend API | `http://localhost:3000` (dữ liệu bị reset mỗi lần restart) |
| Web | `http://localhost:5173` |
| Web Admin | `http://localhost:5174` |
| Mobile | Android Emulator `eshop_api34` (Android 14) + Expo Go, backend truy cập qua `http://10.0.2.2:3000/api` |

Tài khoản: `admin@eshop.com / Admin123!`, `test@eshop.com / Test1234!`.

## Hồ sơ AI phải nộp (theo AI Templates)

- [ ] `ai/prompt_log.md` – Phụ lục A, nguyên văn prompt + output, có thời gian
- [ ] `ai/AI_Audit_Report.md` – mẫu AI-02: 1 hàng / artifact, verdict VALID / INVALID / INCOMPLETE, lý do dẫn slide / ISTQB, bản sửa
- [ ] `ai/AI_Critique.md` – 200–300 từ
- [ ] `ai/AI_Disclosure_Form.md` – mẫu AI-03
- [ ] `ai/AI_Privacy_Checklist.md` – mẫu AI-05
- [ ] Đoạn Mandatory Disclosure ở cuối báo cáo chính
