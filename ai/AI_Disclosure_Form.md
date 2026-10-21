# Biểu mẫu Khai báo Sử dụng AI · HW02 · 23120031

Theo mẫu [AI-03] – FIT@HCMUS – AI Disclosure Form.

## 1. Thông tin môn học & sinh viên

| Mục              | Giá trị                                |
| ---------------- | -------------------------------------- |
| Môn học          | CS423 / CSC13003 – Kiểm chứng Phần mềm |
| Mã bài tập       | HW02-AI                                |
| Tên bài tập      | Domain Testing trên EShop              |
| Cấp độ AI (1–5)  | Cấp 4 – AI hỗ trợ sản xuất             |
| Ngày             |                                        |
| Họ tên sinh viên |                                        |
| MSSV             | 23120031                               |

## 2. Câu hỏi khai báo

### 2.1 Công cụ AI đã dùng

- Claude Code (Anthropic), extension cho VS Code, model Claude Opus 5.5 (`claude-opus-5-5`).
- Google Antigravity IDE (Google DeepMind), model Gemini 4 Argon (`Gemini 4 Argon (Medium)`) – dùng để rà soát chéo báo cáo FR-01 (kiểm tra cấu trúc bảng, cách đặt tên TC, mức độ chi tiết).

### 2.2 Giai đoạn của bài tập có dùng AI

- [x] brainstorm – đọc đề, lập kế hoạch, nêu các điểm chưa rõ của đề (lượt #1–#2)
- [x] outline – khung báo cáo, quy ước test case / commit (`PLAN.md`, `report/00_Phuong_phap.md`)
- [x] viết nháp – bước 1–4 và 6 của Domain Testing + BVA cho 4 feature, nháp 22 bug report
- [x] phản hồi – rà soát chéo báo cáo FR-01 bằng Google Antigravity (lượt #13)
- [x] sửa chữa – sửa FR-01 theo nhận xét rà soát (lượt #13 Antigravity → lượt #14 Claude Code)
- [x] code – script chạy test (Playwright, adb, Python), sinh bảng báo cáo, ảnh bằng chứng, Agent Skills
- [x] phân tích dữ liệu – tổng hợp kết quả chạy test (mục 5 mỗi báo cáo, README)
- [ ] thiết kế đồ hoạ
- [ ] khác (ghi rõ):

### 2.3 Prompt / nhiệm vụ chính cho AI

Toàn bộ prompt ở Phụ lục A (`ai/prompt_log.md`). Bốn prompt chính (nguyên văn):

1. Lượt #1 (20/10/2026 20:46, Claude Code) – lập kế hoạch:

   > đọc đề bài @HW02/ và @\_\_\_2026.Homework.Policies.md, nội dung về domain testing, cách viết test case có trong @Slides tôi đảm nhận các chức năng FR-01, FR-10, FR-15 và đăng nhập ở mobile, Repo sut chung đã có và tôi có thể tạo các issues. Ghi log lại mọi thứ như trong yêu cầu của @"AI Templates/". hãy lên một plan cụ thể để hoàn thành bài này, kiểm tra còn điểm nào chưa rõ ko và thảo luận với tôi.

2. Lượt #12 (20/10/2026 21:31, Claude Code) – thực hiện các bước cho FR-01:

   > Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi tôi, đọc kỹ các bài giảng/hướng dẫn về domain testing có trong @slides và @slides/refs, cũng như cách viết các test cases có trong đó

3. Lượt #13 (20/10/2026 22:30, Google Antigravity) – rà soát chéo báo cáo FR-01:

   > kiểm tra fr-01 đã ổn chưa (bảng, cách đặt tên TC, mức độ chi tiết), ko cần ghi log phần này

4. Lượt #15 (20/10/2026 22:52, Claude Code) – thực hiện FR-15, FR-10, Mobile theo mẫu đã chuẩn hoá:

   > tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả các điểm cần tôi đối chiếu để nhắc lại trước khi nộp bài

### 2.4 Phần cụ thể AI đóng góp

| Phần                                                                                               | AI đóng góp                                                                                                                                                  | Sửa / bổ sung sau rà soát                                                                                                                             |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bước 1–4 (biến I/O, lớp tương đương, Minimum Set, BVA) của FR-01, FR-10, FR-15, Mobile – Đăng nhập | Phiên bản đầu của toàn bộ bảng; 180 / 185 test case Origin AI                                                                                                | FR-01: rà soát chéo bằng Antigravity (lượt #13) và sửa bằng Claude Code (lượt #14) – 5 test case AI-sửa (`FR01-DT-02`, `FR01-BV-19`, `FR01-DT-30…32`) |
| Bước 5 – thực thi                                                                                  | Script chạy test, chạy test trên SUT, bảng kết quả và ảnh bằng chứng (`scripts/`, `evidence/`)                                                               | FR-01: chạy lại 53 test case sau rà soát, mỗi test case một dòng kết quả kèm bằng chứng                                                               |
| Bước 6 – AI gap analysis                                                                           | Mục 6 mỗi báo cáo (FR-01 G1–G8, FR-15 G1–G5, FR-10 G1–G3, Mobile G1–G5) và test case bổ sung FR01-DT-29, FR15-DT-34, MOB-DT-14                               | FR-01 G9–G16, FR01-DT-30…32 phát hiện qua rà soát chéo với Antigravity (lượt #13)                                                                     |
| Bước 7 – bug                                                                                       | Nháp mô tả 22 bug (`bugs/Bug_Report.md`), ảnh bằng chứng và nội dung dán vào issue (`scripts/github_issues.py`); Antigravity đối chiếu 22 bug (lượt #21–#22) | Sinh viên duyệt, tự tạo 22 issue BUG-15…BUG-36 bằng tài khoản d1nhnguyen và đính ảnh                                                                  |
| Agent Skill                                                                                        | `.claude/skills/domain-testing-bva` (quy trình 7 bước, template, thư viện sinh bảng, bài học khi tự động hoá)                                                |                                                                                                                                                       |
| Script hồ sơ AI                                                                                    | `scripts/export_prompt_log.py`, `scripts/audit_draft.py`                                                                                                     | Hỗ trợ trích log cả Claude Code và Google Antigravity                                                                                                 |
| Hồ sơ AI                                                                                           | Prompt log (trích tự động); bảng AI Audit Report, cột lý do, kết luận và Mandatory Disclosure (Claude Code, lượt #26)                                        | Sinh viên đồng ý verdict (lượt #26) và duyệt phần nháp                                                                                                |
| AI Critique                                                                                        | Claude Code nháp theo yêu cầu (lượt #26), dựa trên mục 6 của 4 báo cáo                                                                                       | Sinh viên duyệt / chỉnh                                                                                                                               |
| Video demo | Claude Code gợi ý kịch bản cảnh và prompt (`KICH_BAN_DEMO.md`, lượt #29); phiên chạy skill trong video (FR-02, nhánh demo riêng) hiển thị trực tiếp trong video, không đưa vào bài nộp | Sinh viên tự quay, tự nói, chọn nội dung |
| Điểm tự chấm | Không | |

### 2.5 Cách tôi rà soát / chỉnh sửa / xác minh đầu ra AI

- Mọi kết quả mong đợi dẫn chiếu đặc tả (mục 0 mỗi báo cáo, trích README của SUT); giả định ghi ở mục 1.4 mỗi báo cáo.
- Dùng công cụ AI thứ hai (Google Antigravity – Gemini 4 Argon, lượt #13) rà soát chéo báo cáo FR-01 đối chiếu với slide môn học, sau đó duyệt nhận xét và áp dụng cho cả 4 feature.
- Test được chạy trên SUT thật; oracle đọc trạng thái qua API trước / sau mỗi thao tác; ảnh bằng chứng cho từng test case.

### 2.6 Trích dẫn (IEEE)

[1] Anthropic, "Claude Code (Claude Opus 5.5)," [Large language model], 2026. [Online]. Available: https://claude.com/claude-code

[2] Google DeepMind, "Google Antigravity (Gemini 4 Argon)," [Large language model], 2026.

## 3. Cam đoan trung thực

Bằng việc ký tên dưới đây, tôi cam đoan thông tin khai báo ở trên là chính xác và đầy đủ. Tôi hiểu rằng việc không khai báo hoặc khai báo sai lệch về việc dùng AI sẽ bị coi là vi phạm liêm chính học thuật và có thể dẫn đến điểm 0 cho bài tập cùng việc bị chuyển lên hội đồng kỷ luật.

| Mục                       | Giá trị                                |
| ------------------------- | -------------------------------------- |
| Họ tên sinh viên (in hoa) |                                        |
| MSSV                      | 23120031                               |
| Lớp / Khoá                |                                        |
| Môn học                   | CS423 / CSC13003 – Kiểm chứng Phần mềm |
| Giảng viên                |                                        |
| Ngày                      |                                        |
| Chữ ký                    |                                        |
