# HW02 – Domain Testing trên EShop · 23120031

| Mục | Giá trị |
| --- | --- |
| MSSV | 23120031 |
| Mã bài | HW02-AI |
| SUT | EShop (`ttbhanh/eshop-sut`, bản dùng chung của nhóm: `d1nhnguyen/eshop-sut`) |
| Nơi báo bug | GitHub Issues của `d1nhnguyen/eshop-sut` |
| Feature | FR-01 Đăng ký (Pool A) · FR-10 Máy trạng thái đơn hàng (Pool B) · FR-15 Quản lý sản phẩm (Pool C) · Mobile – Đăng nhập (Pool D, FR-20) |
| Công cụ AI | Claude Code (VS Code extension) · Google Antigravity (Gemini 4 Argon – rà soát chéo FR-01) |

## Bảng tự chấm

| STT | Tiêu chí | Điểm | Tự chấm |
| --- | --- | --- | --- |
| 1 | Feature A – FR-01 Đăng ký tài khoản (Domain + Boundary) | 25 | |
| 2 | Feature B – FR-10 Máy trạng thái đơn hàng (Domain + Boundary) | 25 | |
| 3 | Feature C – FR-15 Quản lý sản phẩm (Domain + Boundary) | 25 | |
| 4 | Feature D – Mobile: Đăng nhập (Domain + Boundary) | 15 | |
| 5 | Agent Skills | 10 | |
| | **Tổng** | **100** | |

## Test summary

Số feature: **4**. Số liệu lấy từ mục 5.4 của từng báo cáo (sinh tự động từ `evidence/<feature>/*_results.json`).

### Theo test case (gộp các kênh)

Một test case **Fail** nếu Fail ở bất kỳ kênh nào; **Blocked** nếu kết quả bị một bug khác che (không kết luận được).

| Feature | Báo cáo | TC đã thiết kế | Đã chạy | Pass | Fail | Blocked | Chưa chạy | Số bug |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR-01 Đăng ký | [FR-01_Dang_ky.md](report/FR-01_Dang_ky.md) | 53 | 53 | 0 | 48 | 5 | 0 | 9 |
| FR-10 Máy trạng thái đơn hàng | [FR-10_Trang_thai_don_hang.md](report/FR-10_Trang_thai_don_hang.md) | 47 | 47 | 43 | 4 | 0 | 0 | 2 |
| FR-15 Quản lý sản phẩm | [FR-15_Quan_ly_san_pham.md](report/FR-15_Quan_ly_san_pham.md) | 61 | 61 | 23 | 38 | 0 | 0 | 6 |
| Mobile – Đăng nhập | [Mobile_Dang_nhap.md](report/Mobile_Dang_nhap.md) | 24 | 24 | 10 | 13 | 1 | 0 | 5 |
| **Tổng** | | **185** | **185** | **76** | **103** | **6** | **0** | **22** |

### Theo lượt chạy (mỗi kênh một lượt)

| Feature | Kênh | Lượt chạy | Pass | Fail | Blocked | Không áp dụng |
| --- | --- | --- | --- | --- | --- | --- |
| FR-01 | Web, API | 101 | 36 | 50 | 15 | 5 |
| FR-10 | Web Admin / Web, API | 56 | 50 | 6 | 0 | 38 |
| FR-15 | Web Admin, API | 101 | 47 | 54 | 0 | 21 |
| Mobile – Đăng nhập | Mobile (Android Emulator), API | 48 | 20 | 26 | 2 | 0 |
| **Tổng** | | **306** | **153** | **136** | **17** | **64** |

"Không áp dụng": test case không có thao tác tương ứng trên kênh đó (vd giao diện không có nút chuyển trạng thái, API không có trường Xác nhận mật khẩu) – lý do ghi ở mục 5.3 từng báo cáo. FR-01 có thêm lượt **khảo sát** cho 15 test case Web bị Blocked (không tính verdict).

### Bug

| Feature | Critical | Major | Minor | Tổng | Chi tiết |
| --- | --- | --- | --- | --- | --- |
| FR-01 | 2 | 4 | 3 | 9 | FR01-B1…FR01-B9 |
| FR-10 | 1 | 1 | 0 | 2 | FR10-B1…FR10-B2 |
| FR-15 | 0 | 5 | 1 | 6 | FR15-B1…FR15-B6 |
| Mobile – Đăng nhập | 1 | 2 | 2 | 5 | MOB-B1…MOB-B5 |
| **Tổng** | **4** | **12** | **6** | **22** | [bugs/Bug_Report.md](bugs/Bug_Report.md) |

## Video demo

| Nội dung | Link |
| --- | --- |
| Agent Skill Domain Testing + BVA trên một feature hoàn chỉnh | |

## Cấu trúc bài nộp

| Thư mục / file | Nội dung |
| --- | --- |
| `report/` | Báo cáo chính (Domain Testing + BVA) cho từng feature, bản Markdown + PDF |
| `bugs/` | Báo cáo bug, ảnh bug và ảnh chụp trang GitHub Issues |
| `ai/` | AI Audit Report, AI Critique, Disclosure Form, Privacy Checklist, prompt log (Phụ lục A) |
| `evidence/` | Ảnh / log kết quả chạy test |
| `scripts/` | Script dựng dữ liệu, chạy test, trích prompt log |
| `skills/` | Agent Skills |
| `git_commit_log.txt` | Git commit log |
| `PLAN.md` | Kế hoạch, quy ước làm bài |
