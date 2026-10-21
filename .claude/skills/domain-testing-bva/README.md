# Hướng dẫn dùng skill `domain-testing-bva`

Skill dẫn Claude Code áp dụng **Domain Testing + Boundary Value Analysis** cho một feature, theo đúng các bước đã học (S04, UC Analysis, S07, Runnels): 7 bước, mỗi bước một commit. Skill được đúc kết sau khi làm 4 feature của HW02 (FR-01, FR-10, FR-15, Mobile – Đăng nhập).

## 1. Cài đặt

| Việc | Lệnh / ghi chú |
| --- | --- |
| Đặt skill vào dự án | Chép thư mục này vào `<dự án>/.claude/skills/domain-testing-bva/`. Claude Code tự nạp khi mở dự án (gõ `/` sẽ thấy `domain-testing-bva`). |
| Thư viện sinh bảng | Chép `scripts/report_lib.py` của skill vào `<dự án>/scripts/report_lib.py`. |
| Playwright cho runner Web | `cd scripts && npm install playwright-core` (dùng Chrome cài sẵn: `channel: 'chrome'`). |
| Python | 3.10+, chỉ dùng thư viện chuẩn (`urllib`, `json`). |
| Dữ liệu sạch | Một script khởi động lại SUT về dữ liệu seed, vd `scripts/restart_backend.sh`. |
| Mobile (nếu cần) | Android SDK + emulator, Expo Go; runner điều khiển bằng `adb` (`uiautomator dump`, `input tap/text`). |

## 2. Thông tin cần đưa cho skill

| Mục | Ví dụ |
| --- | --- |
| Mã feature + chỗ đọc đặc tả | `FR-02` trong `eshop-sut-main/README.md` |
| Kênh kiểm thử | Web `http://localhost:5173/login` + API `POST /api/login` |
| Tiền tố ID test case | `FR02` → `FR02-DT-01`, `FR02-BV-01` |
| Cách reset dữ liệu | `scripts/restart_backend.sh` |

Các mục này **không bắt buộc**: thiếu thì skill tự suy ra (tìm mục FR trong đặc tả, kênh theo đặc tả, tiền tố từ mã feature, script reset có sẵn) và ghi thành giả định A1, A2…; chỉ dừng khi bị chặn thật sự (không thấy đặc tả, SUT không chạy).

## 3. Cách gọi

**Một prompt (chế độ liền mạch, mặc định):**

```text
/domain-testing-bva FR-02
```

Agent tự tìm đặc tả, kênh, tiền tố, cách reset dữ liệu (ghi lại thành giả định), làm tuần tự B1 → B7, mỗi bước một commit, rồi in **Tóm tắt kết quả**: commit từng bước, số lớp / test case, bảng Pass / Fail / Blocked, bug nháp, gap analysis, các điểm cần người duyệt. Có thể nêu rõ thêm thông tin cho chắc, vd `/domain-testing-bva FR-02 – Web http://localhost:5173/login + API POST /api/login`.

**Nhanh** (mục tiêu ≤ 10 phút, vd để demo): thêm chữ `nhanh` – `/domain-testing-bva FR-02 nhanh`. Phương pháp giữ nguyên; API chạy toàn bộ test case, giao diện chỉ chạy các test case đại diện (≤ 5) và ghi rõ phần chưa chạy. Nên bật tự chấp nhận quyền, chạy SUT trước và dùng model nhanh.

**Từng bước** (khi muốn duyệt giữa các bước): thêm "làm B1 rồi dừng", sau đó "làm B2"… Sửa sau khi duyệt bằng prompt, commit `[<F>][B<n>-review]`.

| Bước | Sản phẩm chính |
| --- | --- |
| B1 | Mục 0–1 báo cáo: đặc tả nguyên văn, quan sát hộp đen, biến vào / ra, giả định; ảnh `evidence/<F>/B1_*.png` |
| B2 | Bảng 2.1 (guideline → lớp), 2.2 Complete Set of Partitions |
| B3 | `scripts/<f>/cases.py`, bảng T32 (Minimum Set), T33 (phủ phân vùng 100%) |
| B4 | Bảng 4.1 (LB / UB / bước nhảy), T42 Boundary Value Test Cases |
| B5 | Runner, `evidence/<F>/*_results.json`, ảnh từng test case, T53, T55 |
| B6 | AI gap analysis (nguyên nhân: prompt / công cụ / độ phức tạp), test case bổ sung T62 |
| B7 | Nháp bug theo mẫu Problem Report trong `bugs/Bug_Report.md`, ảnh bằng chứng |

Skill **không tự tạo GitHub issue**; chỉ tạo khi người dùng yêu cầu rõ.

## 4. Kiểm tra kết quả mỗi bước

- Bảng trong báo cáo được sinh từ `cases.py` (`python3 scripts/<f>/report_tables.py T32 T33 …`), không sửa tay.
- B3: bảng phủ phải đạt 100%; mỗi test case invalid phủ đúng 1 lớp invalid.
- B5: đọc lại oracle của runner (từ chối **đúng lý do**, dữ liệu trước / sau qua API); kết quả bất ngờ phải được xác minh bằng một request API.
- B7: danh sách test case của mỗi bug khớp cột Bug của T53.
- `git log --oneline` phải có đủ `[<F>][B1]` … `[<F>][B7]`.

## 5. Tài liệu trong skill

| File | Nội dung |
| --- | --- |
| `SKILL.md` | Quy trình 7 bước agent phải theo |
| `reference/method.md` | Quy tắc của môn học: guideline lớp tương đương, Minimum Set, BVA, định dạng test case |
| `reference/lessons.md` | Các lỗi đã gặp khi tự động hoá 4 feature (oracle, bộ chọn phần tử, thực thi) – bắt buộc tránh |
| `templates/` | Khung báo cáo, `cases.py`, `report_tables.py` |
| `scripts/report_lib.py` | Sinh bảng T32, T33, T42, T53, T55, T62 giữa các mốc `<!-- BEGIN:Txx -->` |
