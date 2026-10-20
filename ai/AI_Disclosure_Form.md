# Biểu mẫu Khai báo Sử dụng AI · HW02 · 23120031

Theo mẫu [AI-03] – FIT@HCMUS – AI Disclosure Form.

## 1. Thông tin môn học & sinh viên

| Mục | Giá trị |
| --- | --- |
| Môn học | CS423 / CSC13003 – Kiểm chứng Phần mềm |
| Mã bài tập | HW02-AI |
| Tên bài tập | Domain Testing trên EShop |
| Cấp độ AI (1–5) | Cấp 4 – AI hỗ trợ sản xuất |
| Ngày | |
| Họ tên sinh viên | |
| MSSV | 23120031 |

## 2. Câu hỏi khai báo

### 2.1 Công cụ AI đã dùng

- Claude Code (Anthropic), extension cho VS Code, model Claude Opus 5.5 (`claude-opus-5-5`).

### 2.2 Giai đoạn của bài tập có dùng AI

- [x] brainstorm – đọc đề, lập kế hoạch, nêu các điểm chưa rõ của đề (lượt #1–#2)
- [x] outline – khung báo cáo, quy ước test case / commit (`PLAN.md`, `report/00_Phuong_phap.md`)
- [x] viết nháp – bước 1–4 và 6 của Domain Testing + BVA cho 4 feature, nháp 22 bug report
- [ ] phản hồi
- [x] sửa chữa – sửa FR-01 theo nhận xét rà soát (lượt #13)
- [x] code – script chạy test (Playwright, adb, Python), sinh bảng báo cáo, ảnh bằng chứng, Agent Skills
- [x] phân tích dữ liệu – tổng hợp kết quả chạy test (mục 5 mỗi báo cáo, README)
- [ ] thiết kế đồ hoạ
- [ ] khác (ghi rõ):

### 2.3 Prompt / nhiệm vụ chính cho AI

Toàn bộ prompt ở Phụ lục A (`ai/prompt_log.md`). Ba prompt chính (nguyên văn):

1. Lượt #1 (20/10/2026 20:46) – lập kế hoạch:

   > đọc đề bài @HW02/ và @___2026.Homework.Policies.md, nội dung về domain testing, cách viết test case có trong @Slides tôi đảm nhận các chức năng  FR-01, FR-10, FR-15 và đăng nhập ở mobile, Repo sut chung đã có và tôi có thể tạo các issues. Ghi log lại mọi thứ như trong yêu cầu của @"AI Templates/". hãy lên một plan cụ thể để hoàn thành bài này, kiểm tra còn điểm nào chưa rõ ko và thảo luận với tôi.

2. Lượt #12 (20/10/2026 21:31) – thực hiện các bước cho FR-01:

   > Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi tôi, đọc kỹ các bài giảng/hướng dẫn về domain testing có trong @slides và @slides/refs, cũng như cách viết các test cases có trong đó

3. Lượt #14 (20/10/2026 22:52) – thực hiện FR-15, FR-10, Mobile:

   > tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả các điểm cần tôi đối chiếu để nhắc lại trước khi nộp bài

### 2.4 Phần cụ thể AI đóng góp

<!-- NHÁP do AI liệt kê từ git log và cột Origin; sinh viên kiểm tra, sửa cho đúng rồi xóa dòng này. -->

| Phần | AI đóng góp | Sửa / bổ sung sau rà soát |
| --- | --- | --- |
| Bước 1–4 (biến I/O, lớp tương đương, Minimum Set, BVA) của FR-01, FR-10, FR-15, Mobile – Đăng nhập | Phiên bản đầu của toàn bộ bảng; 180 / 185 test case Origin AI | FR-01: sửa theo nhận xét rà soát lượt #13 – 2 test case AI-sửa, 3 test case SV (FR01-DT-30…32) |
| Bước 5 – thực thi | Script chạy test, chạy test trên SUT, bảng kết quả và ảnh bằng chứng (`scripts/`, `evidence/`) | FR-01: chạy lại sau rà soát |
| Bước 6 – AI gap analysis | Mục 6 mỗi báo cáo (FR-01 G1–G8, FR-15 G1–G5, FR-10 G1–G3, Mobile G1–G5) và test case bổ sung FR01-DT-29, FR15-DT-34, MOB-DT-14 | FR-01 G9–G16, FR01-DT-30…32 từ bản rà soát |
| Bước 7 – bug | Nháp mô tả 22 bug (`bugs/Bug_Report.md`) và ảnh bằng chứng | Sinh viên duyệt và tự viết issue trên GitHub (sinh viên xác nhận) |
| Agent Skills | `skills/domain-testing-bva`, `skills/ai-audit-log` | |
| Hồ sơ AI | Prompt log (trích tự động), nháp bảng AI Audit Report | Sinh viên duyệt verdict, viết cột lý do và kết luận |
| AI Critique, điểm tự chấm, video demo | Không | |

### 2.5 Cách tôi rà soát / chỉnh sửa / xác minh đầu ra AI

<!-- Sinh viên tự viết (ngôi thứ nhất) những gì mình đã thực sự làm. Dữ kiện có sẵn để dẫn chiếu:
- Mọi kết quả mong đợi dẫn chiếu đặc tả (mục 0 mỗi báo cáo, trích README của SUT); giả định ghi ở mục 1.4 và DOI_CHIEU_TRUOC_KHI_NOP.md.
- Test được chạy trên SUT thật; oracle đọc trạng thái qua API trước / sau mỗi thao tác; ảnh bằng chứng cho từng test case.
- Mỗi bước một commit `[F][Bn]`, phần sửa sau rà soát là commit `[F][Bn-review]` (git_commit_log.txt).
-->

### 2.6 Trích dẫn (IEEE)

[1] Anthropic, "Claude Code (Claude Opus 5.5)," [Large language model], 2026. [Online]. Available: https://claude.com/claude-code

## 3. Cam đoan trung thực

Bằng việc ký tên dưới đây, tôi cam đoan thông tin khai báo ở trên là chính xác và đầy đủ. Tôi hiểu rằng việc không khai báo hoặc khai báo sai lệch về việc dùng AI sẽ bị coi là vi phạm liêm chính học thuật và có thể dẫn đến điểm 0 cho bài tập cùng việc bị chuyển lên hội đồng kỷ luật.

| Mục | Giá trị |
| --- | --- |
| Họ tên sinh viên (in hoa) | |
| MSSV | 23120031 |
| Lớp / Khoá | |
| Môn học | CS423 / CSC13003 – Kiểm chứng Phần mềm |
| Giảng viên | |
| Ngày | |
| Chữ ký | |
