# Các điểm sinh viên cần đối chiếu / quyết định trước khi nộp

Danh sách này được cập nhật trong suốt quá trình làm bài. Đánh dấu `[x]` khi đã xử lý. Không đưa file này vào bản nộp nếu không cần.

## Liêm chính & khai báo AI

- [x] **Nguồn của bản rà soát FR-01** (G9–G16, FR01-DT-30…32): đã khai báo đầy đủ phiên rà soát chéo bằng Google Antigravity (Gemini 4 Argon, lượt #13) trong `ai/prompt_log.md`, `ai/AI_Audit_Report.md`, `ai/AI_Disclosure_Form.md`, `report/FR-01_Dang_ky.md` và cập nhật nhãn Origin / nguồn phát hiện.
- [x] **Các phiên AI trước 20/10** (11/10 tóm tắt đề, 14/10 làm thử FR-01, 19/10 lập kế hoạch) đang không nằm trong prompt log. Quyết định có ghi một dòng trong AI Disclosure Form ("đã dùng AI để tìm hiểu đề, không dùng kết quả") hay không. → Sinh viên quyết định bỏ qua (21/10): các phiên đó không đóng góp vào bài làm.
- [x] **Bug report do AI nháp**: AI-01 §11 ghi "Bug report: 100% sinh viên viết; AI không được nháp mô tả", trong khi đề HW02 §11 ghi Anti-AI-Cheat "None". Đã chọn: AI nháp, sinh viên duyệt và tự viết issue → khai báo rõ trong Disclosure Form. → Đã nháp lời khai báo trong Mandatory Disclosure (Audit Report mục 6); sinh viên xác nhận cách khai báo. Sinh viên đã duyệt (21/10).
- [x] Prompt log có cả phiên tạo repo (`4aefb10a`); kiểm tra nội dung trước khi nộp. → Giữ (21/10).
- [x] 3 commit đầu trên GitHub còn dòng `Co-Authored-By: Claude`; quyết định giữ (minh bạch) hay viết lại lịch sử + force-push. → Giữ nguyên (21/10).

## Giả định cần hỏi TA

Sinh viên quyết định **không hỏi TA** (21/10): giữ các giả định như đã ghi ở mục 1.4 mỗi báo cáo.

- [x] FR-01: A1 (chỉ 7 ký tự `@ $ ! % * ? &` là ký tự đặc biệt), A2 (email phải có TLD), A3 (email trùng không phân biệt hoa thường), A4 (bỏ khoảng trắng đầu/cuối), A5 (không giới hạn độ dài), A10 (chữ hoa/thường chỉ A–Z/a–z).
- [x] FR-15: A1 (255 ký tự tính theo ký tự Unicode), A3 (giá được phép là số thập phân dương, không giới hạn trên – ảnh hưởng kết luận về việc ô Giá chặn `0.5`), A6 (mã 404 khi sản phẩm không tồn tại).
- [x] FR-10: A1 (Admin **không** được hủy đơn `shipping` – sơ đồ không có cạnh `shipping → canceled`, nhưng câu "chỉ Admin mới có thể thao tác" có thể hiểu khác), A6 (User hủy đơn của người khác – giao với FR-11).
- [x] Pool D = các chức năng của FR-20; "Mobile – Đăng nhập" kế thừa quy tắc FR-02 (file phân công nhóm cũng ghi nên hỏi TA).
- [x] Mobile – Đăng nhập: A2 (khóa ngay sau lần sai thứ 3), A3 (đăng nhập đúng đặt lại bộ đếm), A6 (email không phân biệt hoa thường / bỏ khoảng trắng).

## Quyết định phương pháp (đã áp dụng, cần sinh viên xác nhận)

- [x] Test case bị một lỗi khác che → **Blocked** ở lượt chính thức + lượt **khảo sát** không tính verdict (FR-01: 15 test case Web). → Tạm giữ như hiện tại (21/10); cách xử lý đã ghi ở `report/00_Phuong_phap.md` và mục 5 báo cáo FR-01.
- [x] Mức độ nghiêm trọng của từng bug (FR-01: 2 Critical, 4 Major, 3 Minor; FR-15: 5 Major, 1 Minor; FR-10: 1 Critical, 1 Major; Mobile: 1 Critical, 2 Major, 2 Minor). → Giữ theo tài liệu (21/10).
- [x] Cách đếm số liệu tổng: theo lượt chạy từng kênh (Web/API) và theo test case gộp kênh. → Áp dụng (21/10).

## GitHub Issues

- [x] Đã tạo 22 issue #15–#36 (BUG-15…BUG-36) bằng tài khoản d1nhnguyen ngày 21/10; đã đối chiếu tiêu đề, mã, nội dung và ảnh với bản nháp; đã điền link vào `bugs/Bug_Report.md`, mục 7 các báo cáo và chụp trang issue `bugs/screenshots/BUG-NN_issue.png`.
- [x] **#24 (FR15-B1) và #27 (FR15-B4) bị dán trùng ảnh** (cùng một ảnh 2 lần): sửa issue, xóa ảnh trùng; ở #24 có thể thay bằng `bugs/screenshots/FR15-admin-products.png`.
- [x] (Tuỳ chọn, sinh viên không thêm) Thêm ảnh phụ có trong bug report nhưng bản nháp issue chưa nhắc: `FR01-admin-users.png` cho #17 (FR01-B3), #18 (FR01-B4), #20 (FR01-B6).
- [x] Sửa xong (21/10) → đã kiểm tra lại ảnh 22 issue và chụp lại trang #24, #27.
- [x] Kiểm tra không trùng bug với thành viên khác trong nhóm – đặc biệt MOB-B2, MOB-B3, MOB-B4 là lỗi backend của quy tắc đăng nhập (FR-02), có thể trùng với người kiểm thử đăng nhập Web. → Đã đối chiếu 22 bug với BUG-01…BUG-14 (21/10): không trùng hẳn, có 2 nhóm liên quan, giữ riêng và dẫn chiếu chéo trong `bugs/Bug_Report.md`:
  - BUG-15 (FR01-B1) ↔ BUG-01 (FR-03): cùng quy tắc mật khẩu sai trên form Đặt lại mật khẩu – đã kiểm tra lại hộp đen (`evidence/FR-01/explore_reset_password.json`).
  - BUG-18 (FR01-B4), BUG-21 (FR01-B7) ↔ BUG-02 (FR-03): cùng kiểu thiếu kiểm tra định dạng email, khác form.
  - BUG-27 (FR15-B4, tên sản phẩm rỗng) và BUG-07 (FR-14, tên danh mục rỗng): khác đối tượng, không trùng.
  - (Tuỳ chọn) Thêm comment dẫn chiếu chéo trên các issue #15 ↔ #1, #18 / #21 ↔ #2; nếu thêm thì chạy lại `github_issues.py fill --shots`.

## Hồ sơ nộp

- [ ] Điền họ tên, lớp/khoá, giảng viên, ngày, chữ ký trong `ai/AI_Audit_Report.md`, `AI_Disclosure_Form.md`, `AI_Privacy_Checklist.md`.
- [x] **AI Critique**: Claude Code đã nháp (291 từ) theo yêu cầu (lượt #26) – sinh viên đọc, chỉnh theo ý mình, xóa chú thích `NHÁP`. → Sinh viên đã duyệt (21/10).
- [x] **AI Audit Report**: sinh viên đã đồng ý verdict hàng #1–#33 (lượt #26). Claude Code nháp cột (4), hàng #34–#41 (verdict đề xuất – xem kỹ #34, #35, #37), mục 5 và mục 6 Mandatory Disclosure → sinh viên duyệt, xóa chú thích `NHÁP`; nếu sửa Critique / Audit thì đổi `VALID*` của hàng #40, #41. → Sinh viên đã duyệt (21/10); thêm câu khai báo theo đề §9.
- [x] FR-15, FR-10, Mobile không có commit rà soát: sinh viên đồng ý verdict VALID, không sửa (21/10).
- [x] **AI Disclosure Form**: kiểm tra bảng 2.4 (AI nháp), tự viết mục 2.5, xóa chú thích `NHÁP`. → Đã duyệt bảng 2.4 và viết mục 2.5 (21/10).
- [ ] Video demo Agent Skill có **giọng nói của sinh viên** (AI-01 §10), đăng YouTube, điền link vào README.
- [ ] Điểm tự chấm trong README và tên file zip `23120031_HW02_AI_DomainTesting_<điểm>.zip` – điểm **3 chữ số** 000–100 (vd `090`).
- [ ] Đánh dấu các ô trong `ai/AI_Privacy_Checklist.md` (mẫu AI-05).
- [ ] Cross-review bài của thành viên khác trong nhóm (quy định chung của môn, không nằm trong file nộp HW02).
- [ ] Điền sheet phân công nhóm (`HW02_Phan_cong_nhom.xlsx`), kiểm tra không trùng feature.
- [ ] Đóng gói (Claude làm khi sinh viên xong các mục trên):
  - Báo cáo chính gộp `report/` (phương pháp + 4 feature, mỗi feature có Domain Testing và BVA), **kết thúc bằng đoạn Mandatory Disclosure** (AI-01 §8).
  - PDF cho báo cáo chính, bug report, AI Audit Report, AI Critique (và các file .md khác); `git_commit_log.txt`; prompt log cập nhật lần cuối.
  - Giới hạn Moodle 20 MB / file: ảnh PNG trong bản nộp được giảm còn 256 màu (thử: 18,4 MB → 7,2 MB), ảnh gốc giữ nguyên trong git.
  - Không đưa vào zip: `node_modules/`, `DOI_CHIEU_TRUOC_KHI_NOP.md`, `bugs/issues/`.
  - Chuẩn hoá ô đánh dấu `[ x]` / `[x ]` / `[ ]x` thành `[x]` (GFM chỉ hiện checkbox với `[x]`).

## Môi trường

- [ ] Mobile được thực thi trên Android Emulator **Pixel 2** vì trên **Pixel 6** thanh tiêu đề bị thanh trạng thái che, không mở được màn hình Đăng nhập (đã báo bug). Nếu có điện thoại thật, nên thử lại để xác nhận mức độ ảnh hưởng.

- [ ] Bản SUT local đã sửa `frontend-mobile/App.js:16` (API_URL → `10.0.2.2`) để chạy trên Android Emulator – đã ghi trong PLAN.md.

## Quan sát ngoài phạm vi (báo cho thành viên phụ trách nếu cần)

- [ ] Gợi ý cross-review cho nhóm (issue của bạn khác):
  - BUG-12, BUG-14 (web) và BUG-09 (mobile) cùng hiện tượng: áp SAVE10 cho tổng tiền nhân 10 thay vì giảm 10% – nên gộp hoặc dẫn chiếu chéo.
  - BUG-12…BUG-14 gắn `[FR-04]` (hồ sơ cá nhân) nhưng nội dung là mã giảm giá (FR-09).
  - BUG-06 (tổng tiền âm) là một trường hợp của BUG-05 (thanh toán dùng số tiền người dùng nhập).
- [ ] FR-02 / FR-21 (Web – Đăng nhập, không ai làm): trang Đăng nhập Web cũng dùng nhãn "Username" và nút "Sign In" giống MOB-B5 – thấy khi khảo sát FR-03 ngày 21/10.
- [ ] FR-06 (chi tiết sản phẩm): `GET /api/products/:id` trả `price` dạng **chuỗi** với sản phẩm có id chẵn, dạng số với id lẻ (danh sách `GET /api/products` luôn là số) – phát hiện khi làm FR-15.
- [ ] FR-21 (giao diện chung): trang Đăng ký không có thẻ `<h1>`, nút "Đăng Ký" màu đỏ – phát hiện khi làm FR-01.
- [ ] FR-21: danh sách sản phẩm trong Web Admin hiển thị giá không có phân cách hàng nghìn (`30000000 ₫`) – phát hiện khi làm FR-15.
- [ ] Mobile – Đăng xuất (Pool D, người khác): nút đăng xuất ghi "Thoát" thay vì "Đăng xuất" (FR-23).
