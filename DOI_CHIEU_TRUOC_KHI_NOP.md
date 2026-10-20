# Các điểm sinh viên cần đối chiếu / quyết định trước khi nộp

Danh sách này được cập nhật trong suốt quá trình làm bài. Đánh dấu `[x]` khi đã xử lý. Không đưa file này vào bản nộp nếu không cần.

## Liêm chính & khai báo AI

- [ ] **Nguồn của bản rà soát FR-01** (G9–G16, FR01-DT-30…32 đang ghi "sinh viên rà soát" / Origin SV). Nếu bản rà soát do công cụ AI khác tạo: khai báo tên công cụ, prompt, output trong AI Audit Report và đổi nhãn Origin / nguồn phát hiện cho đúng.
- [ ] **Các phiên AI trước 20/10** (11/10 tóm tắt đề, 14/10 làm thử FR-01, 19/10 lập kế hoạch) đang không nằm trong prompt log. Quyết định có ghi một dòng trong AI Disclosure Form ("đã dùng AI để tìm hiểu đề, không dùng kết quả") hay không.
- [ ] **Bug report do AI nháp**: AI-01 §11 ghi "Bug report: 100% sinh viên viết; AI không được nháp mô tả", trong khi đề HW02 §11 ghi Anti-AI-Cheat "None". Đã chọn: AI nháp, sinh viên duyệt và tự viết issue → khai báo rõ trong Disclosure Form.
- [ ] Prompt log có cả phiên tạo repo (`4aefb10a`); kiểm tra nội dung trước khi nộp.
- [ ] 3 commit đầu trên GitHub còn dòng `Co-Authored-By: Claude`; quyết định giữ (minh bạch) hay viết lại lịch sử + force-push.

## Giả định cần hỏi TA

- [ ] FR-01: A1 (chỉ 7 ký tự `@ $ ! % * ? &` là ký tự đặc biệt), A2 (email phải có TLD), A3 (email trùng không phân biệt hoa thường), A4 (bỏ khoảng trắng đầu/cuối), A5 (không giới hạn độ dài), A10 (chữ hoa/thường chỉ A–Z/a–z).
- [ ] Pool D = các chức năng của FR-20; "Mobile – Đăng nhập" kế thừa quy tắc FR-02 (file phân công nhóm cũng ghi nên hỏi TA).

## Quyết định phương pháp (đã áp dụng, cần sinh viên xác nhận)

- [ ] Test case bị một lỗi khác che → **Blocked** ở lượt chính thức + lượt **khảo sát** không tính verdict (FR-01: 15 test case Web).
- [ ] Mức độ nghiêm trọng của từng bug (FR-01: 2 Critical, 4 Major, 3 Minor).
- [ ] Cách đếm số liệu tổng: theo lượt chạy từng kênh (Web/API) và theo test case gộp kênh.

## GitHub Issues

- [ ] Tạo issue cho FR01-B1…FR01-B9 trên `d1nhnguyen/eshop-sut` (số tiếp theo lúc kiểm tra 20/10: BUG-12), đính kèm ảnh trong `bugs/screenshots/`.
- [ ] Gửi lại số BUG-NN để điền vào `bugs/Bug_Report.md` và mục 7 mỗi báo cáo; chụp trang issue lưu `bugs/screenshots/BUG-NN_issue.png`.
- [ ] Kiểm tra không trùng bug với thành viên khác trong nhóm.

## Hồ sơ nộp

- [ ] Điền họ tên, lớp/khoá, giảng viên, ngày, chữ ký trong `ai/AI_Audit_Report.md`, `AI_Disclosure_Form.md`, `AI_Privacy_Checklist.md`.
- [ ] AI Critique 200–300 từ (sinh viên viết / duyệt).
- [ ] Video demo Agent Skill có **giọng nói của sinh viên** (AI-01 §10), đăng YouTube, điền link vào README.
- [ ] Điểm tự chấm trong README và tên file zip `23120031_HW02_AI_DomainTesting_<điểm>.zip`.
- [ ] Điền sheet phân công nhóm (`HW02_Phan_cong_nhom.xlsx`), kiểm tra không trùng feature.
- [ ] Xuất PDF cho báo cáo chính, bug report, AI Audit Report, AI Critique; xuất `git_commit_log.txt`.

## Môi trường

- [ ] Bản SUT local đã sửa `frontend-mobile/App.js:16` (API_URL → `10.0.2.2`) để chạy trên Android Emulator – đã ghi trong PLAN.md.
