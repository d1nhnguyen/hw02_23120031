# AI Audit Report · HW02 · 23120031

Phụ lục bắt buộc theo mẫu [AI-02] – FIT@HCMUS – AI Audit Report.

## 1. Thông tin sinh viên

| Mục | Giá trị |
| --- | --- |
| Họ tên sinh viên (in hoa) | |
| MSSV | 23120031 |
| Lớp / Khoá | |
| Mã bài tập | HW02-AI – Domain Testing trên EShop |
| Ngày làm bài | 20–21/10/2026 |
| Công cụ AI đã dùng | Claude Code (VS Code extension, model `claude-opus-5-5`); Google Antigravity IDE (model `Gemini 4 Argon (Medium)` – rà soát chéo FR-01) |
| Có dùng AI | [x] Có [ ] Không |

## 2. Cách audit

- Mỗi hàng ở mục 3 là một artifact AI sinh ra ở một bước của kỹ thuật (bảng biến I/O, bảng lớp tương đương, bộ test case DT, bộ test case BVA, nháp bug, bản rà soát chéo…).
- Prompt và câu trả lời của AI nguyên văn nằm ở `ai/prompt_log.md` (Phụ lục A, có thời gian, trích từ cả Claude Code lẫn Google Antigravity); output AI dạng file là commit `[<FEATURE>][B<n>]` trong git (cột 2), phần sửa sau rà soát là commit `[<FEATURE>][B<n>-review]` (cột 5).
- Với FR-01, sau khi Claude Code sinh các bước B1–B7, sinh viên dùng Google Antigravity (`Gemini 4 Argon`, lượt #13) để rà soát chéo theo tiêu chí bảng, cách đặt tên TC và mức độ chi tiết (hàng #9), duyệt kết quả rồi chuyển sang Claude Code (lượt #14) tạo các commit `[FR-01][Bn-review]` và tái sử dụng cấu trúc đã chuẩn hoá cho 3 feature còn lại.
- Verdict: **VALID** (đúng, dùng nguyên), **INVALID** (sai, loại bỏ), **INCOMPLETE** (chấp nhận sau khi sửa / bổ sung).
- Lý do dẫn chiếu slide môn học (S04 Domain Testing, S07 Test Case, Test Cases AI-First) hoặc ISTQB Foundation Level.
- Cột (5) ghi phần đã sửa sau rà soát; chi tiết từng mục nằm ở cột Origin trong bảng test case và mục 6.1 (AI gap analysis) của báo cáo từng feature. Mục 6.1 cũng liệt kê các lỗi AI tự phát hiện và sửa **trước** khi commit (không có commit review riêng).
- Bảng mục 3 được nháp bằng `scripts/audit_draft.py --prompt-log ai/prompt_log.md`; cột (1) là lượt prompt gần nhất trước commit.

## 3. Bảng audit — 1 hàng / artifact

<!-- NHÁP: cột (3) là verdict gợi ý tự động (có commit review → INCOMPLETE, không → VALID); sinh viên xác nhận / đổi verdict, điền cột (4), rồi xóa dòng chú thích này. -->

| # | (1) Prompt + Công cụ | (2) Output AI | (3) Verdict gợi ý | (4) Lý do (slide / ISTQB) | (5) Bản sửa sau rà soát |
| --- | --- | --- | --- | --- | --- |
| 1 | Claude Code – Báo cáo chung; prompt: lượt #12 (10-20 21:31): «Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi…» | `3de93f9` 2026-10-20 21:35 – Thêm phần phương pháp; chỉnh khung báo cáo theo mẫu của môn (8 files changed, 171 insertions(+), 90 deletions(-)) | VALID | | Không sửa |
| 2 | Claude Code – FR-01 B1 (Biến Input / Output); prompt: lượt #12 (10-20 21:31): «Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi…» | `c2f760e` 2026-10-20 21:36 – Xác định biến Input/Output, giả định và phạm vi (3 files changed, 56 insertions(+), 10 deletions(-)) | INCOMPLETE | | Theo rà soát chéo Antigravity lượt #13 (10-20 22:30): «kiểm tra fr-01 đã ổn chưa (bảng, cách đặt tên TC, mức độ chi tiết), ko…» → áp dụng ở lượt #14 (10-20 22:37): «&lt;pasted_content id="5e2c"> ### 1. Về Bảng (Cấu trúc & tính nhất quán)…»:<br>`32f8ff9` 2026-10-20 22:42 – Thêm giả định A10 về chữ hoa / chữ thường có dấu (1 file changed, 1 insertion(+)) |
| 3 | Claude Code – FR-01 B2 (Lớp tương đương); prompt: lượt #12 (10-20 21:31): «Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi…» | `8dc9aa6` 2026-10-20 21:38 – Xác định lớp tương đương (Complete Set of Partitions) (1 file changed, 69 insertions(+), 1 deletion(-)) | VALID | | Không sửa |
| 4 | Claude Code – FR-01 B3 (Test case Minimum Set); prompt: lượt #12 (10-20 21:31): «Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi…» | `9d54442` 2026-10-20 21:39 – Thiết kế test case Domain Testing (Minimum Set) (1 file changed, 95 insertions(+), 4 deletions(-)) | INCOMPLETE | | Theo rà soát chéo Antigravity lượt #13 (10-20 22:30): «kiểm tra fr-01 đã ổn chưa (bảng, cách đặt tên TC, mức độ chi tiết), ko…» → áp dụng ở lượt #14 (10-20 22:37): «&lt;pasted_content id="5e2c"> ### 1. Về Bảng (Cấu trúc & tính nhất quán)…»:<br>`1f499aa` 2026-10-20 22:42 – Dữ liệu cụ thể, kết quả mong đợi tường minh, ID có tiền tố feature (6 files changed, 1050 insertions(+), 281 deletions(-)) |
| 5 | Claude Code – FR-01 B4 (Test case BVA); prompt: lượt #12 (10-20 21:31): «Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi…» | `ceb5928` 2026-10-20 21:41 – Phân tích giá trị biên (BVA) (1 file changed, 47 insertions(+), 4 deletions(-)) | INCOMPLETE | | Theo rà soát chéo Antigravity lượt #13 (10-20 22:30): «kiểm tra fr-01 đã ổn chưa (bảng, cách đặt tên TC, mức độ chi tiết), ko…» → áp dụng ở lượt #14 (10-20 22:37): «&lt;pasted_content id="5e2c"> ### 1. Về Bảng (Cấu trúc & tính nhất quán)…»:<br>`9ff726d` 2026-10-20 22:43 – Bảng BVA giữ đủ cột dữ liệu, tên đầy đủ cho dòng dẫn chiếu (1 file changed, 37 insertions(+), 34 deletions(-)) |
| 6 | Claude Code – FR-01 B5 (Thực thi + script); prompt: lượt #12 (10-20 21:31): «Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi…» | `690a316` 2026-10-20 22:06 – Thực thi 49 test case trên Web và API (85 files changed, 3645 insertions(+), 4 deletions(-)) | INCOMPLETE | | Theo rà soát chéo Antigravity lượt #13 (10-20 22:30): «kiểm tra fr-01 đã ổn chưa (bảng, cách đặt tên TC, mức độ chi tiết), ko…» → áp dụng ở lượt #14 (10-20 22:37): «&lt;pasted_content id="5e2c"> ### 1. Về Bảng (Cấu trúc & tính nhất quán)…»:<br>`f798f69` 2026-10-20 22:49 – Chạy lại 53 test case với ID mới; kết quả mỗi test case một dòng (82 files changed, 349 insertions(+), 213 deletions(-)) |
| 7 | Claude Code – FR-01 B6 (AI gap analysis); prompt: lượt #12 (10-20 21:31): «Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi…» | `6ab932b` 2026-10-20 22:08 – AI gap analysis và bổ sung DT-29 (9 files changed, 107 insertions(+), 7 deletions(-)) | INCOMPLETE | | Theo rà soát chéo Antigravity lượt #13 (10-20 22:30): «kiểm tra fr-01 đã ổn chưa (bảng, cách đặt tên TC, mức độ chi tiết), ko…» → áp dụng ở lượt #14 (10-20 22:37): «&lt;pasted_content id="5e2c"> ### 1. Về Bảng (Cấu trúc & tính nhất quán)…»:<br>`8560448` 2026-10-20 22:43 – Bổ sung phát hiện khi rà soát và test case chữ có dấu (1 file changed, 19 insertions(+), 6 deletions(-)) |
| 8 | Claude Code – FR-01 B7 (Nháp bug report); prompt: lượt #12 (10-20 21:31): «Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi…» | `3818f4a` 2026-10-20 22:11 – Nháp báo cáo 9 bug kèm ảnh bằng chứng (13 files changed, 378 insertions(+), 23 deletions(-)) | INCOMPLETE | | Theo rà soát chéo Antigravity lượt #13 (10-20 22:30): «kiểm tra fr-01 đã ổn chưa (bảng, cách đặt tên TC, mức độ chi tiết), ko…» → áp dụng ở lượt #14 (10-20 22:37): «&lt;pasted_content id="5e2c"> ### 1. Về Bảng (Cấu trúc & tính nhất quán)…»:<br>`b7b58bf` 2026-10-20 22:49 – Cập nhật ID test case trong bug report, thêm test case mới vào bug liên quan (2 files changed, 24 insertions(+), 24 deletions(-)) |
| 9 | Google Antigravity (Gemini 4 Argon) – FR-01 Rà soát chéo (bảng, tên TC, mức chi tiết); prompt: lượt #13 (10-20 22:30): «kiểm tra fr-01 đã ổn chưa (bảng, cách đặt tên TC, mức độ chi tiết), ko…» | Bản nhận xét rà soát FR-01 trong `ai/prompt_log.md` mục #13 (phát hiện G9–G16, gợi ý kiểm tra chữ có dấu `Đ`, `ă` từ mục 6.3) | VALID | | Sinh viên duyệt và chuyển sang Claude Code áp dụng ở lượt #14 (10-20 22:37): «&lt;pasted_content id="5e2c"> ### 1. Về Bảng (Cấu trúc & tính nhất quán)…» (commits `32f8ff9`…`b7b58bf`) |
| 10 | Claude Code – FR-15 B1 (Biến Input / Output); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `6dd3331` 2026-10-20 22:55 – Xác định biến Input/Output, giả định và phạm vi (4 files changed, 51 insertions(+), 9 deletions(-)) | VALID | | Không sửa |
| 11 | Claude Code – FR-15 B2 (Lớp tương đương); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `2567e1d` 2026-10-20 22:56 – Xác định lớp tương đương (Complete Set of Partitions) (1 file changed, 54 insertions(+), 1 deletion(-)) | VALID | | Không sửa |
| 12 | Claude Code – FR-15 B3 (Test case Minimum Set); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `2e81bb9` 2026-10-20 23:01 – Thiết kế test case Domain Testing (Minimum Set) (4 files changed, 1793 insertions(+), 4 deletions(-)) | VALID | | Không sửa |
| 13 | Claude Code – FR-15 B4 (Test case BVA); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `91c2856` 2026-10-20 23:01 – Phân tích giá trị biên (BVA) (1 file changed, 52 insertions(+), 4 deletions(-)) | VALID | | Không sửa |
| 14 | Claude Code – FR-15 B5 (Thực thi + script); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `009cef0` 2026-10-20 23:15 – Thực thi 60 test case trên Web Admin và API (47 files changed, 2874 insertions(+), 11 deletions(-)) | VALID | | Không sửa |
| 15 | Claude Code – FR-15 B6 (AI gap analysis); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `0eff687` 2026-10-20 23:18 – AI gap analysis và bổ sung FR15-DT-34 (6 files changed, 229 insertions(+), 72 deletions(-))<br>`bc95ced` 2026-10-20 23:26 – Cập nhật bảng phủ phân vùng với FR15-DT-34 (1 file changed, 6 insertions(+), 6 deletions(-)) | VALID | | Không sửa |
| 16 | Claude Code – FR-15 B7 (Nháp bug report); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `72d380f` 2026-10-20 23:21 – Nháp báo cáo 6 bug kèm ảnh bằng chứng (11 files changed, 329 insertions(+), 4 deletions(-)) | VALID | | Không sửa |
| 17 | Claude Code – FR-10 B1 (Biến Input / Output); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `92dfeeb` 2026-10-20 23:23 – Xác định biến Input/Output, giả định và phạm vi (4 files changed, 45 insertions(+), 9 deletions(-)) | VALID | | Không sửa |
| 18 | Claude Code – FR-10 B2 (Lớp tương đương); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `77e0dd3` 2026-10-20 23:24 – Xác định lớp tương đương (Complete Set of Partitions) (1 file changed, 47 insertions(+), 1 deletion(-)) | VALID | | Không sửa |
| 19 | Claude Code – FR-10 B3 (Test case Minimum Set); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `5265fd8` 2026-10-20 23:26 – Thiết kế test case Domain Testing (Minimum Set) (5 files changed, 1353 insertions(+), 7 deletions(-)) | VALID | | Không sửa |
| 20 | Claude Code – FR-10 B4 (Test case BVA); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `e45dffd` 2026-10-20 23:26 – Phân tích giá trị biên (BVA) (1 file changed, 52 insertions(+), 4 deletions(-)) | VALID | | Không sửa |
| 21 | Claude Code – FR-10 B5 (Thực thi + script); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `4276d8b` 2026-10-20 23:31 – Thực thi 47 test case trên Web Admin, Web và API (18 files changed, 1248 insertions(+), 8 deletions(-)) | VALID | | Không sửa |
| 22 | Claude Code – FR-10 B6 (AI gap analysis); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `2e04420` 2026-10-20 23:32 – AI gap analysis (1 file changed, 31 insertions(+), 3 deletions(-)) | VALID | | Không sửa |
| 23 | Claude Code – FR-10 B7 (Nháp bug report); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `74061ad` 2026-10-20 23:32 – Nháp báo cáo 2 bug kèm ảnh bằng chứng (5 files changed, 139 insertions(+), 2 deletions(-)) | VALID | | Không sửa |
| 24 | Claude Code – Mobile B1 (Biến Input / Output); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `c4e2599` 2026-10-20 23:45 – Xác định biến Input/Output, giả định và phạm vi (6 files changed, 166 insertions(+), 9 deletions(-)) | VALID | | Không sửa |
| 25 | Claude Code – Mobile B2 (Lớp tương đương); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `1e0302e` 2026-10-20 23:46 – Xác định lớp tương đương (Complete Set of Partitions) (1 file changed, 37 insertions(+), 1 deletion(-)) | VALID | | Không sửa |
| 26 | Claude Code – Mobile B3 (Test case Minimum Set); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `5192f42` 2026-10-20 23:47 – Thiết kế test case Domain Testing (Minimum Set) (5 files changed, 850 insertions(+), 7 deletions(-)) | VALID | | Không sửa |
| 27 | Claude Code – Mobile B4 (Test case BVA); prompt: lượt #15 (10-20 22:52): «tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả…» | `17ab584` 2026-10-20 23:47 – Phân tích giá trị biên (BVA) (1 file changed, 30 insertions(+), 4 deletions(-)) | VALID | | Không sửa |
| 28 | Claude Code – Agent Skill; prompt: lượt #19 (10-21 00:26): «kiếm tra lại, vscode vừa bị dừng» | `684d43e` 2026-10-21 00:31 – Agent Skills: domain-testing-bva và ai-audit-log (11 files changed, 868 insertions(+)) | VALID | | Không sửa |
| 29 | Claude Code – Mobile B5 (Thực thi + script); prompt: lượt #19 (10-21 00:26): «kiếm tra lại, vscode vừa bị dừng» | `fc60508` 2026-10-21 01:04 – Thực thi 23 test case trên Mobile (Pixel 2) và API (32 files changed, 1372 insertions(+), 18 deletions(-)) | VALID | | Không sửa |
| 30 | Claude Code – Mobile B6 (AI gap analysis); prompt: lượt #19 (10-21 00:26): «kiếm tra lại, vscode vừa bị dừng» | `9da72e3` 2026-10-21 01:04 – AI gap analysis và bổ sung MOB-DT-14 (6 files changed, 120 insertions(+), 10 deletions(-)) | VALID | | Không sửa |
| 31 | Claude Code – Mobile B7 (Nháp bug report); prompt: lượt #19 (10-21 00:26): «kiếm tra lại, vscode vừa bị dừng» | `47822d2` 2026-10-21 01:05 – Nháp báo cáo 5 bug kèm ảnh bằng chứng (9 files changed, 240 insertions(+), 5 deletions(-)) | VALID | | Không sửa |
| 32 | Claude Code – Agent Skill; prompt: lượt #19 (10-21 00:26): «kiếm tra lại, vscode vừa bị dừng» | `c8533e5` 2026-10-21 01:09 – ai-audit-log: audit_draft ghi lượt prompt và hàng cho commit [skill] / [report] (2 files changed, 51 insertions(+), 16 deletions(-)) | VALID | | Không sửa |
| 33 | Claude Code – Báo cáo chung; prompt: lượt #19 (10-21 00:26): «kiếm tra lại, vscode vừa bị dừng» | `3be474b` 2026-10-21 01:09 – README: test summary 4 feature (test case, lượt chạy, bug) (1 file changed, 34 insertions(+), 6 deletions(-)) | VALID | | Không sửa |

## 4. Tổng kết độ chính xác AI

<!-- NHÁP: tạm tính theo verdict gợi ý ở mục 3; tính lại sau khi sinh viên duyệt. -->

| Chỉ số | Số lượng | Tỉ lệ |
| --- | --- | --- |
| Tổng artifact AI sinh đã audit | 33 | 100% |
| VALID (đúng, dùng nguyên) | 27 | 82% |
| INVALID (sai, loại bỏ) | 0 | 0% |
| INCOMPLETE (chấp nhận sau khi sửa) | 6 | 18% |

## 5. Kết luận — Khi nào nên / không nên dùng AI?

<!-- 80–150 chữ: AI mạnh ở đâu, sai ở đâu, khuyến nghị dùng AI cho loại công việc này. -->

## 6. Mandatory Disclosure

<!-- Điền theo mẫu: "[Test case / script / dataset / báo cáo] này được sinh phiên bản đầu bởi [tên công cụ AI]; tôi đã rà soát và chỉnh sửa [phần X], bổ sung [edge case Y, Z]; [phần W] do tôi tự viết. AI Audit Report chi tiết đính kèm ở Phụ lục A. Tôi cam đoan không dùng AI để sinh bất kỳ artifact nào thuộc danh mục bị cấm." -->

## Chữ ký

| Mục | Giá trị |
| --- | --- |
| Họ tên sinh viên (in hoa) | |
| MSSV | 23120031 |
| Lớp / Khoá | |
| Môn học | CS423 / CSC13003 – Kiểm chứng Phần mềm |
| Giảng viên | |
| Ngày | |
| Chữ ký | |
