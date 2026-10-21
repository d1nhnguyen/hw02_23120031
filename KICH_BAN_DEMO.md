# Kịch bản quay video demo Agent Skill

Tài liệu làm việc cho sinh viên (không cần đưa vào zip). Video phải có **giọng nói của chính sinh viên** (AI-01 §10): các ý dưới đây là gợi ý, hãy nói bằng lời của mình.

## 1. Chọn feature demo

| Phương án | Ưu | Nhược |
| --- | --- | --- |
| **FR-02 – Đăng nhập & Khóa tài khoản trên Web (khuyên dùng)** | Feature mới, chưa ai trong nhóm làm → cho thấy skill **dùng lại** được (đúng mục đích đề §7); đặc tả ngắn, đủ cả biến có thứ tự (số lần sai, thời gian khóa) | Không phải feature được chấm; các lỗi tìm ra trùng với MOB-B2, MOB-B3 (cùng backend) nên **không báo issue** |
| Chạy lại FR-10 trong nhánh riêng | Đúng feature đã nộp, so được với báo cáo đã có | Kết quả gần như lặp lại bài đã nộp |

Ước lượng thời gian chạy thật: 45–90 phút (B5 lâu nhất vì phải chờ khóa 30 giây); video sau khi cắt / tua nhanh: **12–18 phút**.

## 2. Chuẩn bị (trước khi bấm quay)

1. Tạo nhánh demo tách khỏi bài nộp (cùng cấp thư mục để `scripts/restart_backend.sh` tìm đúng SUT):
   ```bash
   cd ~/study/Homeworks/HW02/HW02_23120031
   git worktree add ../HW02_demo_FR02 -b demo/fr02
   ln -s ~/study/Homeworks/HW02/HW02_23120031/scripts/node_modules ../HW02_demo_FR02/scripts/node_modules
   ```
2. Kiểm tra `http://localhost:5173/login` và `http://localhost:3000/api/products` đã chạy (hiện đang chạy sẵn). Nếu chưa: mở terminal riêng, chạy `~/study/Homeworks/HW02/HW02_demo_FR02/scripts/start_env.sh web` và để nguyên terminal đó.
3. Mở VS Code ở thư mục `HW02_demo_FR02`, mở khung Claude Code, **phiên mới**. Gõ `/` → thấy `domain-testing-bva`.
4. Chọn chế độ quyền để agent không hỏi quá nhiều lần (vd tự chấp nhận sửa file); đóng các tab / thông báo có thông tin cá nhân.
5. Công cụ quay: OBS Studio hoặc Kooha (`sudo apt install obs-studio`), thu micro; độ phân giải 1080p, phóng chữ VS Code lên (Ctrl + =) để dễ đọc.

## 3. Các cảnh

| # | Cảnh (thời lượng sau khi cắt) | Thao tác trên màn hình | Ý cần nói |
| --- | --- | --- | --- |
| 0 | Mở đầu (0:30) | Màn hình README của bài | Họ tên, MSSV, HW02; skill `domain-testing-bva` được đúc kết sau khi làm 4 feature; video dùng lại skill cho FR-02 (Web) từ đầu đến cuối |
| 1 | Giới thiệu skill (1:30) | Mở `SKILL.md`, `reference/lessons.md`, `templates/`, `scripts/report_lib.py` | 7 bước, mỗi bước một commit; quy tắc lấy từ slide S04 / UC Analysis / S07; bài học khi tự động hoá (oracle phải kiểm tra lý do từ chối…); bảng báo cáo sinh từ `cases.py` |
| 2 | Gọi skill – B1 (2:00) | Gõ prompt B1 (mục 4); mở báo cáo mục 0–1 và ảnh `B1_*.png` | AI đọc đặc tả nguyên văn, quan sát hộp đen trang Đăng nhập; chỉ ra 1–2 điểm bạn tự kiểm tra (vd đặc tả bắt buộc ô email `type="email"`, nhãn "Username" trên form) |
| 3 | B2 (1:30) | Bảng 2.1, 2.2 | Guideline nào sinh lớp nào (count cho số lần sai, range cho thời gian khóa, must-be cho email…); có cả lớp đầu ra |
| 4 | B3 (2:00) | `cases.py`, bảng T32, T33 | Quy tắc Minimum Set: TC valid phủ nhiều lớp valid, mỗi TC invalid đúng 1 lớp invalid; bảng phủ 100% do script tính |
| 5 | B4 (1:30) | Bảng 4.1, T42 | Biên số lần sai (2 / 3 / 4), thời gian khóa (28 / 32 giây), độ dài email / mật khẩu ±1; điểm biên trùng Minimum Set chỉ dẫn chiếu |
| 6 | B5 (3:00, tua nhanh lúc chạy) | Terminal runner; `web_results.json`; vài ảnh test case; T53, T55 | Reset dữ liệu trước mỗi test case, oracle đọc bộ đếm qua API; kết quả bất ngờ (bộ đếm tăng 2, khóa 180 giây) được xác minh bằng một request API |
| 7 | **Rà soát của bạn** (1:30) | Bạn chỉ ra một chỗ cần sửa, gõ prompt sửa; xem `git diff` | Cho thấy người làm chủ: AI nháp, sinh viên duyệt; commit `[FR-02][Bn-review]` |
| 8 | B6 (1:30) | Mục 6 báo cáo | AI tự liệt kê chỗ mình sai / bỏ sót và nguyên nhân (prompt / công cụ / độ phức tạp) |
| 9 | B7 (1:30) | `bugs/Bug_Report.md` phần FR-02 | Mẫu Problem Report; skill không tự tạo issue; các lỗi này trùng MOB-B2 / MOB-B3 nên không báo lại |
| 10 | Kết (1:00) | `git log --oneline` (đủ `[FR-02][B1]`…`[B7]`) | Dùng lại cho feature khác chỉ cần đổi mã feature, đặc tả, kênh; kết quả và prompt được ghi lại đầy đủ |

## 4. Prompt gợi ý (tự viết lại theo cách của bạn)

- **B1:** `/domain-testing-bva Làm domain testing cho FR-02 Đăng nhập & Khóa tài khoản. Đặc tả: mục FR-02 trong ../../eshop-sut-main/README.md. Kênh: Web http://localhost:5173/login và API POST /api/login. Tiền tố FR02. Reset dữ liệu bằng scripts/restart_backend.sh. Báo cáo: report/FR-02_Dang_nhap.md. Làm B1 rồi dừng để tôi duyệt.`
- **B2:** `Duyệt B1: <nhận xét của bạn>. Làm B2 rồi dừng.`
- **B3 / B4:** `Làm B3 rồi dừng.` – `Làm B4 rồi dừng.`
- **B5:** `Chạy B5 trên Web và API, chạy nền và theo dõi đến khi xong.`
- **Rà soát:** `Sửa <test case / bảng> vì <lý do theo slide>, commit dạng review.`
- **B6 / B7:** `Làm B6.` – `Làm B7, không tạo GitHub issue.`

## 5. Sau khi quay

1. Đăng YouTube ở chế độ **Unlisted**, dán link vào bảng "Video demo" của README.
2. Báo Claude (phiên chính) để: trích prompt log của phiên demo (`scripts/export_prompt_log.py --project-dir ~/.claude/projects/<thư mục có chữ HW02-demo-FR02>`), ghi vào hồ sơ AI, đẩy nhánh `demo/fr02` lên repo riêng làm bằng chứng.
3. Dọn: `git worktree remove ../HW02_demo_FR02` (nhánh `demo/fr02` vẫn còn).
