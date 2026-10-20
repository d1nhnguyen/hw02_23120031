# Phụ lục A — Prompt log (trích tự động từ transcript Claude Code & Google Antigravity)

> Sinh bởi `scripts/export_prompt_log.py` lúc 2026-10-21 06:35 (GMT+7). Prompt và output của AI được giữ **nguyên văn**. Không đưa vào: phần suy luận ẩn của model, nội dung file / kết quả lệnh mà AI đọc được (chỉ liệt kê tên hành động).

| # | Thời gian (GMT+7) | Phiên | Prompt (rút gọn) |
|---|---|---|---|
| 1 | 2026-10-20 20:46 | `1946c20d` | đọc đề bài @HW02/ và @___2026.Homework.Policies.md, nội dung về domain testing, cách viết  |
| 2 | 2026-10-20 21:06 | `1946c20d` | 1. Đây là URL repo chung: https://github.com/d1nhnguyen/eshop-sut, một issues có thể được  |
| 3 | 2026-10-20 21:10 | `1946c20d` | [Request interrupted by user] |
| 4 | 2026-10-20 21:11 | `1946c20d` | ko xem các dữ liệu đã cũ, tôi chỉ test trước để hiểu đề bài |
| 5 | 2026-10-20 21:18 | `4aefb10a` | tao mot private repo trong hw02_23120031, voi github account d1nhnguyen |
| 6 | 2026-10-20 21:19 | `4aefb10a` | [Request interrupted by user for tool use] |
| 7 | 2026-10-20 21:19 | `4aefb10a` | co the dua lenh toi tu chay cung duoc |
| 8 | 2026-10-20 21:21 | `4aefb10a` | git remote add origin git@github-d1nh:d1nhnguyen/hw02_23120031.git error: remote origin al |
| 9 | 2026-10-20 21:23 | `1946c20d` | tôi đã tạo repo rồi, các commit có thể ko cần thêm co-authored claude. Thực hiện tiếp |
| 10 | 2026-10-20 21:25 | `1946c20d` | [Request interrupted by user] |
| 11 | 2026-10-20 21:26 | `1946c20d` | về phần tên file ở pool mobile, m-02 ko phải là tên chính thức đó chỉ là quy định trong nh |
| 12 | 2026-10-20 21:31 | `1946c20d` | Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi tôi, đọc kỹ các bài |
| 13 | 2026-10-20 22:30 | `421e648d` | kiểm tra fr-01 đã ổn chưa (bảng, cách đặt tên TC, mức độ chi tiết), ko cần ghi log phần nà |
| 14 | 2026-10-20 22:37 | `1946c20d` | <pasted_content id="5e2c"> ### 1. Về Bảng (Cấu trúc & tính nhất quán) • Đạt chuẩn: • Đủ ch |
| 15 | 2026-10-20 22:52 | `1946c20d` | tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả các điểm cần tôi đố |
| 16 | 2026-10-21 00:06 | `1946c20d` | tiếp tục |
| 17 | 2026-10-21 00:13 | `1946c20d` | kiểm tra đã xong chưa |
| 18 | 2026-10-21 00:15 | `1946c20d` | theo dõi hoặc nhờ agent khác, ko tự dừng vì sau khi dừng không tự chạy lại được? |
| 19 | 2026-10-21 00:26 | `1946c20d` | kiếm tra lại, vscode vừa bị dừng |
| 20 | 2026-10-21 01:16 | `421e648d` | thêm log phần này vào AI-log và các tài liệu cần thiết khác |
| 21 | 2026-10-21 06:14 | `421e648d` | kiểm tra các bug trong report có đúng chưa? |
| 22 | 2026-10-21 06:22 | `421e648d` | các bug đó thật sự có trong code? |
| 23 | 2026-10-21 06:29 | `1946c20d` | 1. đó là Antigravity, tôi dùng để kiểm tra chéo và đã thêm vào báo cáo. 2. bạn hãy tạo 22  |

## #1 · 2026-10-20 20:46:19 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
đọc đề bài @HW02/ và @___2026.Homework.Policies.md, nội dung về domain testing, cách viết test case có trong @Slides tôi đảm nhận các chức năng  FR-01, FR-10, FR-15 và đăng nhập ở mobile, Repo sut chung đã có và tôi có thể tạo các issues. Ghi log lại mọi thứ như trong yêu cầu của @"AI Templates/". hãy lên một plan cụ thể để hoàn thành bài này, kiểm tra còn điểm nào chưa rõ ko và thảo luận với tôi.
````

**Output AI (nguyên văn):**

````markdown
I'll start by reading the assignment brief and checking what's in the HW02 folder.

The HW02_23120031 folder is still empty. Next I'll pull the text out of the relevant slides and the AI Templates, and look for a local copy of the SUT.

There's a local copy of the SUT (eshop-sut-main), a team assignment sheet (HW02_Phan_cong_nhom.xlsx), and a Templates folder. I'll read the domain testing and test case slides first.

Now the AI Templates (Vietnamese versions), the Templates folder, HW01, and the team assignment sheet.

The team sheet is still blank (no names entered). FR-01, FR-10, FR-15 and M-02 cover one feature per pool, which is valid. Now the SUT spec: README, PROJECT_GUIDE and the API spec.

Tôi đã đọc xong đề HW02, Policies, slide S04 (Domain Testing), S07 và Test_Cases_AI_First (cách viết test case), 6 AI Templates, đặc tả SUT ([README.md](eshop-sut-main/README.md), api_specification, PROJECT_GUIDE) và file phân công nhóm (hiện chưa ai điền tên). Bốn feature bạn chọn mỗi cái thuộc một pool khác nhau, hợp lệ.

## 1. Những điểm cần nắm

- **Mỗi feature cần đủ 4 phần:** Domain Testing theo 4 bước của S04, BVA (LB-1, LB, LB+1, UB-1, UB, UB+1, cộng min/max có thể nhập từ UI), AI gap analysis, và bug report (cả Markdown lẫn GitHub Issue có ảnh).
- **"AI-First" nghĩa là dẫn AI đi từng bước của kỹ thuật**, không phải một prompt kiểu "sinh test case cho tôi". Mỗi bước là 1 prompt, 1 dòng trong audit report và 1 commit.
- **Các file log AI bắt buộc:**
  - `prompt_log.md`: prompt và output nguyên văn, có thời gian.
  - AI-02 Audit Report: 5 cột; verdict VALID/INVALID/INCOMPLETE; lý do phải dẫn slide hoặc ISTQB; bản bạn sửa.
  - AI-03 Disclosure Form và AI-05 Privacy Checklist.
  - AI Critique 200–300 từ, và đoạn Mandatory Disclosure ở cuối báo cáo.
  - AI-01 và AI-06 là giấy tờ đầu kỳ; AI-04 chỉ bắt buộc cho project/seminar.
- **Hai lỗi bị 0 điểm:** thiếu bất kỳ tài liệu bắt buộc nào, hoặc trùng prompt với bạn khác (cả hai cùng 0).

## 2. Plan

**Giai đoạn 0 – Chuẩn bị (~1h)**
1. Chạy `git init` trong `HW02_23120031`, tạo cấu trúc thư mục, push lên repo cá nhân để private.
2. Chạy SUT. Admin và mobile chưa có `node_modules` nên cần `npm install`. Sửa `API_URL` ở [App.js:16](eshop-sut-main/frontend-mobile/App.js#L16).
3. Viết script trích log từ transcript Claude Code ra `ai/prompt_log.md` (đề khuyến khích việc này). Máy đã có sẵn 4 file transcript, và phiên này chính là log #1.
4. Viết script tạo dữ liệu (curl): user, và đơn hàng ở từng trạng thái. Lý do: mỗi lần restart backend là DB bị xoá sạch.

**Giai đoạn 1–4 – Mỗi feature đi 7 bước, mỗi bước 1 commit**

| # | Bước | AI | Bạn |
|---|---|---|---|
| 1 | Xác định biến Input/Output, ghi giả định | Viết nháp từ đoạn FR dán vào | Duyệt |
| 2 | Lớp tương đương valid/invalid, theo 4 quy tắc ở S04 | Viết nháp | Thêm hoặc tách lớp, gắn verdict |
| 3 | Chọn TC: TC valid phủ nhiều lớp, TC invalid mỗi cái đúng 1 lớp | Viết nháp | Đối chiếu expected result với spec |
| 4 | BVA cho mọi biến có thứ tự | Viết nháp | Kiểm tra biên |
| 5 | Chạy test trên UI và API, ghi Actual/Status, chụp ảnh | Hỗ trợ chạy curl/Playwright | Xác nhận kết quả |
| 6 | Gap analysis: so bản AI gốc với bản cuối | — | Phân tích |
| 7 | Bug report và GitHub Issue | (xem câu hỏi 2) | Viết |

- **Lưu bản AI gốc trước khi sửa** vào `ai/raw/`. Đây là bằng chứng cho gap analysis và cho cột "Bản SV sửa" của AI-02.
- **Mỗi TC có cột Origin:** AI / AI-sửa / Human.
- **Template TC (theo S07):** ID | Title (Action + Function + Condition) | Covers (EC/BV) | Precondition | Steps | Data | Expected | Actual | Status | Bug ID.
- **Thứ tự làm:** FR-01 (1.5h), FR-15 (1.5h), FR-10 (2h), M-02 (1.5h).

**Giai đoạn 5 – Agent Skill (~1.5h)**
- Skill `domain-testing-bva` dựng từ kinh nghiệm của FR-01 và FR-15. Skill dừng ở mỗi bước chờ bạn duyệt, xuất đúng template TC, và tự ghi dòng audit.
- Skill `ai-audit-log` để trích log.
- Dùng skill cho FR-10 hoặc M-02 và quay video lúc làm. Video cần giọng nói của bạn (AI-01 §10).

**Giai đoạn 6 – Tổng hợp (~1h)**
- README (bảng tự chấm và test summary).
- Xuất PDF: pandoc ra HTML, rồi in bằng Chrome headless (máy đã có Chrome).
- `git log --stat > git_commit_log.txt`.
- Đặt tên zip `23120031_HW02_AI_DomainTesting_XXX.zip`, rồi đi hết checklist AI-05.

## 3. Ghi chú kỹ thuật theo feature

- **FR-01:** Trang [Register.jsx](eshop-sut-main/frontend-web/src/pages/Register.jsx) chỉ có 3 ô, không có "Xác nhận mật khẩu", và ô email dùng `type="text"`.
  - Các lớp về xác nhận mật khẩu không test được qua UI, sẽ test qua API và ghi nhận thiếu tính năng.
  - Biến: độ dài mật khẩu (7/8/9), mỗi loại ký tự có 0 hay 1, ký tự đặc biệt trong hay ngoài tập `@$!%*?&`, định dạng email, email trùng.
- **FR-10:** UI admin chỉ hiện nút cho các chuyển trạng thái hợp lệ, nên chuyển không hợp lệ phải test qua `PUT /api/admin/orders/:id/status`.
  - Biến: trạng thái hiện tại × trạng thái đích × người thực hiện (user/admin).
  - BVA cho máy trạng thái không tự nhiên. Tôi đề xuất coi pending < confirmed < shipping < delivered là thứ tự; khi đó biên của vùng "được hủy" là confirmed/shipping. Thêm biên của order id và của chuỗi status.
- **FR-15:** Ô danh mục mặc định chọn sẵn id=1, nên lớp "thiếu danh mục" hoặc "danh mục không tồn tại" phải test qua API.
  - Biến: tên (0/1/254/255/256 ký tự), giá (âm/0/0.01/rất lớn/chữ), category_id (0/1/3/4).
  - Test qua API sẽ chạm vào phân quyền, vốn là phạm vi FR-12. Cần thống nhất với người giữ FR-12 để không làm trùng.
- **M-02:** Không có FR riêng, nên lấy quy tắc từ FR-02 và FR-22.
  - Biến: số lần sai liên tiếp (2/3/4), thời gian khoá (29/30/31 giây), bộ đếm có reset khi đăng nhập đúng không, thông báo có để lộ nguyên nhân không.
  - Phần backend dùng chung với FR-02 của bạn cùng nhóm. Máy này không có emulator hay adb.

## 4. Điểm chưa rõ cần bạn quyết định

1. **Repo issues:** URL repo chung là gì? Có quy ước label hoặc tiền tố tiêu đề (vd `[FR-15][23120031]`) không? Bug backend dùng chung với FR-02 thì ai report?
2. **Mâu thuẫn quy định về bug report:** [AI-01 §11](AI%20Templates/) ghi "Bug report: 100% sinh viên viết; AI không được nháp mô tả", trong khi đề HW02 §11 ghi Anti-AI-Cheat là "None". Tôi đề xuất cách an toàn: bạn tự viết nội dung bug, tôi chỉ giúp tái hiện, thu bằng chứng và đối chiếu spec. Tôi cũng sẽ không tạo issue khi bạn chưa duyệt.
3. **Môi trường mobile:** Bạn có điện thoại cài Expo Go (SDK 54) và dùng chung Wi-Fi với máy không? Nếu không có thì cài Android emulator (nặng khoảng 10GB). Tôi không khuyến nghị chạy `expo --web`, vì chạy trên web không tính là test mobile thật.
4. **Ai viết prompt:** Để log trung thực và tránh trùng prompt với bạn khác, tôi đề xuất bạn tự gõ prompt cho từng bước bằng lời của mình; tôi chỉ gợi ý khung ROLE/CONTEXT/TASK/FORMAT/CONSTRAINTS (slide 21). Bạn có dùng thêm ChatGPT hay Gemini để cross-check không? Nếu có thì log của chúng phải export tay.
5. **Black-box:** Tôi đề xuất chỉ thiết kế TC từ SRS và không đọc code. Như vậy đúng tinh thần domain testing, và gap analysis mới trung thực. Để lập plan tôi đã lướt qua các trường của form, tức là những gì nhìn thấy được trên UI.
6. **Đặc tả mơ hồ** (sẽ ghi thành "Giả định" trong báo cáo, nên hỏi TA trên forum):
   - **FR-10:** Câu "đơn shipping thì chỉ Admin mới có thể thao tác" có nghĩa Admin được hủy đơn shipping không? Sơ đồ không có cạnh shipping→canceled.
   - **FR-01:** Tên, email, mật khẩu có độ dài tối đa không? Ký tự `#` bị cấm hay chỉ là không được tính? Email chỉ khác hoa/thường có bị coi là trùng không?
   - **FR-15:** 255 là ký tự hay byte (tiếng Việt)? Giá có được là số thập phân không, tức biên dưới là 0.01 hay 1?
   - **M-02:** Khoá ngay ở lần sai thứ 3 hay từ lần thứ 4? Nhập email không tồn tại có làm tăng bộ đếm không?
7. **Ngôn ngữ báo cáo** là tiếng Việt hay tiếng Anh? **Deadline** trên Moodle là ngày nào?
8. **Repo git nộp bài:** Tôi tạo repo private dưới tài khoản `npdinhx` cho riêng thư mục `HW02_23120031` được không?

Bạn trả lời các câu này (đặc biệt câu 1–4) xong là mình bắt đầu Giai đoạn 0.
````

<details><summary>Hành động AI đã thực hiện (25)</summary>

1. `Bash` — Read HW02 brief and list student folder
2. `Bash` — Check tools, refs, and local SUT clone
3. `Bash` — Extract text from key lecture slides
4. `Bash` — Read domain testing slides text
5. `Bash` — Read test case slides text
6. `Bash` — Read AI-first test case slides text
7. `Bash` — Read AI-first slides part 1 (compacted)
8. `Bash` — Read AI-first slides part 2 (compacted)
9. `Bash` — Convert Vietnamese AI templates to text
10. `Bash` — List Templates/HW01 and dump team sheet
11. `Bash` — Read AI Audit Report and Disclosure Form templates
12. `Bash` — Read Reflective Statement, Privacy Checklist, Agreement
13. `Bash` — Parse team assignment spreadsheet
14. `Bash` — Explore SUT repo structure
15. `Bash` — Read SUT README specification
16. `Bash` — Read API spec, setup guide, run script
17. `Bash` — Read SUT project guide
18. `Bash` — Check gh auth, node, Android tools, deps
19. `Bash` — Skim T03 mobile automation doc
20. `Bash` — Inspect register page fields and API routes
21. `Bash` — Inspect mobile app screens and login flow
22. `Bash` — Inspect admin order status and product form
23. `Bash` — Check PDF engines and session transcripts
24. `Write` — /home/npdinh/.claude/projects/-home-npdinh-study-Homeworks/memory/hw02-domain-testing-scope.md
25. `Write` — /home/npdinh/.claude/projects/-home-npdinh-study-Homeworks/memory/MEMORY.md

</details>

## #2 · 2026-10-20 21:06:31 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
1. Đây là URL repo chung: https://github.com/d1nhnguyen/eshop-sut, một issues có thể được đặt tên như: "[BUG-04] [FR-08] Thanh toán xong không xóa sản phẩm trong giỏ hàng", FR-02 không có ai làm.
2. bạn có thể draft nội dung bug, tôi sẽ là người duyệt và trực tiếp viết.
3. có thể cài android emulator.
4. tôi viết prompt.
5. giữ tinh thần domain testing.
6. ok
7. tiếng việt. không cần quan tâm DL.
8. tạo dưới tài khoản d1nhnguyen (có ssh) cho thư mục đã nêu.
````

**Output AI (nguyên văn):**

````markdown
Đã rõ. Tôi kiểm tra trước: repo issues hiện có (để nối tiếp số BUG), tài khoản gh/SSH nào dùng được cho `d1nhnguyen`, và điều kiện cài emulator (Java, KVM).

Cả hai việc chạy nền đã xong. Tôi xem kết quả.

npm đã cài xong. Script Android thì không in dòng `DONE`; exit 0 chỉ là của lệnh `tail` cuối pipe nên không chứng minh gì. Tôi kiểm tra trực tiếp.

Trong lúc SDK tải nền, tôi dựng repo bài nộp và viết script trích log. Bắt đầu với script `export_prompt_log.py`:

Thư mục thử nghiệm FR-01 đang nằm trong Thùng rác, tức bạn đã xoá; tôi không đụng vào. Tôi xem kết quả lần cài SDK thứ hai.
````

<details><summary>Hành động AI đã thực hiện (17)</summary>

1. `Bash` — Check GitHub accounts, SSH identity, git config
2. `Bash` — Inspect shared repo, issues and labels
3. `Bash` — Check Java, KVM, RAM and disk for emulator
4. `Bash` — Compare local SUT files with shared repo
5. `Bash` — Check KVM ACL and transcript JSONL structure
6. `Bash` — Install Android SDK, emulator and create AVD
7. `Bash` — Install admin and mobile npm dependencies
8. `Bash` — Test d1nhnguyen SSH key; list session first prompts
9. `Bash` — Inspect transcript block shapes and flags
10. `Bash` — Read background install outputs
11. `Bash` — Inspect Android SDK install state
12. `Bash` — Fix install script and rerun SDK setup
13. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/export_prompt_log.py
14. `Bash` — Run log exporter and check output
15. `Bash` — Read log entry #9 (FR-01 trial)
16. `Bash` — Search for leftover FR-01 trial folder
17. `Bash` — Check SDK install result and AVD config

</details>

## #3 · 2026-10-20 21:10:40 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `n/a`

**Prompt (nguyên văn):**

````text
[Request interrupted by user]
````

**Output AI (nguyên văn):**

````markdown
(không có văn bản trả lời)
````

## #4 · 2026-10-20 21:11:02 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
ko xem các dữ liệu đã cũ, tôi chỉ test trước để hiểu đề bài
````

**Output AI (nguyên văn):**

````markdown
Script đã có tuỳ chọn `--since`. Tôi xuất lại log chỉ từ phiên này, rồi dựng khung repo: README có bảng tự chấm, PLAN ghi quy ước và .gitignore.

Khung đã xong. Tôi khởi tạo git, gắn remote qua SSH alias của `d1nhnguyen` rồi tạo commit đầu tiên.

Emulator đang khởi động. Tôi chờ thông báo boot xong.

Tôi đang chờ emulator boot xong; khi xong tôi sẽ cài Expo Go và mở app EShop để kiểm tra kết nối tới backend. Trong lúc chờ, đây là phần Giai đoạn 0 đã xong:

- **Repo bài nộp `HW02_23120031`:** đã `git init` và có commit đầu tiên `[setup] ...`. Trong đó có:
  - [README.md](HW02/HW02_23120031/README.md): khung bảng tự chấm và test summary.
  - [PLAN.md](HW02/HW02_23120031/PLAN.md): quy trình 7 bước cho mỗi feature, quy ước commit `[FR-xx][Bn]` và tên issue `[BUG-NN] [FR-xx]`. Bug mobile dùng `[FR-20]` giống nhóm, phần thân dẫn chiếu FR-02.
  - [scripts/export_prompt_log.py](HW02/HW02_23120031/scripts/export_prompt_log.py): trích nguyên văn prompt và output kèm giờ GMT+7. Log chỉ tính từ phiên này (tuỳ chọn `--since 2026-10-20T20:40`), nên dữ liệu cũ không lọt vào.
- **Android:** đã cài SDK, emulator và AVD `eshop_api34` (Android 14), tổng 2.7GB. Ổ đĩa còn trống 12GB.
- **SUT:** đã `npm install` cho admin và mobile. Tôi đổi `API_URL` ở [App.js:16](eshop-sut-main/frontend-mobile/App.js#L16) thành `http://10.0.2.2:3000/api` để emulator gọi được backend trên máy. Bản SUT local giống hệt repo nhóm. Backend đang chạy.

**Bạn cần làm 1 việc:** gh CLI trên máy đang đăng nhập bằng `npdinhx`, còn SSH thì không tạo được repo trên GitHub. Bạn chọn một trong hai cách:
1. Tạo trên web: đăng nhập `d1nhnguyen`, vào New repository, đặt tên `HW02_23120031`, chọn **Private**, không tick README.
2. Hoặc chạy `gh auth login` trong terminal và đăng nhập thêm tài khoản `d1nhnguyen`; sau đó tôi tự tạo repo.

Xong thì báo tôi để push. Remote đã gắn sẵn là `git@github-d1nh:d1nhnguyen/HW02_23120031.git`.

Emulator đã boot (`emulator-5554`), backend trả về dữ liệu sản phẩm. Tôi khởi động Expo cho Android; Expo sẽ tự cài Expo Go lên emulator rồi mở app.

Expo đang build bundle và cài Expo Go, tôi chờ log báo kết quả.

Mới có cảnh báo lệch phiên bản package, chưa phải lỗi. Tôi tiếp tục chờ bundle.

Expo đã mở `exp://192.168.2.238:8081` trên emulator. Tôi chờ bundle xong.

Expo đang tải Expo Go về emulator.

Đang cài Expo Go lên emulator.

Expo Go đã cài xong và đang tải bundle của app.

Bundle đã build xong. Tôi chụp màn hình emulator để xem app có tải được danh sách sản phẩm từ backend không.

Log báo 11 lượt, nhiều hơn số prompt bạn thực sự gõ (4). Có thể các thông báo hệ thống từ tác vụ nền đã bị tính nhầm là prompt. Tôi kiểm tra.

Giai đoạn 0 xong, chỉ còn bước push lên GitHub.

- **Mobile chạy được trên emulator.** App EShop mở trong Expo Go và tải đúng danh sách sản phẩm từ backend (ví dụ iPhone 15 Pro Max, 30,000,000 ₫). Emulator, backend và Expo vẫn đang chạy nền.
- **Đã sửa lỗi script log.** Các thông báo hệ thống từ tác vụ nền bị tính nhầm là prompt, khiến log đếm thành 11 lượt. Giờ log chỉ còn 4 prompt bạn thực sự gõ trong phiên này, dữ liệu cũ không lọt vào.
- **Repo local có 3 commit:** `[setup]` cấu trúc và kế hoạch, `[setup]` script khởi động môi trường, `[ai-log]` sửa script log. Lần sau bạn chỉ cần chạy `scripts/start_env.sh mobile` (hoặc `web`, hoặc `all`) để bật lại môi trường.

**Việc bạn cần làm để push:** tạo repo private `HW02_23120031` dưới tài khoản `d1nhnguyen`, qua web hoặc qua `gh auth login`. Xong báo tôi một câu là tôi push ngay.

**Bước tiếp theo là FR-01 B1** (xác định biến Input/Output), với prompt do bạn tự viết. Tôi đề xuất mỗi feature làm trong một phiên Claude Code mới, vì hai lý do: log mỗi feature sẽ gọn và tách bạch, và AI không mang theo ngữ cảnh của feature khác nên phần gap analysis trung thực hơn. Các quyết định đã chốt (định dạng issue, bạn tự viết prompt, chỉ test hộp đen, bỏ dữ liệu cũ) tôi đã ghi vào bộ nhớ, nên phiên mới vẫn nắm được.

Monitor theo dõi log Expo đã hết hạn sau 5 phút, đúng như dự kiến. Tôi không bật lại vì app đã chạy và đã kiểm tra xong. Expo, emulator và backend vẫn chạy nền. Tôi đang chờ bạn tạo repo `HW02_23120031` để push.
````

<details><summary>Hành động AI đã thực hiện (26)</summary>

1. `Write` — /home/npdinh/.claude/projects/-home-npdinh-study-Homeworks/memory/hw02-plan-decisions.md
2. `Edit` — /home/npdinh/.claude/projects/-home-npdinh-study-Homeworks/memory/MEMORY.md
3. `Edit` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/export_prompt_log.py
4. `Edit` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/export_prompt_log.py
5. `Bash` — Regenerate log from this session; create folders
6. `Edit` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/export_prompt_log.py
7. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/README.md
8. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/PLAN.md
9. `Bash` — Init git repo, add remote, first commit
10. `Bash` — Check display; point mobile API_URL to host
11. `Bash` — Tidy the API_URL line comment
12. `Bash` — Boot the Android emulator
13. `Bash` — Start the EShop backend server
14. `Bash` — Wait for emulator boot and check backend
15. `ToolSearch` — query=select:Monitor, max_results=1
16. `Bash` — Read boot wait and backend output
17. `Bash` — Start Expo and open app on emulator
18. `Monitor` — command=L=/tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f, description=Expo start progress and errors
19. `Bash` — Screenshot emulator and check Expo errors
20. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/android/home.png
21. `Bash` — Dismiss Expo developer menu on emulator
22. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/start_env.sh
23. `Bash` — Commit env script and refreshed prompt log
24. `Bash` — Inspect which entries were counted as prompts
25. `Edit` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/export_prompt_log.py
26. `Bash` — Regenerate log without notifications and commit

</details>

## #5 · 2026-10-20 21:18:43 · phiên `4aefb10a`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
tao mot private repo trong hw02_23120031, voi github account d1nhnguyen
````

**Output AI (nguyên văn):**

````markdown
(không có văn bản trả lời)
````

<details><summary>Hành động AI đã thực hiện (3)</summary>

1. `Bash` — Read memory, list folder, check gh auth
2. `Bash` — Locate the hw02 folder and SSH alias config
3. `Bash` — Check folder contents, git state, SSH identity

</details>

## #6 · 2026-10-20 21:19:01 · phiên `4aefb10a`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `n/a`

**Prompt (nguyên văn):**

````text
[Request interrupted by user for tool use]
````

**Output AI (nguyên văn):**

````markdown
(không có văn bản trả lời)
````

## #7 · 2026-10-20 21:19:07 · phiên `4aefb10a`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
co the dua lenh toi tu chay cung duoc
````

**Output AI (nguyên văn):**

````markdown
Thư mục nằm ở `HW02/HW02_23120031`. gh CLI trên máy đang đăng nhập bằng `npdinhx`, nên không tạo repo cho `d1nhnguyen` bằng nó được. Có hai cách:

**Cách 1 — qua web (khuyên dùng, không đụng tới gh):**

1. Đăng nhập GitHub bằng `d1nhnguyen` và vào https://github.com/new
   - Repository name: `HW02_23120031`
   - Chọn **Private**
   - Không tick README, .gitignore hay license, để repo rỗng
2. Chạy các lệnh sau trong terminal:

```bash
cd /home/npdinh/study/Homeworks/HW02/HW02_23120031
git init -b main
git remote add origin git@github-d1nh:d1nhnguyen/HW02_23120031.git
ssh -T git@github-d1nh   # phải in ra "Hi d1nhnguyen!"
```

**Cách 2 — qua gh CLI (phải thêm tài khoản d1nhnguyen vào gh):**

```bash
gh auth login --hostname github.com --git-protocol ssh --web --skip-ssh-key   # đăng nhập bằng d1nhnguyen
cd /home/npdinh/study/Homeworks/HW02/HW02_23120031
git init -b main
gh repo create d1nhnguyen/HW02_23120031 --private --source=. --remote=origin
git remote set-url origin git@github-d1nh:d1nhnguyen/HW02_23120031.git
gh auth switch --user npdinhx   # chuyển gh về lại tài khoản cũ
```

Lưu ý:
- Nếu gõ lệnh ngay trong khung chat này thì thêm `!` ở đầu mỗi dòng (ví dụ `! git init -b main`) để mình xem được kết quả.
- Remote dùng alias SSH `github-d1nh` để push bằng key của `d1nhnguyen`, không phải key của `npdinhx`.
- Repo rỗng thì chưa push được. Lần push đầu tiên sẽ đi cùng commit đầu tiên của bạn: `git push -u origin main`.
- Nếu muốn commit đứng tên `d1nhnguyen`, đặt `git config user.name` / `user.email` riêng cho repo này. Mặc định nó dùng cấu hình global trên máy.

Nếu bạn tạo repo theo cách 1, bước 1 xong thì báo mình, mình chạy các lệnh git ở bước 2 cho.
````

## #8 · 2026-10-20 21:21:11 · phiên `4aefb10a`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
git remote add origin git@github-d1nh:d1nhnguyen/hw02_23120031.git
error: remote origin already exists.
````

**Output AI (nguyên văn):**

````markdown
Lỗi đó không sao: remote `origin` đã có sẵn và trỏ đúng chỗ.

```
origin  git@github-d1nh:d1nhnguyen/HW02_23120031.git
```

Thư mục này đã là git repo với 3 commit `[setup]` / `[ai-log]` từ trước. GitHub không phân biệt hoa thường ở tên repo, nên `hw02_23120031` và `HW02_23120031` là cùng một repo. Không cần thêm remote nữa.

Giờ chỉ cần kiểm tra xem repo trên GitHub đã có chưa, rồi push lên:

```bash
git ls-remote origin
```

- **Không lỗi** (in ra trống hoặc in ra danh sách ref): repo đã có trên GitHub. Chạy `git push -u origin main` là xong.
- **Lỗi `Repository not found`**: repo chưa có. Đăng nhập `d1nhnguyen`, vào https://github.com/new, tạo repo `HW02_23120031` ở chế độ **Private** và không tick README. Sau đó chạy `git push -u origin main`.

Nếu nhánh hiện tại không tên `main` thì kiểm tra bằng `git branch --show-current` và push đúng tên nhánh đó.
````

<details><summary>Hành động AI đã thực hiện (2)</summary>

1. `Bash` — Show which repo and remote the folder uses
2. `Bash` — Update outdated note about submission folder in memory

</details>

## #9 · 2026-10-20 21:23:02 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
tôi đã tạo repo rồi, các commit có thể ko cần thêm co-authored claude. Thực hiện tiếp
````

**Output AI (nguyên văn):**

````markdown
Đã rõ: từ giờ không thêm dòng `Co-Authored-By` nữa. Ba commit hiện tại mới nằm ở local, chưa push lần nào, nên tôi xoá dòng đó khỏi chúng luôn rồi mới push. Trước hết tôi ghi nhớ quyết định này và kiểm tra repo trên GitHub.

Đã gắn `origin/main`. Tôi kiểm tra phiên bản pandoc để chọn tuỳ chọn nhúng ảnh khi xuất PDF.

pandoc 3.1.3 hỗ trợ `--embed-resources`. Tôi viết script xuất PDF và file CSS đi kèm.
````

<details><summary>Hành động AI đã thực hiện (9)</summary>

1. `Edit` — /home/npdinh/.claude/projects/-home-npdinh-study-Homeworks/memory/hw02-plan-decisions.md
2. `Bash` — Check the new remote repo is reachable and empty
3. `Bash` — Fetch remote and set upstream tracking
4. `Bash` — Check pandoc and Chrome versions
5. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/pdf.css
6. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/build_pdf.sh
7. `Bash` — Test PDF export on README
8. `Bash` — Generate four feature report skeletons
9. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md

</details>

## #10 · 2026-10-20 21:25:03 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `n/a`

**Prompt (nguyên văn):**

````text
[Request interrupted by user]
````

**Output AI (nguyên văn):**

````markdown
(không có văn bản trả lời)
````

## #11 · 2026-10-20 21:26:06 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
về phần tên file ở pool mobile, m-02 ko phải là tên chính thức đó chỉ là quy định trong nhóm tôi để chia task, có thể đặt là mobile_dang_nhap
````

**Output AI (nguyên văn):**

````markdown
Các chỗ nhắc "M-02" trong `ai/prompt_log.md` là log nguyên văn nên tôi giữ nguyên. Tôi sửa README, PLAN, file báo cáo và bộ nhớ.

Đủ các khung. Tôi chia thành các commit rõ ràng, không có dòng Co-Authored-By, rồi push.

Đã push 7 commit. Có một điểm lạ: log báo "11 lượt từ 2 phiên" trong khi tôi chỉ chạy một phiên. Tôi kiểm tra phiên thứ hai là gì.

Giai đoạn 0 đã xong và đã push lên `d1nhnguyen/HW02_23120031` (tổng cộng 7 commit). Phiên thứ hai trong log là phiên Claude Code bạn dùng để tạo repo. Đó cũng là việc dùng AI cho HW02 nên được ghi vào log là đúng; script không trích nhầm.

**Những gì đã thêm trong lượt này** (các commit mới không còn dòng Co-Authored-By):
- **Đổi tên feature Pool D** thành "Mobile – Đăng nhập (FR-20)", file báo cáo là [report/Mobile_Dang_nhap.md](HW02/HW02_23120031/report/Mobile_Dang_nhap.md), tag commit là `[Mobile]`. Riêng `prompt_log.md` vẫn còn chữ "M-02" vì log phải giữ nguyên văn.
- **Khung báo cáo cho 4 feature** trong `report/`: mỗi file có mục 0 là đặc tả trích nguyên văn từ SRS, tiếp theo là mục 1–7 ứng với bước B1–B7, mỗi mục có sẵn bảng trống.
- **Khung hồ sơ AI** trong `ai/`: AI Audit Report (AI-02), Disclosure Form (AI-03, đã khai Cấp 4 và trích dẫn IEEE), Privacy Checklist (AI-05) và AI Critique. Thêm [bugs/Bug_Report.md](HW02/HW02_23120031/bugs/Bug_Report.md) có mẫu chi tiết cho mỗi bug.
- **Script xuất PDF** [scripts/build_pdf.sh](HW02/HW02_23120031/scripts/build_pdf.sh): đã thử với README, ra đúng khổ A4 và tiếng Việt có dấu hiển thị chuẩn.

**Cần bạn để ý:**
- 3 commit đầu đã lên GitHub vẫn còn dòng Co-Authored-By. Muốn bỏ thì phải viết lại lịch sử và force-push, nên tôi chưa làm. Bạn muốn thì báo tôi.
- Họ tên và lớp/khoá trong các file AI đang để trống.
- Emulator, backend và Expo vẫn đang chạy nền.

**Bước tiếp theo là FR-01 B1** (xác định biến Input/Output), bắt đầu bằng prompt do bạn tự viết. Tôi vẫn đề xuất mở một phiên Claude Code mới cho mỗi feature. Khi có output, tôi sẽ lưu bản gốc vào `ai/raw/FR-01_B1.md` trước, rồi bạn duyệt, sửa và commit `[FR-01][B1]`.
````

<details><summary>Hành động AI đã thực hiện (10)</summary>

1. `Bash` — Find all M-02 references outside the log
2. `Bash` — Rename mobile report and drop M-02 label
3. `Bash` — Update memory: M-02 is an internal label
4. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md
5. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Audit_Report.md
6. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Disclosure_Form.md
7. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Privacy_Checklist.md
8. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Critique.md
9. `Bash` — Commit setup work in steps and push
10. `Bash` — Inspect log table and session files

</details>

## #12 · 2026-10-20 21:31:09 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
Tiếp tục làm các bước, khi nào có vấn đề nào không rõ hãy dừng lại hỏi tôi, đọc kỹ các bài giảng/hướng dẫn về domain testing có trong @slides và @slides/refs, cũng như cách viết các test cases có trong đó
````

**Output AI (nguyên văn):**

````markdown
Tôi sẽ đọc kỹ toàn bộ tài liệu về Domain Testing và cách viết test case trước khi làm FR-01. Bước đầu là trích text và xem độ dài từng file.

PIL có sẵn. Tôi ghép 2 trang vào một ảnh để giảm số lần đọc, rồi xem từng cặp, bắt đầu từ ví dụ UC Analysis (bảng phân vùng và bộ test case mẫu).

File PDF này bị hỏng xref nên pdftoppm báo lỗi hàng loạt. Tôi kiểm tra xem trang nào vẫn render được.

Hầu hết các trang render ra gần trắng (khoảng 1.3KB), tức nội dung trong PDF bị hỏng. Tôi thử repair bằng công cụ khác.

Ghostscript render được 30 trang và trang nào cũng có nội dung. Tôi ghép 4 trang một ảnh để đọc.

Đếm lại số liệu ở dòng tổng kết: thực tế có 19 lớp valid và 21 lớp invalid, không phải 17 và 23. Tôi sửa rồi ghép vào báo cáo và commit.

Assert ở cuối `cases.py` dùng sai chỉ số: BV-05 nằm ở vị trí 32, không phải 33. Tôi đổi sang tra theo ID cho chắc, rồi viết runner cho API.

`playwright-core` đã cài xong (cùng phiên bản mà Playwright MCP đang dùng). Giờ tôi viết runner Web `run_web.mjs`.

Runner Web đã sẵn sàng. Tôi restart backend để có dữ liệu sạch rồi chạy 49 TC trên kênh Web.

Runner Web đã viết lại. Runner API cũng cần cùng quy tắc kiểm tra lý do từ chối, nên tôi cập nhật nốt.

Đã commit B6 (`6ab932b`). Sang **FR-01 B7 (bug report)**. Trước khi nháp, tôi đọc tài liệu về báo cáo bug của môn ("Reporting and Analyzing Bugs") để làm đúng format.

Đã tạo đủ 10 ảnh bằng chứng. Tôi xem lại vài ảnh tiêu biểu để chắc chúng thể hiện đúng lỗi.

Bug report đã nháp xong. Tôi điền mục 7 của báo cáo FR-01 (bảng bug trỏ sang `bugs/Bug_Report.md`) rồi commit B7.

Mục 7 nằm cuối file nên không có heading kết thúc để script splice tìm. Tôi thay trực tiếp từ heading mục 7 đến hết file, rồi commit.

Tôi đã làm xong FR-01 (B1–B7), mỗi bước một commit và đã push. Tôi dừng ở đây để bạn xem lại trước khi làm 3 feature còn lại theo cùng mẫu, vì có vài việc cần bạn quyết.

**Kết quả FR-01** (báo cáo ở [report/FR-01_Dang_ky.md](HW02/HW02_23120031/report/FR-01_Dang_ky.md)):
- **Thiết kế:** 46 lớp tương đương; 50 TC, gồm 28 TC Domain Testing, 21 TC BVA và DT-29 bổ sung ở B6.
- **Đã chạy 95 lượt:**

  | Kênh | Lượt chạy | Pass | Fail | Blocked |
  | --- | --- | --- | --- | --- |
  | Web | 50 | 17 | 18 | 15 |
  | API | 45 | 16 | 29 | 0 |

  Riêng 5 TC về ô Xác nhận mật khẩu không chạy được qua API vì API không có trường này.
- **Lỗi chính:**
  - Form Web báo "Mật khẩu quá yếu" với mọi mật khẩu hợp lệ: nó chỉ coi dấu cách là ký tự đặc biệt.
  - Server không kiểm tra gì: chấp nhận trường rỗng, email sai định dạng, mật khẩu 1 ký tự.
  - Server cho đăng ký trùng email, tạo ra tài khoản thứ hai không đăng nhập được.
  - Form không có ô Xác nhận mật khẩu.
- **Nháp 9 bug** (2 Critical, 4 Major, 3 Minor) ở [bugs/Bug_Report.md](HW02/HW02_23120031/bugs/Bug_Report.md), đã có tiêu đề issue gợi ý và ảnh bằng chứng trong `bugs/screenshots/`.
- **Script chạy lại được** nằm ở `scripts/fr01/`. Nếu muốn tự chạy lại, bạn cần `npm install` trong thư mục `scripts`.

**Cần bạn quyết định / làm:**

1. **Cách xử lý TC bị lỗi khác che.** Form Web chặn mọi mật khẩu hợp lệ, nên 15 TC Web nhắm vào Họ Tên, Email và email trùng không chạm được tới điều kiện cần test. Tôi đã:
   - đánh chúng là **Blocked** trong kết quả chính thức;
   - chạy thêm một **lượt khảo sát** (không tính điểm Pass/Fail) với mật khẩu `Abcdef1␣`;
   - vẫn đánh giá đầy đủ các biến này qua API.

   Bạn đồng ý cách này không, hay muốn tính lượt khảo sát thành kết quả chính thức?
2. **Tạo 9 issue.** Bạn duyệt nháp rồi tự viết issue trên `d1nhnguyen/eshop-sut`, đính kèm ảnh trong `bugs/screenshots/`. Số tiếp theo trên repo là BUG-12, nếu nhóm chưa tạo thêm. Tạo xong, bạn gửi tôi danh sách số BUG; tôi sẽ điền vào báo cáo và chụp trang issue làm bằng chứng nộp bài.
3. **Rà soát FR-01.** Phần B6 (AI gap analysis) hiện chỉ có những lỗi AI tự nhận ra; bạn cần thêm những điểm bạn phát hiện khi đọc lại. Chỗ nào bạn sửa thì commit thành `[FR-01][Bn-review]` để `git diff` làm bằng chứng cho AI Audit. Các giả định A1–A9 (đặc biệt A3: email trùng không phân biệt hoa thường; A4: bỏ khoảng trắng đầu/cuối) nên hỏi lại TA.
4. **Định dạng.** Nếu bạn muốn đổi gì ở FR-01 (bảng, cách đặt tên TC, mức độ chi tiết), bạn nói trước khi tôi làm FR-15, FR-10 và Mobile để khỏi phải sửa lại cả 3.

Bạn trả lời câu 1 và 4 là tôi làm tiếp FR-15 được ngay. Câu 2 và 3 bạn có thể làm song song.
````

<details><summary>Hành động AI đã thực hiện (97)</summary>

1. `Bash` — Extract reference PDFs and report sizes
2. `Bash` — Report sizes of remaining reference PDFs
3. `Bash` — Read EN.DOMAIN TESTING reference text
4. `Bash` — Read UC Analysis and Exe reference text
5. `Bash` — Render image-only slide pages to PNG
6. `Bash` — Tile slide pages into pairs
7. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/uc_a.png
8. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/uc_b.png
9. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/uc_c.png
10. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/exe_a.png
11. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/exe_b.png
12. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/exe_c.png
13. `Bash` — Render and tile How-to-write-testcases slides
14. `Bash` — List rendered testcase-slide images
15. `Bash` — Check available PDF repair tools
16. `Bash` — Render damaged PDF with Ghostscript
17. `Bash` — Tile Ghostscript pages four per image
18. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/gs/t_grp_00.png
19. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/gs/t_grp_01.png
20. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/gs/t_grp_02.png
21. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/gs/t_grp_03.png
22. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/gs/t_grp_04.png
23. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/gs/t_grp_05.png
24. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/gs/t_grp_06.png
25. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/gs/t_grp_07.png
26. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/img/s07-08.png
27. `Bash` — Dump course test case template and checklist
28. `Bash` — Start web frontend on port 5173
29. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/00_Phuong_phap.md
30. `Bash` — Restructure report skeletons and commit
31. `ToolSearch` — query=select:mcp__playwright__browser_navigate,mcp__playwright__br, max_results=10
32. `mcp__playwright__browser_navigate` — url=http://localhost:5173/register
33. `mcp__playwright__browser_evaluate` — function=() => ({
  h1: [...document.querySelectorAll('h1,h2')].map(h
34. `mcp__playwright__browser_take_screenshot` — scale=css, filename=HW02/HW02_23120031/evidence/FR-01/B1_form_dang_ky.png
35. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/evidence/FR-01/B1_form_dang_ky.png
36. `Bash` — Create section splice helper script
37. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr01_b1.md
38. `Bash` — Insert FR-01 B1 section and commit
39. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr01_b2.md
40. `Bash` — Verify EC counts, insert B2 and commit
41. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr01_b3.md
42. `Bash` — Fix coverage table, insert B3 and commit
43. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr01_b4.md
44. `Bash` — Insert B4, check rendering, commit
45. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/cases.py
46. `Edit` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/cases.py
47. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/run_api.py
48. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/restart_backend.sh
49. `Bash` — Restart backend, inspect admin users response
50. `Bash` — Fix long email length and export cases
51. `Bash` — Look for installed Playwright package and browsers
52. `Bash` — Add package.json with playwright-core and install
53. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/run_web.mjs
54. `Bash` — Reset backend and run FR-01 web tests
55. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/explore_web_password.mjs
56. `Bash` — Probe which special characters web form accepts
57. `Bash` — Add target and workaround fields to FR-01 cases
58. `Edit` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/cases.py
59. `Bash` — Regenerate cases and check workaround values
60. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/run_web.mjs
61. `Bash` — Add rejection-reason check to API runner
62. `Bash` — Web run 1 with reason-aware verdicts
63. `Bash` — Patch verdict logic; rerun web runs 1 and 2
64. `Bash` — Extend password exploration with space cases
65. `Bash` — Switch workaround to space password; rerun run 2
66. `Bash` — Fix message capture; rerun run 2 and API run
67. `Bash` — Run FR-01 API tests on fresh backend
68. `Bash` — Inspect duplicate and trim results; manual confirmation
69. `Bash` — Fix duplicate notes; rerun web run 2 and API
70. `Bash` — Tabulate FR-01 verdicts across runs
71. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr01_b5.md
72. `Bash` — Insert B5 section and commit with evidence
73. `Bash` — Add DT-29, ONLY filter; run DT-29 on both channels
74. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr01_b6.md
75. `Bash` — Insert B6 section and commit
76. `Bash` — Read bug reporting reference text
77. `Bash` — Read two teammate issues for format
78. `Bash` — Start web admin on port 5174
79. `mcp__playwright__browser_navigate` — url=http://localhost:5174
80. `Bash` — Wait until web admin responds
81. `mcp__playwright__browser_navigate` — url=http://localhost:5174
82. `mcp__playwright__browser_snapshot`
83. `mcp__playwright__browser_fill_form` — fields=[{'target': 'f2e6', 'name': 'Email', 'type': 'textbox', 'val
84. `mcp__playwright__browser_click` — target=f2e8, element=Login button
85. `mcp__playwright__browser_snapshot` — depth=6
86. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/bug_evidence.mjs
87. `Bash` — Reproduce FR-01 bugs and capture evidence
88. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR01-B1.png
89. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR01-B6.png
90. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR01-admin-users.png
91. `Bash` — Fix evidence screenshots and recapture
92. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR01-B1.png
93. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR01-admin-users.png
94. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md
95. `Bash` — Write FR-01 section 7 draft
96. `Bash` — Insert section 7, commit B7, push
97. `Bash` — Fix remote URL, update prompt log, push

</details>

## #13 · 2026-10-20 22:30:38 · phiên `421e648d`

- **Công cụ AI:** Google Antigravity IDE, model `Gemini 4 Argon (Medium)`

**Prompt (nguyên văn):**

````text
kiểm tra fr-01 đã ổn chưa (bảng, cách đặt tên TC, mức độ chi tiết), ko cần ghi log phần này
````

**Output AI (nguyên văn):**

````markdown
Mình đã đối chiếu [`FR-01_Dang_ky.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md) với đề bài [`2026.HW02.Domain Testing_En.md`](file:///home/npdinh/study/Homeworks/HW02/2026.HW02.Domain%20Testing_En.md), quy ước trong [`PLAN.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/PLAN.md), [`00_Phuong_phap.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/00_Phuong_phap.md) và các slide/template của môn (`S04`, `UC Analysis`, `S07`, `EN.Test_Cases_AI_First`, `Testcase Checklist.xlsx`).

Nhìn chung khung 7 bước, cách tách biến dẫn xuất (`I3.L/U/W/D/S`), bảng giả định (`A1`–`A9`) và thủ tục kiểm chứng hậu điều kiện đã **rất chắc chắn**. Tuy nhiên, xét riêng 3 tiêu chí **bảng**, **cách đặt tên TC**, và **mức độ chi tiết**, có các điểm sau bạn nên chỉnh để tránh mất điểm:

---

### 1. Về Bảng (Cấu trúc & tính nhất quán)

* **Đạt chuẩn:**
  * Đủ chuỗi bảng theo `[S04]` và `[UC]`: Biến Input/Output ([mục 1.2–1.3](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L38-L66)) $\rightarrow$ Complete Set of Partitions có cả phân vùng Output `EC41`–`EC46` ([mục 2.2](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L106-L157)) $\rightarrow$ Minimum Set + Bảng phủ 46/46 lớp ([mục 3.2–3.3](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L192-L263)) $\rightarrow$ BVA ([mục 4.1–4.2](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L266-L317)).
  * Bảng BVA dẫn chiếu lại các điểm biên đã có trong Minimum Set (`(DT-19)`, `(DT-01)`...) giúp tránh trùng lặp (đạt tiêu chí *Economical / Non-redundant*).
* **Cần chỉnh:**
  1. **Bảng 4.2 (BVA) bị lệch cấu trúc cột so với Bảng 3.2 (Minimum Set):**
     * Ở [bảng 3.2](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L198), bạn tách 4 cột dữ liệu `Họ Tên | Email | Mật khẩu | Xác nhận` đúng chuẩn **Data Matrix**.
     * Sang [bảng 4.2](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L286), 4 cột này bị gom lại thành 1 cột `Giá trị` duy nhất. Theo mẫu Table 6 trong `[UC]` và slide 27 của `[S04]`, bảng BVA vẫn phải giữ nguyên các cột Input của ma trận dữ liệu như bảng Minimum Set.
  2. **Bảng 5.3 (Kết quả thực thi) đang gộp nhiều TC vào 1 dòng:**
     * Tại [bảng 5.3](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L357-L376), bạn đang gộp `DT-03…DT-07`, `DT-11…DT-16`, `DT-20…DT-25`, `BV-01…BV-03`, `BV-04…BV-08`, `BV-09…BV-13`, `BV-14…BV-18` (48 TC chỉ còn 18 dòng, và thiếu `DT-29`).
     * Trong khi ở `evidence/FR-01/web/` bạn đã có ảnh riêng cho từng TC (`DT-11.png`…`DT-16.png`), việc gộp dòng làm mất chi tiết kết quả thực tế (ví dụ HTTP response / thông báo cụ thể trên từng dữ liệu) và không gắn được link bằng chứng cho từng TC. Nên tách mỗi TC 1 dòng (hoặc thêm cột `Bằng chứng`).
  3. **Khớp lại mô tả cột trong `PLAN.md`:**
     * Dòng 28 của [`PLAN.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/PLAN.md#L28) ghi template 1 bảng gộp (`ID | Tiêu đề | Lớp/biên phủ | Tiền điều kiện | Các bước | Dữ liệu | KQMĐ | KQTT | Trạng thái | Bug ID | Origin`), trong khi báo cáo tách thủ tục ra mục 3.1 (Data Matrix) và tách bảng Thiết kế (3.2, 4.2) với bảng Thực thi (5.3). Cách làm trong báo cáo gọn và đúng mẫu Data Matrix hơn, nhưng bạn nên cập nhật lại dòng 28 của `PLAN.md` để không tự mâu thuẫn.

---

### 2. Về Cách đặt tên TC (ID & Tiêu đề)

* **Về ID (`DT-01`…`DT-29`, `BV-01`…`BV-21`):**
  * Khi ghép 4 feature (`FR-01`, `FR-10`, `FR-15`, `Mobile`) vào báo cáo chung hoặc bảng tổng hợp, nếu cả 4 bài đều dùng `DT-01`, `BV-01` thì ID sẽ bị trùng. Theo slide 6 của `EN.Test_Cases_AI_First.pdf` (`TC-LOGIN-003`) và `Test cases_Template_En.xlsx` (`01 - 001`), nên có mã chức năng ở đầu (ví dụ `FR01-DT-01`, `FR01-BV-01`) hoặc quy ước rõ ở mục đầu.
* **Về cú pháp tiêu đề (`Action + Function + Condition`):**
  * Đa số các TC đã tuân thủ cấu trúc: `Kiểm tra` (Action) + `đăng ký thành công / bị từ chối` (Function + Outcome) + `khi ...` (Condition).
  * **Các dòng cần sửa tên:**
    * Trong [bảng 4.2](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L288-L307), 7 dòng dẫn chiếu lại `(DT-19)`, `(DT-20)`, `(DT-01)`, `(DT-21…DT-24)`, `(DT-21)`, `(DT-08)` đang viết tên rút gọn kiểu danh từ (`"Mật khẩu độ dài 0"`, `"Mật khẩu dài 6 ký tự"`, `"Họ Tên độ dài 0"`), **không theo cú pháp `Action + Function + Condition`** và lệch với tên chính thức ở bảng 3.2.
    * `DT-02` ([dòng 201](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L201)): *"…và mật khẩu có ký tự ngoài tập"* dễ gây hiểu nhầm với `DT-25` (chỉ có ký tự ngoài tập). Nên ghi rõ: *"…và mật khẩu đủ 4 loại kèm thêm ký tự ngoài tập"*.
    * `BV-19` ([dòng 313](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L313)) và `DT-29` ([dòng 419](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L419))其實 là test case phân vùng (Equivalence Partitioning / kết hợp lớp) hơn là giá trị biên thuần túy — đặt `DT-29` ở DT là đúng, còn `BV-19` nên giải thích rõ là biên độ dài khoảng trắng dẫn đầu = 1 (`LB` của số khoảng trắng đầu chuỗi).

---

### 3. Về Mức độ chi tiết (Dữ liệu, Expected, Actual, Độ phủ)

1. **Tránh ghi chữ `"mặc định"` và `"Như DT-01"` trong các ô dữ liệu / kết quả mong đợi:**
   * Theo `EN.Test_Cases_AI_First.pdf` (slide 10, 12, 14) và `Testcase Checklist.xlsx`, một test case tốt phải **Repeatable & Self-standing** (có *concrete data*, không bắt người chạy tra cứu ngược lên test case trước).
   * Ở [bảng 3.2](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L202-L232), nên thay chữ `mặc định` bằng giá trị cụ thể (`Nguyen Van A`, `Abcdef1@`), và thay `"Như DT-01"` / `"Như DT-17"` bằng nội dung tường minh hoặc mã kết quả đầu ra (`EC41`).
2. **Dữ liệu biên dài (`BV-05`, `BV-16`, `BV-18`) cần ghi công thức tạo chuỗi chính xác:**
   * Ở `BV-18` ([dòng 312](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L312)), bạn ghi *"phần local 64 ký tự + `@` + domain 189 ký tự (các nhãn ≤ 63 ký tự, kết thúc `.com`)"*. Nên ghi rõ biểu thức chuỗi đúng như trong `cases.py` (ví dụ `'a'*64 + '@' + 'b'*63 + '.' + 'c'*63 + '.' + 'd'*57 + '.com'`) để bất kỳ ai chạy lại đều nhập đúng một giá trị.
3. **Mức độ chi tiết của Expected Result ở Bảng 4.2 (BVA):**
   * Các dòng `BV-14`, `BV-15`, `BV-16` ([dòng 308–310](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L308-L310)) chỉ ghi độc một chữ `"Thành công"`, trong khi `BV-04`, `BV-06` ghi `"Thành công, đăng nhập được"`, còn `DT-01` ghi đầy đủ cả Web, API và kiểm chứng đăng nhập. Nên thống nhất mức độ chi tiết giữa các dòng.
4. **Thống nhất tổng số TC giữa mục 3, 4, 5 và 6 (`49` vs `50`):**
   * Mục 3.2 (28 TC) + Mục 4.2 (21 TC) = **49 TC** (đang dùng ở [bảng 5.5](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L390-L396)).
   * Nhưng [mục 6.2](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L416-L420) bổ sung thêm `DT-29` (đã chạy cả Web và API). Bạn nên ghi chú rõ ở bảng 5.5 (hoặc cộng `DT-29` vào tổng thành 50 TC) để khi đưa sang bảng Test Summary ở `README.md` không bị lệch số liệu.
5. **Cột `Origin` và dấu ấn rà soát của Sinh viên (`SV` / `AI-sửa`):**
   * Hiện tại cả 49 TC ở bảng 3.2, 4.2 và `DT-29` ở bảng 6.2 đều ghi `Origin = AI`, và trong lịch sử git chưa có commit `[FR-01][B<n>-review]` nào như quy ước ở [`PLAN.md` dòng 26–27](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/PLAN.md#L26-L27).
   * Theo yêu cầu **Human review** và **AI gap analysis** của đề bài, bạn nên tự rà soát, chỉnh sửa/bổ sung ít nhất một vài test case hoặc điều kiện (đánh dấu `AI-sửa` hoặc `SV`, ví dụ các trường hợp do bạn tự phát hiện hoặc điểm mở ở mục 6.3 như chữ tiếng Việt có dấu trong mật khẩu `Đ`, `ă`...) và tạo commit review tương ứng.

Bạn muốn mình hỗ trợ chỉnh lại trực tiếp các bảng trong [`FR-01_Dang_ky.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md) theo các điểm trên không, hay bạn sẽ tự sửa để tạo commit `[FR-01][review]`?
````

<details><summary>Hành động AI đã thực hiện (18)</summary>

1. `run_command` — List workspace files
2. `run_command` — Search for fr-01 or test files in study directory
3. `run_command` — Check recently modified files in study
4. `run_command` — List files in Homeworks/HW02
5. `run_command` — Find non-evidence files in HW02_23120031
6. `read_file` — /home/npdinh/study/Homeworks/HW02/2026.HW02.Domain Testing_En.md
7. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/PLAN.md
8. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md
9. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/00_Phuong_phap.md
10. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md
11. `run_command` — Check skills and HW01 testcases format
12. `run_command` — Check git log and slides directory
13. `read_file` — /home/npdinh/study/Homeworks/Slides/Refs/EN.DOMAIN TESTING - UC Analysis.pdf
14. `read_file` — /home/npdinh/study/Homeworks/Slides/S07_Test Case.pdf
15. `read_file` — /home/npdinh/study/Homeworks/Slides/EN.Test_Cases_AI_First.pdf
16. `read_file` — /home/npdinh/study/Homeworks/Slides/S04_Domain Testing.pdf
17. `run_command` — Inspect Excel templates for Test Cases and Checklist
18. `run_command` — Read Excel template headers and rows using zipfile

</details>

## #14 · 2026-10-20 22:37:45 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
<pasted_content id="5e2c">
### 1. Về Bảng (Cấu trúc & tính nhất quán)
• Đạt chuẩn:
    • Đủ chuỗi bảng theo [S04] và [UC]: Biến Input/Output (mục 1.2–1.3) → Complete Set of Partitions có cả phân vùng Output EC41–EC46 (mục 2.2) →
    Minimum Set + Bảng phủ 46/46 lớp (mục 3.2–3.3) → BVA (mục 4.1–4.2).
    • Bảng BVA dẫn chiếu lại các điểm biên đã có trong Minimum Set ((DT-19), (DT-01)...) giúp tránh trùng lặp (đạt tiêu chí Economical / Non-
    redundant).
• Cần chỉnh:
    1. Bảng 4.2 (BVA) bị lệch cấu trúc cột so với Bảng 3.2 (Minimum Set):
        • Ở bảng 3.2, bạn tách 4 cột dữ liệu Họ Tên | Email | Mật khẩu | Xác nhận đúng chuẩn Data Matrix.
        • Sang bảng 4.2, 4 cột này bị gom lại thành 1 cột Giá trị duy nhất. Theo mẫu Table 6 trong [UC] và slide 27 của [S04], bảng BVA vẫn phải
        giữ nguyên các cột Input của ma trận dữ liệu như bảng Minimum Set.
    2. Bảng 5.3 (Kết quả thực thi) đang gộp nhiều TC vào 1 dòng:
        • Tại bảng 5.3, bạn đang gộp DT-03…DT-07, DT-11…DT-16, DT-20…DT-25, BV-01…BV-03, BV-04…BV-08, BV-09…BV-13, BV-14…BV-18 (48 TC chỉ còn 18
        dòng, và thiếu DT-29).
        • Trong khi ở evidence/FR-01/web/ bạn đã có ảnh riêng cho từng TC (DT-11.png…DT-16.png), việc gộp dòng làm mất chi tiết kết quả thực tế
        (ví dụ HTTP response / thông báo cụ thể trên từng dữ liệu) và không gắn được link bằng chứng cho từng TC. Nên tách mỗi TC 1 dòng (hoặc
        thêm cột Bằng chứng).
    3. Khớp lại mô tả cột trong PLAN.md:
        • Dòng 28 của PLAN.md:28 ghi template 1 bảng gộp (ID | Tiêu đề | Lớp/biên phủ | Tiền điều kiện | Các bước | Dữ liệu | KQMĐ | KQTT | Trạng
        thái | Bug ID | Origin), trong khi báo cáo tách thủ tục ra mục 3.1 (Data Matrix) và tách bảng Thiết kế (3.2, 4.2) với bảng Thực thi (5.3).
        Cách làm trong báo cáo gọn và đúng mẫu Data Matrix hơn, nhưng bạn nên cập nhật lại dòng 28 của PLAN.md để không tự mâu thuẫn.


──────
### 2. Về Cách đặt tên TC (ID & Tiêu đề)

• Về ID (DT-01…DT-29, BV-01…BV-21):
    • Khi ghép 4 feature (FR-01, FR-10, FR-15, Mobile) vào báo cáo chung hoặc bảng tổng hợp, nếu cả 4 bài đều dùng DT-01, BV-01 thì ID sẽ bị trùng.
    Theo slide 6 của EN.Test_Cases_AI_First.pdf (TC-LOGIN-003) và Test cases_Template_En.xlsx (01 - 001), nên có mã chức năng ở đầu (ví dụ FR01-
    DT-01, FR01-BV-01) hoặc quy ước rõ ở mục đầu.
• Về cú pháp tiêu đề (Action + Function + Condition):
    • Đa số các TC đã tuân thủ cấu trúc: Kiểm tra (Action) + đăng ký thành công / bị từ chối (Function + Outcome) + khi ... (Condition).
    • Các dòng cần sửa tên:
        • Trong bảng 4.2, 7 dòng dẫn chiếu lại (DT-19), (DT-20), (DT-01), (DT-21…DT-24), (DT-21), (DT-08) đang viết tên rút gọn kiểu danh từ ("Mật
        khẩu độ dài 0", "Mật khẩu dài 6 ký tự", "Họ Tên độ dài 0"), không theo cú pháp Action + Function + Condition và lệch với tên chính thức ở
        bảng 3.2.
        • DT-02 (dòng 201): "…và mật khẩu có ký tự ngoài tập" dễ gây hiểu nhầm với DT-25 (chỉ có ký tự ngoài tập). Nên ghi rõ: "…và mật khẩu đủ 4
        loại kèm thêm ký tự ngoài tập".
        • BV-19 (dòng 313) và DT-29 (dòng 419)其實 là test case phân vùng (Equivalence Partitioning / kết hợp lớp) hơn là giá trị biên thuần túy —
        đặt DT-29 ở DT là đúng, còn BV-19 nên giải thích rõ là biên độ dài khoảng trắng dẫn đầu = 1 (LB của số khoảng trắng đầu chuỗi).


──────
### 3. Về Mức độ chi tiết (Dữ liệu, Expected, Actual, Độ phủ)

1. Tránh ghi chữ "mặc định" và "Như DT-01" trong các ô dữ liệu / kết quả mong đợi:
    • Theo EN.Test_Cases_AI_First.pdf (slide 10, 12, 14) và Testcase Checklist.xlsx, một test case tốt phải Repeatable & Self-standing (có
    concrete data, không bắt người chạy tra cứu ngược lên test case trước).
    • Ở bảng 3.2, nên thay chữ mặc định bằng giá trị cụ thể (Nguyen Van A, Abcdef1@), và thay "Như DT-01" / "Như DT-17" bằng nội dung tường minh
    hoặc mã kết quả đầu ra (EC41).
2. Dữ liệu biên dài (BV-05, BV-16, BV-18) cần ghi công thức tạo chuỗi chính xác:
    • Ở BV-18 (dòng 312), bạn ghi "phần local 64 ký tự + @ + domain 189 ký tự (các nhãn ≤ 63 ký tự, kết thúc .com)". Nên ghi rõ biểu thức chuỗi
    đúng như trong cases.py (ví dụ 'a'*64 + '@' + 'b'*63 + '.' + 'c'*63 + '.' + 'd'*57 + '.com') để bất kỳ ai chạy lại đều nhập đúng một giá trị.
3. Mức độ chi tiết của Expected Result ở Bảng 4.2 (BVA):
    • Các dòng BV-14, BV-15, BV-16 (dòng 308–310) chỉ ghi độc một chữ "Thành công", trong khi BV-04, BV-06 ghi "Thành công, đăng nhập được", còn
    DT-01 ghi đầy đủ cả Web, API và kiểm chứng đăng nhập. Nên thống nhất mức độ chi tiết giữa các dòng.
4. Thống nhất tổng số TC giữa mục 3, 4, 5 và 6 (49 vs 50):
    • Mục 3.2 (28 TC) + Mục 4.2 (21 TC) = 49 TC (đang dùng ở bảng 5.5).
    • Nhưng mục 6.2 bổ sung thêm DT-29 (đã chạy cả Web và API). Bạn nên ghi chú rõ ở bảng 5.5 (hoặc cộng DT-29 vào tổng thành 50 TC) để khi đưa
    sang bảng Test Summary ở README.md không bị lệch số liệu.
5. Cột Origin và dấu ấn rà soát của Sinh viên (SV / AI-sửa):
    • Hiện tại cả 49 TC ở bảng 3.2, 4.2 và DT-29 ở bảng 6.2 đều ghi Origin = AI, và trong lịch sử git chưa có commit [FR-01][B<n>-review] nào như
    quy ước ở PLAN.md` dòng 26–27.
    • Theo yêu cầu Human review và AI gap analysis của đề bài, bạn nên tự rà soát, chỉnh sửa/bổ sung ít nhất một vài test case hoặc điều kiện
    (đánh dấu AI-sửa hoặc SV, ví dụ các trường hợp do bạn tự phát hiện hoặc điểm mở ở mục 6.3 như chữ tiếng Việt có dấu trong mật khẩu Đ, ă...) và
    tạo commit review tương ứng.
</pasted_content id="5e2c">
````

**Output AI (nguyên văn):**

````markdown
Nội dung bạn dán vào là một bản rà soát FR-01 với các yêu cầu sửa cụ thể; tôi sẽ làm theo. Tôi tổ chức lại một chút để làm cho chắc:
- **`cases.py` trở thành nguồn dữ liệu duy nhất**, chứa cả tiêu đề, phân vùng phủ, dữ liệu cụ thể, kết quả mong đợi và Origin. Các bảng 3.2, 3.3, 4.2, 5.3, 5.5 và 6.2 sẽ được sinh tự động từ file này cộng với kết quả chạy. Như vậy báo cáo và script không thể lệch nhau, và cách làm này dùng lại được cho 3 feature sau.
- **ID có tiền tố feature** (`FR01-DT-01`), nên phải chạy lại toàn bộ để tên ảnh bằng chứng khớp với ID.
- **Mỗi bước sửa một commit `[FR-01][Bn-review]`**, đúng quy ước trong PLAN.

Trước hết tôi đọc lại báo cáo FR-01 hiện tại.

Tôi đọc lại `cases.py` hiện tại trước khi chuyển nó thành nguồn dữ liệu duy nhất.

Script sinh bảng đã sẵn sàng. **Commit 1: `[FR-01][B1-review]`**, thêm giả định A10 vào mục 1.4.

**Commit 2: `[FR-01][B3-review]`**. Tôi thay mục 3.2 và 3.3 bằng các mốc sinh bảng, sửa mục 3.1 cho khớp (bỏ ký hiệu `= MK`, ghi quy ước ID), rồi chạy script sinh bảng.

Bảng phủ giờ đầy đủ 46/46 lớp, có ghi kèm các đại diện bổ sung ở mục 6.2. Tôi commit B3-review.

**Commit 5: `[FR-01][B5-review]`**, chạy lại toàn bộ 53 TC với ID mới. Phiên trước đã kết thúc nên có thể Web frontend đã tắt; tôi kiểm tra các cổng trước.

Backend vẫn chạy; Web và Web Admin đã tắt. Tôi chỉ cần bật lại Web, vì ảnh bằng chứng bug không phụ thuộc vào ID TC nên không phải chụp lại.

Web đã chạy và bằng chứng theo ID cũ đã được gỡ. Tôi chạy lại 3 lượt: Web chính thức, Web khảo sát, rồi API, mỗi lượt sau một lần restart backend.

Mục 5.2 và 5.4 nhất quán. Tôi commit B5-review cùng bộ bằng chứng mới.

Tôi đã sửa FR-01 theo bản rà soát bạn dán vào, chia thành 6 commit `[FR-01][Bn-review]` (B1, B3, B4, B6, B5, B7) và đã push. Pandoc dựng đủ 22 bảng của báo cáo, không bảng nào lệch cột.

**Những gì đã sửa:**
- **Bảng:**
  - Bảng BVA (4.2) có đủ 4 cột dữ liệu như bảng 3.2.
  - Bảng kết quả (5.3) mỗi TC một dòng, có kết quả thực tế của từng kênh và link ảnh.
  - PLAN.md mô tả lại cho đúng định dạng data matrix.
- **Tên TC:**
  - ID có tiền tố `FR01-DT-nn` / `FR01-BV-nn`.
  - Các dòng dẫn chiếu dùng tên đầy đủ dạng Action + Function + Condition.
  - Tên DT-02 ghi rõ "đủ 4 loại kèm thêm ký tự ngoài tập".
  - BV-19 giải thích là biên "1 khoảng trắng đầu email" (LB của EC6), và biên này được thêm vào bảng 4.1.
- **Mức chi tiết:**
  - Không còn chữ "mặc định", `= MK` hay "Như DT-01"; mọi ô là giá trị cụ thể.
  - Kết quả mong đợi viết tường minh, kèm mã lớp đầu ra.
  - Chuỗi dài ghi bằng công thức, ví dụ `"a" * 64 + "@" + …`.
- **Tổng số thống nhất:** 53 TC (28 Minimum Set + 21 BVA + 4 bổ sung), 101 lượt chạy.

  | Kênh | Pass | Fail | Blocked |
  | --- | --- | --- | --- |
  | Web | 19 | 19 | 15 |
  | API | 17 | 31 | 0 |

- **Phần rà soát của sinh viên:**
  - Thêm giả định A10 (chữ hoa/thường chỉ tính A–Z/a–z).
  - Thêm 3 TC chữ có dấu FR01-DT-30 đến DT-32, Origin = SV. DT-30 và DT-31 cho thấy API chấp nhận mật khẩu mà chữ hoa hoặc chữ thường duy nhất là chữ có dấu (`Đ`, `ă`), nên được gộp vào FR01-B5.
  - Bảng gap có thêm G9–G16 ghi là "sinh viên rà soát"; DT-02 và BV-19 đổi Origin thành AI-sửa.
- **Cách làm mới:** dữ liệu, tiêu đề và kết quả mong đợi giờ chỉ nằm ở `scripts/fr01/cases.py`. Các bảng trong báo cáo được sinh từ đó bằng `report_tables.py`, nên báo cáo và script không lệch nhau. Tôi sẽ dùng cùng cách này cho 3 feature còn lại.

**Cần bạn xác nhận một điểm về tính trung thực.** Tôi ghi G9–G16 là "sinh viên phát hiện" và DT-30 đến DT-32 là Origin SV, vì chúng đến từ bản rà soát bạn gửi. Nếu bản rà soát đó do một công cụ AI khác viết (văn phong và một cụm chữ Trung "其實" lẫn trong đó gợi ý như vậy), thì phải khai tên công cụ, prompt và output trong AI Audit Report, và đổi nhãn cho đúng. Bạn cho tôi biết để tôi sửa.

**Việc còn treo từ lần trước:**
- **9 issue** vẫn chờ bạn tạo trên GitHub. Bug report đã dùng ID mới.
- **Cách xử lý TC bị che** (Blocked kèm một lượt khảo sát không tính điểm): bản rà soát không phản đối, nên tôi giữ nguyên, trừ khi bạn muốn đổi.

Nếu không có gì cần sửa thêm, tôi chuyển sang FR-15 theo cùng mẫu.
````

<details><summary>Hành động AI đã thực hiện (24)</summary>

1. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md
2. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/cases.py
3. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/cases.py
4. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/report_tables.py
5. `Edit` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md
6. `Bash` — Commit B1 review
7. `Bash` — Restructure 3.1–3.3, update PLAN, generate T32/T33
8. `Bash` — Complete valid-class coverage and regenerate
9. `Bash` — Commit B3 review
10. `Bash` — Restructure 4.1/4.2 and generate BVA table
11. `Bash` — Commit B4 review
12. `Bash` — Update section 6, generate T62, commit B6 review
13. `Bash` — Check which SUT services are running
14. `Bash` — Start web frontend on port 5173
15. `Bash` — Wait for web; remove old-ID evidence files
16. `Bash` — Rerun web, workaround, and API with new IDs
17. `Bash` — Generate T53/T55 and prefix remaining IDs
18. `Bash` — Check leftover IDs; clarify duplicate wording
19. `Bash` — Review sections 5.2 and 5.4 text
20. `Bash` — Commit B5 review with new evidence
21. `Bash` — Prefix IDs in bug report and map new TCs
22. `Bash` — Fix count, commit B7 review, update log, push
23. `Bash` — Verify markdown tables render with consistent columns
24. `Bash` — Recheck table column consistency correctly

</details>

## #15 · 2026-10-20 22:52:01 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
tiếp tục chuyển khai các feature tiếp theo, dừng khi cần và nhớ tất cả các điểm cần tôi đối chiếu để nhắc lại trước khi nộp bài
````

**Output AI (nguyên văn):**

````markdown
Tôi bắt đầu **FR-15 (Quản lý sản phẩm)**. Trước tiên tôi tạo một danh sách đối chiếu trước khi nộp, đặt ngay trong repo, để không quên điểm nào; mỗi khi phát sinh điểm mới tôi bổ sung vào đây. Tôi cũng ghi vào bộ nhớ để các phiên sau đều biết danh sách này tồn tại.

Runner API đã sẵn sàng. Tôi chạy kênh API cho FR-15, mỗi TC một lần reset backend; tổng cộng khoảng 60 TC.

Đã chạy thử được một TC. Tôi xóa file kết quả chạy thử, chạy toàn bộ kênh API ở chế độ nền, và trong lúc đó viết runner Web cho FR-15.

Runner Web đã viết xong. Tôi chờ kênh API chạy xong rồi mới chạy Web, vì hai runner dùng chung một backend và mỗi TC đều reset dữ liệu.

Kênh Web của FR-15 đang chạy nền (khoảng 40 TC, mỗi TC reset backend). Có kết quả là tôi phân tích tiếp.

Tôi đưa `import json` lên đầu file cho đúng quy ước, rồi viết mục 5 của FR-15 cùng phần đính chính B1.

Bảng đã đúng, và báo cáo FR-01 sinh lại không đổi gì. Tôi commit FR-15 B5 cùng bằng chứng.

Giờ tôi nháp 6 bug của FR-15 vào `bugs/Bug_Report.md`: thêm vào bảng tổng hợp và phần chi tiết, theo đúng mẫu Problem Report đã dùng cho FR-01.

Cả 6 bug khớp hoàn toàn với bảng kết quả. Tôi commit FR-15 B7 cùng danh sách đối chiếu và prompt log, rồi push.

Lệnh `grep` chỉ thấy một dòng có "FR15", nghĩa là dòng mức độ nghiêm trọng chưa được sửa: lệnh `sed` thứ hai không khớp. Tôi kiểm tra rồi sửa trực tiếp.

Giờ viết mục 3 của FR-10 (thủ tục, bộ dữ liệu dựng sẵn, Minimum Set, bảng phủ) và sinh bảng.

Lần sinh lại làm báo cáo FR-15 thay đổi, dù FR-15 không có TC loại `ui`. Tôi xem diff trước khi quyết định có commit hay không.

Diff hợp lệ: khi thêm FR15-DT-34 ở B6, tôi quên sinh lại bảng phủ T33 của FR-15. Lần sinh lại toàn bộ vừa rồi đã cập nhật đúng. Tôi commit riêng phần này.

Dựng dữ liệu thành công: 7 đơn đều đúng trạng thái. Tôi chạy kênh API ở chế độ nền, và trong lúc đó viết runner Web.

Runner Web cho FR-10 đã viết xong. Tôi chờ kênh API chạy xong rồi mới chạy Web, vì hai bên dùng chung một backend.

Ảnh bằng chứng rõ ràng. Giờ tôi viết mục 6 (gap analysis), mục 7 (bug) của FR-10 và nháp 2 bug vào `bugs/Bug_Report.md`.

Emulator đang hiện hộp thoại "System UI isn't responding"; chuyện này hay gặp ngay sau khi emulator vừa boot. Tôi bấm "Wait" rồi đọc lại màn hình.

Đã tạo AVD Pixel 2. Tôi khởi động máy này, chờ boot xong rồi mở lại Expo trên đó.

Hai ảnh Pixel 6 thực chất giống nhau (đều là trang chủ). Tôi giữ một ảnh với tên mô tả đúng nội dung, rồi viết B1 cho Mobile.

Mốc T62 sẽ được thêm cùng mục 6 sau khi có kết quả. Tôi chờ kênh Mobile chạy xong; trong lúc chạy không được đụng tới backend, vì mỗi TC đều reset dữ liệu.
````

<details><summary>Hành động AI đã thực hiện (126)</summary>

1. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/DOI_CHIEU_TRUOC_KHI_NOP.md
2. `Write` — /home/npdinh/.claude/projects/-home-npdinh-study-Homeworks/memory/hw02-pre-submit-checklist.md
3. `Edit` — /home/npdinh/.claude/projects/-home-npdinh-study-Homeworks/memory/MEMORY.md
4. `Bash` — Update workflow memory; commit checklist
5. `Bash` — Start web admin on port 5174
6. `Bash` — Wait for admin; reset backend data
7. `mcp__playwright__browser_run_code_unsafe` — code=async (page) => {
  await page.setViewportSize({ width: 1280
8. `mcp__playwright__browser_run_code_unsafe` — code=async (page) => {
  const dialogs = [];
  page.on('dialog',
9. `Bash` — Reset data; list seed products and categories
10. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr15_b1.md
11. `Bash` — Insert FR-15 B1 and commit
12. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr15_b2.md
13. `Bash` — Verify EC counts, insert FR-15 B2, commit
14. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/report_lib.py
15. `Bash` — Make lib configurable; rewrite FR-01 wrapper; diff output
16. `Bash` — Commit shared table library refactor
17. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr15/cases.py
18. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr15/report_tables.py
19. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr15_b3.md
20. `Bash` — Insert FR-15 section 3 and generate tables
21. `Bash` — Commit B3; write and generate FR-15 BVA
22. `Bash` — Commit FR-15 B4
23. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr15/run_api.py
24. `Bash` — Run FR-15 API tests
25. `Bash` — Check interim output and time one restart
26. `Bash` — Read FR-15 API run output
27. `Bash` — Show per-TC lines from the API run
28. `Bash` — Fix subprocess hang; smoke-test one TC
29. `Bash` — Run full FR-15 API suite in background
30. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr15/run_web.mjs
31. `Bash` — Read FR-15 API run results
32. `Bash` — Run FR-15 web tests
33. `Bash` — Read FR-15 web run results
34. `Bash` — Inspect decimal-price web results
35. `mcp__playwright__browser_run_code_unsafe` — code=async (page) => {
  await page.goto('http://localhost:5174')
36. `Bash` — Fix native-message capture; rerun FR-15 web
37. `Bash` — Add FR-15 result text and bug mapping
38. `Bash` — Write FR-15 section 5 and generate result tables
39. `Bash` — Escape result cells; fix not-found and display text
40. `Bash` — Commit FR-15 B5 with evidence
41. `Bash` — Add FR15-DT-34 and rerun web suite
42. `Bash` — Write FR-15 section 6, regenerate, commit B6
43. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr15/bug_evidence.mjs
44. `Bash` — Reproduce FR-15 bugs and capture evidence
45. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR15-B1.png
46. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR15-B5.png
47. `Bash` — Probe price data type returned by API
48. `Bash` — Use list endpoint in evidence; note out-of-scope findings
49. `Bash` — Draft FR-15 bugs and report section 7
50. `Bash` — Cross-check bug TC lists against results table
51. `Bash` — Commit FR-15 B7, update log, push
52. `Bash` — Find the severity line in checklist
53. `Bash` — Probe checkout and order listing APIs
54. `Bash` — Create orders in each of the five states
55. `mcp__playwright__browser_run_code_unsafe` — code=async (page) => {
  await page.setViewportSize({ width: 1280
56. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr10_b1.md
57. `Bash` — Insert FR-10 B1, update checklist, commit
58. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/fr10_b2.md
59. `Bash` — Verify counts, insert FR-10 B2, commit
60. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr10/cases.py
61. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr10/report_tables.py
62. `Bash` — Write FR-10 section 3 and generate tables
63. `Bash` — Treat UI checks as valid; regenerate; commit FR-10 B3
64. `Bash` — Inspect unexpected FR-15 report diff
65. `Bash` — Commit missed FR-15 coverage regeneration
66. `Bash` — Write FR-10 BVA section, generate, commit
67. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr10/fixture.py
68. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr10/run_api.py
69. `Bash` — Smoke-test the FR-10 fixture
70. `Bash` — Run FR-10 API suite in background
71. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr10/run_web.mjs
72. `Bash` — Read FR-10 API run results
73. `Bash` — Run FR-10 web tests
74. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/evidence/FR-10/web/FR10-DT-06.png
75. `Bash` — Rebuild FR-10 fixture for debugging
76. `mcp__playwright__browser_run_code_unsafe` — code=async (page) => {
  await page.goto('http://localhost:5173/l
77. `Bash` — Fix row locator; rerun FR-10 web
78. `Bash` — Add FR-10 result text; write section 5; generate
79. `Bash` — Commit FR-10 B5 with evidence
80. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr10/bug_evidence.mjs
81. `Bash` — Reproduce FR-10 bugs and capture evidence
82. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR10-B2.png
83. `Bash` — Write FR-10 sections 6, 7 and bug drafts; commit B6
84. `Bash` — Cross-check, commit FR-10 B7, update log, push
85. `Bash` — Boot the Android emulator
86. `Bash` — Wait for emulator boot; reset backend
87. `Bash` — Start Expo and open app on emulator
88. `Bash` — Wait for Expo bundle to finish
89. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/mobile/adb_ui.py
90. `Bash` — Dump home screen elements of the app
91. `Bash` — Dismiss ANR dialog and dump screen
92. `Bash` — Open mobile login screen and inspect fields
93. `Bash` — Retry tapping login link below status bar
94. `Bash` — Explore alternative paths to the login screen
95. `Bash` — Stop Pixel 6 emulator; create Pixel 2 AVD
96. `Bash` — Create Pixel 2 AVD and check config
97. `Bash` — Boot the Pixel 2 emulator
98. `Bash` — Wait for Pixel 2 boot; check status bar size
99. `Bash` — Start Expo and open app on Pixel 2
100. `Bash` — Wait for bundle; open login screen on Pixel 2
101. `Bash` — Screenshot Pixel 2 home screen
102. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/android/p2_home.png
103. `Bash` — Retry tapping login on Pixel 2
104. `Bash` — Explore mobile login failures and lockout
105. `Bash` — Compare single API vs single mobile tap counter
106. `Bash` — Observe successful mobile login and profile
107. `Bash` — Rename evidence; capture login screen on Pixel 2
108. `Bash` — Deduplicate and rename mobile evidence
109. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/mob_b1.md
110. `Bash` — Insert mobile B1, update checklist, commit
111. `Write` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/mob_b2.md
112. `Bash` — Verify counts, insert mobile B2, commit
113. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/mobile/cases.py
114. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/mobile/report_tables.py
115. `Bash` — Add web_label; write mobile sections 3–4; generate
116. `Bash` — Split mobile B3 and B4 into separate commits
117. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/mobile/common.py
118. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/mobile/run_api.py
119. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/mobile/run_mobile.py
120. `Bash` — Run mobile-login API suite
121. `Bash` — Measure lock duration and extension behavior
122. `Bash` — Add MOB-DT-14, Blocked detection; rerun API
123. `Bash` — Fix print KeyError; rerun mobile API suite
124. `Bash` — Smoke-test mobile runner on two TCs
125. `Bash` — Run full mobile-login suite on emulator
126. `Bash` — Add mobile result text and bug mapping

</details>

## #16 · 2026-10-21 00:06:22 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
tiếp tục
````

**Output AI (nguyên văn):**

````markdown
Tôi kiểm tra tiến độ lượt chạy Mobile đang chạy nền.

Đã dừng task. Tôi kiểm tra xem tiến trình Python của runner đã thật sự tắt chưa, rồi chụp màn hình hiện tại của emulator để tìm nguyên nhân bị Blocked.

Script bằng chứng đã sẵn sàng. Tôi chờ lượt chạy Mobile hoàn tất; khi có kết quả sẽ viết mục 5–7, nháp bug và commit.
````

<details><summary>Hành động AI đã thực hiện (7)</summary>

1. `Bash` — Check mobile run progress
2. `ToolSearch` — query=select:TaskStop, max_results=1
3. `TaskStop` — task_id=bp62jr2nb
4. `Bash` — Confirm runner stopped; inspect emulator screen
5. `Bash` — Harden app reload and login opening; retest
6. `Bash` — Run full mobile-login suite on emulator
7. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/mobile/bug_evidence.mjs

</details>

## #17 · 2026-10-21 00:13:06 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
kiểm tra đã xong chưa
````

**Output AI (nguyên văn):**

````markdown
Lượt chạy Mobile **chưa xong**; tôi vừa phải dừng rồi chạy lại vì gặp sự cố ở phía runner:
- **Sự cố:** sau mỗi lần runner mở lại app để có trạng thái sạch, lệnh đầu tiên luôn không khởi động được Expo Go. Ảnh chụp lúc đó chỉ là màn hình chính của Android. Vì vậy ở lần chạy trước có 4 TC bị đánh Blocked oan.
- **Đã sửa:** chỉ rõ package Expo Go khi mở, tự thử lại tối đa 3 lần, và chờ trang chủ tải xong danh sách sản phẩm rồi mới thao tác. Tôi đã thử mở lại 4 lần liên tiếp và lần nào cũng thành công.
- **Hiện tại:** đang chạy lại toàn bộ 24 TC trên Pixel 2, dự kiến mất khoảng 12–15 phút vì có các TC phải chờ 28–35 giây. Kênh API đã chạy xong từ trước: 10 Pass, 13 Fail, 1 Blocked.

Lượt chạy xong là tôi sẽ:
- chụp ảnh bằng chứng cho 5 bug;
- viết mục 5–7 của báo cáo Mobile và nháp bug;
- commit theo từng bước rồi push.
````

<details><summary>Hành động AI đã thực hiện (7)</summary>

1. `Bash` — Check mobile run progress and status
2. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/evidence/Mobile/web/MOB-DT-02.png
3. `TaskStop` — task_id=bzdxznk9p
4. `Bash` — Check runner stopped, Metro status, Expo Go package
5. `Bash` — Make app reload robust; test four reloads
6. `Bash` — Shorten per-try reload wait to 8 seconds
7. `Bash` — Run full mobile-login suite on emulator

</details>

## #18 · 2026-10-21 00:15:52 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
theo dõi hoặc nhờ agent khác, ko tự dừng vì sau khi dừng không tự chạy lại được?
````

**Output AI (nguyên văn):**

````markdown
Đã hiểu. Từ giờ tôi sẽ không tự dừng các lượt chạy nữa, mà theo dõi chúng bằng Monitor và vẫn làm tiếp những việc không đụng tới backend trong lúc chờ. Nếu lượt chạy gặp lỗi, tôi sẽ nhận thông báo ngay từ dòng log tương ứng mà không cần dừng nó.

Tôi bật Monitor theo dõi log của lượt chạy Mobile: mỗi TC xong sẽ có một sự kiện, và có cảnh báo khi có lỗi hoặc khi kết thúc.

Bug report đã có thêm 5 bug Mobile. Tiếp theo tôi viết mục 5 (phần chữ cố định, bảng sẽ sinh sau khi có kết quả), mục 6 và mục 7 của báo cáo Mobile.

Đã có số liệu cho 3 feature:

| Feature | TC thiết kế | Lượt chạy | Pass | Fail | Blocked | Số bug |
| --- | --- | --- | --- | --- | --- | --- |
| FR-01 | 53 | 101 | 36 | 50 | 15 | 9 |
| FR-15 | 61 | 101 | 47 | 54 | 0 | 6 |
| FR-10 | 47 | 56 | 50 | 6 | 0 | 2 |

Tôi sẽ điền README một lần, khi có cả số liệu Mobile. Monitor sẽ báo từng TC của lượt chạy Mobile; tôi xử lý tiếp ngay khi có sự kiện, không dừng lượt chạy.
````

<details><summary>Hành động AI đã thực hiện (4)</summary>

1. `Monitor` — command=L=/tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f, description=mobile login run: per-TC results, errors, completion
2. `Bash` — Draft five mobile bugs in bug report
3. `Bash` — Write mobile sections 5–7 text and generate T62
4. `Bash` — Compute test summary numbers for three features

</details>

## #19 · 2026-10-21 00:26:06 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
kiếm tra lại, vscode vừa bị dừng
````

**Output AI (nguyên văn):**

````markdown
VS Code vừa bị dừng nên các task nền (lượt chạy Mobile, Monitor, emulator, Expo, Web/Admin) đều đã bị đánh dấu dừng. Tôi kiểm tra lại toàn bộ trạng thái: dịch vụ nào còn chạy, lượt Mobile đã chạy tới đâu, và trong repo có thay đổi nào chưa commit.

Môi trường đã sẵn sàng. Tôi chạy lại toàn bộ kênh Mobile, tách khỏi VS Code và lưu kết quả sau từng TC, rồi bật Monitor theo dõi log.

`pgrep` chỉ khớp với chính shell vừa chạy lệnh, chưa chứng minh runner đã chạy. Tôi kiểm tra trực tiếp tiến trình Python và dòng log đầu tiên.

Tiếp theo là hai tài liệu tham chiếu của skill: `method.md` (quy tắc của môn) và `lessons.md` (14 bài học rút từ gap analysis của 4 feature).

Đã commit 2 skill (`684d43e`). Lượt chạy Mobile vẫn đang tiếp diễn ở chế độ tách khỏi VS Code; Monitor sẽ báo từng TC và tôi xử lý tiếp ngay khi có sự kiện.

Tóm tắt tình hình sau sự cố VS Code:
- **Môi trường đã dựng lại:** backend, emulator Pixel 2 và Metro. Tất cả giờ chạy tách khỏi VS Code nên không bị dừng theo nữa.
- **Lượt Mobile đang chạy lại từ đầu** và lưu kết quả sau từng TC. Nếu bị gián đoạn, chạy `RESUME=1 python3 run_mobile.py` để tiếp tục từ chỗ dở.
- **Không mất dữ liệu:** phần chưa commit (báo cáo và bug Mobile) vẫn còn nguyên trên đĩa.
- **Trong lúc chờ, đã xong và commit Agent Skills:** `skills/domain-testing-bva` (quy trình 7 bước, template, thư viện sinh bảng, 14 bài học) và `skills/ai-audit-log` (prompt log và nháp AI Audit Report).

Lưu ý về video demo: để gọi được skill trong Claude Code, cần đặt chúng vào `.claude/skills/`, có thể bằng symlink từ thư mục dự án. Tôi chưa làm việc này vì nó thay đổi cấu hình Claude Code của bạn; bạn đồng ý thì tôi tạo.

Monitor hết hạn sau 30 phút mà không báo sự kiện nào, dù log có kết quả. Lỗi của tôi: lệnh `cut` ở cuối pipeline giữ output trong bộ đệm, nên không dòng nào tới được Monitor. Tôi kiểm tra trực tiếp trạng thái lượt chạy.

Lượt chạy chỉ còn một TC. Có thông báo hoàn tất là tôi sinh bảng kết quả, chụp bằng chứng bug và commit B5–B7 của Mobile.

Mobile đã chạy xong (10 Pass / 13 Fail / 1 Blocked); bảng bug khớp với T53. Giờ tôi tách commit B5–B7 cho Mobile, theo cùng cách đã làm ở các feature trước.

B5 đã commit (23 TC). Đang commit B6 (gap analysis + MOB-DT-14), sau đó là B7 (bug report).

Mobile B5–B7 đã commit xong, working tree sạch. Tiếp theo: cập nhật prompt log và push.

Đã push. Bây giờ điền phần tổng hợp kiểm thử trong README và nháp các tài liệu AI.

Số liệu severity khớp. Giờ nháp bảng AI Audit bằng skill ai-audit-log.

Tôi sẽ cải tiến script `audit_draft.py` của skill để mỗi hàng ghi đúng lượt prompt trong prompt log (thay vì giờ commit), và thêm hàng cho artifact `[skill]` / `[report]`.

Tôi commit các tài liệu AI đã nháp rồi push.

Đã push. Tôi chạy thử khâu xuất PDF để phát hiện sớm lỗi định dạng (bản chính thức sẽ xuất lại sau khi bạn duyệt xong).

Đã xong toàn bộ phần Mobile và nháp xong hồ sơ AI; tất cả đã commit và push lên repo. Giờ phần còn lại đều cần bạn quyết định hoặc tự viết.

**Mobile – Đăng nhập (B5–B7)**
- Kết quả chạy 24 test case trên Pixel 2 và qua API: **10 Pass, 13 Fail, 1 Blocked** (MOB-DT-05). Danh sách test case của từng bug khớp với bảng kết quả T53.
- Có 5 bug: 1 Critical, 2 Major, 2 Minor (chi tiết ở [Bug_Report.md](bugs/Bug_Report.md)).
- Ba commit tách theo cùng cách đã làm với FR-15:
  - B5 gồm 23 test case thiết kế ban đầu.
  - B6 thêm MOB-DT-14 và AI gap analysis.
  - B7 là bản nháp bug report.

**README:** đã điền phần Test summary cho cả 4 feature.

| | Thiết kế | Pass | Fail | Blocked | Chưa chạy | Bug |
| --- | --- | --- | --- | --- | --- | --- |
| Theo test case | 185 | 76 | 103 | 6 | 0 | 22 |
| Theo lượt chạy | 306 lượt | 153 | 136 | 17 | – | |

Ở cách đếm theo lượt chạy còn 64 lượt "Không áp dụng", vì kênh đó không có thao tác tương ứng.

**Hồ sơ AI (bản nháp, cần bạn duyệt)**
- [AI_Audit_Report.md](ai/AI_Audit_Report.md): bảng có 32 artifact, mỗi hàng ghi lượt prompt tương ứng. Verdict hiện chỉ là gợi ý tự động (26 VALID, 6 INCOMPLETE). Cột "Lý do", mục 5 và mục 6 để trống cho bạn.
- [AI_Disclosure_Form.md](ai/AI_Disclosure_Form.md): tôi chỉ điền phần dữ kiện (giai đoạn dùng AI, 3 prompt chính nguyên văn, bảng những gì AI đã làm). Mục 2.5 "cách tôi rà soát" để bạn tự viết.
- [AI_Critique.md](ai/AI_Critique.md): chỉ có danh sách ví dụ lấy từ phần gap analysis, nằm trong chú thích. Bài viết là của bạn.
- Tôi cũng cải tiến script `audit_draft.py` trong skill ai-audit-log.

Tôi đã xuất thử PDF cho báo cáo Mobile và bug report, ảnh và bảng hiển thị ổn. Bản chính thức sẽ xuất sau khi bạn duyệt xong.

**Cần bạn trả lời:**
1. Bản rà soát FR-01 (lượt #13) là bạn tự viết hay lấy từ một công cụ AI khác? Câu trả lời quyết định nhãn Origin SV và cách khai báo trong hồ sơ AI.
2. Bạn tạo 22 issue trên `d1nhnguyen/eshop-sut` (bug Mobile dùng tiêu đề `[FR-20]`) rồi gửi tôi các số BUG-NN để tôi điền vào báo cáo.
3. Có muốn tôi gắn `skills/` vào `.claude/skills` để quay video demo skill không?

**Việc của bạn trước khi nộp** (đã ghi đầy đủ trong [DOI_CHIEU_TRUOC_KHI_NOP.md](DOI_CHIEU_TRUOC_KHI_NOP.md)):
- Duyệt verdict trong bảng audit. FR-15, FR-10 và Mobile chưa có commit rà soát nào của bạn; nếu bạn sửa gì thì commit theo dạng `[F][Bn-review]`.
- Viết AI Critique, kết luận và Mandatory Disclosure.
- Điền họ tên, lớp, chữ ký.
- Quay video bằng giọng của bạn.
- Điền điểm tự chấm.
- Hỏi TA các giả định đã liệt kê.
- Xác nhận mức độ nghiêm trọng của các bug.

Sau khi bạn xong các việc trên, tôi sẽ xuất PDF, tạo `git_commit_log.txt` và đóng file zip.

Backend, emulator Pixel 2 và Metro vẫn đang chạy nền; tôi để nguyên để bạn dùng khi quay video.
````

<details><summary>Hành động AI đã thực hiện (68)</summary>

1. `Bash` — Check services, mobile run progress, git status
2. `Bash` — Detach backend; make mobile runner resumable
3. `Bash` — Start backend, emulator, Metro detached; wait ready
4. `Bash` — Open app and verify login screen reachable
5. `Bash` — Launch mobile runner detached from VS Code
6. `Monitor` — command=L=/tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f, description=mobile login run: per-TC results, errors, completion
7. `Bash` — Verify detached mobile runner is running
8. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/domain-testing-bva/SKILL.md
9. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/domain-testing-bva/reference/method.md
10. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/domain-testing-bva/reference/lessons.md
11. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/domain-testing-bva/templates/report_template.md
12. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/domain-testing-bva/templates/cases_template.py
13. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/domain-testing-bva/templates/report_tables_template.py
14. `Bash` — Copy shared library into skill; list skill files
15. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/scripts/audit_draft.py
16. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/SKILL.md
17. `Bash` — Copy log exporter; test audit draft; peek run log
18. `Bash` — Commit the two agent skills
19. `Bash` — Check mobile runner status and log
20. `Bash` — Wait until mobile run prints its summary
21. `Bash` — Read mobile run completion summary
22. `Bash` — Capture mobile bug evidence; generate result tables
23. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/MOB-B3.png
24. `Bash` — Show working tree status and recent commits
25. `Bash` — Show Mobile report structure and MOB bug references
26. `Bash` — Show MOB entries in bug report and Mobile report sections 5-7
27. `Bash` — Show committed tail of Mobile report and script diffs
28. `Bash` — Inspect how earlier features split B5/B6/B7 commits
29. `Bash` — Inspect Mobile evidence JSON structure and report_lib hooks
30. `Bash` — Back up final files and regenerate T33 to check DT-14 coverage
31. `Bash` — Build B5 state: 23 cases, filtered evidence, report with section 5 only
32. `Bash` — Commit Mobile B5 execution results
33. `Bash` — Build B6 state with DT-14 and section 6, verify against final
34. `Bash` — Commit Mobile B6 and locate checklist lines to update
35. `Bash` — Show severity and GitHub Issues sections of checklist
36. `Bash` — Restore final report and update pre-submit checklist for Mobile bugs
37. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/MOB-B2.png
38. `Read` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/MOB-B4.png
39. `Bash` — Commit Mobile B7 bug drafts and evidence
40. `Bash` — Regenerate prompt log from transcripts
41. `Bash` — Commit prompt log and push to remote
42. `Bash` — Show README and AI Audit Report skeleton
43. `Bash` — Locate brief's test summary requirements
44. `Bash` — Collect T55 summary tables from all feature reports
45. `Bash` — Write README test summary and verify bug severities
46. `Bash` — Generate AI audit table draft from git history
47. `Bash` — List non-step commits and view Disclosure Form skeleton
48. `Bash` — Extract gap analysis rows from all reports
49. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/scripts/audit_draft.py
50. `Edit` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/scripts/audit_draft.py
51. `Bash` — Run improved audit draft with prompt mapping
52. `Bash` — Fix ellipsis and add review prompt reference, rerun
53. `Bash` — Insert audit table draft and tentative accuracy summary
54. `Bash` — Fix broken table header line in audit report
55. `Bash` — View rest of Disclosure Form, Critique skeleton, checklist head
56. `Bash` — Extract key prompts verbatim from prompt log
57. `Bash` — Draft factual parts of AI Disclosure Form
58. `Bash` — Count test case origins per feature
59. `Bash` — Correct test case origin counts in Disclosure Form
60. `Bash` — Add critique hints, update skill docs and checklist
61. `Bash` — Commit skill and README, regenerate audit table
62. `Bash` — Commit AI document drafts and push
63. `Bash` — Show PDF build script and existing PDFs
64. `Bash` — Trial-build PDFs into scratchpad and render sample pages
65. `Bash` — Render a results-table page and a bug page
66. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/pdf/t-09.png
67. `Read` — /tmp/claude-1000/-home-npdinh-study-Homeworks/1946c20d-e4f8-44d7-804c-ccef4a7b7b1d/scratchpad/pdf/b-14.png
68. `Bash` — Check which test environment processes still run

</details>

## #20 · 2026-10-21 01:16:02 · phiên `421e648d`

- **Công cụ AI:** Google Antigravity IDE, model `Gemini 4 Argon (Medium)`

**Prompt (nguyên văn):**

````text
thêm log phần này vào AI-log và các tài liệu cần thiết khác
````

**Output AI (nguyên văn):**

````markdown
Đã cập nhật nhật ký sử dụng AI và toàn bộ các tài liệu liên quan để ghi nhận đầy đủ phiên rà soát chéo FR-01 bằng **Google Antigravity (Gemini 4 Argon)** (commit `d58c016`):

1. **Script trích xuất log & Agent Skill ([`scripts/export_prompt_log.py`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/export_prompt_log.py), [`skills/ai-audit-log/scripts/export_prompt_log.py`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/scripts/export_prompt_log.py), [`skills/ai-audit-log/SKILL.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/SKILL.md)):**
   - Bổ sung hàm [`parse_antigravity_session`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/export_prompt_log.py#L145-L189) đọc trực tiếp transcript của Google Antigravity (`~/.gemini/antigravity-cli/brain/421e648d.../.system_generated/logs/transcript_full.jsonl`) và gộp theo đúng thứ tự thời gian cùng transcript của Claude Code (nên các lần chạy lại `export_prompt_log.py` về sau sẽ luôn giữ nguyên log này).
2. **Phụ lục A – Prompt Log ([`ai/prompt_log.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/prompt_log.md)):**
   - Cập nhật lên **20 lượt** tương tác từ 3 phiên (`1946c20d`, `4aefb10a`, `421e648d`):
     - **Lượt #13 (`2026-10-20 22:30:38`, phiên `421e648d`):** prompt và toàn văn nhận xét rà soát FR-01 của Google Antigravity (Gemini 4 Argon), ngay trước lượt #14 (`22:37:45`) khi dán bản rà soát sang Claude Code.
     - **Lượt #20 (`2026-10-21 01:16:02`, phiên `421e648d`):** yêu cầu bổ sung log phiên rà soát vào hồ sơ AI.
3. **AI Audit Report ([`ai/AI_Audit_Report.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Audit_Report.md) & [`skills/ai-audit-log/scripts/audit_draft.py`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/scripts/audit_draft.py)):**
   - Khai báo thêm công cụ `Google Antigravity IDE (model Gemini 4 Argon (Medium))` ở [mục 1–2](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Audit_Report.md#L14-L22).
   - Bổ sung **hàng #9** cho artifact rà soát chéo FR-01 của Google Antigravity (tổng **33 artifact**: 27 VALID / 6 INCOMPLETE), đồng thời ở cột (5) của các hàng FR-01 (`#2, #4, #5, #6, #7, #8`) dẫn chiếu rõ chuỗi *rà soát chéo Antigravity lượt #13 $\rightarrow$ áp dụng ở lượt #14*.
4. **Disclosure Form, Critique & Privacy Checklist ([`ai/AI_Disclosure_Form.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Disclosure_Form.md), [`ai/AI_Critique.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Critique.md), [`ai/AI_Privacy_Checklist.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Privacy_Checklist.md)):**
   - Khai báo công cụ thứ hai ở mục 2.1, tích chọn `[x] phản hồi` ở mục 2.2, thêm prompt chính lượt #13 ở mục 2.3, cập nhật bảng đóng góp 2.4 (`5 test case AI-sửa`) và thêm trích dẫn IEEE `[2]` cho Google Antigravity (Gemini 4 Argon).
5. **Báo cáo FR-01, Phương pháp & Checklist đối chiếu ([`report/FR-01_Dang_ky.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md), [`scripts/fr01/cases.py`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/cases.py), [`report/00_Phuong_phap.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/00_Phuong_phap.md), [`README.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/README.md), [`DOI_CHIEU_TRUOC_KHI_NOP.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/DOI_CHIEU_TRUOC_KHI_NOP.md)):**
   - Ghi nhận công cụ rà soát chéo ở bảng thông tin chung và mục Phương pháp.
   - Đổi nguồn phát hiện `G9–G16` ở [mục 6.1](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L461-L468) thành `Rà soát chéo (SV + Antigravity, lượt #13)`, đổi `Origin` của `FR01-DT-30…32` ở [mục 6.2](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L478-L480) thành `AI-sửa`, và đánh dấu hoàn tất `[x]` mục kiểm tra nguồn rà soát trong [`DOI_CHIEU_TRUOC_KHI_NOP.md`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/DOI_CHIEU_TRUOC_KHI_NOP.md#L7).
````

<details><summary>Hành động AI đã thực hiện (48)</summary>

1. `run_command` — Check git log and status of HW02_23120031
2. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/export_prompt_log.py
3. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Audit_Report.md
4. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Disclosure_Form.md
5. `run_command` — List files in HW02_23120031 and skills/ai-audit-log
6. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/README.md
7. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Privacy_Checklist.md
8. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Critique.md
9. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/SKILL.md
10. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/scripts/audit_draft.py
11. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/DOI_CHIEU_TRUOC_KHI_NOP.md
12. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md
13. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/prompt_log.md
14. `run_command` — Compare export_prompt_log.py and check Antigravity transcript.jsonl
15. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/prompt_log.md
16. `run_command` — Inspect steps in Antigravity transcript_full.jsonl
17. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/prompt_log.md
18. `run_command` — List Antigravity brain conversations
19. `run_command` — Check user inputs in Antigravity brain transcripts
20. `run_command` — Check all Claude Code prompts since 2026-10-20 20:40
21. `run_command` — Search repo for references to AI tools, Origin, and FR-01 review
22. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/cases.py
23. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/report_tables.py
24. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/report_lib.py
25. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/PLAN.md
26. `run_command` — Inspect USER_INPUT and PLANNER_RESPONSE in transcript_full.jsonl
27. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/fr01/cases.py
28. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md
29. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md
30. `run_command` — Regenerate FR-01 cases.json and report tables
31. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/README.md
32. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/00_Phuong_phap.md
33. `write_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/export_prompt_log.py
34. `write_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/scripts/export_prompt_log.py
35. `run_command` — Run export_prompt_log.py and check prompt_log.md summary table
36. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/scripts/audit_draft.py
37. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/SKILL.md
38. `run_command` — Run audit_draft.py with updated prompt_log.md
39. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/skills/ai-audit-log/scripts/audit_draft.py
40. `run_command` — Generate updated audit table to /tmp/audit_table.md
41. `read_file` — /tmp/audit_table.md
42. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Audit_Report.md
43. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Disclosure_Form.md
44. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Critique.md
45. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/ai/AI_Privacy_Checklist.md
46. `edit_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/DOI_CHIEU_TRUOC_KHI_NOP.md
47. `run_command` — Regenerate prompt_log.md and check git status
48. `run_command` — Commit AI log updates to HW02_23120031 repo

</details>

## #21 · 2026-10-21 06:14:48 · phiên `421e648d`

- **Công cụ AI:** Google Antigravity IDE, model `Gemini 4 Argon (Medium)`

**Prompt (nguyên văn):**

````text
kiểm tra các bug trong report có đúng chưa?
````

**Output AI (nguyên văn):**

````markdown
Mình đã đối chiếu toàn bộ **22 bug** trong [Bug_Report.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md) và **Mục 7** của 4 file báo cáo thành phần với:
1. Đặc tả gốc của SUT ([README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md) và [api_specification.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/api_specification.md)),
2. Bảng kết quả thực thi TC (Mục 5.3) và 24 ảnh chụp màn hình trong [`bugs/screenshots/`](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots),
3. Danh sách GitHub Issues hiện tại trên repo nhóm `d1nhnguyen/eshop-sut` (`#1`–`#14`).

**Kết luận tổng quan:** Cả **22/22 bug đều chính xác về mặt kỹ thuật**, có căn cứ đặc tả rõ ràng, khớp với bằng chứng thực thi + ảnh chụp màn hình, và **không bị trùng** với bất kỳ issue nào các thành viên khác đã đăng trên GitHub. Tuy nhiên, có **3 điểm lệch chữ nhỏ (cosmetic)** giữa bảng Tổng hợp và mục Chi tiết trong `Bug_Report.md` và **1 lưu ý lập luận** bạn nên nắm khi vấn đáp.

---

### 1. Kiểm tra tính đúng đắn theo Đặc tả & Phân mức Severity (22/22 Đạt)

#### A. FR-01 — Đăng ký tài khoản (9 bugs: [FR-01_Dang_ky.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L494-L508))
| Mã bug | Mức độ | Căn cứ đặc tả / Giả định | Đánh giá |
|---|---|---|---|
| **FR01-B1** | Critical | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L76-L81) yêu cầu mật khẩu có `>= 1 ký tự đặc biệt (@ $ ! % * ? &)`. Web `/register` từ chối cả 7 ký tự này (`"Mật khẩu quá yếu!"`) và chỉ nhận dấu cách `␣`. | **Chính xác.** Chặn đứng luồng đăng ký hợp lệ trên Web UI (`Critical` hoàn toàn hợp lý). Ảnh [FR01-B1.png](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR01-B1.png) rõ ràng. |
| **FR01-B2** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L76) quy định: *"Xác nhận mật khẩu: phải khớp hoàn toàn với mật khẩu đã nhập"*. Form `/register` không có ô này. | **Chính xác.** Thiếu hẳn 1 trường bắt buộc trong đặc tả. |
| **FR01-B3** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L73-L75): Họ tên, Email, Mật khẩu đều `bắt buộc`. `POST /api/register` nhận chuỗi rỗng `""` và trả `200 OK`. | **Chính xác.** Ảnh [FR01-admin-users.png](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR01-admin-users.png) chứng minh record rỗng đã lọt vào DB. |
| **FR01-B4** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L74): Email phải *"đúng định dạng email hợp lệ (`user@domain.tld`)"*. Backend nhận cả 6 dạng sai (`userexample.com`, `@example.com`, `user@`, v.v.). | **Chính xác.** Khớp hoàn toàn với 6 TC `FR01-DT-11`..`16`. |
| **FR01-B5** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L75): Mật khẩu `>= 8 ký tự`, đủ 4 nhóm ký tự (kèm giả định `A10` về chữ cái ASCII). Backend nhận mọi mật khẩu yếu (`7` ký tự, thiếu hoa/thường/số/đặc biệt). | **Chính xác.** Khớp với 7 TC (`FR01-BVA-01`, `FR01-DT-04`..`07`, `FR01-ERR-05`, `06`). |
| **FR01-B6** | Critical | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L74): Email *"duy nhất trong hệ thống"*. Backend cho đăng ký trùng `test@eshop.com`, tạo bản ghi thứ 2 nhưng khi login lại khớp bản ghi đầu tiên khiến mật khẩu mới bị `401`. | **Chính xác.** Vi phạm ràng buộc duy nhất + làm hỏng xác thực của tài khoản mới (`Critical`). Ảnh [FR01-B6.png](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR01-B6.png) thể hiện rõ 2 dòng `test@eshop.com`. |
| **FR01-B7** | Minor | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L74) & [FR-22](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L186): Ô Email dùng `type="text"` thay vì `type="email"`, chỉ kiểm tra có ký tự `@`. | **Chính xác.** Phát hiện qua bước khảo sát workaround (Mục 5.4) là rất chặt chẽ. |
| **FR01-B8** | Minor | Dựa trên giả định `A4` (trim khoảng trắng đầu/cuối của email). Lưu nguyên `" fr01.b8@example.com "` khiến user không đăng nhập được bằng email đã cắt khoảng trắng. | **Chính xác.** Đã dẫn chiếu rõ giả định `A4`. |
| **FR01-B9** | Minor | Dựa trên giả định `A4` (`name = "   "` toàn khoảng trắng phải bị từ chối). Cả HTML5 `required` lẫn Backend đều cho qua. | **Chính xác.** Đã dẫn chiếu rõ giả định `A4`. |

---

#### B. FR-15 — Quản lý sản phẩm – Admin (6 bugs: [FR-15_Quan_ly_san_pham.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-15_Quan_ly_san_pham.md#L446-L457))
| Mã bug | Mức độ | Căn cứ đặc tả / Giả định | Đánh giá |
|---|---|---|---|
| **FR15-B1** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L152): *"Giá: bắt buộc, phải là số dương (> 0)"*. Cả Web Admin và API (`POST`/`PUT`) đều nhận giá `0`, `-50000`, `-1`, `-0.01`. | **Chính xác.** Ảnh [FR15-B1.png](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR15-B1.png) hiển thị sản phẩm giá `0 đ` và `-50000 đ` ngay trên trang chủ. |
| **FR15-B2** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L152): Giá bắt buộc và là số dương. Hệ thống nhận cả giá rỗng (`""`/bỏ trống) và chữ (`"abc"`), hiển thị thành `đ` hoặc `abc đ`. | **Chính xác.** Ảnh [FR15-B2.png](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR15-B2.png) minh họa trực quan lỗi hiển thị `đ` và `abc đ`. |
| **FR15-B3** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L151): *"Tên sản phẩm: bắt buộc, tối đa 255 ký tự"*. Hệ thống cho tạo và sửa tên dài `256` và `300` ký tự. | **Chính xác.** Khớp với các TC biên `FR15-BVA-03`, `06`, `FR15-EP-03`, `FR15-ERR-05`. |
| **FR15-B4** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L151) + Giả định `A3`: Tên sản phẩm bắt buộc. API nhận `name = ""`, và cả Web Admin lẫn API nhận `name = "   "`. | **Chính xác.** Đã phân biệt rõ trên Web `name = ""` bị HTML5 `required` chặn (Pass), chỉ Fail ở API và ở chuỗi toàn khoảng trắng `"   "`. |
| **FR15-B5** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L153): *"Danh mục: bắt buộc chọn danh mục hợp lệ"*. API `POST`/`PUT` nhận `category_id` thiếu, `99`, `0`, `"abc"`, `4`. | **Chính xác.** Ghi rõ phạm vi `Backend` (vì trên Web Admin dùng `<select>` cố định 3 danh mục). |
| **FR15-B6** | Minor | Giả định `A6`: `PUT`/`DELETE /api/products/:id` với `id` không tồn tại (`9999`, `0`, `abc`, hoặc xóa lặp lần 2) vẫn trả `200 OK` thay vì `404`. | **Chính xác.** Phân mức `Minor` và dẫn chiếu giả định `A6` rất chuẩn. |

---

#### C. FR-10 — Quản lý trạng thái đơn hàng (2 bugs: [FR-10_Trang_thai_don_hang.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-10_Trang_thai_don_hang.md#L401-L408))
| Mã bug | Mức độ | Căn cứ đặc tả / Giả định | Đánh giá |
|---|---|---|---|
| **FR10-B1** | Critical | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L123): *"delivered và canceled là trạng thái kết thúc (không chuyển tiếp được)"*. Đơn đã `canceled` vẫn hiện nút `"Đánh dấu Đã giao"` trên Web Admin và API cho chuyển sang `delivered` (mất cả thông tin `cancel_reason` trên UI). | **Chính xác.** Phá vỡ trực tiếp máy trạng thái đơn hàng (`Critical`). Ảnh [FR10-B1.png](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR10-B1.png) chụp rõ cả nút bấm lẫn trạng thái sau khi bấm. |
| **FR10-B2** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L125): *"Khi đơn hàng đã ở trạng thái shipping, User không được phép tự hủy"*. Trang `/profile` vẫn hiện nút `"Hủy đơn"` ở đơn `shipping` và `PUT /api/orders/:id/cancel` trả `200 OK`. | **Chính xác.** Vi phạm trực tiếp quy tắc phân quyền hủy đơn. Ảnh [FR10-B2.png](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR10-B2.png) rất rõ. |

---

#### D. Mobile — Đăng nhập (5 bugs: [Mobile_Dang_nhap.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/Mobile_Dang_nhap.md#L338-L348))
| Mã bug | Mức độ | Căn cứ đặc tả / Giả định | Đánh giá |
|---|---|---|---|
| **MOB-B1** | Critical | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L168-L176) (`FR-20`): Trên thiết bị có camera đục lỗ / status bar cao (`128 px` như Pixel 6), thanh header (`y = 37–108 px`) bị che khuất hoàn toàn, không bấm được nút `"Đăng nhập"`. | **Chính xác.** Lỗi đặc thù nền tảng Mobile rất đắt giá (`Critical`), ảnh [MOB-B1.png](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/MOB-B1.png) so sánh trực quan 2 chế độ cutout. |
| **MOB-B2** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L84): *"Sau 3 lần đăng nhập thất bại liên tiếp, tài khoản bị tạm khóa"*. Thực tế mỗi lần sai `login_attempts` tăng thêm 2, nên mới sai **2 lần** đã bị khóa (`403`). | **Chính xác.** Kết hợp kiểm tra giao diện Mobile và truy vấn DB (`login_attempts = 2, 4`) rất thuyết phục. |
| **MOB-B3** | Major | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L84): *"tạm khóa trong 30 giây"*. Thực tế `locked_until` bị cộng thêm **180 giây** (3 phút), nên ở giây thứ 31 đăng nhập lại vẫn bị khóa. | **Chính xác.** Khớp hoàn toàn với kiểm thử biên thời gian `MOB-BVA-02` (`t = 31s`). |
| **MOB-B4** | Minor | Giả định `A6`: Email đúng nhưng viết hoa (`TEST@eshop.com`) hoặc dư khoảng trắng đầu/cuối (`" test@eshop.com "`) bị từ chối `401` (rất dễ xảy ra do bàn phím Mobile tự viết hoa / tự thêm dấu cách). | **Chính xác.** Gắn kết tốt giữa giả định `A6` và hành vi thực tế của bàn phím ảo trên Mobile. |
| **MOB-B5** | Minor | [README.md](file:///home/npdinh/study/Homeworks/eshop-sut-main/README.md#L180) (`FR-21`): *"Toàn bộ giao diện dùng tiếng Việt"*. Màn hình Đăng nhập Mobile lại hiển thị nhãn `"Username"` (cho trường Email) và nút `"Sign In"`. | **Chính xác.** Xem thêm lưu ý nhỏ ở Mục 3 bên dưới để trả lời nếu giảng viên hỏi về phạm vi. |

---

### 2. Đối chiếu chéo với GitHub Issues của nhóm (`d1nhnguyen/eshop-sut`)

Mình đã kiểm tra trực tiếp danh sách Issues trên repo `d1nhnguyen/eshop-sut` (hiện có **14 issues**, từ `#1` đến `#14`):
- `#1`–`#3`: `[FR-03]` (Cập nhật hồ sơ) — `stardust65613`
- `#4`–`#6`: `[FR-08]` (Mã giảm giá) — `stardust65613`
- `#7`–`#8`: `[FR-14]` (Bộ lọc ngày Admin) — `stardust65613`
- `#9`: `[FR-20]` (Nhập mã giảm giá `SAVE10` trên Mobile) — `stardust65613`
- `#10`–`#14`: `[FR-04]` (Danh sách sản phẩm & Mã giảm giá) — `UngDuong125`

$\Rightarrow$ **Không có bất kỳ sự trùng lặp nào** với 22 bug thuộc `FR-01`, `FR-15`, `FR-10`, và `Mobile Đăng nhập` của bạn.
*(Lưu ý nhỏ: Trong [DOI_CHIEU_TRUOC_KHI_NOP.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/DOI_CHIEU_TRUOC_KHI_NOP.md#L29) đang ghi số thứ tự tiếp theo là `BUG-12` từ lúc nhóm mới có 11 issues; hiện tại `UngDuong125` đã tạo thêm đến `#14`, nên nếu bạn đăng tiếp lên GitHub thì sẽ bắt đầu từ **`BUG-15`**).*

---

### 3. Ba điểm lệch chữ nhỏ (Cosmetic) & Lưu ý khi bảo vệ

Khi đối chiếu từng chữ giữa **Bảng 5.3**, **Bảng Mục 7** của 4 báo cáo, **Bảng Tổng hợp** ([Bug_Report.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md#L11-L34)) và **Mục Chi tiết** ([Bug_Report.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md#L38-L601)), có 3 chỗ tiêu đề/dòng TC chênh nhau vài từ:

1. **`FR01-B8`** — Tiêu đề ở Bảng Tổng hợp ([dòng 20](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md#L20)) ghi:
   > `Email đăng ký được lưu kèm khoảng trắng đầu/cuối, không đăng nhập được bằng email bình thường`
   Trong khi tiêu đề Chi tiết ([dòng 218](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md#L218)) và [FR-01_Dang_ky.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L507) chỉ ghi:
   > `Email đăng ký được lưu kèm khoảng trắng đầu/cuối`
2. **`FR15-B6`** — Tiêu đề ở Bảng Tổng hợp ([dòng 27](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md#L27)) và [FR-15_Quan_ly_san_pham.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-15_Quan_ly_san_pham.md#L457) có cụm `"Product updated / deleted"`, còn tiêu đề Chi tiết ([dòng 393](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md#L393)) lược bỏ cụm này.
3. **`MOB-B2`** — Ở mục Chi tiết ([dòng 507](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md#L507) & [dòng 516](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md#L516)):
   - Tiêu đề thiếu chữ `ngay` so với Bảng Tổng hợp (`bị khóa sau lần sai thứ 2` vs `bị khóa ngay sau lần sai thứ 2`).
   - Dòng `TC phát hiện` ở mục Chi tiết có ghi thêm `; MOB-DT-05 Blocked` (`MOB-BVA-01, MOB-DT-04; MOB-DT-05 Blocked`), trong khi Bảng Tổng hợp và [Mobile_Dang_nhap.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/Mobile_Dang_nhap.md#L345) chỉ ghi `MOB-BVA-01, MOB-DT-04`.
4. **Mẹo bảo vệ cho `MOB-B5` (`"Username"` / `"Sign In"`)**:
   - Ở `FR-01` và `FR-15`, bạn có ghi chú các lỗi thuần giao diện `FR-21` (thiếu thẻ `<h1>`, màu nút Xóa, định dạng dấu chấm giá tiền) nằm ngoài phạm vi Domain Testing nên không lập mã bug.
   - Riêng ở Mobile, việc lập `MOB-B5` cho nhãn `"Username"` và `"Sign In"` là **hợp lý** vì nhãn `"Username"` gây hiểu nhầm trực tiếp về **miền dữ liệu đầu vào (input domain)** của trường đăng nhập (khiến người dùng tưởng nhập tên tài khoản thay vì địa chỉ `email` theo `FR-02`/`FR-20`).

Bạn có muốn mình đồng bộ luôn 3 tiêu đề/dòng TC trong [Bug_Report.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md) và cập nhật con số `BUG-12` $\rightarrow$ `BUG-15` trong [DOI_CHIEU_TRUOC_KHI_NOP.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/DOI_CHIEU_TRUOC_KHI_NOP.md) không?
````

<details><summary>Hành động AI đã thực hiện (23)</summary>

1. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md
2. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md
3. `read_file` — /home/npdinh/study/Homeworks/eshop-sut-main/README.md
4. `read_file` — /home/npdinh/study/Homeworks/eshop-sut-main/api_specification.md
5. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-15_Quan_ly_san_pham.md
6. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-10_Trang_thai_don_hang.md
7. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/report/Mobile_Dang_nhap.md
8. `run_command` — Verify screenshot files and paths in Bug_Report.md
9. `run_command` — Cross-check bug images and TC lists across all reports
10. `run_command` — Check existing GitHub issues on d1nhnguyen/eshop-sut
11. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR01-B1.png
12. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR15-B1.png
13. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR10-B1.png
14. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/MOB-B1.png
15. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR01-B6.png
16. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR10-B2.png
17. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/MOB-B2.png
18. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/MOB-B3.png
19. `run_command` — List files in bugs/screenshots/
20. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR15-B2.png
21. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/FR15-B6.png
22. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/MOB-B4.png
23. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/screenshots/MOB-B5.png

</details>

## #22 · 2026-10-21 06:22:38 · phiên `421e648d`

- **Công cụ AI:** Google Antigravity IDE, model `Gemini 4 Argon (Medium)`

**Prompt (nguyên văn):**

````text
các bug đó thật sự có trong code?
````

**Output AI (nguyên văn):**

````markdown
**Có, 100% cả 22 bug đều nằm thật trong mã nguồn của SUT** (thậm chí nhiều bug còn do giảng viên/tác giả đề bài cố tình cài vào kèm theo tên biến hoặc comment đánh dấu trong code).

Dưới đây là vị trí dòng code chính xác trong [`eshop-sut-main`](file:///home/npdinh/study/Homeworks/eshop-sut-main) cho từng bug:

---

### 1. Nhóm FR-01 — Đăng ký tài khoản (9/9 có trong code)

- **`FR01-B1` (Web từ chối `@ $ ! % * ? &`, chỉ nhận dấu cách `␣`)**:
  Tại [Register.jsx](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-web/src/pages/Register.jsx#L15-L20), tác giả đặt tên biến là `flawedStrongPasswordRegex` và dùng `\s` (khoảng trắng) thay vì ký tự đặc biệt:
  ```javascript
  const flawedStrongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\s)[A-Za-z\d\s]{8,}$/;
  ```
- **`FR01-B2` (Form Web thiếu ô "Xác nhận mật khẩu")**:
  Tại [Register.jsx](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-web/src/pages/Register.jsx#L34-L80), toàn bộ `<form>` chỉ có 3 `<input>` (`name`, `email`, `password`), hoàn toàn không có state hay ô nhập xác nhận mật khẩu.
- **`FR01-B3`, `FR01-B4`, `FR01-B5`, `FR01-B6`, `FR01-B8` (Backend không validate rỗng, định dạng email, độ mạnh mật khẩu, email trùng, khoảng trắng đầu/cuối)**:
  - Tại [server.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/server.js#L20-L30), API `POST /api/register` **không có bất kỳ dòng kiểm tra nào** mà `INSERT` thẳng `req.body` vào SQLite:
    ```javascript
    app.post("/api/register", (req, res) => {
      const { name, email, password } = req.body;
      db.run(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        [name, email, password],
        ...
    ```
  - Tại [database.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/database.js#L50-L61), cột `email TEXT` trong bảng `users` **không có ràng buộc `UNIQUE`** và không `NOT NULL`:
    ```sql
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT, ...
    ```
  - Khi đăng nhập ([server.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/server.js#L35)), `db.get("SELECT * FROM users WHERE email = ?", [email])` luôn lấy bản ghi đầu tiên khớp `email`, nên tài khoản đăng ký trùng thứ 2 (`FR01-B6`) không bao giờ đăng nhập được bằng mật khẩu mới.
- **`FR01-B7` (Ô Email trên Web dùng `type="text"` thay vì `type="email"`)**:
  Tại [Register.jsx](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-web/src/pages/Register.jsx#L46-L53):
  ```jsx
  <label className="block text-gray-700 mb-2">Email</label>
  <input
    type="text"
    value={email} ...
  ```
  *(Lưu ý nhỏ: Vì `type="text"` nên trình duyệt không kiểm tra cả ký tự `@`; trong [Bug_Report.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md#L194-L216) bạn đã mô tả đúng là `type="text"` không kiểm tra định dạng email).*
- **`FR01-B9` (Họ tên toàn khoảng trắng `"   "` vượt qua cả Web và Backend)**:
  Tại [Register.jsx](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-web/src/pages/Register.jsx#L37-L43), `<input type="text" required />` của HTML5 chỉ chặn chuỗi rỗng `""` chứ không chặn `"   "`, và `handleSubmit` không `.trim()` trước khi gửi lên [server.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/server.js#L20-L30).

---

### 2. Nhóm FR-15 — Quản lý sản phẩm – Admin (6/6 có trong code)

- **`FR15-B1`, `FR15-B2`, `FR15-B3`, `FR15-B4`, `FR15-B5` (Không kiểm tra `price <= 0`, `price` rỗng/chữ, `name > 255` ký tự, `name` rỗng/toàn khoảng trắng, `category_id` không tồn tại)**:
  - **Backend**: Tại [server.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/server.js#L167-L189), cả `POST /api/products` và `PUT /api/products/:id` đều `INSERT` / `UPDATE` thẳng không kiểm tra bất kỳ điều kiện nào:
    ```javascript
    app.post("/api/products", (req, res) => {
      const { name, price, description, imageUrl, category_id } = req.body;
      db.run(
        "INSERT INTO products (name, price, description, imageUrl, category_id) VALUES (?, ?, ?, ?, ?)",
        [name, price, description, imageUrl, category_id], ...
    ```
  - **Database**: Tại [database.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/database.js#L64-L71), bảng `products` dùng kiểu động của SQLite, không có `CHECK(price > 0)`, không giới hạn độ dài `name`, không khai báo `FOREIGN KEY (category_id)`.
  - **Web Admin**: Tại [frontend-admin/src/App.jsx](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-admin/src/App.jsx#L491-L508), ô `name` không có `maxLength`, không `.trim()`, còn ô `price` **không có cả `required` lẫn `min`**:
    ```jsx
    <input
      placeholder="Giá tiền"
      type="number"
      className="border p-2 rounded"
      value={productForm.price} ...
    />
    ```
- **`FR15-B6` (Sửa / Xóa `id` sản phẩm không tồn tại vẫn trả `200 OK`)**:
  Tại [server.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/server.js#L179-L196), cả `PUT /api/products/:id` và `DELETE /api/products/:id` đều không kiểm tra `this.changes === 0` mà trả thẳng `res.json({ message: "Product updated" })` / `res.json({ message: "Product deleted" })`.

---

### 3. Nhóm FR-10 — Quản lý trạng thái đơn hàng (2/2 có trong code)

- **`FR10-B1` (Đơn `canceled` chuyển tiếp được sang `delivered`)**:
  - **Backend** ([server.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/server.js#L550-L551)) cố tình mở cửa cho cạnh `canceled -> delivered`:
    ```javascript
    if (currentStatus === "canceled" && status === "delivered")
      isValidTransition = true;
    ```
  - **Web Admin** ([frontend-admin/src/App.jsx](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-admin/src/App.jsx#L862-L869)) cố tình vẽ nút màu xanh cho đơn đã hủy:
    ```jsx
    {o.status === "canceled" && (
      <button
        className="bg-green-500 text-white px-2 py-1 rounded text-xs"
        onClick={() => updateOrderStatus(o.id, "delivered")}
      >
        Đánh dấu Đã giao
      </button>
    )}
    ```
- **`FR10-B2` (User tự hủy được đơn đang ở trạng thái `shipping`)**:
  - **Backend** ([server.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/server.js#L328-L331)) thậm chí có sẵn comment tiếng Việt của tác giả đề bài:
    ```javascript
    // Lẽ ra phải là: if (order.status !== 'pending' && order.status !== 'confirmed')
    if (order.status === "delivered" || order.status === "canceled") {
      return res.status(400).json({ error: "Cannot cancel this order." });
    }
    ```
  - **Web Profile** ([Profile.jsx](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-web/src/pages/Profile.jsx#L199-L207)) cũng có comment cố tình:
    ```jsx
    {/* Nút hủy hiển thị khi chưa giao xong và chưa hủy (kể cả khi đang giao) */}
    {o.status !== "delivered" && o.status !== "canceled" && (
      <button onClick={() => cancelOrder(o.id)} ...>Hủy đơn</button>
    )}
    ```

---

### 4. Nhóm Mobile — Đăng nhập (5/5 có trong code)

- **`MOB-B1` (Header bị thanh StatusBar/camera cutout che khuất trên Android)**:
  Tại [frontend-mobile/App.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-mobile/App.js#L4,L443,L989), app dùng `SafeAreaView` của `react-native` (vốn chỉ tự động chèn top inset trên iOS, **bỏ qua trên Android**) thay vì `react-native-safe-area-context` và không cộng `StatusBar.currentHeight` vào `styles.safeArea` hay `styles.navBar`.
- **`MOB-B2` (Đăng nhập sai 2 lần đã bị khóa thay vì 3 lần)** & **`MOB-B3` (Khóa 180 giây thay vì 30 giây)**:
  Tại [server.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/server.js#L54-L58), mỗi lần sai mật khẩu code cộng `+ 2` vào `login_attempts` và khóa `180000` ms (`180` giây):
  ```javascript
  const newAttempts = user.login_attempts + 2;
  let lockedUntil = null;
  if (newAttempts >= 3) {
    lockedUntil = new Date(Date.now() + 180000).toISOString();
  }
  ```
- **`MOB-B4` (Email viết hoa hoặc dư khoảng trắng đầu/cuối bị báo `401`)**:
  - Trên Mobile ([frontend-mobile/App.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-mobile/App.js#L189-L193)): gửi nguyên `email` (`JSON.stringify({ email, password })`) không `.trim()` / `.toLowerCase()`.
  - Trên Backend ([server.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/backend/server.js#L35)): so sánh `WHERE email = ?` phân biệt chữ hoa/thường và khoảng trắng.
- **`MOB-B5` (Màn hình Đăng nhập Mobile dùng nhãn tiếng Anh `"Username"` và `"Sign In"`)**:
  Tại [frontend-mobile/App.js](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-mobile/App.js#L763-L784):
  ```jsx
  <Text style={styles.label}>Username</Text>
  <TextInput
    style={styles.textInput}
    placeholder="Email" ...
  />
  ...
  <TouchableOpacity style={styles.button} onPress={handleLogin}>
    <Text style={styles.buttonText}>Sign In</Text>
  </TouchableOpacity>
  ```

---

### Lưu ý duy nhất rất nhỏ trong báo cáo `FR-01` để bạn nắm rõ
Ở [FR-01_Dang_ky.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L483-L486) (Mục 5.4 — khảo sát bổ sung sau khi lách `FR01-B1`), có câu: *"Form chỉ kiểm tra có ký tự `@` hay không"*. Thực tế trong [Register.jsx](file:///home/npdinh/study/Homeworks/eshop-sut-main/frontend-web/src/pages/Register.jsx#L48), vì ô Email là `type="text"` nên form **không kiểm tra cả ký tự `@`** (như bạn đã ghi chính xác trong [Bug_Report.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md#L207-L212) ở bước tái hiện `FR01-B7` với email `fr01.b7example.com` không có `@` vẫn gửi đi được).

Bạn có muốn mình sửa lại câu mô tả ngắn ở Mục 5.4 của [FR-01_Dang_ky.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/report/FR-01_Dang_ky.md#L485) và 3 tiêu đề nhỏ trong [Bug_Report.md](file:///home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md) cho khớp tuyệt đối với code không?
````

<details><summary>Hành động AI đã thực hiện (11)</summary>

1. `run_command` — List SUT source code files
2. `read_file` — /home/npdinh/study/Homeworks/eshop-sut-main/backend/server.js
3. `read_file` — /home/npdinh/study/Homeworks/eshop-sut-main/backend/database.js
4. `read_file` — /home/npdinh/study/Homeworks/eshop-sut-main/frontend-web/src/pages/Register.jsx
5. `read_file` — /home/npdinh/study/Homeworks/eshop-sut-main/frontend-web/src/pages/Profile.jsx
6. `read_file` — /home/npdinh/study/Homeworks/eshop-sut-main/frontend-admin/src/App.jsx
7. `read_file` — /home/npdinh/study/Homeworks/eshop-sut-main/frontend-mobile/App.js
8. `read_file` — /home/npdinh/study/Homeworks/eshop-sut-main/frontend-admin/src/App.jsx
9. `read_file` — /home/npdinh/study/Homeworks/eshop-sut-main/frontend-mobile/App.js
10. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md
11. `read_file` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/bugs/Bug_Report.md

</details>

## #23 · 2026-10-21 06:29:51 · phiên `1946c20d`

- **Công cụ AI:** Claude Code 2.1.304 (VS Code extension), model `claude-opus-5-5`

**Prompt (nguyên văn):**

````text
1. đó là Antigravity, tôi dùng để kiểm tra chéo và đã thêm vào báo cáo.
2. bạn hãy tạo 22 issúe trên github theo đúng yêu cầu và điền lại báo cáo.
3. hãy gắn skills vào .claude/ và chỉ cần skill Yapply the domain testing andboundary value analysis techniques, ko cần skill ai-audit-log (có thể loại bỏ)
````

**Output AI (nguyên văn):**

````markdown
Skill đã chuyển xong. Giờ tôi chuẩn bị nội dung 22 issue để bạn dán vào.

Đã có bản nháp nội dung 22 issue. Tôi cập nhật danh sách đối chiếu, commit, rồi cập nhật prompt log.
````

**Sinh viên trả lời câu hỏi của AI:**

````text
The user answered: "Issue nên đứng tên tài khoản GitHub nào? (gh CLI trên máy đang đăng nhập npdinhx; tài khoản d1nhnguyen hiện chỉ có SSH, không gọi được API)"="d1nhnguyen", "Ảnh bug đính vào issue bằng cách nào? API của GitHub không cho upload file đính kèm (kiểu kéo-thả user-attachments như các bạn trong nhóm đang làm), nên ảnh phải nằm ở một nơi public rồi nhúng bằng link."="vậy phần này tôi sẽ tự tạo, làm các yêu cầu khác". Read the answers carefully — they may request clarification, changes, or that you not proceed — and follow what they actually say.
````

<details><summary>Hành động AI đã thực hiện (22)</summary>

1. `Bash` — Check tree status, Antigravity mentions, gh auth and SUT repo access
2. `Bash` — Show recent commits and existing issues on shared SUT repo
3. `Bash` — View format of existing issues on shared repo
4. `Bash` — Read brief requirements on GitHub issues and Agent Skills
5. `Bash` — Check which GitHub accounts SSH aliases and gh map to
6. `Bash` — Inspect Antigravity commit and current skills layout
7. `Bash` — Find references to skills paths and ai-audit-log
8. `Bash` — Move skill into .claude/skills, drop ai-audit-log, add symlink
9. `Bash` — Read domain-testing-bva SKILL.md for path references
10. `AskUserQuestion` — Issue nên đứng tên tài khoản GitHub nào? (gh CLI trên máy đang đăng nhập npdinhx; tài khoản d1nhnguyen hiện chỉ có SSH, không gọi được API) / Ảnh bug đính vào issue bằng cách nào? API của GitHub không cho upload file đính kèm (kiểu kéo-thả user-attachments như các bạn trong nhóm đang làm), nên ảnh phải nằm ở một nơi public rồi nhúng bằng link.
11. `Bash` — View lines referencing skills in docs
12. `Bash` — Update docs and SKILL.md for the new skill location
13. `Bash` — Verify report_lib sync and commit skill restructure
14. `Bash` — Inspect Bug_Report.md structure and a sample bug
15. `Bash` — View bug summary table, issue screenshot section, report section 7 headers
16. `Bash` — Check browser launch code, links, gitignore, group env notes
17. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/github_issues.py
18. `Write` — /home/npdinh/study/Homeworks/HW02/HW02_23120031/scripts/issue_shots.mjs
19. `Bash` — Generate issue drafts and dry-run the fill step
20. `Bash` — Fix summary regex and rerun draft and dry fill
21. `Bash` — Check status, ignore drafts folder, view issues checklist
22. `Bash` — Update checklist, commit issue scripts, regenerate prompt log

</details>
