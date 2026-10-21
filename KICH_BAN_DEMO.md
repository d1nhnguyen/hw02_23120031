# Kịch bản quay video demo Agent Skill

Tài liệu làm việc cho sinh viên (không cần đưa vào zip). Video phải có **giọng nói của chính sinh viên** (AI-01 §10): các ý dưới đây là gợi ý, hãy nói bằng lời của mình.

Cách demo: **một prompt gọi skill**, agent tự làm B1 → B7 (mỗi bước một commit), sau đó trình bày kết quả.

## 1. Feature demo

**FR-02 – Đăng nhập & Khóa tài khoản trên Web**: chưa ai trong nhóm làm → cho thấy skill dùng lại được cho feature mới (đề §7); đặc tả ngắn nhưng có đủ biến có thứ tự (số lần sai, thời gian khóa). Các lỗi tìm ra có thể trùng MOB-B2, MOB-B3 (cùng backend) nên **không báo issue**.

Thời gian agent chạy thật: khoảng 45–90 phút (B5 lâu nhất vì phải chờ khóa 30 giây). Video sau khi cắt / tua nhanh: **10–15 phút**.

## 2. Chuẩn bị (trước khi bấm quay)

1. Nhánh demo tách khỏi bài nộp (cùng cấp thư mục để `scripts/restart_backend.sh` tìm đúng SUT):
   ```bash
   cd ~/study/Homeworks/HW02/HW02_23120031
   git worktree add ../HW02_demo_FR02 -b demo/fr02
   ln -s ~/study/Homeworks/HW02/HW02_23120031/scripts/node_modules ../HW02_demo_FR02/scripts/node_modules
   ```
2. SUT đang chạy: `http://localhost:5173/login` và `http://localhost:3000/api/products` mở được. Nếu chưa: terminal riêng chạy `~/study/Homeworks/HW02/HW02_demo_FR02/scripts/start_env.sh web`.
3. Mở VS Code ở thư mục `HW02_demo_FR02`, khung Claude Code, **phiên mới**; gõ `/` → thấy `domain-testing-bva`.
4. **Quyền:** để agent chạy liền mạch không dừng chờ bấm "Allow", chọn chế độ tự chấp nhận (Auto / bỏ qua hỏi quyền) cho phiên demo này – an toàn vì chạy trong nhánh demo riêng. Nếu không muốn, thêm danh sách lệnh cho phép vào `HW02_demo_FR02/.claude/settings.local.json` (Claude có thể tạo sẵn).
5. Máy không ngủ / tắt màn hình trong lúc chạy; đóng các tab, thông báo có thông tin cá nhân.
6. Quay: OBS Studio hoặc Kooha, thu micro, 1080p; phóng chữ VS Code (Ctrl + =). Mở thêm một terminal `watch -n 20 git log --oneline -8` để thấy commit từng bước xuất hiện.

## 3. Prompt duy nhất

```text
/domain-testing-bva FR-02 – đặc tả trong ../../eshop-sut-main/README.md; Web http://localhost:5173/login + API POST /api/login
```

(Gõ `/domain-testing-bva FR-02` cũng được – agent tự tìm đặc tả và kênh; phần thêm chỉ để chắc chắn.)

## 4. Các cảnh

| # | Cảnh (thời lượng sau khi cắt) | Trên màn hình | Ý cần nói |
| --- | --- | --- | --- |
| 0 | Mở đầu (0:30) | README của bài | Họ tên, MSSV, HW02; skill được đúc kết sau khi làm 4 feature; video dùng lại skill cho FR-02 |
| 1 | Giới thiệu skill (1:30) | `SKILL.md` (hai chế độ, 7 bước, bảng tự kiểm tra), `reference/lessons.md`, `templates/` | Skill vẫn đi đúng từng bước của kỹ thuật (S04 / UC Analysis / S07), mỗi bước một commit, tự kiểm tra trước khi sang bước sau; bài học khi tự động hoá |
| 2 | Gọi skill (0:30) | Gõ prompt ở mục 3 | Chỉ đưa mã feature và chỗ đọc đặc tả, phần còn lại agent tự lo |
| 3 | Agent làm việc (2:30, tua nhanh) | Khung Claude Code + terminal `git log` thấy `[FR-02][B1]` … `[B7]` lần lượt xuất hiện; trình duyệt / ảnh B1 | Nói ngắn agent đang ở bước nào: đọc đặc tả → quan sát hộp đen → phân vùng → Minimum Set → BVA → chạy Web + API → gap analysis → bug |
| 4 | Tóm tắt của agent (1:00) | Phần "Tóm tắt kết quả" agent in ra cuối | Bảng commit, số lớp / test case, Pass / Fail / Blocked, bug nháp, điểm cần duyệt |
| 5 | Kết quả chi tiết (4:00) | `report/FR-02_*.md`: mục 1 (biến, giả định) → 2.2 (phân vùng) → T32 + T33 (phủ 100%) → T42 (BVA) → T53, T55 → mục 6 (gap analysis); vài ảnh trong `evidence/FR-02/`; `bugs/Bug_Report.md` phần FR-02 | Chỉ ra tính đúng kỹ thuật: mỗi TC invalid một lớp; biên số lần sai 2 / 3 / 4 và thời gian 28 / 32 giây; kết quả bất ngờ được xác minh bằng API; bug theo mẫu Problem Report, không tự tạo issue |
| 6 | Bạn duyệt (1:00) | Mục "Điểm cần người duyệt" của tóm tắt; một chỗ bạn đồng ý / không đồng ý | AI làm nháp, người quyết định giả định, mức độ bug; nếu cần sửa thì prompt sửa → commit `[FR-02][Bn-review]` |
| 7 | Kết (0:30) | `git log --oneline` | Dùng lại cho feature khác chỉ cần đổi mã feature; mọi prompt / output được ghi log |

Cảnh 6 nên giữ (dù ngắn): đề §2 yêu cầu sinh viên rà soát mọi kết quả AI, không nộp output thô.

## 5. Sau khi quay

1. Đăng YouTube ở chế độ **Unlisted**, dán link vào bảng "Video demo" của README.
2. Báo Claude (phiên chính) để: trích prompt log phiên demo vào hồ sơ AI, đẩy nhánh `demo/fr02` lên repo riêng làm bằng chứng.
3. Dọn: `git worktree remove ../HW02_demo_FR02` (nhánh `demo/fr02` vẫn còn).
