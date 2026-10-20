# Các điểm sinh viên cần đối chiếu / quyết định trước khi nộp

Danh sách này được cập nhật trong suốt quá trình làm bài. Đánh dấu `[x]` khi đã xử lý. Không đưa file này vào bản nộp nếu không cần.

## Liêm chính & khai báo AI

- [x] **Nguồn của bản rà soát FR-01** (G9–G16, FR01-DT-30…32): đã khai báo đầy đủ phiên rà soát chéo bằng Google Antigravity (Gemini 4 Argon, lượt #13) trong `ai/prompt_log.md`, `ai/AI_Audit_Report.md`, `ai/AI_Disclosure_Form.md`, `report/FR-01_Dang_ky.md` và cập nhật nhãn Origin / nguồn phát hiện.
- [ ] **Các phiên AI trước 20/10** (11/10 tóm tắt đề, 14/10 làm thử FR-01, 19/10 lập kế hoạch) đang không nằm trong prompt log. Quyết định có ghi một dòng trong AI Disclosure Form ("đã dùng AI để tìm hiểu đề, không dùng kết quả") hay không.
- [ ] **Bug report do AI nháp**: AI-01 §11 ghi "Bug report: 100% sinh viên viết; AI không được nháp mô tả", trong khi đề HW02 §11 ghi Anti-AI-Cheat "None". Đã chọn: AI nháp, sinh viên duyệt và tự viết issue → khai báo rõ trong Disclosure Form.
- [ ] Prompt log có cả phiên tạo repo (`4aefb10a`); kiểm tra nội dung trước khi nộp.
- [ ] 3 commit đầu trên GitHub còn dòng `Co-Authored-By: Claude`; quyết định giữ (minh bạch) hay viết lại lịch sử + force-push.

## Giả định cần hỏi TA

- [ ] FR-01: A1 (chỉ 7 ký tự `@ $ ! % * ? &` là ký tự đặc biệt), A2 (email phải có TLD), A3 (email trùng không phân biệt hoa thường), A4 (bỏ khoảng trắng đầu/cuối), A5 (không giới hạn độ dài), A10 (chữ hoa/thường chỉ A–Z/a–z).
- [ ] FR-15: A1 (255 ký tự tính theo ký tự Unicode), A3 (giá được phép là số thập phân dương, không giới hạn trên – ảnh hưởng kết luận về việc ô Giá chặn `0.5`), A6 (mã 404 khi sản phẩm không tồn tại).
- [ ] FR-10: A1 (Admin **không** được hủy đơn `shipping` – sơ đồ không có cạnh `shipping → canceled`, nhưng câu "chỉ Admin mới có thể thao tác" có thể hiểu khác), A6 (User hủy đơn của người khác – giao với FR-11).
- [ ] Pool D = các chức năng của FR-20; "Mobile – Đăng nhập" kế thừa quy tắc FR-02 (file phân công nhóm cũng ghi nên hỏi TA).
- [ ] Mobile – Đăng nhập: A2 (khóa ngay sau lần sai thứ 3), A3 (đăng nhập đúng đặt lại bộ đếm), A6 (email không phân biệt hoa thường / bỏ khoảng trắng).

## Quyết định phương pháp (đã áp dụng, cần sinh viên xác nhận)

- [ ] Test case bị một lỗi khác che → **Blocked** ở lượt chính thức + lượt **khảo sát** không tính verdict (FR-01: 15 test case Web).
- [ ] Mức độ nghiêm trọng của từng bug (FR-01: 2 Critical, 4 Major, 3 Minor; FR-15: 5 Major, 1 Minor; FR-10: 1 Critical, 1 Major; Mobile: 1 Critical, 2 Major, 2 Minor).
- [ ] Cách đếm số liệu tổng: theo lượt chạy từng kênh (Web/API) và theo test case gộp kênh.

## GitHub Issues

- [ ] Tạo issue cho FR01-B1…FR01-B9, FR15-B1…FR15-B6, FR10-B1…FR10-B2, MOB-B1…MOB-B5 (tiêu đề dùng `[FR-20]`) trên `d1nhnguyen/eshop-sut` (số tiếp theo lúc kiểm tra 20/10: BUG-12), đính kèm ảnh trong `bugs/screenshots/`.
- [ ] Gửi lại số BUG-NN để điền vào `bugs/Bug_Report.md` và mục 7 mỗi báo cáo; chụp trang issue lưu `bugs/screenshots/BUG-NN_issue.png`.
- [ ] Kiểm tra không trùng bug với thành viên khác trong nhóm – đặc biệt MOB-B2, MOB-B3, MOB-B4 là lỗi backend của quy tắc đăng nhập (FR-02), có thể trùng với người kiểm thử đăng nhập Web.

## Hồ sơ nộp

- [ ] Điền họ tên, lớp/khoá, giảng viên, ngày, chữ ký trong `ai/AI_Audit_Report.md`, `AI_Disclosure_Form.md`, `AI_Privacy_Checklist.md`.
- [ ] AI Critique 200–300 từ (sinh viên viết / duyệt); xóa khối chú thích gợi ý trong `ai/AI_Critique.md`.
- [ ] **AI Audit Report**: bảng mục 3 là nháp tự động (33 artifact; verdict gợi ý 27 VALID / 6 INCOMPLETE). Xác nhận / đổi verdict từng hàng, điền cột (4) lý do có dẫn chiếu slide / ISTQB, tính lại mục 4, viết mục 5 (80–150 chữ) và mục 6 Mandatory Disclosure, xóa các chú thích `NHÁP`.
- [ ] FR-15, FR-10, Mobile **chưa có commit rà soát** của sinh viên (mọi hàng đang "Không sửa" → VALID). Nếu sửa gì khi duyệt: commit `[<F>][Bn-review]` rồi chạy lại `audit_draft.py --prompt-log ai/prompt_log.md`.
- [ ] **AI Disclosure Form**: kiểm tra bảng 2.4 (AI nháp), tự viết mục 2.5, xóa chú thích `NHÁP`.
- [ ] Video demo Agent Skill có **giọng nói của sinh viên** (AI-01 §10), đăng YouTube, điền link vào README.
- [ ] Điểm tự chấm trong README và tên file zip `23120031_HW02_AI_DomainTesting_<điểm>.zip`.
- [ ] Điền sheet phân công nhóm (`HW02_Phan_cong_nhom.xlsx`), kiểm tra không trùng feature.
- [ ] Xuất PDF cho báo cáo chính, bug report, AI Audit Report, AI Critique; xuất `git_commit_log.txt`.

## Môi trường

- [ ] Mobile được thực thi trên Android Emulator **Pixel 2** vì trên **Pixel 6** thanh tiêu đề bị thanh trạng thái che, không mở được màn hình Đăng nhập (đã báo bug). Nếu có điện thoại thật, nên thử lại để xác nhận mức độ ảnh hưởng.

- [ ] Bản SUT local đã sửa `frontend-mobile/App.js:16` (API_URL → `10.0.2.2`) để chạy trên Android Emulator – đã ghi trong PLAN.md.

## Quan sát ngoài phạm vi (báo cho thành viên phụ trách nếu cần)

- [ ] FR-06 (chi tiết sản phẩm): `GET /api/products/:id` trả `price` dạng **chuỗi** với sản phẩm có id chẵn, dạng số với id lẻ (danh sách `GET /api/products` luôn là số) – phát hiện khi làm FR-15.
- [ ] FR-21 (giao diện chung): trang Đăng ký không có thẻ `<h1>`, nút "Đăng Ký" màu đỏ – phát hiện khi làm FR-01.
- [ ] FR-21: danh sách sản phẩm trong Web Admin hiển thị giá không có phân cách hàng nghìn (`30000000 ₫`) – phát hiện khi làm FR-15.
- [ ] Mobile – Đăng xuất (Pool D, người khác): nút đăng xuất ghi "Thoát" thay vì "Đăng xuất" (FR-23).
