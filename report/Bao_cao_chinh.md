# Báo cáo chính · HW02 – Domain Testing trên EShop · 23120031

Báo cáo gộp phần phương pháp và 4 báo cáo feature; mỗi feature gồm báo cáo Domain Testing (bước 1–3) và Boundary Value Analysis (bước 4), kết quả thực thi, AI gap analysis và bug. Bug chi tiết: `bugs/Bug_Report.md`; hồ sơ AI: thư mục `ai/`.

## Mục lục

1. Phương pháp áp dụng – Domain Testing & Boundary Value Analysis
2. FR-01 – Đăng ký tài khoản · Domain Testing & Boundary Value Analysis
3. FR-10 – Máy trạng thái đơn hàng · Domain Testing & Boundary Value Analysis
4. FR-15 – Quản lý sản phẩm (CRUD) · Domain Testing & Boundary Value Analysis
5. Mobile – Đăng nhập · Domain Testing & Boundary Value Analysis
6. Khai báo sử dụng AI (Mandatory Disclosure)

## Tổng hợp kết quả

Số feature: **4**. Số liệu lấy từ mục 5.4 của từng báo cáo (sinh tự động từ `evidence/<feature>/*_results.json`).

#### Theo test case (gộp các kênh)

Một test case **Fail** nếu Fail ở bất kỳ kênh nào; **Blocked** nếu kết quả bị một bug khác che (không kết luận được).

| Feature | Báo cáo | TC đã thiết kế | Đã chạy | Pass | Fail | Blocked | Chưa chạy | Số bug |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR-01 Đăng ký | [FR-01_Dang_ky.md](FR-01_Dang_ky.md) | 53 | 53 | 0 | 48 | 5 | 0 | 9 |
| FR-10 Máy trạng thái đơn hàng | [FR-10_Trang_thai_don_hang.md](FR-10_Trang_thai_don_hang.md) | 47 | 47 | 43 | 4 | 0 | 0 | 2 |
| FR-15 Quản lý sản phẩm | [FR-15_Quan_ly_san_pham.md](FR-15_Quan_ly_san_pham.md) | 61 | 61 | 23 | 38 | 0 | 0 | 6 |
| Mobile – Đăng nhập | [Mobile_Dang_nhap.md](Mobile_Dang_nhap.md) | 24 | 24 | 10 | 13 | 1 | 0 | 5 |
| **Tổng** | | **185** | **185** | **76** | **103** | **6** | **0** | **22** |

#### Theo lượt chạy (mỗi kênh một lượt)

| Feature | Kênh | Lượt chạy | Pass | Fail | Blocked | Không áp dụng |
| --- | --- | --- | --- | --- | --- | --- |
| FR-01 | Web, API | 101 | 36 | 50 | 15 | 5 |
| FR-10 | Web Admin / Web, API | 56 | 50 | 6 | 0 | 38 |
| FR-15 | Web Admin, API | 101 | 47 | 54 | 0 | 21 |
| Mobile – Đăng nhập | Mobile (Android Emulator), API | 48 | 20 | 26 | 2 | 0 |
| **Tổng** | | **306** | **153** | **136** | **17** | **64** |

"Không áp dụng": test case không có thao tác tương ứng trên kênh đó (vd giao diện không có nút chuyển trạng thái, API không có trường Xác nhận mật khẩu) – lý do ghi ở mục 5.3 từng báo cáo. FR-01 có thêm lượt **khảo sát** cho 15 test case Web bị Blocked (không tính verdict).

#### Bug

| Feature | Critical | Major | Minor | Tổng | Chi tiết |
| --- | --- | --- | --- | --- | --- |
| FR-01 | 2 | 4 | 3 | 9 | FR01-B1…FR01-B9 |
| FR-10 | 1 | 1 | 0 | 2 | FR10-B1…FR10-B2 |
| FR-15 | 0 | 5 | 1 | 6 | FR15-B1…FR15-B6 |
| Mobile – Đăng nhập | 1 | 2 | 2 | 5 | MOB-B1…MOB-B5 |
| **Tổng** | **4** | **12** | **6** | **22** | [bugs/Bug_Report.md](../bugs/Bug_Report.md) |

## Phương pháp áp dụng – Domain Testing & Boundary Value Analysis

Phần này mô tả cách bài làm áp dụng kỹ thuật theo tài liệu môn học; mọi feature (FR-01, FR-10, FR-15, Mobile – Đăng nhập) đều làm theo đúng các bước dưới đây.

### Tài liệu tham chiếu

| Ký hiệu | Tài liệu |
| --- | --- |
| [S04] | S04_Domain Testing.pdf – quy trình 4 bước, guideline lớp tương đương, BVA 9 điểm |
| [KB] | Refs/EN.DOMAIN TESTING.pdf (Cem Kaner & James Bach) – 4 quan niệm về "tương đương", best representative |
| [UC] | Refs/EN.DOMAIN TESTING - UC Analysis.pdf – ví dụ mẫu: Complete Set of Partitions, Minimum Set, Boundary Value Test Cases |
| [S07] | S07_Test Case.pdf, EN.Test_Cases_AI_First.pdf – cấu trúc test case, tiêu đề Action + Function + Condition |
| [DR] | Refs/How to write better testcases.pdf (Dianne Runnels) – step-by-step vs data matrix, 7 lỗi thường gặp |
| [TPL] | Templates/Test Cases – Test cases_Template_En.xlsx, Testcase Checklist.xlsx |

### Bước 1 – Xác định biến Input / Output [S04]

- Đọc đặc tả (README của SUT, `api_specification.md`) và giao diện thật (quan sát hộp đen: các trường nhập, kiểu trường) để liệt kê **biến đầu vào** và **biến đầu ra**.
- Biến đầu ra gồm cả kết quả thành công lẫn từng loại thông báo lỗi, vì [UC] phân vùng cả output (vd. "Insufficient Funds", "Invalid Input").
- Chỗ đặc tả không nói rõ được ghi thành **giả định** có mã (A1, A2…), mỗi test case phụ thuộc giả định sẽ dẫn chiếu mã đó.

### Bước 2 – Xác định lớp tương đương [S04], [KB]

Áp dụng 5 guideline:

| Loại điều kiện | Lớp valid | Lớp invalid |
| --- | --- | --- |
| Khoảng giá trị (vd 1–999) | 1 | 2 (dưới, trên) |
| Số lượng giá trị (vd 1–6 phần tử) | 1 | 2 (không có, quá nhiều) |
| Tập giá trị được xử lý khác nhau | mỗi giá trị 1 lớp | 1 (giá trị ngoài tập) |
| Điều kiện "phải là" | 1 | 1 |
| Có lý do tin rằng các phần tử trong lớp được xử lý khác nhau | tách lớp | tách lớp |

- Ngoài ràng buộc nghiệp vụ, mỗi biến có thêm các lớp về **kiểu** (sai kiểu dữ liệu, rỗng, chỉ có khoảng trắng) như cách [UC] thêm "alphabetic string", "three decimal places".
- Kết quả trình bày thành bảng **Complete Set of Partitions** [UC]: mỗi lớp có mã EC, biến, điều kiện, Valid / Invalid.

### Bước 3 – Chọn test case [S04], [UC]

- Mỗi lớp chọn một **best representative** [KB]: giá trị có khả năng lộ lỗi cao nhất trong lớp.
- **Minimum Set**: test case valid phủ càng nhiều lớp valid càng tốt; mỗi test case invalid phủ **đúng một** lớp invalid (các biến còn lại giữ giá trị valid) để khi fail biết ngay nguyên nhân.
- Bảng **phủ phân vùng** chỉ ra mỗi EC được test case nào phủ, chứng minh 100% lớp được phủ.

### Bước 4 – Boundary Value Analysis [S04], [UC]

- Áp dụng cho biến có thứ tự (độ dài chuỗi, số tiền, số lần, thời gian, thứ tự trạng thái…).
- Mỗi phân vùng xét tối đa 9 điểm: giá trị đại diện, LB-1, LB, LB+1, UB-1, UB, UB+1, giá trị nhỏ nhất và lớn nhất nhập được qua UI/API.
- Bước nhảy giữa các điểm bằng độ chính xác nhỏ nhất của biến (1 ký tự, 1 đơn vị, 0.01…), như [UC] dùng 0.01 vì hệ thống xử lý 2 chữ số thập phân.
- Cột **Partition tested** ghi biên giữa hai phân vùng dạng `EC3/EC4`.

### Định dạng test case [S07], [DR], [TPL]

- ID có tiền tố feature (`FR01-DT-01`, `FR01-BV-01`…) như `TC-LOGIN-003` [S07] và `01 - 001` [TPL], để không trùng khi gộp 4 feature.
- Tiêu đề theo cú pháp **Action + Function + Condition**, ví dụ "Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ hoa".
- Mỗi ô dữ liệu là giá trị cụ thể, mỗi kết quả mong đợi viết tường minh kèm mã lớp đầu ra (vd EC41) – không ghi "mặc định" hay "như TC khác" (Repeatable, Self-standing [S07]).
- Với form nhập liệu, mọi test case có cùng thủ tục, chỉ dữ liệu thay đổi → dùng dạng **data matrix** [DR]: mỗi feature có một thủ tục step-by-step (Precondition + Steps) cho từng kênh (Web UI, API), mỗi dòng của ma trận là một test case có ID, tiêu đề, dữ liệu và kết quả mong đợi kiểm chứng được.
- Kết quả thực thi ghi theo mẫu [TPL]: Actual Result, Status (Pass / Fail / Blocked), Tester, Tested Date, Bug ID.
- Tự rà soát bằng *Testcase Checklist* [TPL] (Accurate, Economical, Repeatable, Traceable, Appropriate, Self standing, Self cleaning; ≤ 15 bước; matrix chạy ≤ 20 phút).

### Kênh kiểm thử

- Mỗi test case được thực thi trên giao diện người dùng (Web / Web Admin / Mobile) và, khi có API tương ứng, gọi trực tiếp API để kiểm tra phía server có tự kiểm tra dữ liệu hay chỉ dựa vào kiểm tra phía client.
- Dữ liệu được reset bằng cách khởi động lại backend trước mỗi phiên thực thi (Self cleaning).

### Vai trò của AI

- Mỗi bước được thực hiện với Claude Code theo đúng thứ tự trên (không dùng một prompt "sinh test case" duy nhất).
- Sau khi hoàn thành phiên bản đầu của FR-01, sinh viên dùng công cụ AI thứ hai là **Google Antigravity (Gemini 4 Argon)** để rà soát chéo độc lập theo tiêu chí bảng (data matrix), cách đặt tên TC và mức độ chi tiết (lượt #13 trong `ai/prompt_log.md`), rồi duyệt và áp dụng mẫu chuẩn hoá đó cho cả 4 feature.
- Output AI của mỗi bước là một commit riêng `[<FR>][B<n>]`; phần rà soát, sửa và bổ sung là commit tiếp theo `[<FR>][B<n>-review]`, nên `git diff` giữa hai commit chính là bằng chứng chỉnh sửa cho AI Audit Report và AI gap analysis.

## FR-01 – Đăng ký tài khoản · Domain Testing & Boundary Value Analysis

| Mục | Giá trị |
| --- | --- |
| Feature | FR-01 – Đăng ký tài khoản (Pool A) |
| Kênh kiểm thử | Web khách hàng (`/register`, http://localhost:5173) + API `POST /api/register` |
| Người thực hiện | 23120031 |
| Công cụ AI | Claude Code (VS Code extension) · Google Antigravity (Gemini 4 Argon – rà soát chéo) |
| Kỹ thuật | Domain Testing (S04 – bước 1–3), Boundary Value Analysis (S04 – bước 4) |

### 0. Đặc tả (trích nguyên văn README của SUT)

> ### FR-01: Đăng ký tài khoản
>
> - Người dùng phải cung cấp: **Họ Tên**, **Email**, **Mật khẩu**.
> - Email phải có định dạng hợp lệ (`user@domain.com`) và là duy nhất trong hệ thống.
> - **Yêu cầu mật khẩu mạnh**: Tối thiểu 8 ký tự, có ít nhất 1 chữ hoa, 1 chữ thường, 1 chữ số và 1 ký tự đặc biệt (`@`, `$`, `!`, `%`, `*`, `?`, `&`).
> - Phải có trường **Xác nhận mật khẩu** — hệ thống từ chối nếu hai trường không khớp.
> - Sau khi đăng ký thành công, người dùng được chuyển tới trang Đăng nhập.

### 1. Bước 1 – Xác định biến Input / Output

#### 1.1 Quan sát giao diện (hộp đen)

Trang `http://localhost:5173/register` (ảnh: `evidence/FR-01/B1_form_dang_ky.png`):

| Thành phần | Quan sát |
| --- | --- |
| Ô "Họ Tên" | `type="text"`, có thuộc tính `required`, không giới hạn độ dài |
| Ô "Email" | `type="text"` (không phải `type="email"`), `required`, không giới hạn độ dài |
| Ô "Mật khẩu" | `type="password"` (ký tự bị che), `required`, không giới hạn độ dài; dòng gợi ý "Yêu cầu: Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt." |
| Ô "Xác nhận mật khẩu" | **Không có** trên giao diện |
| Nút "Đăng Ký" | nút submit của form |
| Link "Đăng nhập" | chuyển tới `/login` |

API tương ứng (`api_specification.md` mục 1.1): `POST /api/register`, body `{"name", "email", "password"}`, phản hồi thành công `200 {"message": "User registered successfully", "id": <id>}`. API không có trường xác nhận mật khẩu.

#### 1.2 Biến đầu vào

| ID | Biến | Kênh nhập | Kiểu / miền giá trị | Ràng buộc theo đặc tả | Nguồn |
| --- | --- | --- | --- | --- | --- |
| I1 | Họ Tên | Web: ô "Họ Tên"; API: `name` | chuỗi ký tự | Bắt buộc | FR-01 ("phải cung cấp Họ Tên") |
| I2 | Email | Web: ô "Email"; API: `email` | chuỗi ký tự | Bắt buộc; đúng định dạng `user@domain.com`; duy nhất trong hệ thống | FR-01; FR-22 (ô email dùng `type="email"`) |
| I3 | Mật khẩu | Web: ô "Mật khẩu"; API: `password` | chuỗi ký tự | Bắt buộc; ≥ 8 ký tự; có ≥ 1 chữ hoa, ≥ 1 chữ thường, ≥ 1 chữ số, ≥ 1 ký tự đặc biệt thuộc `@ $ ! % * ? &` | FR-01; FR-22 (ô mật khẩu dùng `type="password"`) |
| I4 | Xác nhận mật khẩu | Web: ô "Xác nhận mật khẩu" (theo đặc tả) | chuỗi ký tự | Phải khớp với I3, nếu không hệ thống từ chối | FR-01 |
| I5 | Trạng thái email trong hệ thống | Tiền điều kiện (dữ liệu đã có) | {chưa tồn tại, đã tồn tại} | Email phải là duy nhất | FR-01 |

Biến I3 là chuỗi nhưng ràng buộc của nó đo trên 5 đại lượng có thứ tự, nên khi phân vùng (bước 2) và phân tích biên (bước 4) sẽ xét riêng từng đại lượng:

| ID | Đại lượng dẫn xuất của I3 | Miền | Ràng buộc |
| --- | --- | --- | --- |
| I3.L | Độ dài mật khẩu | 0, 1, 2, … | ≥ 8 |
| I3.U | Số chữ hoa (A–Z) | 0, 1, 2, … | ≥ 1 |
| I3.W | Số chữ thường (a–z) | 0, 1, 2, … | ≥ 1 |
| I3.D | Số chữ số (0–9) | 0, 1, 2, … | ≥ 1 |
| I3.S | Số ký tự thuộc tập `@ $ ! % * ? &` | 0, 1, 2, … | ≥ 1 |

#### 1.3 Biến đầu ra

| ID | Biến | Giá trị có thể có | Nguồn |
| --- | --- | --- | --- |
| O1 | Kết quả đăng ký | (a) Thành công: tài khoản được tạo và người dùng được chuyển tới trang Đăng nhập; (b) Bị từ chối: không tạo tài khoản, ở lại trang Đăng ký | FR-01 |
| O2 | Thông báo lỗi | thiếu trường bắt buộc / email sai định dạng / email đã tồn tại / mật khẩu không đủ mạnh / xác nhận mật khẩu không khớp | FR-01 (nội dung câu chữ không được quy định) |
| O3 | Phản hồi API | `200` + `{"message": "User registered successfully", "id"}` khi thành công; mã lỗi kèm thông báo khi bị từ chối | `api_specification.md` 1.1; giả định A7 |
| O4 | Trạng thái dữ liệu | tài khoản mới tồn tại / không tồn tại; kiểm chứng bằng cách đăng nhập (`POST /api/login`) với email + mật khẩu vừa dùng | FR-01, FR-02 |

#### 1.4 Giả định cho những chỗ đặc tả chưa rõ

| ID | Giả định | Căn cứ |
| --- | --- | --- |
| A1 | Chỉ 7 ký tự `@ $ ! % * ? &` được tính là "ký tự đặc biệt". Ký tự đặc biệt khác (`#`, `^`, `-`, `_`, khoảng trắng…) không làm thỏa điều kiện, nhưng cũng không bị cấm khi mật khẩu đã đủ 4 loại ký tự. | Đặc tả liệt kê tập ký tự trong ngoặc; không có câu nào cấm ký tự khác |
| A2 | Email hợp lệ có dạng `local@domain.tld`: đúng một `@`, phần local không rỗng, phần domain có ít nhất một dấu `.` và không bắt đầu / kết thúc bằng `.` | Ví dụ định dạng `user@domain.com` của đặc tả |
| A3 | Hai email chỉ khác nhau ở chữ hoa / chữ thường được coi là trùng | Hệ thống email thực tế không phân biệt hoa thường; phần domain không phân biệt hoa thường theo RFC 5321 |
| A4 | Khoảng trắng ở đầu / cuối email được bỏ đi trước khi kiểm tra; Họ Tên chỉ gồm khoảng trắng được coi như bỏ trống | Thuật toán làm sạch giá trị của `type="email"` (HTML5) mà FR-22 yêu cầu; "phải cung cấp Họ Tên" |
| A5 | Đặc tả không giới hạn độ dài tối đa của Họ Tên, Email, Mật khẩu → giá trị dài (vd 255–256 ký tự) phải được chấp nhận bình thường, không gây lỗi hệ thống | FR-01 không nêu giới hạn trên |
| A6 | Họ Tên chứa chữ có dấu tiếng Việt, chữ số hoặc ký tự đặc biệt đều hợp lệ | FR-01 chỉ yêu cầu bắt buộc |
| A7 | Khi từ chối: không tạo tài khoản, ở lại trang Đăng ký, có thông báo lỗi chỉ đúng lý do; API trả mã lỗi 4xx kèm thông báo | Đặc tả không quy định câu chữ / mã lỗi; quy ước REST |
| A8 | "Xác nhận mật khẩu" là yêu cầu của giao diện; các lớp của biến I4 chỉ thực thi trên kênh Web | `api_specification.md` 1.1 không có trường này |
| A9 | Kiểm tra trùng email áp dụng cho mọi tài khoản đã có, kể cả tài khoản seed `admin@eshop.com`, `test@eshop.com` | FR-01 "duy nhất trong hệ thống" |
| A10 | "Chữ hoa" / "chữ thường" là chữ cái Latin không dấu `A–Z` / `a–z`. Chữ có dấu (`Đ`, `Ă`, `ê`…) không làm thỏa điều kiện chữ hoa / chữ thường, nhưng không bị cấm khi mật khẩu đã đủ 4 loại (giống A1) | Đặc tả không nói rõ; cách hiểu thông dụng của quy tắc mật khẩu; đã dùng khi định nghĩa I3.U, I3.W. Cần TA xác nhận |

#### 1.5 Ngoài phạm vi

- Yêu cầu giao diện chung (màu nút, thẻ `<h1>`, dấu `*` cạnh nhãn, vị trí thông báo lỗi – FR-21, FR-22) và lưu trữ mật khẩu (SEC-01): không phải miền dữ liệu đầu vào của FR-01.
- Đăng ký trên Mobile: thuộc Pool D, không nằm trong feature này.

### 2. Bước 2 – Lớp tương đương (Complete Set of Partitions)

#### 2.1 Cách áp dụng guideline cho từng biến

| Biến | Điều kiện trong đặc tả | Guideline [S04] | Lớp tạo ra |
| --- | --- | --- | --- |
| I1 Họ Tên | "phải cung cấp" | "Phải là" → 1 valid + 1 invalid | có giá trị / rỗng |
| | | Tách lớp (G5): chuỗi chỉ có khoảng trắng có thể lọt qua kiểm tra "không rỗng"; chữ có dấu có thể bị xử lý khác do mã hóa Unicode | thêm "chỉ khoảng trắng" (invalid), "có dấu tiếng Việt" (valid) |
| I2 Email | "phải cung cấp" | "Phải là" | rỗng (invalid) |
| | "định dạng hợp lệ `user@domain.com`" | "Phải là" + tách lớp (G5): mỗi kiểu sai định dạng có thể bị một phép kiểm tra khác nhau bắt (hoặc bỏ sót) | 6 lớp sai định dạng; khoảng trắng đầu/cuối là valid theo A4 |
| | "duy nhất trong hệ thống" | Tập giá trị {chưa tồn tại, đã tồn tại} + tách lớp (G5): so sánh trùng có thể phân biệt hoa/thường | chưa tồn tại (valid), trùng chính xác, trùng khác hoa/thường (invalid) |
| I3 Mật khẩu | "phải cung cấp" | "Phải là" + tách lớp (G5): rỗng thường bị kiểm tra "bắt buộc" bắt trước kiểm tra độ dài | rỗng (invalid) |
| | "tối thiểu 8 ký tự" | Khoảng giá trị chỉ có cận dưới → 1 valid + 1 invalid (không có lớp "quá dài" theo A5) | L ≥ 8 / 1 ≤ L ≤ 7 |
| | "ít nhất 1 chữ hoa / 1 chữ thường / 1 chữ số" | "Phải là" cho từng loại → 1 valid + 1 invalid mỗi loại | có / không có |
| | "ít nhất 1 ký tự đặc biệt (`@ $ ! % * ? &`)" | "Phải là" + tách lớp (G5): ký tự đặc biệt ngoài tập có thể bị tính nhầm (A1) | có ký tự thuộc tập (valid); không có ký tự đặc biệt nào, chỉ có ký tự ngoài tập (invalid) |
| | Tập 7 ký tự `@ $ ! % * ? &` | Tập giá trị được xử lý khác nhau → mỗi giá trị 1 lớp valid: `$ * ? !` là ký tự đặc biệt trong biểu thức chính quy, `&` trong HTML/URL, `%` trong mã hóa URL | 7 lớp, mỗi lớp là mật khẩu có **duy nhất** ký tự đặc biệt đó |
| | Ký tự khác ngoài 4 loại | Theo A1 không bị cấm | đủ 4 loại + có thêm ký tự ngoài tập (valid) |
| I4 Xác nhận mật khẩu | "phải khớp" | "Phải là" + tách lớp (G5): so sánh có thể bỏ qua hoa/thường; ô bỏ trống có thể được xử lý như "không nhập" | khớp (valid); bỏ trống, khác, khác chỉ ở hoa/thường (invalid) |
| Đầu ra O1–O3 | thành công / từng loại lỗi | Phân vùng đầu ra như ví dụ [UC] | 1 lớp thành công + 5 lớp từ chối |

#### 2.2 Complete Set of Partitions

| EC | Biến | Phân vùng | Ví dụ đại diện | Valid / Invalid |
| --- | --- | --- | --- | --- |
| EC1 | I1 Họ Tên | Có ít nhất 1 ký tự không phải khoảng trắng, chữ Latin không dấu | `Nguyen Van A` | Valid |
| EC2 | I1 Họ Tên | Có chữ tiếng Việt có dấu (A6) | `Nguyễn Thị Ánh` | Valid |
| EC3 | I1 Họ Tên | Rỗng | `` | Invalid |
| EC4 | I1 Họ Tên | Chỉ gồm khoảng trắng (A4) | `   ` | Invalid |
| EC5 | I2 Email | Đúng định dạng `local@domain.tld` (A2) | `an.nguyen@gmail.com` | Valid |
| EC6 | I2 Email | Đúng định dạng nhưng có khoảng trắng đầu / cuối (A4) | ` an.nguyen@gmail.com ` | Valid |
| EC7 | I2 Email | Rỗng | `` | Invalid |
| EC8 | I2 Email | Thiếu `@` | `an.nguyengmail.com` | Invalid |
| EC9 | I2 Email | Thiếu phần local trước `@` | `@gmail.com` | Invalid |
| EC10 | I2 Email | Thiếu phần domain sau `@` | `an.nguyen@` | Invalid |
| EC11 | I2 Email | Domain không có dấu `.` (thiếu TLD) (A2) | `an.nguyen@gmail` | Invalid |
| EC12 | I2 Email | Có nhiều hơn một `@` | `an@nguyen@gmail.com` | Invalid |
| EC13 | I2 Email | Có khoảng trắng ở giữa | `an nguyen@gmail.com` | Invalid |
| EC14 | I2 / I5 | Email chưa tồn tại trong hệ thống | email mới | Valid |
| EC15 | I2 / I5 | Email đã tồn tại (trùng chính xác) (A9) | `test@eshop.com` | Invalid |
| EC16 | I2 / I5 | Email trùng nhưng khác chữ hoa / thường (A3) | `TEST@eshop.com` | Invalid |
| EC17 | I3 Mật khẩu | Rỗng | `` | Invalid |
| EC18 | I3.L | Độ dài ≥ 8 | `Abcdef1@` (8) | Valid |
| EC19 | I3.L | Độ dài 1–7 | `Abcd1@` (6) | Invalid |
| EC20 | I3.U | Có ≥ 1 chữ hoa | `Abcdef1@` | Valid |
| EC21 | I3.U | Không có chữ hoa | `abcdef1@` | Invalid |
| EC22 | I3.W | Có ≥ 1 chữ thường | `Abcdef1@` | Valid |
| EC23 | I3.W | Không có chữ thường | `ABCDEF1@` | Invalid |
| EC24 | I3.D | Có ≥ 1 chữ số | `Abcdef1@` | Valid |
| EC25 | I3.D | Không có chữ số | `Abcdefg@` | Invalid |
| EC26 | I3.S | Có ≥ 1 ký tự thuộc tập `@ $ ! % * ? &` | `Abcdef1@` | Valid |
| EC27 | I3.S | Không có ký tự đặc biệt nào | `Abcdefg1` | Invalid |
| EC28 | I3.S | Chỉ có ký tự đặc biệt ngoài tập (A1) | `Abcdef1#` | Invalid |
| EC29 | I3.S | Ký tự đặc biệt duy nhất là `@` | `Abcdef1@` | Valid |
| EC30 | I3.S | Ký tự đặc biệt duy nhất là `$` | `Abcdef1$` | Valid |
| EC31 | I3.S | Ký tự đặc biệt duy nhất là `!` | `Abcdef1!` | Valid |
| EC32 | I3.S | Ký tự đặc biệt duy nhất là `%` | `Abcdef1%` | Valid |
| EC33 | I3.S | Ký tự đặc biệt duy nhất là `*` | `Abcdef1*` | Valid |
| EC34 | I3.S | Ký tự đặc biệt duy nhất là `?` | `Abcdef1?` | Valid |
| EC35 | I3.S | Ký tự đặc biệt duy nhất là `&` | `Abcdef1&` | Valid |
| EC36 | I3 | Đủ 4 loại và có thêm ký tự ngoài tập (A1) | `Abc#def 1@` | Valid |
| EC37 | I4 Xác nhận | Khớp với mật khẩu | giống I3 | Valid |
| EC38 | I4 Xác nhận | Bỏ trống | `` | Invalid |
| EC39 | I4 Xác nhận | Khác mật khẩu | `Abcdef2@` khi I3 = `Abcdef1@` | Invalid |
| EC40 | I4 Xác nhận | Chỉ khác mật khẩu ở chữ hoa / thường | `abcdef1@` khi I3 = `Abcdef1@` | Invalid |
| EC41 | O1–O3 | Đăng ký thành công: tạo tài khoản, chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng tài khoản mới | | Output |
| EC42 | O1–O3 | Từ chối – thiếu trường bắt buộc | | Output |
| EC43 | O1–O3 | Từ chối – email sai định dạng | | Output |
| EC44 | O1–O3 | Từ chối – email đã tồn tại | | Output |
| EC45 | O1–O3 | Từ chối – mật khẩu không đủ mạnh | | Output |
| EC46 | O1–O3 | Từ chối – xác nhận mật khẩu không khớp | | Output |

Tổng: 40 lớp đầu vào (19 valid, 21 invalid) và 6 lớp đầu ra.

### 3. Bước 3 – Test case Domain Testing

#### 3.1 Thủ tục thực hiện

Mọi test case dùng chung thủ tục, chỉ dữ liệu thay đổi, nên được viết dạng **data matrix** [DR]: thủ tục dưới đây + mỗi dòng ở mục 3.2, 4.2, 6.2 là một test case với dữ liệu cụ thể. ID test case có tiền tố feature: `FR01-DT-nn` (Domain Testing), `FR01-BV-nn` (BVA) để không trùng khi gộp báo cáo 4 feature.

**Tiền điều kiện chung**

- Backend `http://localhost:3000` vừa được khởi động lại (dữ liệu seed, có sẵn `test@eshop.com / Test1234!`, `admin@eshop.com / Admin123!`).
- Web `http://localhost:5173` đang chạy; Chrome, chưa đăng nhập.
- Email trong mỗi test case là duy nhất (dạng `fr01.dt01@example.com`) để các test case độc lập nhau, trừ các test case email trùng.

**P-WEB – Thực hiện trên giao diện Web**

| Bước | Hành động | Kết quả mong đợi của bước |
| --- | --- | --- |
| 1 | Mở `http://localhost:5173/register` | Trang "Đăng Ký Tài Khoản" hiện các ô Họ Tên, Email, Mật khẩu, Xác nhận mật khẩu và nút "Đăng Ký" |
| 2 | Nhập Họ Tên, Email, Mật khẩu theo cột dữ liệu | Giá trị hiện đúng như nhập; ô Mật khẩu che ký tự |
| 3 | Nhập Xác nhận mật khẩu theo cột dữ liệu | Ô che ký tự |
| 4 | Bấm "Đăng Ký" | Như cột Kết quả mong đợi |
| 5 | Kiểm chứng tài khoản: gửi `POST /api/login` với Email (đã bỏ khoảng trắng đầu/cuối) + Mật khẩu của test case | Có token nếu mong đợi đăng ký thành công; bị từ chối nếu mong đợi đăng ký bị từ chối |

**P-API – Thực hiện trên API**

| Bước | Hành động | Kết quả mong đợi của bước |
| --- | --- | --- |
| 1 | Gửi `POST http://localhost:3000/api/register`, `Content-Type: application/json`, body `{"name": <Họ Tên>, "email": <Email>, "password": <Mật khẩu>}` | Như cột Kết quả mong đợi: `200` + `{"message": "User registered successfully", "id"}` khi hợp lệ, mã 4xx + thông báo lỗi khi không hợp lệ (A7) |
| 2 | Kiểm chứng tài khoản như bước 5 của P-WEB | như trên |

Test case thuộc biến Xác nhận mật khẩu (I4) chỉ chạy P-WEB (A8). Trong bảng dữ liệu: `␣` là một dấu cách; `(rỗng)` là để trống ô; chuỗi dài ghi bằng công thức Python cho đúng từng ký tự (vd `"A" * 1000`).

**Hậu điều kiện (self cleaning):** khởi động lại backend sau phiên thực thi để xóa các tài khoản đã tạo.

#### 3.2 Minimum Set of Test Cases

Dữ liệu và kết quả mong đợi được sinh từ `scripts/fr01/cases.py` (cùng nguồn với script thực thi) bằng `scripts/fr01/report_tables.py`.

<!-- BEGIN:T32 -->
**Test case valid** – mỗi test case phủ nhiều lớp valid nhất có thể:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Họ Tên | Email | Mật khẩu | Xác nhận | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR01-DT-01 | Kiểm tra đăng ký thành công với dữ liệu hợp lệ điển hình | EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC29, EC37, EC41 | `Nguyen␣Van␣A` | `fr01.dt01@example.com` | `Abcdef1@` | `Abcdef1@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-DT-02 | Kiểm tra đăng ký thành công khi Họ Tên có dấu, Email có khoảng trắng đầu/cuối và Mật khẩu đủ 4 loại kèm thêm ký tự ngoài tập | EC2, EC6, EC14, EC18, EC20, EC22, EC24, EC26, EC30, EC36, EC37, EC41 | `Nguyễn␣Thị␣Ánh` | `␣fr01.dt02@example.com␣` | `Abc#def1$` | `Abc#def1$` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41); email được lưu là `fr01.dt02@example.com` (A4) | Web, API | AI-sửa |
| FR01-DT-03 | Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất của Mật khẩu là `!` | EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC31, EC37, EC41 | `Nguyen␣Van␣A` | `fr01.dt03@example.com` | `Abcdef1!` | `Abcdef1!` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-DT-04 | Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất của Mật khẩu là `%` | EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC32, EC37, EC41 | `Nguyen␣Van␣A` | `fr01.dt04@example.com` | `Abcdef1%` | `Abcdef1%` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-DT-05 | Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất của Mật khẩu là `*` | EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC33, EC37, EC41 | `Nguyen␣Van␣A` | `fr01.dt05@example.com` | `Abcdef1*` | `Abcdef1*` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-DT-06 | Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất của Mật khẩu là `?` | EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC34, EC37, EC41 | `Nguyen␣Van␣A` | `fr01.dt06@example.com` | `Abcdef1?` | `Abcdef1?` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-DT-07 | Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất của Mật khẩu là `&` | EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC35, EC37, EC41 | `Nguyen␣Van␣A` | `fr01.dt07@example.com` | `Abcdef1&` | `Abcdef1&` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |

**Test case invalid** – mỗi test case phủ đúng một lớp invalid, các biến còn lại hợp lệ:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Họ Tên | Email | Mật khẩu | Xác nhận | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR01-DT-08 | Kiểm tra đăng ký bị từ chối khi bỏ trống Họ Tên | EC3, EC42 | (rỗng) | `fr01.dt08@example.com` | `Abcdef1@` | `Abcdef1@` | Từ chối, báo thiếu Họ Tên; không tạo tài khoản; API trả 4xx (EC42) | Web, API | AI |
| FR01-DT-09 | Kiểm tra đăng ký bị từ chối khi Họ Tên chỉ gồm khoảng trắng | EC4, EC42 | `␣␣␣` | `fr01.dt09@example.com` | `Abcdef1@` | `Abcdef1@` | Từ chối, báo thiếu Họ Tên; không tạo tài khoản; API trả 4xx (EC42); A4 | Web, API | AI |
| FR01-DT-10 | Kiểm tra đăng ký bị từ chối khi bỏ trống Email | EC7, EC42 | `Nguyen␣Van␣A` | (rỗng) | `Abcdef1@` | `Abcdef1@` | Từ chối, báo thiếu Email; không tạo tài khoản; API trả 4xx (EC42) | Web, API | AI |
| FR01-DT-11 | Kiểm tra đăng ký bị từ chối khi Email thiếu ký tự `@` | EC8, EC43 | `Nguyen␣Van␣A` | `fr01.dt11example.com` | `Abcdef1@` | `Abcdef1@` | Từ chối, báo email sai định dạng; không tạo tài khoản; API trả 4xx (EC43) | Web, API | AI |
| FR01-DT-12 | Kiểm tra đăng ký bị từ chối khi Email thiếu phần trước `@` | EC9, EC43 | `Nguyen␣Van␣A` | `@example.com` | `Abcdef1@` | `Abcdef1@` | Từ chối, báo email sai định dạng; không tạo tài khoản; API trả 4xx (EC43) | Web, API | AI |
| FR01-DT-13 | Kiểm tra đăng ký bị từ chối khi Email thiếu phần domain sau `@` | EC10, EC43 | `Nguyen␣Van␣A` | `fr01.dt13@` | `Abcdef1@` | `Abcdef1@` | Từ chối, báo email sai định dạng; không tạo tài khoản; API trả 4xx (EC43) | Web, API | AI |
| FR01-DT-14 | Kiểm tra đăng ký bị từ chối khi domain của Email không có dấu `.` | EC11, EC43 | `Nguyen␣Van␣A` | `fr01.dt14@example` | `Abcdef1@` | `Abcdef1@` | Từ chối, báo email sai định dạng; không tạo tài khoản; API trả 4xx (EC43); A2 | Web, API | AI |
| FR01-DT-15 | Kiểm tra đăng ký bị từ chối khi Email có hai ký tự `@` | EC12, EC43 | `Nguyen␣Van␣A` | `fr01@dt15@example.com` | `Abcdef1@` | `Abcdef1@` | Từ chối, báo email sai định dạng; không tạo tài khoản; API trả 4xx (EC43) | Web, API | AI |
| FR01-DT-16 | Kiểm tra đăng ký bị từ chối khi Email có khoảng trắng ở giữa | EC13, EC43 | `Nguyen␣Van␣A` | `fr01␣dt16@example.com` | `Abcdef1@` | `Abcdef1@` | Từ chối, báo email sai định dạng; không tạo tài khoản; API trả 4xx (EC43) | Web, API | AI |
| FR01-DT-17 | Kiểm tra đăng ký bị từ chối khi Email đã tồn tại | EC15, EC44 | `Nguyen␣Van␣A` | `test@eshop.com` | `Newpass1@` | `Newpass1@` | Từ chối, báo email đã tồn tại; không tạo tài khoản; API trả 4xx; `test@eshop.com / Test1234!` vẫn đăng nhập được (EC44) | Web, API | AI |
| FR01-DT-18 | Kiểm tra đăng ký bị từ chối khi Email trùng tài khoản có sẵn nhưng khác chữ hoa / thường | EC16, EC44 | `Nguyen␣Van␣A` | `TEST@eshop.com` | `Newpass1@` | `Newpass1@` | Từ chối, báo email đã tồn tại; không tạo tài khoản; API trả 4xx; `test@eshop.com / Test1234!` vẫn đăng nhập được (EC44); A3 | Web, API | AI |
| FR01-DT-19 | Kiểm tra đăng ký bị từ chối khi bỏ trống Mật khẩu | EC17, EC42 | `Nguyen␣Van␣A` | `fr01.dt19@example.com` | (rỗng) | (rỗng) | Từ chối, báo thiếu Mật khẩu; không tạo tài khoản; API trả 4xx (EC42) | Web, API | AI |
| FR01-DT-20 | Kiểm tra đăng ký bị từ chối khi Mật khẩu ngắn hơn 8 ký tự | EC19, EC45 | `Nguyen␣Van␣A` | `fr01.dt20@example.com` | `Abcd1@` | `Abcd1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| FR01-DT-21 | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ hoa | EC21, EC45 | `Nguyen␣Van␣A` | `fr01.dt21@example.com` | `abcdef1@` | `abcdef1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| FR01-DT-22 | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ thường | EC23, EC45 | `Nguyen␣Van␣A` | `fr01.dt22@example.com` | `ABCDEF1@` | `ABCDEF1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| FR01-DT-23 | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ số | EC25, EC45 | `Nguyen␣Van␣A` | `fr01.dt23@example.com` | `Abcdefg@` | `Abcdefg@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| FR01-DT-24 | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có ký tự đặc biệt | EC27, EC45 | `Nguyen␣Van␣A` | `fr01.dt24@example.com` | `Abcdefg1` | `Abcdefg1` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| FR01-DT-25 | Kiểm tra đăng ký bị từ chối khi ký tự đặc biệt duy nhất của Mật khẩu nằm ngoài tập `@ $ ! % * ? &` | EC28, EC45 | `Nguyen␣Van␣A` | `fr01.dt25@example.com` | `Abcdef1#` | `Abcdef1#` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45); A1 | Web, API | AI |
| FR01-DT-26 | Kiểm tra đăng ký bị từ chối khi bỏ trống Xác nhận mật khẩu | EC38, EC42 | `Nguyen␣Van␣A` | `fr01.dt26@example.com` | `Abcdef1@` | (rỗng) | Từ chối, báo thiếu Xác nhận mật khẩu hoặc không khớp; không tạo tài khoản (EC42/EC46) | Web | AI |
| FR01-DT-27 | Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu khác Mật khẩu | EC39, EC46 | `Nguyen␣Van␣A` | `fr01.dt27@example.com` | `Abcdef1@` | `Abcdef2@` | Từ chối, báo xác nhận mật khẩu không khớp; không tạo tài khoản (EC46) | Web | AI |
| FR01-DT-28 | Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu chỉ khác Mật khẩu ở chữ hoa / thường | EC40, EC46 | `Nguyen␣Van␣A` | `fr01.dt28@example.com` | `Abcdef1@` | `abcdef1@` | Từ chối, báo xác nhận mật khẩu không khớp; không tạo tài khoản (EC46) | Web | AI |
<!-- END:T32 -->

#### 3.3 Bảng phủ phân vùng

<!-- BEGIN:T33 -->
| EC | Test case phủ | | EC | Test case phủ |
| --- | --- | --- | --- | --- |
| EC1 | FR01-DT-01, FR01-DT-03…FR01-DT-07 | | EC24 | FR01-DT-01…FR01-DT-07 |
| EC2 | FR01-DT-02 | | EC25 | FR01-DT-23 |
| EC3 | FR01-DT-08 | | EC26 | FR01-DT-01…FR01-DT-07 |
| EC4 | FR01-DT-09 | | EC27 | FR01-DT-24 |
| EC5 | FR01-DT-01, FR01-DT-03…FR01-DT-07 | | EC28 | FR01-DT-25; bổ sung: FR01-DT-29 (mục 6.2) |
| EC6 | FR01-DT-02 | | EC29 | FR01-DT-01 |
| EC7 | FR01-DT-10 | | EC30 | FR01-DT-02 |
| EC8 | FR01-DT-11 | | EC31 | FR01-DT-03 |
| EC9 | FR01-DT-12 | | EC32 | FR01-DT-04 |
| EC10 | FR01-DT-13 | | EC33 | FR01-DT-05 |
| EC11 | FR01-DT-14 | | EC34 | FR01-DT-06 |
| EC12 | FR01-DT-15 | | EC35 | FR01-DT-07 |
| EC13 | FR01-DT-16 | | EC36 | FR01-DT-02; bổ sung: FR01-DT-32 (mục 6.2) |
| EC14 | FR01-DT-01…FR01-DT-07 | | EC37 | FR01-DT-01…FR01-DT-07 |
| EC15 | FR01-DT-17 | | EC38 | FR01-DT-26 |
| EC16 | FR01-DT-18 | | EC39 | FR01-DT-27 |
| EC17 | FR01-DT-19 | | EC40 | FR01-DT-28 |
| EC18 | FR01-DT-01…FR01-DT-07 | | EC41 | FR01-DT-01…FR01-DT-07; bổ sung: FR01-DT-32 (mục 6.2) |
| EC19 | FR01-DT-20 | | EC42 | FR01-DT-08…FR01-DT-10, FR01-DT-19, FR01-DT-26 |
| EC20 | FR01-DT-01…FR01-DT-07 | | EC43 | FR01-DT-11…FR01-DT-16 |
| EC21 | FR01-DT-21; bổ sung: FR01-DT-30 (mục 6.2) | | EC44 | FR01-DT-17, FR01-DT-18 |
| EC22 | FR01-DT-01…FR01-DT-07 | | EC45 | FR01-DT-20…FR01-DT-25; bổ sung: FR01-DT-29, FR01-DT-30, FR01-DT-31 (mục 6.2) |
| EC23 | FR01-DT-22; bổ sung: FR01-DT-31 (mục 6.2) | | EC46 | FR01-DT-27, FR01-DT-28 |

46 / 46 lớp được phủ bởi 28 test case Minimum Set (7 valid, 21 invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp invalid có test case riêng. Các đại diện bổ sung sau rà soát (mục 6.2) ghi sau dấu `;`.
<!-- END:T33 -->

### 4. Bước 4 – Boundary Value Analysis

#### 4.1 Xác định biên

BVA áp dụng cho các biến / đại lượng có thứ tự. Với mỗi phân vùng xét LB-1, LB, LB+1, UB-1, UB, UB+1 và giá trị lớn nhất nhập được [S04]; điểm nào đã có trong Minimum Set thì dẫn chiếu test case đó thay vì tạo test case trùng [KB – không lặp].

| Biến / đại lượng | Phân vùng | LB | UB | Bước nhảy | Điểm kiểm tra |
| --- | --- | --- | --- | --- | --- |
| I3.L độ dài mật khẩu | EC17 (rỗng) / EC19 (1–7) / EC18 (≥ 8) | 1; 8 | 7; không giới hạn (A5) | 1 ký tự | 0, 1, 2, 6, 7, 8, 9, 1000 |
| I3.U / I3.W / I3.D / I3.S số ký tự mỗi loại | EC21/EC20, EC23/EC22, EC25/EC24, EC27/EC26 (0 / ≥ 1) | 1 | không giới hạn | 1 ký tự | 0, 1 |
| Khoảng chữ hoa | `A`–`Z` (mã 65–90) | `A` | `Z` | 1 mã ký tự | `@` (64), `A`, `Z`, `[` (91) |
| Khoảng chữ thường | `a`–`z` (mã 97–122) | `a` | `z` | 1 mã ký tự | `` ` `` (96), `a`, `z`, `{` (123) |
| Khoảng chữ số | `0`–`9` (mã 48–57) | `0` | `9` | 1 mã ký tự | `/` (47), `0`, `9`, `:` (58) |
| I1 độ dài Họ Tên (không tính khoảng trắng đầu/cuối) | EC3, EC4 (0) / EC1 (≥ 1) | 1 | không giới hạn (A5) | 1 ký tự | 0, 1, 1000 |
| I2 độ dài Email | EC5 | 5 (`a@b.c`, ngắn nhất theo A2) | 254 (giới hạn độ dài địa chỉ của RFC 5321) | 1 ký tự | 5, 254 |
| Số khoảng trắng ở đầu email | EC5 (0) / EC6 (≥ 1) | 1 | không giới hạn | 1 ký tự | 0 (FR01-DT-01); 1 đầu + 1 cuối (FR01-DT-02); 1 – kết hợp email đã tồn tại EC15 để kiểm tra việc bỏ khoảng trắng trước khi so trùng (FR01-BV-19) |
| I4 so với I3 | EC37 (khớp) / EC39 (khác) | độ dài = độ dài MK | | 1 ký tự | MK thiếu 1 ký tự cuối, MK thừa 1 ký tự |

#### 4.2 Boundary Value Test Cases

Thủ tục: P-WEB / P-API ở mục 3.1. Bảng giữ nguyên các cột dữ liệu của data matrix như mục 3.2 (theo Table 6 của [UC] và slide 27 của [S04]). Dòng có ID trong ngoặc là điểm biên đã có trong Minimum Set, chỉ dẫn chiếu.

<!-- BEGIN:T42 -->
| ID | Tên test case (Action + Function + Condition) | Partition tested | Họ Tên | Email | Mật khẩu | Xác nhận | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| (FR01-DT-19) | Kiểm tra đăng ký bị từ chối khi bỏ trống Mật khẩu | EC17 – độ dài 0 | `Nguyen␣Van␣A` | `fr01.dt19@example.com` | (rỗng) | (rỗng) | Từ chối, báo thiếu Mật khẩu; không tạo tài khoản; API trả 4xx (EC42) | Web, API | xem 3.2 |
| FR01-BV-01 | Kiểm tra đăng ký bị từ chối khi Mật khẩu dài 1 ký tự | EC17/EC19 – độ dài 1 (LB của EC19) | `Nguyen␣Van␣A` | `fr01.bv01@example.com` | `@` | `@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| FR01-BV-02 | Kiểm tra đăng ký bị từ chối khi Mật khẩu dài 2 ký tự | EC19 – độ dài 2 (LB+1) | `Nguyen␣Van␣A` | `fr01.bv02@example.com` | `A1` | `A1` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| (FR01-DT-20) | Kiểm tra đăng ký bị từ chối khi Mật khẩu ngắn hơn 8 ký tự | EC19 – độ dài 6 (UB-1) | `Nguyen␣Van␣A` | `fr01.dt20@example.com` | `Abcd1@` | `Abcd1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | xem 3.2 |
| FR01-BV-03 | Kiểm tra đăng ký bị từ chối khi Mật khẩu dài 7 ký tự và đủ 4 loại ký tự | EC19/EC18 – độ dài 7 (UB của EC19) | `Nguyen␣Van␣A` | `fr01.bv03@example.com` | `Abcde1@` | `Abcde1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| (FR01-DT-01) | Kiểm tra đăng ký thành công với dữ liệu hợp lệ điển hình | EC19/EC18 – độ dài 8 (LB của EC18); EC20, EC24, EC26 – đúng 1 chữ hoa, 1 chữ số, 1 ký tự đặc biệt (LB); số khoảng trắng đầu email = 0 | `Nguyen␣Van␣A` | `fr01.dt01@example.com` | `Abcdef1@` | `Abcdef1@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | xem 3.2 |
| FR01-BV-04 | Kiểm tra đăng ký thành công khi Mật khẩu dài 9 ký tự | EC18 – độ dài 9 (LB+1 của EC18) | `Nguyen␣Van␣A` | `fr01.bv04@example.com` | `Abcdefg1@` | `Abcdefg1@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-BV-05 | Kiểm tra đăng ký thành công khi Mật khẩu dài 1000 ký tự | EC18 – độ dài 1000 (lớn nhất chọn thử) | `Nguyen␣Van␣A` | `fr01.bv05@example.com` | `"Abcdef1@" + "a" * 992` (1000 ký tự) | `"Abcdef1@" + "a" * 992` (1000 ký tự) | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41); A5 | Web, API | AI |
| (FR01-DT-21) | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ hoa | EC21 – 0 chữ hoa; `@`/`A` (`@` là ký tự liền trước `A`, LB-1 chữ hoa) | `Nguyen␣Van␣A` | `fr01.dt21@example.com` | `abcdef1@` | `abcdef1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | xem 3.2 |
| (FR01-DT-22) | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ thường | EC23 – 0 chữ thường | `Nguyen␣Van␣A` | `fr01.dt22@example.com` | `ABCDEF1@` | `ABCDEF1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | xem 3.2 |
| (FR01-DT-23) | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ số | EC25 – 0 chữ số | `Nguyen␣Van␣A` | `fr01.dt23@example.com` | `Abcdefg@` | `Abcdefg@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | xem 3.2 |
| (FR01-DT-24) | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có ký tự đặc biệt | EC27 – 0 ký tự đặc biệt | `Nguyen␣Van␣A` | `fr01.dt24@example.com` | `Abcdefg1` | `Abcdefg1` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | xem 3.2 |
| FR01-BV-06 | Kiểm tra đăng ký thành công khi Mật khẩu có đúng 1 chữ thường | EC22 – 1 chữ thường (LB) | `Nguyen␣Van␣A` | `fr01.bv06@example.com` | `ABCDEa1@` | `ABCDEa1@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-BV-07 | Kiểm tra đăng ký thành công khi chữ hoa duy nhất là `Z`, chữ thường duy nhất là `a`, chữ số duy nhất là `9` | `Z` (UB chữ hoa), `a` (LB chữ thường), `9` (UB chữ số) | `Nguyen␣Van␣A` | `fr01.bv07@example.com` | `Zaaaaa9@` | `Zaaaaa9@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-BV-08 | Kiểm tra đăng ký thành công khi chữ hoa duy nhất là `A`, chữ thường duy nhất là `z`, chữ số duy nhất là `0` | `A` (LB chữ hoa), `z` (UB chữ thường), `0` (LB chữ số) | `Nguyen␣Van␣A` | `fr01.bv08@example.com` | `Azzzzz0@` | `Azzzzz0@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-BV-09 | Kiểm tra đăng ký bị từ chối khi ký tự liền sau `Z` (`[`) thay cho chữ hoa | `Z`/`[` (UB+1 chữ hoa) | `Nguyen␣Van␣A` | `fr01.bv09@example.com` | `[bcdef1@` | `[bcdef1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| FR01-BV-10 | Kiểm tra đăng ký bị từ chối khi ký tự liền trước `a` (`` ` ``) thay cho chữ thường | `` ` ``/`a` (LB-1 chữ thường) | `Nguyen␣Van␣A` | `fr01.bv10@example.com` | ``````A`````1@`````` | ``````A`````1@`````` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| FR01-BV-11 | Kiểm tra đăng ký bị từ chối khi ký tự liền sau `z` (`{`) thay cho chữ thường | `z`/`{` (UB+1 chữ thường) | `Nguyen␣Van␣A` | `fr01.bv11@example.com` | `A{{{{{1@` | `A{{{{{1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| FR01-BV-12 | Kiểm tra đăng ký bị từ chối khi ký tự liền trước `0` (`/`) thay cho chữ số | `/`/`0` (LB-1 chữ số) | `Nguyen␣Van␣A` | `fr01.bv12@example.com` | `Abcdef/@` | `Abcdef/@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| FR01-BV-13 | Kiểm tra đăng ký bị từ chối khi ký tự liền sau `9` (`:`) thay cho chữ số | `9`/`:` (UB+1 chữ số) | `Nguyen␣Van␣A` | `fr01.bv13@example.com` | `Abcdef:@` | `Abcdef:@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45) | Web, API | AI |
| (FR01-DT-08) | Kiểm tra đăng ký bị từ chối khi bỏ trống Họ Tên | EC3 – Họ Tên độ dài 0 | (rỗng) | `fr01.dt08@example.com` | `Abcdef1@` | `Abcdef1@` | Từ chối, báo thiếu Họ Tên; không tạo tài khoản; API trả 4xx (EC42) | Web, API | xem 3.2 |
| FR01-BV-14 | Kiểm tra đăng ký thành công khi Họ Tên dài 1 ký tự | EC3/EC1 – độ dài 1 (LB của EC1) | `A` | `fr01.bv14@example.com` | `Abcdef1@` | `Abcdef1@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-BV-15 | Kiểm tra đăng ký thành công khi Họ Tên có 1 ký tự giữa các khoảng trắng | EC4/EC1 – 1 ký tự khác khoảng trắng (LB) | `␣A␣` | `fr01.bv15@example.com` | `Abcdef1@` | `Abcdef1@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41); A4 | Web, API | AI |
| FR01-BV-16 | Kiểm tra đăng ký thành công khi Họ Tên dài 1000 ký tự | EC1 – độ dài 1000 (lớn nhất chọn thử) | `"A" * 1000` | `fr01.bv16@example.com` | `Abcdef1@` | `Abcdef1@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41); A5 | Web, API | AI |
| FR01-BV-17 | Kiểm tra đăng ký thành công với Email ngắn nhất hợp lệ | EC5 – độ dài 5 (LB theo A2) | `Nguyen␣Van␣A` | `a@b.c` | `Abcdef1@` | `Abcdef1@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-BV-18 | Kiểm tra đăng ký thành công với Email dài 254 ký tự | EC5 – độ dài 254 (UB theo RFC 5321) | `Nguyen␣Van␣A` | `"a" * 64 + "@" + "b" * 63 + "." + "c" * 63 + "." + "d" * 57 + ".com"` (254 ký tự) | `Abcdef1@` | `Abcdef1@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41) | Web, API | AI |
| FR01-BV-19 | Kiểm tra đăng ký bị từ chối khi Email đã tồn tại có đúng 1 khoảng trắng ở đầu | Số khoảng trắng đầu email = 1 (LB của EC6) kết hợp EC15 | `Nguyen␣Van␣A` | `␣test@eshop.com` | `Newpass1@` | `Newpass1@` | Từ chối, báo email đã tồn tại; không tạo tài khoản; API trả 4xx; `test@eshop.com / Test1234!` vẫn đăng nhập được (EC44); A4 | Web, API | AI-sửa |
| FR01-BV-20 | Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu thiếu ký tự cuối | EC37/EC39 – độ dài Mật khẩu - 1 | `Nguyen␣Van␣A` | `fr01.bv20@example.com` | `Abcdef1@` | `Abcdef1` | Từ chối, báo xác nhận mật khẩu không khớp; không tạo tài khoản (EC46) | Web | AI |
| FR01-BV-21 | Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu thừa 1 ký tự | EC37/EC39 – độ dài Mật khẩu + 1 | `Nguyen␣Van␣A` | `fr01.bv21@example.com` | `Abcdef1@` | `Abcdef1@1` | Từ chối, báo xác nhận mật khẩu không khớp; không tạo tài khoản (EC46) | Web | AI |

Tổng: 21 test case BVA mới (FR01-BV-01…FR01-BV-21); 8 dòng có ID trong ngoặc là điểm biên đã được phủ bởi test case Minimum Set (mục 3.2), chỉ dẫn chiếu, không chạy lại.
<!-- END:T42 -->

### 5. Bước 5 – Kết quả thực thi

#### 5.1 Môi trường và cách chạy

| Mục | Giá trị |
| --- | --- |
| Ngày chạy | 2026-10-20 |
| Người chạy | 23120031 (script tự động, kết quả được rà soát thủ công) |
| SUT | `eshop-sut-main` (trùng với `d1nhnguyen/eshop-sut`), Node 20.19.5 |
| Web | Chrome 155 (headless, Playwright), `http://localhost:5173` |
| API | `http://localhost:3000/api`, gọi bằng Python `urllib` |
| Dữ liệu | Backend được khởi động lại trước mỗi lượt chạy (`scripts/restart_backend.sh`) |
| Script | `scripts/fr01/cases.py` (dữ liệu), `run_web.mjs` (P-WEB), `run_api.py` (P-API), `explore_web_password.mjs` (khảo sát) |
| Bằng chứng | `evidence/FR-01/web_results.json`, `api_results.json`, `web_results_workaround.json`, `explore_web_password.json`; ảnh sau khi bấm "Đăng Ký" của từng test case: `evidence/FR-01/web/<ID>.png` (lượt khảo sát: `<ID>_wa.png`) |

Cách kết luận (A7): test case "thành công" Pass khi chuyển tới trang Đăng nhập (Web) / HTTP 200 (API), tài khoản xuất hiện trong danh sách người dùng (`GET /api/admin/users`) và đăng nhập được. Test case "từ chối" Pass khi không tạo tài khoản **và** thông báo lỗi nói đúng lý do mong đợi; bị từ chối nhưng sai lý do là Fail. Test case email trùng còn kiểm tra tài khoản gốc `test@eshop.com / Test1234!` vẫn đăng nhập được.

#### 5.2 Phát hiện chặn khi chạy trên Web

Lượt chạy Web đầu tiên cho thấy **mọi mật khẩu hợp lệ theo đặc tả đều bị form báo "Mật khẩu quá yếu!"** và không gửi request. Khảo sát thêm 43 mật khẩu (`explore_web_password.json`):

| Mật khẩu thử | Form Web |
| --- | --- |
| `Abcdef1` + một trong 7 ký tự `@ $ ! % * ? &` | Chặn |
| `Abcdef1` + một trong 25 ký tự đặc biệt khác (`# ^ - _ . ~ + = / \ ( ) [ ] { } < > \| : ; , ' " ` ``) | Chặn |
| `Abcdef1␣`, `Abc␣def1`, `␣Abcdef1` | Gửi request, đăng ký thành công |
| `Abcdef1@␣` (có cả `@` và dấu cách) | Chặn |
| `abcdef1␣`, `ABCDEF1␣`, `Abcdefg␣`, `Abcde1␣` | Chặn (thiếu chữ thường / chữ hoa / chữ số / đủ 8 ký tự) |

→ Form Web kiểm tra đúng độ dài, chữ hoa, chữ thường, chữ số, nhưng **chỉ coi dấu cách là ký tự đặc biệt** và chặn mọi ký tự đặc biệt khác. Không tồn tại mật khẩu vừa hợp lệ theo đặc tả vừa qua được form, nên:

- 15 test case Web không nhắm vào mật khẩu (Họ Tên, Email, email trùng) bị **Blocked** ở lượt chính thức: form từ chối vì mật khẩu trước khi tới điều kiện cần kiểm tra. Các biến này vẫn được đánh giá đầy đủ trên kênh API.
- Lượt **khảo sát** (không tính verdict) chạy lại 22 test case này với mật khẩu `Abcdef1␣` (thay `@` bằng dấu cách – không hợp lệ theo A1) để quan sát cách Web xử lý các biến khác (mục 5.4).

#### 5.3 Kết quả theo test case

Mỗi test case một dòng, gồm cả 4 test case bổ sung ở mục 6.2. Web = lượt chính thức (P-WEB, dữ liệu đúng thiết kế). Bảng sinh từ `evidence/FR-01/web_results.json` và `api_results.json`.

<!-- BEGIN:T53 -->
| TC | Web | Kết quả thực tế – Web | API | Kết quả thực tế – API | Bằng chứng | Bug |
| --- | --- | --- | --- | --- | --- | --- |
| FR01-DT-01 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-DT-01.png) · `api_results.json` | FR01-B1 |
| FR01-DT-02 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tài khoản lưu với email chưa bỏ khoảng trắng; không đăng nhập được bằng email đã bỏ khoảng trắng | [ảnh Web](../evidence/FR-01/web/FR01-DT-02.png) · `api_results.json` | FR01-B1, FR01-B8 |
| FR01-DT-03 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-DT-03.png) · `api_results.json` | FR01-B1 |
| FR01-DT-04 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-DT-04.png) · `api_results.json` | FR01-B1 |
| FR01-DT-05 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-DT-05.png) · `api_results.json` | FR01-B1 |
| FR01-DT-06 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-DT-06.png) · `api_results.json` | FR01-B1 |
| FR01-DT-07 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-DT-07.png) · `api_results.json` | FR01-B1 |
| FR01-DT-08 | Pass | Trình duyệt chặn ô Họ Tên: “Please fill out this field.”; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-08.png) · `api_results.json` | FR01-B3 |
| FR01-DT-09 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-09.png) · `api_results.json` | FR01-B9 |
| FR01-DT-10 | Pass | Trình duyệt chặn ô Email: “Please fill out this field.”; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-10.png) · `api_results.json` | FR01-B3 |
| FR01-DT-11 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-11.png) · `api_results.json` | FR01-B4 |
| FR01-DT-12 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-12.png) · `api_results.json` | FR01-B4 |
| FR01-DT-13 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-13.png) · `api_results.json` | FR01-B4 |
| FR01-DT-14 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-14.png) · `api_results.json` | FR01-B4 |
| FR01-DT-15 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-15.png) · `api_results.json` | FR01-B4 |
| FR01-DT-16 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-16.png) · `api_results.json` | FR01-B4 |
| FR01-DT-17 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Fail | HTTP 200 “User registered successfully”; tạo thêm tài khoản trùng email (có 2 tài khoản cùng email); tài khoản gốc vẫn đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-DT-17.png) · `api_results.json` | FR01-B6 |
| FR01-DT-18 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Fail | HTTP 200 “User registered successfully”; tạo thêm tài khoản trùng email (có 3 tài khoản cùng email); tài khoản gốc vẫn đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-DT-18.png) · `api_results.json` | FR01-B6 |
| FR01-DT-19 | Pass | Trình duyệt chặn ô Mật khẩu: “Please fill out this field.”; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-19.png) · `api_results.json` | FR01-B3 |
| FR01-DT-20 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-20.png) · `api_results.json` | FR01-B5 |
| FR01-DT-21 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-21.png) · `api_results.json` | FR01-B5 |
| FR01-DT-22 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-22.png) · `api_results.json` | FR01-B5 |
| FR01-DT-23 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-23.png) · `api_results.json` | FR01-B5 |
| FR01-DT-24 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-24.png) · `api_results.json` | FR01-B5 |
| FR01-DT-25 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-25.png) · `api_results.json` | FR01-B5 |
| FR01-DT-26 | Fail | Không có ô Xác nhận mật khẩu; form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | – | Không áp dụng (A8) | [ảnh Web](../evidence/FR-01/web/FR01-DT-26.png) | FR01-B2 |
| FR01-DT-27 | Fail | Không có ô Xác nhận mật khẩu; form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | – | Không áp dụng (A8) | [ảnh Web](../evidence/FR-01/web/FR01-DT-27.png) | FR01-B2 |
| FR01-DT-28 | Fail | Không có ô Xác nhận mật khẩu; form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | – | Không áp dụng (A8) | [ảnh Web](../evidence/FR-01/web/FR01-DT-28.png) | FR01-B2 |
| FR01-BV-01 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-BV-01.png) · `api_results.json` | FR01-B5 |
| FR01-BV-02 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-BV-02.png) · `api_results.json` | FR01-B5 |
| FR01-BV-03 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-BV-03.png) · `api_results.json` | FR01-B5 |
| FR01-BV-04 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-04.png) · `api_results.json` | FR01-B1 |
| FR01-BV-05 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-05.png) · `api_results.json` | FR01-B1 |
| FR01-BV-06 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-06.png) · `api_results.json` | FR01-B1 |
| FR01-BV-07 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-07.png) · `api_results.json` | FR01-B1 |
| FR01-BV-08 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-08.png) · `api_results.json` | FR01-B1 |
| FR01-BV-09 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-BV-09.png) · `api_results.json` | FR01-B5 |
| FR01-BV-10 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-BV-10.png) · `api_results.json` | FR01-B5 |
| FR01-BV-11 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-BV-11.png) · `api_results.json` | FR01-B5 |
| FR01-BV-12 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-BV-12.png) · `api_results.json` | FR01-B5 |
| FR01-BV-13 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-BV-13.png) · `api_results.json` | FR01-B5 |
| FR01-BV-14 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-14.png) · `api_results.json` | – |
| FR01-BV-15 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-15.png) · `api_results.json` | – |
| FR01-BV-16 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-16.png) · `api_results.json` | – |
| FR01-BV-17 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-17.png) · `api_results.json` | – |
| FR01-BV-18 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-18.png) · `api_results.json` | – |
| FR01-BV-19 | Blocked | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra | Fail | HTTP 200 “User registered successfully”; tài khoản lưu với email chưa bỏ khoảng trắng; tài khoản gốc vẫn đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-BV-19.png) · `api_results.json` | FR01-B6, FR01-B8 |
| FR01-BV-20 | Fail | Không có ô Xác nhận mật khẩu; form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | – | Không áp dụng (A8) | [ảnh Web](../evidence/FR-01/web/FR01-BV-20.png) | FR01-B2 |
| FR01-BV-21 | Fail | Không có ô Xác nhận mật khẩu; form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | – | Không áp dụng (A8) | [ảnh Web](../evidence/FR-01/web/FR01-BV-21.png) | FR01-B2 |
| FR01-DT-29 | Fail | Form gửi request, HTTP 200, chuyển tới `/login`; tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-29.png) · `api_results.json` | FR01-B1, FR01-B5 |
| FR01-DT-30 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-30.png) · `api_results.json` | FR01-B5 |
| FR01-DT-31 | Pass | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Fail | HTTP 200 “User registered successfully”; tạo tài khoản | [ảnh Web](../evidence/FR-01/web/FR01-DT-31.png) · `api_results.json` | FR01-B5 |
| FR01-DT-32 | Fail | Form báo “Mật khẩu quá yếu!”, không gửi request; không tạo tài khoản | Pass | HTTP 200 “User registered successfully”; tạo tài khoản; đăng nhập được | [ảnh Web](../evidence/FR-01/web/FR01-DT-32.png) · `api_results.json` | FR01-B1 |
<!-- END:T53 -->

#### 5.4 Quan sát từ lượt khảo sát trên Web (không tính verdict)

Với mật khẩu `Abcdef1␣` form Web gửi request; `web_results_workaround.json`, ảnh `evidence/FR-01/web/<ID>_wa.png`:

- Họ Tên `␣␣␣` (FR01-DT-09) qua được thuộc tính `required` của trình duyệt và được server chấp nhận → FR01-B9.
- Cả 6 email sai định dạng (FR01-DT-11…FR01-DT-16) được form gửi đi mà không cảnh báo (ô Email là `type="text"`) và được server chấp nhận → FR01-B7, FR01-B4.
- Email trùng `test@eshop.com`, `TEST@eshop.com`, `␣test@eshop.com` (FR01-DT-17, FR01-DT-18, FR01-BV-19) được chấp nhận → FR01-B6.
- Họ Tên / Email ở biên (FR01-BV-14…FR01-BV-18) đăng ký và đăng nhập được, khớp kết quả API.
- Bản thân việc mật khẩu `Abcdef1␣` (không có ký tự nào thuộc tập `@ $ ! % * ? &`) được chấp nhận ở cả Web và API là vi phạm A1 → FR01-B1, FR01-B5.

#### 5.5 Tổng hợp

<!-- BEGIN:T55 -->
| Kênh | Thiết kế | Đã chạy | Pass | Fail | Blocked | Không áp dụng |
| --- | --- | --- | --- | --- | --- | --- |
| Web | 53 | 53 | 19 | 19 | 15 | 0 |
| API | 53 | 48 | 17 | 31 | 0 | 5 (biến Xác nhận mật khẩu, A8) |
| **Tổng lượt chạy** | | **101** | **36** | **50** | **15** | |

53 test case = 28 Minimum Set (mục 3.2) + 21 BVA (mục 4.2) + 4 bổ sung sau rà soát (mục 6.2). Gộp các kênh theo test case (Fail nếu Fail ở bất kỳ kênh nào, Blocked nếu còn kênh bị Blocked): 0 Pass, 48 Fail, 5 Blocked.
<!-- END:T55 -->

### 6. Bước 6 – AI gap analysis

> G1–G8: AI (Claude Code) tự phát hiện trong lúc làm các bước 1–5. G9–G16: phát hiện khi sinh viên dùng Google Antigravity (Gemini 4 Argon, lượt #13 trong `ai/prompt_log.md`) rà soát chéo báo cáo theo tiêu chí bảng, cách đặt tên TC và mức độ chi tiết (đối chiếu [UC] Table 6, [S07], Testcase Checklist); sinh viên duyệt và chuyển sang Claude Code (lượt #14) thực hiện ở các commit `[FR-01][Bn-review]`.

#### 6.1 Những gì AI bỏ sót hoặc làm sai

| # | AI bỏ sót / làm sai | Loại | Nguyên nhân | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |
| G1 | Lớp EC28 "chỉ có ký tự đặc biệt ngoài tập" dùng `#` làm đại diện; không xét dấu cách – đúng ký tự mà form Web coi là "ký tự đặc biệt". Thiết kế ban đầu không có test case phát hiện việc Web / API chấp nhận mật khẩu không có ký tự nào thuộc tập | Test case / chọn best representative | **Giới hạn công cụ AI**: chọn đại diện "điển hình" thay vì theo rủi ro; trước khi chạy không quan sát được cách SUT xử lý từng ký tự. **Độ phức tạp feature**: các phần tử của cùng một lớp lại được SUT xử lý khác nhau – đúng trường hợp guideline G5 yêu cầu tách lớp | Khảo sát 43 mật khẩu ở bước 5 | Bổ sung FR01-DT-29 (mục 6.2) |
| G2 | Bản đầu của script Web coi "bị từ chối với bất kỳ thông báo nào" là Pass → 10 test case Email / Họ Tên / email trùng được báo Pass trong khi thật ra bị từ chối vì "Mật khẩu quá yếu!" | Kết quả mong đợi / oracle quá lỏng | **Giới hạn công cụ AI**: tự động hoá kiểm tra không bám đúng giả định A7 ("thông báo chỉ đúng lý do") mà chính nó đã đặt ra | Rà soát output lượt chạy đầu: mọi test case từ chối đều cùng một câu thông báo | Kiểm tra lý do từ chối theo trường; thêm trạng thái Blocked |
| G3 | Bản đầu của script không đánh Fail 5 test case Xác nhận mật khẩu khi ô này không tồn tại (chúng "Pass" vì bị từ chối do mật khẩu) | Oracle | Như G2 | Rà soát output | Kiểm tra sự tồn tại của ô trước khi kết luận |
| G4 | Giả định đường vòng `Abcdef1@␣` sẽ qua được form vì `Abcdef1␣` qua được – khái quát hoá từ một mẫu | Giả định sai | **Giới hạn công cụ AI**: suy luận quá đà từ dữ liệu khảo sát ít | Lượt chạy lại vẫn bị chặn | Khảo sát thêm 10 mật khẩu; chuyển lượt chạy lại thành khảo sát, không tính verdict |
| G5 | Script đọc thông báo validation của form Đăng nhập sau khi đã chuyển trang, ghi vào bằng chứng như thông báo của form Đăng ký | Bằng chứng sai lệch | **Giới hạn công cụ AI**: không lường trước việc chuyển trang làm thay đổi phần tử được chọn | Đọc output: test case thành công lại có "Please fill out this field." | Chỉ đọc thông báo khi còn ở `/register` |
| G6 | Kiểm tra "tài khoản gốc bị ảnh hưởng" dựa vào số tài khoản trùng email = 1, bị nhiễm trạng thái do test case trước tạo ra → kết luận sai cho FR01-DT-18, FR01-BV-19 | Oracle / test case không độc lập | **Độ phức tạp feature**: một lỗi (cho trùng email) làm thay đổi trạng thái dùng chung giữa các test case | Đối chiếu thủ công bằng `curl` | Chỉ dựa vào việc tài khoản gốc còn đăng nhập được |
| G7 | Email 254 ký tự bị tính thành 255 | Dữ liệu test | Lỗi tính toán của AI | `assert` trong `cases.py` | Sửa |
| G8 | Trước khi commit B3, bảng phủ tính cả test case invalid là phủ lớp valid; FR01-DT-19 ghi ô Xác nhận rỗng thay vì `= MK` | Bảng phủ / dữ liệu | AI áp dụng quy tắc Minimum Set chưa chặt | AI tự rà soát trước khi commit (không có trong lịch sử commit) | Sửa trước commit |
| G9 | Bảng BVA gom 4 cột dữ liệu thành 1 cột "Giá trị", lệch cấu trúc data matrix của bảng 3.2 và mẫu Table 6 [UC] | Định dạng bảng | **Giới hạn công cụ AI**: ưu tiên bảng ngắn gọn, không giữ cấu trúc nhất quán giữa các bảng | Rà soát chéo (SV + Antigravity, lượt #13) | Sinh bảng từ `cases.py`, giữ đủ cột (B4-review) |
| G10 | Bảng kết quả 5.3 gộp nhiều test case vào một dòng (48 test case còn 18 dòng), thiếu FR01-DT-29, không gắn bằng chứng cho từng test case | Báo cáo kết quả | **Giới hạn công cụ AI**: tóm tắt thay vì báo cáo đủ chi tiết như mẫu [TPL] | Rà soát chéo (SV + Antigravity, lượt #13) | Mỗi test case một dòng + cột Bằng chứng (B5-review) |
| G11 | ID `DT-01`, `BV-01` không có mã feature, sẽ trùng khi gộp báo cáo 4 feature | Quy ước đặt tên | **Do prompt**: prompt chỉ nói về từng bước của một feature, không nhắc báo cáo chung | Rà soát chéo (SV + Antigravity, lượt #13) | Đổi sang `FR01-DT-nn`, `FR01-BV-nn` (B3-review) |
| G12 | Ô dữ liệu ghi "mặc định", "= MK"; kết quả mong đợi ghi "Như FR01-DT-01" → test case không Self-standing, không Repeatable | Chất lượng test case | **Giới hạn công cụ AI**: rút gọn bảng, vi phạm checklist [S07] mà chính nó đã dẫn trong phần phương pháp | Rà soát chéo (SV + Antigravity, lượt #13) | Giá trị cụ thể, kết quả mong đợi tường minh kèm mã lớp đầu ra (B3-review) |
| G13 | 7 dòng dẫn chiếu ở bảng BVA dùng tên dạng danh từ, không theo Action + Function + Condition; tên FR01-DT-02 dễ nhầm với FR01-DT-25 | Tên test case | Như G12 | Rà soát chéo (SV + Antigravity, lượt #13) | Dùng tên chính thức của mục 3.2; sửa tên FR01-DT-02 (B3-, B4-review) |
| G14 | FR01-BV-19 là test case kết hợp lớp, không nêu biên nào được kiểm tra | Áp dụng BVA | **Giới hạn công cụ AI**: xếp test case vào BVA mà không chỉ ra biến có thứ tự | Rà soát chéo (SV + Antigravity, lượt #13) | Nêu biên số khoảng trắng đầu email = 1 (LB của EC6); thêm vào bảng 4.1 (B4-review) |
| G15 | Tổng số test case lệch giữa các mục (49 ở mục 5, nhưng mục 6 đã thêm FR01-DT-29) | Số liệu | **Giới hạn công cụ AI**: thêm test case nhưng không cập nhật lại các tổng | Rà soát chéo (SV + Antigravity, lượt #13) | Bảng tổng hợp sinh tự động từ `cases.py` + kết quả (B5-review) |
| G16 | Không có test case cho chữ có dấu trong mật khẩu (`Đ`, `ă`); AI chỉ nêu thành câu hỏi ở 6.3 | Test case thiếu | **Độ phức tạp / đặc tả mơ hồ**: AI dừng ở việc nêu câu hỏi thay vì đặt giả định và thiết kế | Rà soát chéo (SV + Antigravity, lượt #13) | Thêm A10 và FR01-DT-30…FR01-DT-32 (Origin AI-sửa) |

#### 6.2 Test case bổ sung

FR01-DT-29 do Claude Code thêm sau khảo sát (G1); FR01-DT-30…FR01-DT-32 được bổ sung từ điểm mở 6.3 sau bước rà soát chéo với Antigravity (G16). Kết quả thực thi nằm ở mục 5.3.

<!-- BEGIN:T62 -->
| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Họ Tên | Email | Mật khẩu | Xác nhận | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR01-DT-29 | Kiểm tra đăng ký bị từ chối khi ký tự đặc biệt duy nhất của Mật khẩu là dấu cách | EC28 (đại diện thứ hai), EC45 | `Nguyen␣Van␣A` | `fr01.dt29@example.com` | `Abcdef1␣` | `Abcdef1␣` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45); A1 | Web, API | AI |
| FR01-DT-30 | Kiểm tra đăng ký bị từ chối khi chữ hoa duy nhất của Mật khẩu là chữ có dấu `Đ` | EC21 (đại diện thứ hai), EC45 | `Nguyen␣Van␣A` | `fr01.dt30@example.com` | `Đbcdef1@` | `Đbcdef1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45); A10 | Web, API | AI-sửa |
| FR01-DT-31 | Kiểm tra đăng ký bị từ chối khi chữ thường duy nhất của Mật khẩu là chữ có dấu `ă` | EC23 (đại diện thứ hai), EC45 | `Nguyen␣Van␣A` | `fr01.dt31@example.com` | `ABCDEă1@` | `ABCDEă1@` | Từ chối, báo mật khẩu không đủ mạnh; không tạo tài khoản; API trả 4xx (EC45); A10 | Web, API | AI-sửa |
| FR01-DT-32 | Kiểm tra đăng ký thành công khi Mật khẩu đủ 4 loại kèm thêm chữ có dấu tiếng Việt | EC36 (đại diện thứ hai), EC41 | `Nguyen␣Van␣A` | `fr01.dt32@example.com` | `Mậtkhẩu1@` | `Mậtkhẩu1@` | Đăng ký thành công: Web chuyển tới trang Đăng nhập; API trả `200` + `id`; đăng nhập được bằng email + mật khẩu vừa nhập (EC41); A1, A10 | Web, API | AI-sửa |
<!-- END:T62 -->

#### 6.3 Điểm còn mở (chưa xử lý)

- Đặc tả không nói "chữ hoa / chữ thường" có gồm chữ có dấu (`Đ`, `Ă`, `ê`…) hay không. Đã đặt giả định A10 và thêm FR01-DT-30…FR01-DT-32; vẫn cần TA xác nhận A10.
- Các giả định A1–A5 ảnh hưởng trực tiếp tới kết quả mong đợi (đặc biệt A3, A4 liên quan FR01-B6, FR01-B8); nên xác nhận với TA.

#### 6.4 Nhận xét

- **Do prompt:** prompt "tiếp tục làm các bước" không quy định cách xử lý test case bị một lỗi khác che, nên AI tự chọn cách xử lý (Blocked + lượt khảo sát); sinh viên cần xác nhận lựa chọn này.
- **Do giới hạn công cụ AI:** phần lớn sai sót (G2–G7) nằm ở script tự động hoá và oracle, không phải ở bảng phân vùng; AI viết oracle lỏng hơn chính giả định nó đặt ra.
- **Do độ phức tạp feature:** hai lỗi chồng nhau (Web chặn mật khẩu hợp lệ, server không kiểm tra gì) khiến kết quả "Pass" trên Web dễ là Pass giả nếu không kiểm tra lý do từ chối.

### 7. Bước 7 – Bug

Chi tiết từng bug (các bước tái hiện, kết quả mong đợi / thực tế, phân tích, ảnh): `bugs/Bug_Report.md`. Cột GitHub Issue dẫn tới issue trên repo nhóm `d1nhnguyen/eshop-sut` (ảnh chụp trang issue ở cuối `bugs/Bug_Report.md`).

| Mã | Tiêu đề | Mức độ | Thành phần | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- | --- |
| FR01-B1 | Form Đăng ký trên Web báo "Mật khẩu quá yếu" với mọi mật khẩu hợp lệ có ký tự đặc biệt `@ $ ! % * ? &` | Critical | Web | FR01-DT-01…FR01-DT-07, FR01-BV-04…FR01-BV-08, FR01-DT-29, FR01-DT-32 | [BUG-15](https://github.com/d1nhnguyen/eshop-sut/issues/15) |
| FR01-B2 | Form Đăng ký thiếu ô "Xác nhận mật khẩu" | Major | Web | FR01-DT-26…FR01-DT-28, FR01-BV-20, FR01-BV-21 | [BUG-16](https://github.com/d1nhnguyen/eshop-sut/issues/16) |
| FR01-B3 | API đăng ký chấp nhận Họ Tên, Email hoặc Mật khẩu rỗng | Major | Backend | FR01-DT-08, FR01-DT-10, FR01-DT-19 | [BUG-17](https://github.com/d1nhnguyen/eshop-sut/issues/17) |
| FR01-B4 | API đăng ký chấp nhận email sai định dạng | Major | Backend | FR01-DT-11…FR01-DT-16 | [BUG-18](https://github.com/d1nhnguyen/eshop-sut/issues/18) |
| FR01-B5 | API đăng ký chấp nhận mật khẩu không đủ mạnh | Major | Backend | FR01-DT-20…FR01-DT-25, FR01-BV-01…FR01-BV-03, FR01-BV-09…FR01-BV-13, FR01-DT-29…FR01-DT-31 | [BUG-19](https://github.com/d1nhnguyen/eshop-sut/issues/19) |
| FR01-B6 | Hệ thống cho đăng ký bằng email đã tồn tại, tạo tài khoản trùng | Critical | Backend | FR01-DT-17, FR01-DT-18, FR01-BV-19 | [BUG-20](https://github.com/d1nhnguyen/eshop-sut/issues/20) |
| FR01-B7 | Ô Email ở form Đăng ký dùng `type="text"`, không kiểm tra định dạng email | Minor | Web | Quan sát B1; FR01-DT-11…FR01-DT-16 (khảo sát) | [BUG-21](https://github.com/d1nhnguyen/eshop-sut/issues/21) |
| FR01-B8 | Email đăng ký được lưu kèm khoảng trắng đầu/cuối, không đăng nhập được bằng email bình thường | Minor | Backend | FR01-DT-02, FR01-BV-19 | [BUG-22](https://github.com/d1nhnguyen/eshop-sut/issues/22) |
| FR01-B9 | Hệ thống chấp nhận Họ Tên chỉ gồm khoảng trắng | Minor | Web, Backend | FR01-DT-09 | [BUG-23](https://github.com/d1nhnguyen/eshop-sut/issues/23) |

Tổng: 9 bug (2 Critical, 4 Major, 3 Minor). Ngoài phạm vi FR-01 (không báo ở đây): trang Đăng ký không có thẻ `<h1>` và nút "Đăng Ký" màu đỏ (FR-21).

## FR-10 – Máy trạng thái đơn hàng · Domain Testing & Boundary Value Analysis

| Mục | Giá trị |
| --- | --- |
| Feature | FR-10 – Máy trạng thái đơn hàng (Pool B) |
| Kênh kiểm thử | Web Admin – tab Đơn hàng (http://localhost:5174) + Web khách hàng – hủy đơn ở trang Hồ sơ + API `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel` |
| Người thực hiện | 23120031 |
| Công cụ AI | Claude Code (VS Code extension) |
| Kỹ thuật | Domain Testing (S04 – bước 1–3), Boundary Value Analysis (S04 – bước 4) |

### 0. Đặc tả (trích nguyên văn README của SUT)

> ### FR-10: Trạng thái Đơn hàng (Order State Machine)
>
> Đơn hàng có **5 trạng thái** và phải tuân theo sơ đồ chuyển đổi sau:
>
> ```
>                  [Admin xác nhận]          [Admin giao hàng]      [Admin hoàn tất]
>   ┌──────────┐ ─────────────────► ┌───────────┐ ──────────────► ┌──────────┐ ──────────► ┌───────────┐
>   │ pending  │                    │ confirmed │                  │ shipping │             │ delivered │
>   └──────────┘                    └───────────┘                  └──────────┘             └───────────┘
>        │                               │
>        │ [User/Admin hủy]              │ [User/Admin hủy]
>        ▼                               ▼
>   ┌──────────┐                    ┌──────────┐
>   │ canceled │                    │ canceled │
>   └──────────┘                    └──────────┘
> ```
>
> **Ràng buộc trạng thái kết thúc (Final States):**
>
> - Trạng thái `delivered` và `canceled` là **trạng thái kết thúc** — không được phép chuyển sang bất kỳ trạng thái nào khác.
> - Khi đơn hàng đã ở trạng thái `shipping`, **User không được phép tự hủy** — chỉ Admin mới có thể thao tác.
> - Mọi chuyển đổi không hợp lệ phải trả về lỗi với thông báo phù hợp.

### 1. Bước 1 – Xác định biến Input / Output

#### 1.1 Quan sát giao diện và API (hộp đen)

Tạo 5 đơn của `test@eshop.com` bằng `POST /api/checkout` rồi đưa mỗi đơn về một trạng thái bằng các chuyển đổi hợp lệ (`PUT /api/admin/orders/:id/status`). Ảnh: `evidence/FR-10/B1_admin_don_hang.png`, `B1_web_ho_so.png`.

| Trạng thái (nhãn hiển thị) | Nút trên Web Admin – tab "Đơn hàng" | Nút trên Web – trang Hồ sơ, "Lịch sử đơn hàng" |
| --- | --- | --- |
| `pending` ("Chờ xác nhận") | Xác nhận, Hủy | Hủy đơn |
| `confirmed` ("Đã xác nhận") | Giao hàng, Hủy | Hủy đơn |
| `shipping` ("Đang giao") | Hoàn thành | Hủy đơn |
| `delivered` ("Đã giao") | – | – |
| `canceled` ("Đã hủy") | Đánh dấu Đã giao | – |

API (`api_specification.md` 4.3, 4.6, 6.2): tạo đơn `POST /api/checkout` (`{"total_amount", "shipping_address"}` → `{"orderId"}`); Admin đổi trạng thái `PUT /api/admin/orders/:id/status` body `{"status": "<pending|confirmed|shipping|delivered|canceled>"}`; User hủy `PUT /api/orders/:id/cancel`; xem `GET /api/admin/orders`, `GET /api/orders/my-orders`.

#### 1.2 Biến đầu vào

| ID | Biến | Kênh nhập | Kiểu / miền giá trị | Ràng buộc theo đặc tả | Nguồn |
| --- | --- | --- | --- | --- | --- |
| I1 | Trạng thái hiện tại của đơn | Tiền điều kiện (dữ liệu) | {`pending`, `confirmed`, `shipping`, `delivered`, `canceled`} | Xác định các chuyển đổi được phép | FR-10 |
| I2 | Trạng thái đích Admin yêu cầu | Web Admin: nút thao tác; API: trường `status` | chuỗi | Phải là chuyển đổi có trên sơ đồ; giá trị thuộc 5 trạng thái | FR-10, `api_specification.md` 6.2 |
| I3 | Yêu cầu hủy của User | Web: nút "Hủy đơn"; API: `PUT /api/orders/:id/cancel` | thao tác | Chỉ khi đơn `pending` / `confirmed`; không được khi `shipping` | FR-10 |
| I4 | Tác nhân | Tài khoản thực hiện | {Admin, User chủ đơn, User khác} | Admin xác nhận / giao / hoàn tất / hủy; User hủy | FR-10 (sơ đồ) |
| I5 | Mã đơn | Dòng được bấm; `:id` trên URL | số nguyên | Phải là đơn đang tồn tại | FR-10 |

Vì trạng thái có thứ tự `pending (0) < confirmed (1) < shipping (2) < delivered (3)` (`canceled` là nhánh riêng), chuyển đổi tiến hợp lệ là **khoảng cách d = thứ tự đích − thứ tự hiện tại = +1**; đại lượng d dùng cho phân tích biên ở bước 4.

#### 1.3 Biến đầu ra

| ID | Biến | Giá trị có thể có | Nguồn |
| --- | --- | --- | --- |
| O1 | Trạng thái đơn sau thao tác | trạng thái mới (thành công) / giữ nguyên (bị từ chối) | FR-10 |
| O2 | Phản hồi | Thành công; lỗi kèm thông báo phù hợp (4xx); không tìm thấy (404) | FR-10 ("Mọi chuyển đổi không hợp lệ phải trả về lỗi với thông báo phù hợp"); A5 |
| O3 | Các đơn khác | Giữ nguyên / bị thay đổi | A5 |
| O4 | Thao tác giao diện hiển thị cho từng trạng thái | Tập nút trên Web Admin / trang Hồ sơ | A7 |

#### 1.4 Giả định cho những chỗ đặc tả chưa rõ

| ID | Giả định | Căn cứ |
| --- | --- | --- |
| A1 | Admin **không** được chuyển `shipping → canceled`; câu "khi shipping … chỉ Admin mới có thể thao tác" hiểu là Admin tiếp tục chuyển `shipping → delivered` | Sơ đồ không có cạnh `shipping → canceled`; "mọi chuyển đổi không hợp lệ phải trả về lỗi". Cần TA xác nhận |
| A2 | Chuyển sang chính trạng thái hiện tại (vd `pending → pending`) không hợp lệ | Không có trên sơ đồ |
| A3 | Bỏ bước (`pending → shipping`, `pending → delivered`, `confirmed → delivered`) và lùi trạng thái không hợp lệ | Không có trên sơ đồ |
| A4 | `status` phải đúng một trong 5 chuỗi chữ thường; giá trị khác (sai hoa / thường, có khoảng trắng, rỗng, thiếu trường) không hợp lệ | `api_specification.md` 6.2 liệt kê đúng 5 giá trị |
| A5 | Bị từ chối: trả 4xx kèm thông báo, trạng thái đơn và các đơn khác giữ nguyên; đơn không tồn tại: 404 | Quy ước REST; FR-10 |
| A6 | User chỉ hủy được đơn của chính mình | FR-11 ("chỉ xem được đơn hàng của chính mình") |
| A7 | Giao diện chỉ hiển thị thao tác tương ứng chuyển đổi hợp lệ của trạng thái hiện tại | Giao diện là một kênh nhập của miền I2 / I3 |
| A8 | Kênh API dùng token đúng vai trò (Admin / User) | Kiểm soát truy cập thuộc FR-12 (ngoài phạm vi) |

#### 1.5 Ngoài phạm vi

- Gọi API Admin bằng token User hoặc không có token (FR-12); hủy đơn trên Mobile (Pool D – FR-20); hiển thị lịch sử đơn (FR-11), tính doanh thu (FR-13).

### 2. Bước 2 – Lớp tương đương (Complete Set of Partitions)

#### 2.1 Cách áp dụng guideline cho từng biến

| Biến | Điều kiện trong đặc tả | Guideline [S04] | Lớp tạo ra |
| --- | --- | --- | --- |
| I1 × I2 (Admin đổi trạng thái) | Sơ đồ có 5 cạnh: `pending→confirmed`, `confirmed→shipping`, `shipping→delivered`, `pending→canceled`, `confirmed→canceled` | Tập giá trị được xử lý khác nhau (mỗi cạnh là một thao tác riêng: Xác nhận / Giao hàng / Hoàn thành / Hủy) → mỗi cạnh 1 lớp valid | 5 lớp valid |
| | "`delivered` và `canceled` là trạng thái kết thúc"; "mọi chuyển đổi không hợp lệ phải trả về lỗi" | "Phải là" cạnh trên sơ đồ → lớp invalid; tách lớp (G5) theo kiểu sai vì mỗi kiểu có thể bị một điều kiện khác bỏ sót: đi ra từ `delivered`, đi ra từ `canceled` (giao diện còn hiện nút cho đơn đã hủy), bỏ bước (d ≥ 2), lùi (d ≤ −1), giữ nguyên (d = 0), `shipping→canceled` (A1) | 6 lớp invalid |
| I3 (User hủy) | "User/Admin hủy" từ `pending`, `confirmed`; "khi `shipping` User không được tự hủy" | "Phải là" đơn `pending` / `confirmed`; tách lớp (G5) theo trạng thái hiện tại vì mỗi trạng thái có thể được kiểm tra riêng | 2 lớp valid; `shipping`, `delivered`, `canceled` (3 lớp invalid) |
| I4 (Tác nhân) | User hủy đơn của mình (A6) | "Phải là" chủ đơn | User khác hủy (invalid) |
| I2 giá trị `status` | 5 giá trị (`api_specification.md` 6.2) | "Phải là" một trong tập → 1 valid + 1 invalid (ngoài tập); tách lớp (G5): sai hoa / thường, rỗng, thiếu trường (A4) | 1 valid, 4 invalid |
| I5 Mã đơn | Đơn đang tồn tại | "Phải là" → tồn tại / không tồn tại; tách lớp (G5): id không phải số | 1 valid, 2 invalid |
| Đầu ra O1–O4 | thành công / từ chối / không tìm thấy / thao tác giao diện | Phân vùng đầu ra như ví dụ [UC] | 5 lớp đầu ra |

#### 2.2 Complete Set of Partitions

| EC | Biến | Phân vùng | Ví dụ đại diện | Valid / Invalid |
| --- | --- | --- | --- | --- |
| EC1 | I1 × I2 Admin | `pending → confirmed` (Xác nhận) | đơn `pending`, `status = confirmed` | Valid |
| EC2 | I1 × I2 Admin | `confirmed → shipping` (Giao hàng) | | Valid |
| EC3 | I1 × I2 Admin | `shipping → delivered` (Hoàn thành) | | Valid |
| EC4 | I1 × I2 Admin | `pending → canceled` (Hủy) | | Valid |
| EC5 | I1 × I2 Admin | `confirmed → canceled` (Hủy) | | Valid |
| EC6 | I3 User | Hủy đơn `pending` của mình | | Valid |
| EC7 | I3 User | Hủy đơn `confirmed` của mình | | Valid |
| EC8 | I1 × I2 Admin | Đi ra từ `delivered` (trạng thái kết thúc) | `delivered → canceled` | Invalid |
| EC9 | I1 × I2 Admin | Đi ra từ `canceled` (trạng thái kết thúc) | `canceled → delivered` | Invalid |
| EC10 | I1 × I2 Admin | Bỏ bước tiến (d ≥ 2) (A3) | `pending → shipping` | Invalid |
| EC11 | I1 × I2 Admin | Lùi trạng thái (d ≤ −1) (A3) | `shipping → confirmed` | Invalid |
| EC12 | I1 × I2 Admin | Giữ nguyên trạng thái (d = 0) (A2) | `confirmed → confirmed` | Invalid |
| EC13 | I1 × I2 Admin | `shipping → canceled` (A1) | | Invalid |
| EC14 | I3 User | Hủy đơn `shipping` | | Invalid |
| EC15 | I3 User | Hủy đơn `delivered` | | Invalid |
| EC16 | I3 User | Hủy đơn `canceled` | | Invalid |
| EC17 | I4 | User hủy đơn của người khác (A6) | | Invalid |
| EC18 | I2 `status` | Một trong 5 giá trị chữ thường | `confirmed` | Valid |
| EC19 | I2 `status` | Ngoài tập (A4) | `abc` | Invalid |
| EC20 | I2 `status` | Sai chữ hoa / thường (A4) | `Confirmed` | Invalid |
| EC21 | I2 `status` | Rỗng (A4) | `` | Invalid |
| EC22 | I2 `status` | Thiếu trường `status` (A4) | `{}` | Invalid |
| EC23 | I5 Mã đơn | Đơn đang tồn tại | id `1` | Valid |
| EC24 | I5 Mã đơn | Không tồn tại | `9999` | Invalid |
| EC25 | I5 Mã đơn | Không phải số | `abc` | Invalid |
| EC26 | O1, O3 | Chuyển thành công: đơn có trạng thái mới, các đơn khác giữ nguyên | | Output |
| EC27 | O1, O2 | Từ chối chuyển đổi không hợp lệ: 4xx + thông báo, trạng thái giữ nguyên | | Output |
| EC28 | O1, O2 | Từ chối giá trị `status` không hợp lệ: 4xx, trạng thái giữ nguyên | | Output |
| EC29 | O2 | Không tìm thấy đơn: 404 | | Output |
| EC30 | O4 | Giao diện chỉ hiện thao tác của chuyển đổi hợp lệ cho trạng thái hiện tại (A7) | | Output |

Tổng: 25 lớp đầu vào (9 valid, 16 invalid) và 5 lớp đầu ra.

### 3. Bước 3 – Test case Domain Testing

#### 3.1 Thủ tục thực hiện

Mọi test case dùng chung thủ tục, chỉ dữ liệu thay đổi → dạng **data matrix** [DR]. ID có tiền tố `FR10-`. Trong bảng: `(bỏ trống / không gửi)` là không gửi trường `status`; `(rỗng)` là chuỗi rỗng; `␣` là một dấu cách.

**Tiền điều kiện chung – dựng trước mỗi test case (self-standing, self-cleaning)**

1. Khởi động lại backend (dữ liệu seed, chưa có đơn).
2. Đăng ký User B `fr10.userb@example.com / Abcdef1@` (`POST /api/register`).
3. Tạo đơn bằng `POST /api/checkout` và đưa về trạng thái bằng các chuyển đổi hợp lệ của Admin:

| Đơn | Chủ đơn | Trạng thái | Cách dựng |
| --- | --- | --- | --- |
| #1 | `test@eshop.com` | `pending` | tạo mới |
| #2 | `test@eshop.com` | `confirmed` | `pending → confirmed` |
| #3 | `test@eshop.com` | `shipping` | `pending → confirmed → shipping` |
| #4 | `test@eshop.com` | `delivered` | `pending → confirmed → shipping → delivered` |
| #5 | `test@eshop.com` | `canceled` | `pending → canceled` |
| #6 | `test@eshop.com` | `pending` | tạo mới |
| #7 | User B | `pending` | tạo mới |

4. Đọc `GET /api/admin/orders`, kiểm tra đúng bảng trên; nếu không dựng được, test case **Blocked**.

**P-WEB-ADMIN** – Web Admin `http://localhost:5174` (đăng nhập `admin@eshop.com`) → tab "Đơn hàng" → ở dòng đơn theo cột dữ liệu bấm nút ứng với trạng thái đích (Xác nhận → `confirmed`, Giao hàng → `shipping`, Hoàn thành → `delivered`, Hủy → `canceled`, Đánh dấu Đã giao → `delivered`), chấp nhận hộp thoại nếu có.

**P-WEB-USER** – Web `http://localhost:5173` đăng nhập `test@eshop.com / Test1234!` → trang Hồ sơ → "Lịch sử đơn hàng" → bấm "Hủy đơn" ở đơn theo cột dữ liệu, chấp nhận hộp thoại nếu có.

**P-API** – Admin: `PUT /api/admin/orders/<đơn>/status` body `{"status": <giá trị>}` với token Admin. User: `PUT /api/orders/<đơn>/cancel` với token của tác nhân.

**Kiểm chứng (mọi kênh):** so `GET /api/admin/orders` trước / sau – trạng thái đơn được thao tác và các đơn khác; với kênh API kiểm tra thêm mã HTTP và thông báo.

Chuyển đổi không có nút trên giao diện chỉ chạy P-API; việc giao diện không có nút được kiểm tra riêng ở FR10-DT-26, FR10-DT-27.

#### 3.2 Minimum Set of Test Cases

Dữ liệu và kết quả mong đợi được sinh từ `scripts/fr10/cases.py` (cùng nguồn với script thực thi) bằng `scripts/fr10/report_tables.py`.

<!-- BEGIN:T32 -->
**Test case valid** – mỗi test case phủ nhiều lớp valid nhất có thể:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Tác nhân | Thao tác | Đơn | Trạng thái hiện tại | Giá trị `status` | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR10-DT-01 | Kiểm tra Admin xác nhận đơn đang chờ xác nhận thành công | EC1, EC18, EC23, EC26 | Admin | Đổi trạng thái | #1 | `pending` | `confirmed` | Đơn #1 chuyển `pending` → `confirmed`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-02 | Kiểm tra Admin chuyển đơn đã xác nhận sang đang giao thành công | EC2, EC18, EC23, EC26 | Admin | Đổi trạng thái | #2 | `confirmed` | `shipping` | Đơn #2 chuyển `confirmed` → `shipping`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-03 | Kiểm tra Admin hoàn tất đơn đang giao thành công | EC3, EC18, EC23, EC26 | Admin | Đổi trạng thái | #3 | `shipping` | `delivered` | Đơn #3 chuyển `shipping` → `delivered`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-04 | Kiểm tra Admin hủy đơn đang chờ xác nhận thành công | EC4, EC18, EC23, EC26 | Admin | Đổi trạng thái | #1 | `pending` | `canceled` | Đơn #1 chuyển `pending` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-05 | Kiểm tra Admin hủy đơn đã xác nhận thành công | EC5, EC18, EC23, EC26 | Admin | Đổi trạng thái | #2 | `confirmed` | `canceled` | Đơn #2 chuyển `confirmed` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-06 | Kiểm tra User hủy đơn đang chờ xác nhận của mình thành công | EC6, EC23, EC26 | User chủ đơn | Hủy đơn | #1 | `pending` | – | Đơn #1 chuyển `pending` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-07 | Kiểm tra User hủy đơn đã xác nhận của mình thành công | EC7, EC23, EC26 | User chủ đơn | Hủy đơn | #2 | `confirmed` | – | Đơn #2 chuyển `confirmed` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-26 | Kiểm tra Web Admin chỉ hiện thao tác hợp lệ cho từng trạng thái đơn | EC30 (Admin) | Admin | Xem tab Đơn hàng | #1–#5 | – | – | Web Admin hiện: Chờ xác nhận – Xác nhận, Hủy; Đã xác nhận – Giao hàng, Hủy; Đang giao – Hoàn thành; Đã giao, Đã hủy – không có nút (EC30) | Web | AI |
| FR10-DT-27 | Kiểm tra trang Hồ sơ chỉ hiện nút Hủy đơn cho đơn được phép hủy | EC30 (User) | User chủ đơn | Xem Lịch sử đơn hàng | #1–#5 | – | – | Trang Hồ sơ hiện nút "Hủy đơn" chỉ ở đơn Chờ xác nhận, Đã xác nhận; không có ở Đang giao, Đã giao, Đã hủy (EC30) | Web | AI |

**Test case invalid** – mỗi test case phủ đúng một lớp invalid, các biến còn lại hợp lệ:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Tác nhân | Thao tác | Đơn | Trạng thái hiện tại | Giá trị `status` | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR10-DT-08 | Kiểm tra Admin chuyển đơn đã giao sang đã hủy bị từ chối | EC8, EC27 | Admin | Đổi trạng thái | #4 | `delivered` | `canceled` | Từ chối, báo chuyển đổi không hợp lệ; đơn #4 giữ `delivered`; các đơn khác giữ nguyên; API trả 4xx (EC27) | API | AI |
| FR10-DT-09 | Kiểm tra Admin chuyển đơn đã hủy sang đã giao bị từ chối | EC9, EC27 | Admin | Đổi trạng thái | #5 | `canceled` | `delivered` | Từ chối, báo chuyển đổi không hợp lệ; đơn #5 giữ `canceled`; các đơn khác giữ nguyên; API trả 4xx (EC27); trên Web Admin bấm nút "Đánh dấu Đã giao" có sẵn ở đơn đã hủy | Web, API | AI |
| FR10-DT-10 | Kiểm tra Admin chuyển đơn chờ xác nhận thẳng sang đang giao bị từ chối | EC10, EC27 | Admin | Đổi trạng thái | #1 | `pending` | `shipping` | Từ chối, báo chuyển đổi không hợp lệ; đơn #1 giữ `pending`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| FR10-DT-11 | Kiểm tra Admin chuyển đơn đang giao lùi về đã xác nhận bị từ chối | EC11, EC27 | Admin | Đổi trạng thái | #3 | `shipping` | `confirmed` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| FR10-DT-12 | Kiểm tra Admin chuyển đơn đã xác nhận sang chính trạng thái đã xác nhận bị từ chối | EC12, EC27 | Admin | Đổi trạng thái | #2 | `confirmed` | `confirmed` | Từ chối, báo chuyển đổi không hợp lệ; đơn #2 giữ `confirmed`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | AI |
| FR10-DT-13 | Kiểm tra Admin hủy đơn đang giao bị từ chối | EC13, EC27 | Admin | Đổi trạng thái | #3 | `shipping` | `canceled` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A1 | API | AI |
| FR10-DT-14 | Kiểm tra User hủy đơn đang giao bị từ chối | EC14, EC27 | User chủ đơn | Hủy đơn | #3 | `shipping` | – | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); trên Web bấm nút "Hủy đơn" có sẵn ở đơn đang giao | Web, API | AI |
| FR10-DT-15 | Kiểm tra User hủy đơn đã giao bị từ chối | EC15, EC27 | User chủ đơn | Hủy đơn | #4 | `delivered` | – | Từ chối, báo chuyển đổi không hợp lệ; đơn #4 giữ `delivered`; các đơn khác giữ nguyên; API trả 4xx (EC27) | API | AI |
| FR10-DT-16 | Kiểm tra User hủy đơn đã hủy bị từ chối | EC16, EC27 | User chủ đơn | Hủy đơn | #5 | `canceled` | – | Từ chối, báo chuyển đổi không hợp lệ; đơn #5 giữ `canceled`; các đơn khác giữ nguyên; API trả 4xx (EC27) | API | AI |
| FR10-DT-17 | Kiểm tra User hủy đơn của người dùng khác bị từ chối | EC17, EC27 | User khác (test@eshop.com hủy đơn của User B) | Hủy đơn | #7 | `pending` | – | Từ chối, báo chuyển đổi không hợp lệ; đơn #7 giữ `pending`; các đơn khác giữ nguyên; API trả 4xx (EC27); A6; đơn #7 của User B giữ `pending` | API | AI |
| FR10-DT-18 | Kiểm tra Admin đổi trạng thái bị từ chối khi status ngoài tập | EC19, EC28 | Admin | Đổi trạng thái | #1 | `pending` | `abc` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28) | API | AI |
| FR10-DT-19 | Kiểm tra Admin đổi trạng thái bị từ chối khi status sai chữ hoa / thường | EC20, EC28 | Admin | Đổi trạng thái | #1 | `pending` | `Confirmed` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28) | API | AI |
| FR10-DT-20 | Kiểm tra Admin đổi trạng thái bị từ chối khi status rỗng | EC21, EC28 | Admin | Đổi trạng thái | #1 | `pending` | (rỗng) | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28) | API | AI |
| FR10-DT-21 | Kiểm tra Admin đổi trạng thái bị từ chối khi không gửi status | EC22, EC28 | Admin | Đổi trạng thái | #1 | `pending` | (bỏ trống / không gửi) | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28) | API | AI |
| FR10-DT-22 | Kiểm tra Admin đổi trạng thái đơn không tồn tại bị từ chối | EC24 (Admin), EC29 | Admin | Đổi trạng thái | #9999 | – | `confirmed` | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| FR10-DT-23 | Kiểm tra Admin đổi trạng thái bị từ chối khi mã đơn không phải số | EC25 (Admin), EC29 | Admin | Đổi trạng thái | `abc` | – | `confirmed` | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| FR10-DT-24 | Kiểm tra User hủy đơn không tồn tại bị từ chối | EC24 (User), EC29 | User chủ đơn | Hủy đơn | #9999 | – | – | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| FR10-DT-25 | Kiểm tra User hủy đơn bị từ chối khi mã đơn không phải số | EC25 (User), EC29 | User chủ đơn | Hủy đơn | `abc` | – | – | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
<!-- END:T32 -->

#### 3.3 Bảng phủ phân vùng

<!-- BEGIN:T33 -->
| EC | Test case phủ | | EC | Test case phủ |
| --- | --- | --- | --- | --- |
| EC1 | FR10-DT-01 | | EC16 | FR10-DT-16 |
| EC2 | FR10-DT-02 | | EC17 | FR10-DT-17 |
| EC3 | FR10-DT-03 | | EC18 | FR10-DT-01…FR10-DT-05 |
| EC4 | FR10-DT-04 | | EC19 | FR10-DT-18 |
| EC5 | FR10-DT-05 | | EC20 | FR10-DT-19 |
| EC6 | FR10-DT-06 | | EC21 | FR10-DT-20 |
| EC7 | FR10-DT-07 | | EC22 | FR10-DT-21 |
| EC8 | FR10-DT-08 | | EC23 | FR10-DT-01…FR10-DT-07 |
| EC9 | FR10-DT-09 | | EC24 | FR10-DT-22, FR10-DT-24 |
| EC10 | FR10-DT-10 | | EC25 | FR10-DT-23, FR10-DT-25 |
| EC11 | FR10-DT-11 | | EC26 | FR10-DT-01…FR10-DT-07 |
| EC12 | FR10-DT-12 | | EC27 | FR10-DT-08…FR10-DT-17 |
| EC13 | FR10-DT-13 | | EC28 | FR10-DT-18…FR10-DT-21 |
| EC14 | FR10-DT-14 | | EC29 | FR10-DT-22…FR10-DT-25 |
| EC15 | FR10-DT-15 | | EC30 | FR10-DT-26, FR10-DT-27 |

30 / 30 lớp được phủ bởi 27 test case Minimum Set (9 valid, 18 invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp invalid có test case riêng.
<!-- END:T33 -->

### 4. Bước 4 – Boundary Value Analysis

#### 4.1 Xác định biên

Trạng thái `pending (0) < confirmed (1) < shipping (2) < delivered (3)` có thứ tự, nên BVA áp dụng cho khoảng cách **d = thứ tự đích − thứ tự hiện tại**: chuyển tiến hợp lệ chỉ khi d = +1 (vừa là LB vừa là UB), nên các điểm biên là d = 0 (UB−1), d = +1, d = +2 (UB+1), cùng d âm (lùi) và giá trị lớn nhất. Ngoài ra xét vùng "được hủy" `{pending, confirmed}` (UB = `confirmed`, UB+1 = `shipping`), độ dài chuỗi `status` quanh giá trị hợp lệ `confirmed`, và mã đơn của bộ dữ liệu (#1–#7).

| Biến | Phân vùng | LB | UB | Bước nhảy | Điểm kiểm tra |
| --- | --- | --- | --- | --- | --- |
| d từ `pending` | EC12 (d = 0) / EC1 (d = +1) / EC10 (d ≥ 2) | +1 | +1 | 1 trạng thái | 0, +1, +2, +3 |
| d từ `confirmed` | EC11 (d < 0) / EC12 / EC2 / EC10 | +1 | +1 | 1 trạng thái | −1, 0, +1, +2 |
| d từ `shipping` | EC11 / EC12 / EC3 | +1 | +1 | 1 trạng thái | −2, −1, 0, +1 |
| d từ `delivered` (kết thúc) | EC8 | – | – | 1 trạng thái | −1, 0 |
| `canceled` (kết thúc) | EC9 | – | – | – | → `canceled`, → `pending` |
| Vùng được hủy (Admin, User) | EC4/EC5, EC6/EC7 (valid) / EC13, EC14 (invalid) | `pending` | `confirmed` | 1 trạng thái | `confirmed` (UB), `shipping` (UB+1) |
| Chuỗi `status` | EC18 / EC19 | `confirmed` (9 ký tự) | `confirmed` | 1 ký tự | thiếu 1 ký tự, thừa 1 ký tự, thừa 1 khoảng trắng đầu / cuối |
| Mã đơn Admin | EC24 / EC23 (#1–#7) | 1 | 7 | 1 | 0, 1, 7, 8 |
| Mã đơn User (đơn của mình #1–#6) | EC24 / EC23 | 1 | 6 | 1 | 0, 6, 8 |

#### 4.2 Boundary Value Test Cases

Thủ tục: mục 3.1 (chỉ chạy P-API – giao diện không có thao tác cho các điểm biên này). Dòng có ID trong ngoặc là điểm biên đã có trong Minimum Set, chỉ dẫn chiếu.

<!-- BEGIN:T42 -->
| ID | Tên test case (Action + Function + Condition) | Partition tested | Tác nhân | Thao tác | Đơn | Trạng thái hiện tại | Giá trị `status` | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR10-BV-01 | Kiểm tra Admin chuyển đơn chờ xác nhận sang chính nó bị từ chối | `pending`: d = 0 (UB-1) | Admin | Đổi trạng thái | #1 | `pending` | `pending` | Từ chối, báo chuyển đổi không hợp lệ; đơn #1 giữ `pending`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | AI |
| (FR10-DT-01) | Kiểm tra Admin xác nhận đơn đang chờ xác nhận thành công | `pending`: d = +1 (UB – cạnh hợp lệ) | Admin | Đổi trạng thái | #1 | `pending` | `confirmed` | Đơn #1 chuyển `pending` → `confirmed`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| (FR10-DT-10) | Kiểm tra Admin chuyển đơn chờ xác nhận thẳng sang đang giao bị từ chối | `pending`: d = +2 (UB+1) | Admin | Đổi trạng thái | #1 | `pending` | `shipping` | Từ chối, báo chuyển đổi không hợp lệ; đơn #1 giữ `pending`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | xem 3.2 |
| FR10-BV-02 | Kiểm tra Admin chuyển đơn chờ xác nhận thẳng sang đã giao bị từ chối | `pending`: d = +3 (lớn nhất) | Admin | Đổi trạng thái | #1 | `pending` | `delivered` | Từ chối, báo chuyển đổi không hợp lệ; đơn #1 giữ `pending`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| FR10-BV-03 | Kiểm tra Admin chuyển đơn đã xác nhận lùi về chờ xác nhận bị từ chối | `confirmed`: d = −1 | Admin | Đổi trạng thái | #2 | `confirmed` | `pending` | Từ chối, báo chuyển đổi không hợp lệ; đơn #2 giữ `confirmed`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| (FR10-DT-12) | Kiểm tra Admin chuyển đơn đã xác nhận sang chính trạng thái đã xác nhận bị từ chối | `confirmed`: d = 0 (UB-1) | Admin | Đổi trạng thái | #2 | `confirmed` | `confirmed` | Từ chối, báo chuyển đổi không hợp lệ; đơn #2 giữ `confirmed`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | xem 3.2 |
| (FR10-DT-02) | Kiểm tra Admin chuyển đơn đã xác nhận sang đang giao thành công | `confirmed`: d = +1 (UB) | Admin | Đổi trạng thái | #2 | `confirmed` | `shipping` | Đơn #2 chuyển `confirmed` → `shipping`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| FR10-BV-04 | Kiểm tra Admin chuyển đơn đã xác nhận thẳng sang đã giao bị từ chối | `confirmed`: d = +2 (UB+1) | Admin | Đổi trạng thái | #2 | `confirmed` | `delivered` | Từ chối, báo chuyển đổi không hợp lệ; đơn #2 giữ `confirmed`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| FR10-BV-05 | Kiểm tra Admin chuyển đơn đang giao lùi về chờ xác nhận bị từ chối | `shipping`: d = −2 | Admin | Đổi trạng thái | #3 | `shipping` | `pending` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| (FR10-DT-11) | Kiểm tra Admin chuyển đơn đang giao lùi về đã xác nhận bị từ chối | `shipping`: d = −1 (UB-2) | Admin | Đổi trạng thái | #3 | `shipping` | `confirmed` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | xem 3.2 |
| FR10-BV-06 | Kiểm tra Admin chuyển đơn đang giao sang chính nó bị từ chối | `shipping`: d = 0 | Admin | Đổi trạng thái | #3 | `shipping` | `shipping` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | AI |
| (FR10-DT-03) | Kiểm tra Admin hoàn tất đơn đang giao thành công | `shipping`: d = +1 (UB) | Admin | Đổi trạng thái | #3 | `shipping` | `delivered` | Đơn #3 chuyển `shipping` → `delivered`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| FR10-BV-07 | Kiểm tra Admin chuyển đơn đã giao lùi về đang giao bị từ chối | `delivered` (kết thúc): d = −1 | Admin | Đổi trạng thái | #4 | `delivered` | `shipping` | Từ chối, báo chuyển đổi không hợp lệ; đơn #4 giữ `delivered`; các đơn khác giữ nguyên; API trả 4xx (EC27) | API | AI |
| FR10-BV-08 | Kiểm tra Admin chuyển đơn đã giao sang chính nó bị từ chối | `delivered` (kết thúc): d = 0 | Admin | Đổi trạng thái | #4 | `delivered` | `delivered` | Từ chối, báo chuyển đổi không hợp lệ; đơn #4 giữ `delivered`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | AI |
| (FR10-DT-05) | Kiểm tra Admin hủy đơn đã xác nhận thành công | Vùng được hủy {pending, confirmed} – Admin hủy `confirmed` (UB) | Admin | Đổi trạng thái | #2 | `confirmed` | `canceled` | Đơn #2 chuyển `confirmed` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| (FR10-DT-13) | Kiểm tra Admin hủy đơn đang giao bị từ chối | Admin hủy `shipping` (UB+1, A1) | Admin | Đổi trạng thái | #3 | `shipping` | `canceled` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A1 | API | xem 3.2 |
| (FR10-DT-07) | Kiểm tra User hủy đơn đã xác nhận của mình thành công | User hủy `confirmed` (UB) | User chủ đơn | Hủy đơn | #2 | `confirmed` | – | Đơn #2 chuyển `confirmed` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| (FR10-DT-14) | Kiểm tra User hủy đơn đang giao bị từ chối | User hủy `shipping` (UB+1) | User chủ đơn | Hủy đơn | #3 | `shipping` | – | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); trên Web bấm nút "Hủy đơn" có sẵn ở đơn đang giao | Web, API | xem 3.2 |
| FR10-BV-09 | Kiểm tra Admin hủy lại đơn đã hủy bị từ chối | `canceled` (kết thúc) → `canceled` | Admin | Đổi trạng thái | #5 | `canceled` | `canceled` | Từ chối, báo chuyển đổi không hợp lệ; đơn #5 giữ `canceled`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | AI |
| FR10-BV-10 | Kiểm tra Admin khôi phục đơn đã hủy về chờ xác nhận bị từ chối | `canceled` (kết thúc) → `pending` | Admin | Đổi trạng thái | #5 | `canceled` | `pending` | Từ chối, báo chuyển đổi không hợp lệ; đơn #5 giữ `canceled`; các đơn khác giữ nguyên; API trả 4xx (EC27) | API | AI |
| FR10-BV-11 | Kiểm tra Admin đổi trạng thái bị từ chối khi status thừa 1 khoảng trắng đầu | `confirmed` + 1 ký tự ở đầu | Admin | Đổi trạng thái | #1 | `pending` | `␣confirmed` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28); A4 | API | AI |
| FR10-BV-12 | Kiểm tra Admin đổi trạng thái bị từ chối khi status thừa 1 khoảng trắng cuối | `confirmed` + 1 ký tự ở cuối | Admin | Đổi trạng thái | #1 | `pending` | `confirmed␣` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28); A4 | API | AI |
| FR10-BV-13 | Kiểm tra Admin đổi trạng thái bị từ chối khi status thiếu 1 ký tự | độ dài `confirmed` − 1 | Admin | Đổi trạng thái | #1 | `pending` | `confirme` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28); A4 | API | AI |
| FR10-BV-14 | Kiểm tra Admin đổi trạng thái bị từ chối khi status thừa 1 ký tự | độ dài `confirmed` + 1 | Admin | Đổi trạng thái | #1 | `pending` | `confirmedd` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28); A4 | API | AI |
| FR10-BV-15 | Kiểm tra Admin đổi trạng thái đơn mã 0 bị từ chối | mã đơn 0 (LB-1) | Admin | Đổi trạng thái | #0 | – | `confirmed` | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| (FR10-DT-01) | Kiểm tra Admin xác nhận đơn đang chờ xác nhận thành công | mã đơn 1 (LB) | Admin | Đổi trạng thái | #1 | `pending` | `confirmed` | Đơn #1 chuyển `pending` → `confirmed`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| FR10-BV-16 | Kiểm tra Admin xác nhận đơn có mã lớn nhất đang tồn tại thành công | mã đơn 7 (UB) | Admin | Đổi trạng thái | #7 | `pending` | `confirmed` | Đơn #7 chuyển `pending` → `confirmed`; các đơn khác giữ nguyên; API trả 2xx (EC26) | API | AI |
| FR10-BV-17 | Kiểm tra Admin đổi trạng thái đơn mã 8 bị từ chối | mã đơn 8 (UB+1) | Admin | Đổi trạng thái | #8 | – | `confirmed` | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| FR10-BV-18 | Kiểm tra User hủy đơn mã 0 bị từ chối | mã đơn 0 (LB-1) | User chủ đơn | Hủy đơn | #0 | – | – | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| FR10-BV-19 | Kiểm tra User hủy đơn có mã lớn nhất của mình thành công | mã đơn 6 (UB của User) | User chủ đơn | Hủy đơn | #6 | `pending` | – | Đơn #6 chuyển `pending` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | API | AI |
| FR10-BV-20 | Kiểm tra User hủy đơn mã 8 bị từ chối | mã đơn 8 (UB+1) | User chủ đơn | Hủy đơn | #8 | – | – | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |

Tổng: 20 test case BVA mới (FR10-BV-01…FR10-BV-20); 11 dòng có ID trong ngoặc là điểm biên đã được phủ bởi test case Minimum Set (mục 3.2), chỉ dẫn chiếu, không chạy lại.
<!-- END:T42 -->

### 5. Bước 5 – Kết quả thực thi

#### 5.1 Môi trường và cách chạy

| Mục | Giá trị |
| --- | --- |
| Ngày chạy | 2026-10-20 |
| Người chạy | 23120031 (script tự động, kết quả được rà soát thủ công) |
| SUT | `eshop-sut-main` (trùng với `d1nhnguyen/eshop-sut`), Node 20.19.5 |
| Web | Web Admin `http://localhost:5174`, Web `http://localhost:5173`, Chrome 155 (headless, Playwright) |
| API | `http://localhost:3000/api`, gọi bằng Python `urllib` với token Admin / `test@eshop.com` |
| Dữ liệu | Bộ dữ liệu 7 đơn (mục 3.1) được dựng lại **trước mỗi test case** (`scripts/fr10/fixture.py`) |
| Script | `scripts/fr10/cases.py` (dữ liệu), `fixture.py`, `run_web.mjs` (P-WEB-ADMIN / P-WEB-USER), `run_api.py` (P-API), `report_tables.py` |
| Bằng chứng | `evidence/FR-10/web_results.json`, `api_results.json`; ảnh sau thao tác của từng test case `evidence/FR-10/web/<ID>.png` |

Cách kết luận (A5): so trạng thái mọi đơn trước / sau. "Thành công" Pass khi chỉ đơn được thao tác đổi sang đúng trạng thái đích. "Từ chối" Pass khi không đơn nào đổi trạng thái **và** API trả 4xx kèm thông báo (trên Web: không có nút cho thao tác, hoặc có thông báo lỗi). "Không tìm thấy" Pass khi API trả 404.

#### 5.2 Phát hiện chính

- API thực thi đúng phần lớn sơ đồ: 5 cạnh hợp lệ chạy được; bỏ bước, lùi, giữ nguyên, đi ra từ `delivered`, `shipping → canceled`, giá trị `status` sai đều bị từ chối (400 "Invalid state transition from … to …"); đơn không tồn tại / của người khác trả 404.
- **Hai lỗ hổng của sơ đồ:** Admin chuyển được `canceled → delivered` (Web Admin còn hiện sẵn nút "Đánh dấu Đã giao" cho đơn đã hủy); User hủy được đơn `shipping` (trang Hồ sơ hiện nút "Hủy đơn" cho đơn đang giao).
- Thông báo lỗi cho giá trị `status` không hợp lệ dùng chung câu "Invalid state transition from pending to abc"; đặc tả chỉ yêu cầu "thông báo phù hợp" nên không tính là lỗi.

#### 5.3 Kết quả theo test case

Mỗi test case một dòng. Bảng sinh từ `evidence/FR-10/web_results.json` và `api_results.json`.

<!-- BEGIN:T53 -->
| TC | Web | Kết quả thực tế – Web | API | Kết quả thực tế – API | Bằng chứng | Bug |
| --- | --- | --- | --- | --- | --- | --- |
| FR10-DT-01 | Pass | Bấm “Xác nhận”, không có thông báo lỗi; đơn #1 chuyển `pending` → `confirmed` | Pass | HTTP 200 “Order status updated”; đơn #1 chuyển `pending` → `confirmed` | [ảnh Web](../evidence/FR-10/web/FR10-DT-01.png) · `api_results.json` | – |
| FR10-DT-02 | Pass | Bấm “Giao hàng”, không có thông báo lỗi; đơn #2 chuyển `confirmed` → `shipping` | Pass | HTTP 200 “Order status updated”; đơn #2 chuyển `confirmed` → `shipping` | [ảnh Web](../evidence/FR-10/web/FR10-DT-02.png) · `api_results.json` | – |
| FR10-DT-03 | Pass | Bấm “Hoàn thành”, không có thông báo lỗi; đơn #3 chuyển `shipping` → `delivered` | Pass | HTTP 200 “Order status updated”; đơn #3 chuyển `shipping` → `delivered` | [ảnh Web](../evidence/FR-10/web/FR10-DT-03.png) · `api_results.json` | – |
| FR10-DT-04 | Pass | Bấm “Hủy”, không có thông báo lỗi; đơn #1 chuyển `pending` → `canceled` | Pass | HTTP 200 “Order status updated”; đơn #1 chuyển `pending` → `canceled` | [ảnh Web](../evidence/FR-10/web/FR10-DT-04.png) · `api_results.json` | – |
| FR10-DT-05 | Pass | Bấm “Hủy”, không có thông báo lỗi; đơn #2 chuyển `confirmed` → `canceled` | Pass | HTTP 200 “Order status updated”; đơn #2 chuyển `confirmed` → `canceled` | [ảnh Web](../evidence/FR-10/web/FR10-DT-05.png) · `api_results.json` | – |
| FR10-DT-06 | Pass | Bấm “Hủy đơn”, hiện “Hủy đơn thành công!”; đơn #1 chuyển `pending` → `canceled` | Pass | HTTP 200 “Order canceled successfully”; đơn #1 chuyển `pending` → `canceled` | [ảnh Web](../evidence/FR-10/web/FR10-DT-06.png) · `api_results.json` | – |
| FR10-DT-07 | Pass | Bấm “Hủy đơn”, hiện “Hủy đơn thành công!”; đơn #2 chuyển `confirmed` → `canceled` | Pass | HTTP 200 “Order canceled successfully”; đơn #2 chuyển `confirmed` → `canceled` | [ảnh Web](../evidence/FR-10/web/FR10-DT-07.png) · `api_results.json` | – |
| FR10-DT-08 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from delivered to canceled”; đơn #4 giữ nguyên `delivered` | `api_results.json` | – |
| FR10-DT-09 | Fail | Bấm “Đánh dấu Đã giao”, không có thông báo lỗi; đơn #5 chuyển `canceled` → `delivered` | Fail | HTTP 200 “Order status updated”; đơn #5 chuyển `canceled` → `delivered` | [ảnh Web](../evidence/FR-10/web/FR10-DT-09.png) · `api_results.json` | FR10-B1 |
| FR10-DT-10 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to shipping”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-11 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from shipping to confirmed”; đơn #3 giữ nguyên `shipping` | `api_results.json` | – |
| FR10-DT-12 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from confirmed to confirmed”; đơn #2 giữ nguyên `confirmed` | `api_results.json` | – |
| FR10-DT-13 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from shipping to canceled”; đơn #3 giữ nguyên `shipping` | `api_results.json` | – |
| FR10-DT-14 | Fail | Bấm “Hủy đơn”, hiện “Hủy đơn thành công!”; đơn #3 chuyển `shipping` → `canceled` | Fail | HTTP 200 “Order canceled successfully”; đơn #3 chuyển `shipping` → `canceled` | [ảnh Web](../evidence/FR-10/web/FR10-DT-14.png) · `api_results.json` | FR10-B2 |
| FR10-DT-15 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Cannot cancel this order.”; đơn #4 giữ nguyên `delivered` | `api_results.json` | – |
| FR10-DT-16 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Cannot cancel this order.”; đơn #5 giữ nguyên `canceled` | `api_results.json` | – |
| FR10-DT-17 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; đơn #7 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-18 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to abc”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-19 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to Confirmed”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-20 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to ”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-21 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to undefined”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-22 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-DT-23 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-DT-24 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-DT-25 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-DT-26 | Fail | #1 Chờ xác nhận: Xác nhận, Hủy; #2 Đã xác nhận: Giao hàng, Hủy; #3 Đang giao: Hoàn thành; #4 Đã giao: không có nút; #5 Đã hủy: Đánh dấu Đã giao – sai: #5 Đã hủy: có [Đánh dấu Đã giao], mong đợi [không có] | – | Không áp dụng (giao diện không có thao tác này) | [ảnh Web](../evidence/FR-10/web/FR10-DT-26.png) | FR10-B1 |
| FR10-DT-27 | Fail | #1 Chờ xác nhận: Hủy đơn; #2 Đã xác nhận: Hủy đơn; #3 Đang giao: Hủy đơn; #4 Đã giao: không có nút; #5 Đã hủy: không có nút – sai: #3 Đang giao: có [Hủy đơn], mong đợi [không có] | – | Không áp dụng (giao diện không có thao tác này) | [ảnh Web](../evidence/FR-10/web/FR10-DT-27.png) | FR10-B2 |
| FR10-BV-01 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to pending”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-02 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to delivered”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-03 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from confirmed to pending”; đơn #2 giữ nguyên `confirmed` | `api_results.json` | – |
| FR10-BV-04 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from confirmed to delivered”; đơn #2 giữ nguyên `confirmed` | `api_results.json` | – |
| FR10-BV-05 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from shipping to pending”; đơn #3 giữ nguyên `shipping` | `api_results.json` | – |
| FR10-BV-06 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from shipping to shipping”; đơn #3 giữ nguyên `shipping` | `api_results.json` | – |
| FR10-BV-07 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from delivered to shipping”; đơn #4 giữ nguyên `delivered` | `api_results.json` | – |
| FR10-BV-08 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from delivered to delivered”; đơn #4 giữ nguyên `delivered` | `api_results.json` | – |
| FR10-BV-09 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from canceled to canceled”; đơn #5 giữ nguyên `canceled` | `api_results.json` | – |
| FR10-BV-10 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from canceled to pending”; đơn #5 giữ nguyên `canceled` | `api_results.json` | – |
| FR10-BV-11 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to  confirmed”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-12 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to confirmed ”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-13 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to confirme”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-14 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to confirmedd”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-15 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-BV-16 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 200 “Order status updated”; đơn #7 chuyển `pending` → `confirmed` | `api_results.json` | – |
| FR10-BV-17 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-BV-18 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-BV-19 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 200 “Order canceled successfully”; đơn #6 chuyển `pending` → `canceled` | `api_results.json` | – |
| FR10-BV-20 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
<!-- END:T53 -->

#### 5.4 Tổng hợp

<!-- BEGIN:T55 -->
| Kênh | Thiết kế | Đã chạy | Pass | Fail | Blocked | Không áp dụng |
| --- | --- | --- | --- | --- | --- | --- |
| Web | 47 | 11 | 7 | 4 | 0 | 36 |
| API | 47 | 45 | 43 | 2 | 0 | 2 |
| **Tổng lượt chạy** | | **56** | **50** | **6** | **0** | |

47 test case = 27 Minimum Set (mục 3.2) + 20 BVA (mục 4.2). Gộp các kênh theo test case (Fail nếu Fail ở bất kỳ kênh nào, Blocked nếu còn kênh bị Blocked): 43 Pass, 4 Fail, 0 Blocked.
<!-- END:T55 -->

### 6. Bước 6 – AI gap analysis

> G1–G3: AI (Claude Code) tự phát hiện trong lúc làm các bước 1–5 của FR-10. Sinh viên rà soát và bổ sung các điểm tự phát hiện ở commit `[FR-10][Bn-review]`.

#### 6.1 Những gì AI bỏ sót hoặc làm sai

| # | AI bỏ sót / làm sai | Loại | Nguyên nhân | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |
| G1 | Script Web bản đầu tìm dòng đơn bằng biểu thức `#<id>(\D|$)` trên `textContent` của cả dòng; ở trang Hồ sơ các ô nối liền (`#110/20/2026…`) nên không tìm thấy dòng nào → FR10-DT-06, FR10-DT-07 **Fail giả**, FR10-DT-14 **Pass giả** ("không có nút Hủy đơn" bị hiểu là giao diện đã chặn) | Oracle / script | **Giới hạn công cụ AI**: giả định văn bản các ô có khoảng cách; không đối chiếu với quan sát ở bước 1 trước khi kết luận | Kết quả mâu thuẫn với ảnh bước 1 (trang Hồ sơ có nút "Hủy đơn" ở #1, #2, #3) | Tìm dòng theo ô mã đơn khớp chính xác; chạy lại toàn bộ |
| G2 | Oracle của test case "từ chối" chỉ kiểm tra có thông báo, không đánh giá thông báo có "phù hợp" (đặc tả) hay không – vd `status = abc` nhận "Invalid state transition from pending to abc" | Kết quả mong đợi chưa đủ chặt | **Đặc tả mơ hồ**: "thông báo phù hợp" không định nghĩa; AI chọn tiêu chí lỏng | AI rà soát kết quả bước 5 | Ghi nhận ở 6.3, không tính là lỗi |
| G3 | Ghi nhận thông báo trên Web lấy cả dòng đơn vừa đổi trạng thái (`#1 … Đã hủy`) như một "thông báo" | Bằng chứng | **Giới hạn công cụ AI**: so khác biệt văn bản trang trước / sau mà không lọc phần dữ liệu | Đọc output | Lọc khi diễn giải kết quả (mục 5.3) |

#### 6.2 Test case bổ sung

Không bổ sung test case sau rà soát của AI: các lỗi tìm thấy nằm trong phạm vi các lớp đã thiết kế (EC9, EC14, EC30).

#### 6.3 Điểm còn mở (chưa xử lý)

- A1 (Admin không được hủy đơn `shipping`): SUT từ chối `shipping → canceled` đúng theo A1; nếu TA xác nhận Admin được hủy đơn đang giao thì FR10-DT-13 phải đổi kết quả mong đợi.
- Mức độ "phù hợp" của thông báo lỗi (G2) và ngôn ngữ thông báo (API trả tiếng Anh trong khi FR-21 yêu cầu giao diện tiếng Việt – thuộc FR-21).

#### 6.4 Nhận xét

- **Do prompt:** không có yêu cầu đối chiếu kết quả với quan sát bước 1, nên AI suýt chấp nhận kết quả sai của G1; chỉ phát hiện vì kết quả mâu thuẫn rõ với ảnh đã chụp.
- **Do giới hạn công cụ AI:** lỗi lặp lại ở cả 3 feature là oracle / bộ chọn phần tử của script (FR-01 G2, G5; FR-15 G3; FR-10 G1) – AI viết test tự động nhanh nhưng dễ sinh Pass / Fail giả.
- **Do độ phức tạp feature:** lỗi của FR-10 nằm ở hai cạnh lạ (`canceled → delivered`, User hủy `shipping`) mà cả giao diện lẫn API đều cho phép – chỉ phát hiện được nhờ phân vùng tách riêng "đi ra từ `canceled`" và "User hủy `shipping`" (G5).

### 7. Bước 7 – Bug

Chi tiết từng bug: `bugs/Bug_Report.md`. Cột GitHub Issue dẫn tới issue trên repo nhóm `d1nhnguyen/eshop-sut` (ảnh chụp trang issue ở cuối `bugs/Bug_Report.md`).

| Mã | Tiêu đề | Mức độ | Thành phần | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- | --- |
| FR10-B1 | Đơn đã hủy chuyển được sang "Đã giao"; Web Admin hiện nút "Đánh dấu Đã giao" cho đơn đã hủy | Critical | Backend, Web Admin | FR10-DT-09, FR10-DT-26 | [BUG-30](https://github.com/d1nhnguyen/eshop-sut/issues/30) |
| FR10-B2 | User hủy được đơn đang giao; trang Hồ sơ hiện nút "Hủy đơn" cho đơn đang giao | Major | Backend, Web | FR10-DT-14, FR10-DT-27 | [BUG-31](https://github.com/d1nhnguyen/eshop-sut/issues/31) |

Tổng: 2 bug (1 Critical, 1 Major).

## FR-15 – Quản lý sản phẩm (CRUD) · Domain Testing & Boundary Value Analysis

| Mục | Giá trị |
| --- | --- |
| Feature | FR-15 – Quản lý sản phẩm (CRUD) (Pool C) |
| Kênh kiểm thử | Web Admin – tab Sản phẩm (http://localhost:5174) + API `POST/PUT/DELETE /api/products` |
| Người thực hiện | 23120031 |
| Công cụ AI | Claude Code (VS Code extension) |
| Kỹ thuật | Domain Testing (S04 – bước 1–3), Boundary Value Analysis (S04 – bước 4) |

### 0. Đặc tả (trích nguyên văn README của SUT)

> ### FR-15: Quản lý Sản phẩm (Product CRUD)
>
> - Admin có thể Thêm / Xem / Sửa / Xóa sản phẩm.
> - **Ràng buộc đầu vào:**
>   - Tên sản phẩm: bắt buộc, tối đa 255 ký tự.
>   - Giá: bắt buộc, phải là số **dương** (> 0).
>   - Danh mục: bắt buộc, phải chọn từ danh sách có sẵn.
> - Khi Sửa một sản phẩm, chỉ sản phẩm đó bị thay đổi — các sản phẩm khác giữ nguyên.

### 1. Bước 1 – Xác định biến Input / Output

#### 1.1 Quan sát giao diện (hộp đen)

Web Admin `http://localhost:5174` → đăng nhập `admin@eshop.com` → tab "Sản phẩm" (ảnh: `evidence/FR-15/B1_tab_san_pham.png`, `B1_form_sua.png`):

| Thành phần | Quan sát |
| --- | --- |
| Form "Thêm sản phẩm mới" | Không có nhãn, chỉ có placeholder; nút "Lưu sản phẩm" |
| Ô "Tên sản phẩm" | `type="text"`, `required`, không giới hạn độ dài (`maxlength` không đặt) |
| Ô "Giá tiền" | `type="number"`, **không** `required`, không đặt `min` / `step`. Với `0.5` ô báo "The two nearest valid values are 0 and 1" (bước mặc định 1), với `0`, `-1`, `1e3` không báo gì. *Đính chính ở bước 5: dù ô báo như vậy, bấm "Lưu sản phẩm" vẫn gửi và lưu giá thập phân* |
| Ô "URL Ảnh", "Mô tả" | `text`, `textarea`, không bắt buộc |
| Ô Danh mục | `select` gồm `1 = Điện thoại`, `2 = Laptop`, `3 = Phụ kiện`; mặc định chọn `1`; trên giao diện không thể để trống hay chọn giá trị ngoài danh sách |
| Danh sách sản phẩm | Cột Ảnh, Tên SP, Giá, Hành động (Sửa / Xóa); không hiển thị danh mục |
| Nút "Sửa" | Đổ dữ liệu sản phẩm vào cùng form (tiêu đề "Sửa sản phẩm"), thêm nút "Hủy sửa" |
| Nút "Xóa" | Xóa ngay, không hỏi xác nhận (đặc tả FR-15 không yêu cầu xác nhận – chỉ ghi nhận) |

Dữ liệu seed: 5 sản phẩm (id 1–5: iPhone 15 Pro Max – danh mục 1, Samsung Galaxy S24 Ultra – 1, MacBook Pro M3 – 2, Tai nghe AirPods Pro 2 – 3, Bàn phím cơ Keychron Q1 – 3); 3 danh mục (id 1–3).

API (`api_specification.md` mục 3.3): `POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id`, body `{"name", "price", "description", "imageUrl", "category_id"}`; xem: `GET /api/products`, `GET /api/products/:id`.

#### 1.2 Biến đầu vào

| ID | Biến | Kênh nhập | Kiểu / miền giá trị | Ràng buộc theo đặc tả | Nguồn |
| --- | --- | --- | --- | --- | --- |
| I1 | Thao tác | Web: form Thêm / nút Sửa / nút Xóa / danh sách; API: method | {Thêm, Xem, Sửa, Xóa} | Admin thực hiện được cả 4 thao tác | FR-15 |
| I2 | Tên sản phẩm | Web: ô "Tên sản phẩm"; API: `name` | chuỗi ký tự | Bắt buộc; tối đa 255 ký tự | FR-15 |
| I3 | Giá | Web: ô "Giá tiền"; API: `price` | số | Bắt buộc; > 0 | FR-15 |
| I4 | Danh mục | Web: ô chọn danh mục; API: `category_id` | id danh mục | Bắt buộc; thuộc danh sách có sẵn (seed: 1, 2, 3) | FR-15 |
| I5 | Sản phẩm được Sửa / Xóa | Web: dòng được bấm; API: `:id` trên URL | id sản phẩm | Phải là sản phẩm đang tồn tại (seed: 1–5) | FR-15 (Sửa / Xóa một sản phẩm) |
| I6 | Mô tả, URL Ảnh | Web: ô "Mô tả", "URL Ảnh"; API: `description`, `imageUrl` | chuỗi | Không có ràng buộc (A5) | – |

#### 1.3 Biến đầu ra

| ID | Biến | Giá trị có thể có | Nguồn |
| --- | --- | --- | --- |
| O1 | Kết quả thao tác | Thêm / Sửa / Xóa thành công; bị từ chối kèm thông báo lỗi | FR-15 |
| O2 | Phản hồi API | 2xx khi thành công; 4xx khi dữ liệu không hợp lệ; 404 khi sản phẩm không tồn tại (A6) | `api_specification.md`; A6 |
| O3 | Dữ liệu sản phẩm được thao tác | Giá trị Tên / Giá / Danh mục lưu trong hệ thống (`GET /api/products`) và hiển thị trên danh sách Admin | FR-15 (Xem) |
| O4 | Dữ liệu các sản phẩm khác | Giữ nguyên / bị thay đổi | FR-15 ("chỉ sản phẩm đó bị thay đổi") |

#### 1.4 Giả định cho những chỗ đặc tả chưa rõ

| ID | Giả định | Căn cứ |
| --- | --- | --- |
| A1 | "Tối đa 255 ký tự" tính theo ký tự Unicode (chữ có dấu tính 1 ký tự), không theo byte | Đặc tả viết "ký tự" |
| A2 | Tên chỉ gồm khoảng trắng được coi như bỏ trống | "Tên sản phẩm: bắt buộc" |
| A3 | Giá là số dương bất kỳ, kể cả số thập phân (vd `0.01`); không có giới hạn trên – giá trị lớn được lưu và hiển thị đúng | Đặc tả chỉ ghi "số dương (> 0)", không nói số nguyên. Cần TA xác nhận vì đơn vị ₫ thường không có phần lẻ |
| A4 | Giá phải là kiểu số; chuỗi không phải số (vd `"abc"`) không hợp lệ | "phải là số" |
| A5 | Mô tả, URL Ảnh không có ràng buộc → không phân vùng, dùng giá trị hợp lệ cố định | FR-15 không nêu |
| A6 | Khi từ chối: không tạo / không thay đổi sản phẩm, thông báo lỗi nêu đúng trường; API trả 4xx. Sửa / Xóa sản phẩm không tồn tại: API trả 404 | Đặc tả không quy định mã lỗi; quy ước REST |
| A7 | Kênh API luôn gửi token admin hợp lệ | Kiểm soát truy cập thuộc FR-12 (ngoài phạm vi) |
| A8 | Tên chứa ký tự HTML (vd `<b>`) được lưu nguyên và hiển thị dạng văn bản | SEC-04 |
| A9 | Khi Sửa, trường không đổi giữ nguyên giá trị cũ (form điền sẵn giá trị hiện tại) | FR-15 Sửa; quan sát form Sửa |

#### 1.5 Ngoài phạm vi

- Kiểm soát truy cập API sản phẩm (token / role) – FR-12; Import CSV – FR-16; hiển thị sản phẩm phía người dùng – FR-05, FR-06.
- Yêu cầu giao diện chung (nhãn, `*` bắt buộc, định dạng `₫` có phân cách hàng nghìn – FR-21, FR-22).

### 2. Bước 2 – Lớp tương đương (Complete Set of Partitions)

#### 2.1 Cách áp dụng guideline cho từng biến

| Biến | Điều kiện trong đặc tả | Guideline [S04] | Lớp tạo ra |
| --- | --- | --- | --- |
| I1 Thao tác | "Thêm / Xem / Sửa / Xóa" | Tập giá trị được xử lý khác nhau → mỗi thao tác 1 lớp valid. Giao diện / API chỉ cung cấp 4 thao tác nên không có lớp invalid | 4 lớp valid |
| I2 Tên | "bắt buộc" | "Phải là" → có giá trị / rỗng; tách lớp (G5): chuỗi chỉ có khoảng trắng có thể lọt qua kiểm tra "không rỗng" (A2) | có giá trị (valid); rỗng, chỉ khoảng trắng (invalid) |
| | "tối đa 255 ký tự" | Khoảng giá trị 1–255 → 1 valid + 1 invalid phía trên (phía dưới là "rỗng") | 1–255 (valid), > 255 (invalid) |
| | (không nêu bộ ký tự) | Tách lớp (G5): chữ có dấu có thể bị đếm theo byte (A1); ký tự HTML có thể bị render khi hiển thị (A8) | thêm "có dấu tiếng Việt", "có ký tự HTML" (valid) |
| I3 Giá | "bắt buộc" | "Phải là" | bỏ trống (invalid) |
| | "phải là số" | "Phải là" (A4) | không phải số (invalid) |
| | "dương (> 0)" | Khoảng giá trị chỉ có cận dưới → 1 valid + các invalid phía dưới; tách lớp (G5): `0` và số âm hay bị xử lý khác nhau (`> 0` vs `>= 0`); số thập phân có thể bị chặn bởi kiểu số nguyên (A3) | > 0 nguyên, > 0 thập phân (valid); = 0, < 0 (invalid) |
| I4 Danh mục | "bắt buộc" | "Phải là" | bỏ trống (invalid) |
| | "chọn từ danh sách có sẵn" | Tập giá trị {1, 2, 3}: không có lý do tin rằng mỗi danh mục được xử lý khác nhau → 1 lớp valid; invalid: id ngoài danh sách; tách lớp (G5): id không phải số | thuộc danh sách (valid); ngoài danh sách, không phải số (invalid) |
| I5 Sản phẩm được Sửa / Xóa | "Sửa / Xóa một sản phẩm" | "Phải là" sản phẩm đang tồn tại; tách lớp (G5): id không phải số; sản phẩm vừa bị xóa (rủi ro xóa mềm – bản ghi còn trong CSDL) | tồn tại (valid); không tồn tại, không phải số, đã bị xóa (invalid) |
| Thao tác × dữ liệu | Thêm và Sửa cùng ràng buộc | Tách lớp (G5): Thêm (`POST`) và Sửa (`PUT`) là hai đường xử lý khác nhau → các lớp invalid của I2–I4 được kiểm tra cho cả hai thao tác | – |
| Đầu ra O1–O4 | thành công / từng loại lỗi / sản phẩm khác | Phân vùng đầu ra như ví dụ [UC] | 8 lớp đầu ra |

#### 2.2 Complete Set of Partitions

| EC | Biến | Phân vùng | Ví dụ đại diện | Valid / Invalid |
| --- | --- | --- | --- | --- |
| EC1 | I1 Thao tác | Thêm sản phẩm | form "Thêm sản phẩm mới" / `POST` | Valid |
| EC2 | I1 Thao tác | Xem danh sách sản phẩm | danh sách Admin / `GET /api/products` | Valid |
| EC3 | I1 Thao tác | Sửa sản phẩm | nút "Sửa" / `PUT` | Valid |
| EC4 | I1 Thao tác | Xóa sản phẩm | nút "Xóa" / `DELETE` | Valid |
| EC5 | I2 Tên | 1–255 ký tự Latin | `Sac nhanh USB-C 20W` | Valid |
| EC6 | I2 Tên | Có chữ tiếng Việt có dấu (A1) | `Ốp lưng chống sốc iPhone 15` | Valid |
| EC7 | I2 Tên | Có ký tự HTML (A8) | `<b>Loa Bluetooth</b> Mini` | Valid |
| EC8 | I2 Tên | Rỗng | `` | Invalid |
| EC9 | I2 Tên | Chỉ gồm khoảng trắng (A2) | `   ` | Invalid |
| EC10 | I2 Tên | Dài hơn 255 ký tự | 300 ký tự | Invalid |
| EC11 | I3 Giá | Số nguyên > 0 | `350000` | Valid |
| EC12 | I3 Giá | Số thập phân > 0 (A3) | `99999.5` | Valid |
| EC13 | I3 Giá | Bằng 0 | `0` | Invalid |
| EC14 | I3 Giá | Âm | `-50000` | Invalid |
| EC15 | I3 Giá | Bỏ trống / không gửi | `` | Invalid |
| EC16 | I3 Giá | Không phải số (A4) | `"abc"` | Invalid |
| EC17 | I4 Danh mục | Thuộc danh sách có sẵn | `3` | Valid |
| EC18 | I4 Danh mục | Bỏ trống / không gửi | không có `category_id` | Invalid |
| EC19 | I4 Danh mục | Id không có trong danh sách | `99` | Invalid |
| EC20 | I4 Danh mục | Không phải số | `"abc"` | Invalid |
| EC21 | I5 Sản phẩm | Đang tồn tại | id `3` | Valid |
| EC22 | I5 Sản phẩm | Id không tồn tại | `9999` | Invalid |
| EC23 | I5 Sản phẩm | Id không phải số | `abc` | Invalid |
| EC24 | I5 Sản phẩm | Vừa bị xóa trước đó | id `5` sau khi xóa | Invalid |
| EC25 | O1, O3 | Thêm thành công: sản phẩm mới có trong danh sách với đúng Tên / Giá / Danh mục | | Output |
| EC26 | O1, O3 | Sửa thành công: sản phẩm mang giá trị mới, trường không sửa giữ nguyên (A9) | | Output |
| EC27 | O1, O3 | Xóa thành công: sản phẩm không còn trong danh sách | | Output |
| EC28 | O4 | Các sản phẩm khác giữ nguyên | | Output |
| EC29 | O1, O2 | Từ chối – tên không hợp lệ | | Output |
| EC30 | O1, O2 | Từ chối – giá không hợp lệ | | Output |
| EC31 | O1, O2 | Từ chối – danh mục không hợp lệ | | Output |
| EC32 | O1, O2 | Không tìm thấy sản phẩm (404) | | Output |

Tổng: 24 lớp đầu vào (11 valid, 13 invalid) và 8 lớp đầu ra.

### 3. Bước 3 – Test case Domain Testing

#### 3.1 Thủ tục thực hiện

Mọi test case dùng chung thủ tục theo thao tác, chỉ dữ liệu thay đổi → dạng **data matrix** [DR]. ID có tiền tố `FR15-`. Trong bảng: `␣` là một dấu cách; `(rỗng)` là chuỗi rỗng; `(bỏ trống / không gửi)` là để trống ô trên Web, không gửi trường đó qua API; `"abc"` là giá trị kiểu chuỗi; chuỗi dài ghi bằng công thức Python. Mô tả và URL Ảnh luôn là `Mô tả kiểm thử FR-15` và `https://placehold.co/300x300/png?text=FR15` khi Thêm, giữ nguyên khi Sửa (A5).

**Tiền điều kiện chung (self-standing, self-cleaning)**

- Backend được **khởi động lại trước mỗi test case** → dữ liệu seed: 5 sản phẩm (id 1–5, mục 1.1), 3 danh mục (id 1–3). Test case nào cần thêm tiền điều kiện (vd sản phẩm id 5 đã bị xóa) ghi trong tên / cột dữ liệu.
- Web Admin `http://localhost:5174` đã đăng nhập `admin@eshop.com / Admin123!`; API dùng token admin lấy từ `POST /api/login` (A7).

**P-WEB – Web Admin, tab "Sản phẩm"**

| Bước | Hành động | Kết quả mong đợi của bước |
| --- | --- | --- |
| 1 | Mở tab "Sản phẩm" | Danh sách 5 sản phẩm seed |
| 2a | *Thêm*: nhập Tên, Giá, chọn Danh mục theo cột dữ liệu, nhập Mô tả / URL Ảnh cố định; bấm "Lưu sản phẩm" | Như cột Kết quả mong đợi |
| 2b | *Sửa*: bấm "Sửa" ở dòng sản phẩm có id theo cột dữ liệu; thay Tên / Giá / Danh mục bằng giá trị trong cột dữ liệu; bấm "Lưu sản phẩm" | Như cột Kết quả mong đợi |
| 2c | *Xóa*: bấm "Xóa" ở dòng sản phẩm có id theo cột dữ liệu | Như cột Kết quả mong đợi |
| 3 | Kiểm chứng: so `GET /api/products` trước / sau thao tác (sản phẩm được thao tác và các sản phẩm khác) | Đúng như cột Kết quả mong đợi |

**P-API – gọi API với `Authorization: Bearer <token admin>`**

| Bước | Hành động | Kết quả mong đợi của bước |
| --- | --- | --- |
| 1 | *Thêm*: `POST /api/products` body `{"name", "price", "description", "imageUrl", "category_id"}` theo cột dữ liệu | Như cột Kết quả mong đợi |
| 1' | *Sửa*: `PUT /api/products/<id>` với body đầy đủ như form Sửa (giá trị hiện tại của sản phẩm, thay bằng giá trị trong cột dữ liệu) | Như cột Kết quả mong đợi |
| 1'' | *Xóa*: `DELETE /api/products/<id>` | Như cột Kết quả mong đợi |
| 2 | Kiểm chứng như bước 3 của P-WEB | như trên |

Test case có giá trị giao diện không cho nhập (Giá không phải số, Danh mục ngoài danh sách / không phải số, id sản phẩm không tồn tại) chỉ chạy P-API.

#### 3.2 Minimum Set of Test Cases

Dữ liệu và kết quả mong đợi được sinh từ `scripts/fr15/cases.py` (cùng nguồn với script thực thi) bằng `scripts/fr15/report_tables.py`. Các lớp invalid của Tên / Giá / Danh mục được kiểm tra cho cả Thêm và Sửa (G5, mục 2.1); các test case Sửa bị từ chối dùng sản phẩm id 2 (`Samsung Galaxy S24 Ultra`, `28000000`, danh mục `1`).

<!-- BEGIN:T32 -->
**Test case valid** – mỗi test case phủ nhiều lớp valid nhất có thể:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Thao tác | Sản phẩm (id) | Tên | Giá | Danh mục | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR15-DT-01 | Kiểm tra thêm sản phẩm thành công với dữ liệu hợp lệ điển hình | EC1, EC2, EC5, EC11, EC17, EC25 | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `350000` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25) | Web, API | AI |
| FR15-DT-02 | Kiểm tra thêm sản phẩm thành công khi Tên có chữ tiếng Việt có dấu | EC1, EC2, EC6, EC11, EC17, EC25 | Thêm | – | `Ốp␣lưng␣chống␣sốc␣iPhone␣15` | `150000` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25) | Web, API | AI |
| FR15-DT-03 | Kiểm tra thêm sản phẩm thành công và Tên hiển thị nguyên văn khi Tên có ký tự HTML | EC1, EC2, EC7, EC11, EC17, EC25 | Thêm | – | `<b>Loa␣Bluetooth</b>␣Mini` | `500000` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25); danh sách Admin hiển thị đúng chuỗi `<b>Loa Bluetooth</b> Mini`, không in đậm (A8) | Web, API | AI |
| FR15-DT-04 | Kiểm tra thêm sản phẩm thành công khi Giá là số thập phân dương | EC1, EC2, EC5, EC12, EC17, EC25 | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `99999.5` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25); A3 | Web, API | AI |
| FR15-DT-15 | Kiểm tra sửa Giá sản phẩm thành công và các sản phẩm khác giữ nguyên | EC2, EC3, EC5, EC11, EC17, EC21, EC26, EC28 | Sửa | `3` | `MacBook␣Pro␣M3` | `42000000` | `2` | Sửa thành công: sản phẩm id 3 mang Tên / Giá / Danh mục như cột dữ liệu, Mô tả / Ảnh giữ nguyên; các sản phẩm khác giữ nguyên; API trả 2xx (EC26, EC28) | Web, API | AI |
| FR15-DT-16 | Kiểm tra sửa Tên và Danh mục sản phẩm thành công và các sản phẩm khác giữ nguyên | EC2, EC3, EC6, EC11, EC17, EC21, EC26, EC28 | Sửa | `4` | `Tai␣nghe␣AirPods␣Pro␣2␣–␣bản␣2026` | `6000000` | `1` | Sửa thành công: sản phẩm id 4 mang Tên / Giá / Danh mục như cột dữ liệu, Mô tả / Ảnh giữ nguyên; các sản phẩm khác giữ nguyên; API trả 2xx (EC26, EC28) | Web, API | AI |
| FR15-DT-30 | Kiểm tra xóa sản phẩm thành công và các sản phẩm khác giữ nguyên | EC2, EC4, EC21, EC27, EC28 | Xóa | `5` | – | – | – | Xóa thành công: sản phẩm id 5 không còn trong danh sách; các sản phẩm khác giữ nguyên; API trả 2xx (EC27, EC28) | Web, API | AI |

**Test case invalid** – mỗi test case phủ đúng một lớp invalid, các biến còn lại hợp lệ:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Thao tác | Sản phẩm (id) | Tên | Giá | Danh mục | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR15-DT-05 | Kiểm tra thêm sản phẩm bị từ chối khi bỏ trống Tên | EC8 (Thêm), EC29 | Thêm | – | (rỗng) | `350000` | `3` | Từ chối, báo Tên không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC29) | Web, API | AI |
| FR15-DT-06 | Kiểm tra thêm sản phẩm bị từ chối khi Tên chỉ gồm khoảng trắng | EC9 (Thêm), EC29 | Thêm | – | `␣␣␣` | `350000` | `3` | Từ chối, báo Tên không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC29); A2 | Web, API | AI |
| FR15-DT-07 | Kiểm tra thêm sản phẩm bị từ chối khi Tên dài hơn 255 ký tự | EC10 (Thêm), EC29 | Thêm | – | `"B" * 300` | `350000` | `3` | Từ chối, báo Tên không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC29) | Web, API | AI |
| FR15-DT-08 | Kiểm tra thêm sản phẩm bị từ chối khi Giá bằng 0 | EC13 (Thêm), EC30 | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `0` | `3` | Từ chối, báo Giá không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC30) | Web, API | AI |
| FR15-DT-09 | Kiểm tra thêm sản phẩm bị từ chối khi Giá âm | EC14 (Thêm), EC30 | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `-50000` | `3` | Từ chối, báo Giá không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC30) | Web, API | AI |
| FR15-DT-10 | Kiểm tra thêm sản phẩm bị từ chối khi bỏ trống Giá | EC15 (Thêm), EC30 | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | (bỏ trống / không gửi) | `3` | Từ chối, báo Giá không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC30) | Web, API | AI |
| FR15-DT-11 | Kiểm tra thêm sản phẩm bị từ chối khi Giá không phải số | EC16 (Thêm), EC30 | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `"abc"` | `3` | Từ chối, báo Giá không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC30); A4 | API | AI |
| FR15-DT-12 | Kiểm tra thêm sản phẩm bị từ chối khi không có Danh mục | EC18 (Thêm), EC31 | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `350000` | (bỏ trống / không gửi) | Từ chối, báo Danh mục không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC31) | API | AI |
| FR15-DT-13 | Kiểm tra thêm sản phẩm bị từ chối khi Danh mục không có trong danh sách | EC19 (Thêm), EC31 | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `350000` | `99` | Từ chối, báo Danh mục không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC31) | API | AI |
| FR15-DT-14 | Kiểm tra thêm sản phẩm bị từ chối khi Danh mục không phải số | EC20 (Thêm), EC31 | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `350000` | `"abc"` | Từ chối, báo Danh mục không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC31) | API | AI |
| FR15-DT-17 | Kiểm tra sửa sản phẩm bị từ chối khi bỏ trống Tên | EC8 (Sửa), EC29 | Sửa | `2` | (rỗng) | `28000000` | `1` | Từ chối, báo Tên không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC29) | Web, API | AI |
| FR15-DT-18 | Kiểm tra sửa sản phẩm bị từ chối khi Tên chỉ gồm khoảng trắng | EC9 (Sửa), EC29 | Sửa | `2` | `␣␣␣` | `28000000` | `1` | Từ chối, báo Tên không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC29); A2 | Web, API | AI |
| FR15-DT-19 | Kiểm tra sửa sản phẩm bị từ chối khi Tên dài hơn 255 ký tự | EC10 (Sửa), EC29 | Sửa | `2` | `"B" * 300` | `28000000` | `1` | Từ chối, báo Tên không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC29) | Web, API | AI |
| FR15-DT-20 | Kiểm tra sửa sản phẩm bị từ chối khi Giá bằng 0 | EC13 (Sửa), EC30 | Sửa | `2` | `Samsung␣Galaxy␣S24␣Ultra` | `0` | `1` | Từ chối, báo Giá không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC30) | Web, API | AI |
| FR15-DT-21 | Kiểm tra sửa sản phẩm bị từ chối khi Giá âm | EC14 (Sửa), EC30 | Sửa | `2` | `Samsung␣Galaxy␣S24␣Ultra` | `-50000` | `1` | Từ chối, báo Giá không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC30) | Web, API | AI |
| FR15-DT-22 | Kiểm tra sửa sản phẩm bị từ chối khi bỏ trống Giá | EC15 (Sửa), EC30 | Sửa | `2` | `Samsung␣Galaxy␣S24␣Ultra` | (bỏ trống / không gửi) | `1` | Từ chối, báo Giá không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC30) | Web, API | AI |
| FR15-DT-23 | Kiểm tra sửa sản phẩm bị từ chối khi Giá không phải số | EC16 (Sửa), EC30 | Sửa | `2` | `Samsung␣Galaxy␣S24␣Ultra` | `"abc"` | `1` | Từ chối, báo Giá không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC30); A4 | API | AI |
| FR15-DT-24 | Kiểm tra sửa sản phẩm bị từ chối khi không có Danh mục | EC18 (Sửa), EC31 | Sửa | `2` | `Samsung␣Galaxy␣S24␣Ultra` | `28000000` | (bỏ trống / không gửi) | Từ chối, báo Danh mục không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC31) | API | AI |
| FR15-DT-25 | Kiểm tra sửa sản phẩm bị từ chối khi Danh mục không có trong danh sách | EC19 (Sửa), EC31 | Sửa | `2` | `Samsung␣Galaxy␣S24␣Ultra` | `28000000` | `99` | Từ chối, báo Danh mục không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC31) | API | AI |
| FR15-DT-26 | Kiểm tra sửa sản phẩm bị từ chối khi Danh mục không phải số | EC20 (Sửa), EC31 | Sửa | `2` | `Samsung␣Galaxy␣S24␣Ultra` | `28000000` | `"abc"` | Từ chối, báo Danh mục không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC31) | API | AI |
| FR15-DT-27 | Kiểm tra sửa sản phẩm bị từ chối khi sản phẩm không tồn tại | EC22 (Sửa), EC32 | Sửa | `9999` | `San␣pham␣sua␣thu` | `1000000` | `1` | Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32) | API | AI |
| FR15-DT-28 | Kiểm tra sửa sản phẩm bị từ chối khi id sản phẩm không phải số | EC23 (Sửa), EC32 | Sửa | `"abc"` | `San␣pham␣sua␣thu` | `1000000` | `1` | Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32) | API | AI |
| FR15-DT-29 | Kiểm tra sửa sản phẩm bị từ chối khi sản phẩm vừa bị xóa | EC24 (Sửa), EC32 | Sửa | `5` (đã xóa ở tiền điều kiện) | `Bàn␣phím␣cơ␣Keychron␣Q1` | `4000000` | `3` | Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32) | API | AI |
| FR15-DT-31 | Kiểm tra xóa sản phẩm bị từ chối khi sản phẩm không tồn tại | EC22 (Xóa), EC32 | Xóa | `9999` | – | – | – | Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32) | API | AI |
| FR15-DT-32 | Kiểm tra xóa sản phẩm bị từ chối khi id sản phẩm không phải số | EC23 (Xóa), EC32 | Xóa | `"abc"` | – | – | – | Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32) | API | AI |
| FR15-DT-33 | Kiểm tra xóa sản phẩm bị từ chối khi sản phẩm đã bị xóa trước đó | EC24 (Xóa), EC32 | Xóa | `5` (đã xóa ở tiền điều kiện) | – | – | – | Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32) | API | AI |
<!-- END:T32 -->

#### 3.3 Bảng phủ phân vùng

<!-- BEGIN:T33 -->
| EC | Test case phủ | | EC | Test case phủ |
| --- | --- | --- | --- | --- |
| EC1 | FR15-DT-01…FR15-DT-04 | | EC17 | FR15-DT-01…FR15-DT-04, FR15-DT-15, FR15-DT-16; bổ sung: FR15-DT-34 (mục 6.2) |
| EC2 | FR15-DT-01…FR15-DT-04, FR15-DT-15, FR15-DT-16, FR15-DT-30 | | EC18 | FR15-DT-12, FR15-DT-24 |
| EC3 | FR15-DT-15, FR15-DT-16; bổ sung: FR15-DT-34 (mục 6.2) | | EC19 | FR15-DT-13, FR15-DT-25 |
| EC4 | FR15-DT-30 | | EC20 | FR15-DT-14, FR15-DT-26 |
| EC5 | FR15-DT-01, FR15-DT-04, FR15-DT-15 | | EC21 | FR15-DT-15, FR15-DT-16, FR15-DT-30; bổ sung: FR15-DT-34 (mục 6.2) |
| EC6 | FR15-DT-02, FR15-DT-16 | | EC22 | FR15-DT-27, FR15-DT-31 |
| EC7 | FR15-DT-03 | | EC23 | FR15-DT-28, FR15-DT-32 |
| EC8 | FR15-DT-05, FR15-DT-17 | | EC24 | FR15-DT-29, FR15-DT-33 |
| EC9 | FR15-DT-06, FR15-DT-18 | | EC25 | FR15-DT-01…FR15-DT-04 |
| EC10 | FR15-DT-07, FR15-DT-19 | | EC26 | FR15-DT-15, FR15-DT-16; bổ sung: FR15-DT-34 (mục 6.2) |
| EC11 | FR15-DT-01…FR15-DT-03, FR15-DT-15, FR15-DT-16; bổ sung: FR15-DT-34 (mục 6.2) | | EC27 | FR15-DT-30 |
| EC12 | FR15-DT-04 | | EC28 | FR15-DT-15, FR15-DT-16, FR15-DT-30 |
| EC13 | FR15-DT-08, FR15-DT-20 | | EC29 | FR15-DT-05…FR15-DT-07, FR15-DT-17…FR15-DT-19 |
| EC14 | FR15-DT-09, FR15-DT-21 | | EC30 | FR15-DT-08…FR15-DT-11, FR15-DT-20…FR15-DT-23 |
| EC15 | FR15-DT-10, FR15-DT-22 | | EC31 | FR15-DT-12…FR15-DT-14, FR15-DT-24…FR15-DT-26 |
| EC16 | FR15-DT-11, FR15-DT-23 | | EC32 | FR15-DT-27…FR15-DT-29, FR15-DT-31…FR15-DT-33 |

32 / 32 lớp được phủ bởi 33 test case Minimum Set (7 valid, 26 invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp invalid có test case riêng. Các đại diện bổ sung sau rà soát (mục 6.2) ghi sau dấu `;`.
<!-- END:T33 -->

### 4. Bước 4 – Boundary Value Analysis

#### 4.1 Xác định biên

BVA áp dụng cho các biến có thứ tự. Với mỗi phân vùng xét LB-1, LB, LB+1, UB-1, UB, UB+1 và giá trị lớn nhất chọn thử [S04]; điểm đã có trong Minimum Set chỉ dẫn chiếu.

| Biến | Phân vùng | LB | UB | Bước nhảy | Điểm kiểm tra |
| --- | --- | --- | --- | --- | --- |
| I2 độ dài Tên (Thêm) | EC8 (0) / EC5 (1–255) / EC10 (> 255) | 1 | 255 | 1 ký tự | 0, 1, 2, 254, 255, 256 |
| I2 độ dài Tên có dấu (A1) | EC6 / EC10 | 1 | 255 ký tự (không phải byte) | 1 ký tự | 255, 256 ký tự `Ố` (mỗi ký tự 3 byte UTF-8) |
| I2 khoảng trắng | EC9 / EC5 | 1 ký tự khác khoảng trắng | – | 1 ký tự | `␣A␣` |
| I2 độ dài Tên (Sửa) | EC5 / EC10 | – | 255 | 1 ký tự | 255, 256 |
| I3 Giá (Thêm) | EC14 (< 0) / EC13 (0) / EC12, EC11 (> 0) | > 0 | không giới hạn (A3) | 0.01 (A3) và 1 | -1, -0.01, 0, 0.01, 1, 9007199254740991 (2^53 − 1, số nguyên lớn nhất biểu diễn chính xác) |
| I3 Giá (Sửa) | EC14 / EC11 | 1 | – | 1 | -1, 1 |
| I4 id Danh mục | EC19 (ngoài danh sách) / EC17 (1–3) | 1 | 3 | 1 | 0, 1, 3, 4 |
| I5 id sản phẩm (Sửa, Xóa) | EC22 / EC21 (1–5, seed) | 1 | 5 | 1 | 0, 1, 5, 6 |

#### 4.2 Boundary Value Test Cases

Thủ tục: P-WEB / P-API ở mục 3.1. Bảng giữ các cột dữ liệu của data matrix như mục 3.2. Dòng có ID trong ngoặc là điểm biên đã có trong Minimum Set, chỉ dẫn chiếu.

<!-- BEGIN:T42 -->
| ID | Tên test case (Action + Function + Condition) | Partition tested | Thao tác | Sản phẩm (id) | Tên | Giá | Danh mục | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| (FR15-DT-05) | Kiểm tra thêm sản phẩm bị từ chối khi bỏ trống Tên | EC8 – Tên độ dài 0 | Thêm | – | (rỗng) | `350000` | `3` | Từ chối, báo Tên không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC29) | Web, API | xem 3.2 |
| FR15-BV-01 | Kiểm tra thêm sản phẩm thành công khi Tên dài 1 ký tự | EC8/EC5 – độ dài 1 (LB) | Thêm | – | `A` | `350000` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25) | Web, API | AI |
| FR15-BV-02 | Kiểm tra thêm sản phẩm thành công khi Tên dài 2 ký tự | EC5 – độ dài 2 (LB+1) | Thêm | – | `AB` | `350000` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25) | Web, API | AI |
| FR15-BV-03 | Kiểm tra thêm sản phẩm thành công khi Tên dài 254 ký tự | EC5 – độ dài 254 (UB-1) | Thêm | – | `"A" * 254` | `350000` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25) | Web, API | AI |
| FR15-BV-04 | Kiểm tra thêm sản phẩm thành công khi Tên dài 255 ký tự | EC5/EC10 – độ dài 255 (UB) | Thêm | – | `"A" * 255` | `350000` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25) | Web, API | AI |
| FR15-BV-05 | Kiểm tra thêm sản phẩm bị từ chối khi Tên dài 256 ký tự | EC5/EC10 – độ dài 256 (UB+1) | Thêm | – | `"A" * 256` | `350000` | `3` | Từ chối, báo Tên không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC29) | Web, API | AI |
| FR15-BV-06 | Kiểm tra thêm sản phẩm thành công khi Tên dài 255 ký tự có dấu | EC6/EC10 – 255 ký tự có dấu (UB, A1) | Thêm | – | `"Ố" * 255` | `350000` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25); A1 | Web, API | AI |
| FR15-BV-07 | Kiểm tra thêm sản phẩm bị từ chối khi Tên dài 256 ký tự có dấu | EC6/EC10 – 256 ký tự có dấu (UB+1, A1) | Thêm | – | `"Ố" * 256` | `350000` | `3` | Từ chối, báo Tên không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC29); A1 | Web, API | AI |
| FR15-BV-08 | Kiểm tra thêm sản phẩm thành công khi Tên có 1 ký tự giữa các khoảng trắng | EC9/EC5 – 1 ký tự khác khoảng trắng (LB, A2) | Thêm | – | `␣A␣` | `350000` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25); A2 | Web, API | AI |
| FR15-BV-09 | Kiểm tra sửa sản phẩm thành công khi Tên mới dài 255 ký tự | EC5/EC10 (Sửa) – độ dài 255 (UB) | Sửa | `2` | `"A" * 255` | `28000000` | `1` | Sửa thành công: sản phẩm id 2 mang Tên / Giá / Danh mục như cột dữ liệu, Mô tả / Ảnh giữ nguyên; các sản phẩm khác giữ nguyên; API trả 2xx (EC26, EC28) | Web, API | AI |
| FR15-BV-10 | Kiểm tra sửa sản phẩm bị từ chối khi Tên mới dài 256 ký tự | EC5/EC10 (Sửa) – độ dài 256 (UB+1) | Sửa | `2` | `"A" * 256` | `28000000` | `1` | Từ chối, báo Tên không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC29) | Web, API | AI |
| FR15-BV-11 | Kiểm tra thêm sản phẩm bị từ chối khi Giá bằng -1 | EC14/EC13 – Giá -1 (bước 1) | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `-1` | `3` | Từ chối, báo Giá không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC30) | Web, API | AI |
| FR15-BV-12 | Kiểm tra thêm sản phẩm bị từ chối khi Giá bằng -0.01 | EC14/EC13 – Giá -0.01 (bước 0.01, A3) | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `-0.01` | `3` | Từ chối, báo Giá không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC30); A3 | Web, API | AI |
| (FR15-DT-08) | Kiểm tra thêm sản phẩm bị từ chối khi Giá bằng 0 | EC13 – Giá 0 | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `0` | `3` | Từ chối, báo Giá không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC30) | Web, API | xem 3.2 |
| FR15-BV-13 | Kiểm tra thêm sản phẩm thành công khi Giá bằng 0.01 | EC13/EC12 – Giá 0.01 (LB thập phân, A3) | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `0.01` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25); A3 | Web, API | AI |
| FR15-BV-14 | Kiểm tra thêm sản phẩm thành công khi Giá bằng 1 | EC13/EC11 – Giá 1 (LB nguyên) | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `1` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25) | Web, API | AI |
| FR15-BV-15 | Kiểm tra thêm sản phẩm thành công khi Giá bằng 9007199254740991 | EC11 – giá trị lớn nhất biểu diễn chính xác (2^53 - 1, A3) | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `9007199254740991` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25); A3 | Web, API | AI |
| FR15-BV-16 | Kiểm tra sửa sản phẩm thành công khi Giá mới bằng 1 | EC13/EC11 (Sửa) – Giá 1 (LB) | Sửa | `2` | `Samsung␣Galaxy␣S24␣Ultra` | `1` | `1` | Sửa thành công: sản phẩm id 2 mang Tên / Giá / Danh mục như cột dữ liệu, Mô tả / Ảnh giữ nguyên; các sản phẩm khác giữ nguyên; API trả 2xx (EC26, EC28) | Web, API | AI |
| FR15-BV-17 | Kiểm tra sửa sản phẩm bị từ chối khi Giá mới bằng -1 | EC14/EC13 (Sửa) – Giá -1 | Sửa | `2` | `Samsung␣Galaxy␣S24␣Ultra` | `-1` | `1` | Từ chối, báo Giá không hợp lệ; sản phẩm id 2 và các sản phẩm khác giữ nguyên; API trả 4xx (EC30) | Web, API | AI |
| FR15-BV-18 | Kiểm tra thêm sản phẩm bị từ chối khi Danh mục bằng 0 | EC19/EC17 – id 0 (LB-1) | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `350000` | `0` | Từ chối, báo Danh mục không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC31) | API | AI |
| FR15-BV-19 | Kiểm tra thêm sản phẩm thành công khi Danh mục bằng 1 | EC17 – id 1 (LB) | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `350000` | `1` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25) | Web, API | AI |
| (FR15-DT-01) | Kiểm tra thêm sản phẩm thành công với dữ liệu hợp lệ điển hình | EC17 – Danh mục id 3 (UB) | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `350000` | `3` | Thêm thành công: sản phẩm mới có trong danh sách Admin và `GET /api/products` với đúng Tên / Giá / Danh mục; API trả 2xx (EC25) | Web, API | xem 3.2 |
| FR15-BV-20 | Kiểm tra thêm sản phẩm bị từ chối khi Danh mục bằng 4 | EC17/EC19 – id 4 (UB+1) | Thêm | – | `Sac␣nhanh␣USB-C␣20W` | `350000` | `4` | Từ chối, báo Danh mục không hợp lệ; không tạo sản phẩm; danh sách sản phẩm không đổi; API trả 4xx (EC31) | API | AI |
| FR15-BV-21 | Kiểm tra sửa sản phẩm bị từ chối khi id sản phẩm bằng 0 | EC22/EC21 (Sửa) – id 0 (LB-1) | Sửa | `0` | `San␣pham␣sua␣thu` | `1000000` | `1` | Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32) | API | AI |
| FR15-BV-22 | Kiểm tra sửa sản phẩm id 1 thành công | EC21 (Sửa) – id 1 (LB) | Sửa | `1` | `iPhone␣15␣Pro␣Max` | `31000000` | `1` | Sửa thành công: sản phẩm id 1 mang Tên / Giá / Danh mục như cột dữ liệu, Mô tả / Ảnh giữ nguyên; các sản phẩm khác giữ nguyên; API trả 2xx (EC26, EC28) | Web, API | AI |
| (FR15-DT-15) | Kiểm tra sửa Giá sản phẩm thành công và các sản phẩm khác giữ nguyên | EC21 (Sửa) – id 3 (giá trị giữa) | Sửa | `3` | `MacBook␣Pro␣M3` | `42000000` | `2` | Sửa thành công: sản phẩm id 3 mang Tên / Giá / Danh mục như cột dữ liệu, Mô tả / Ảnh giữ nguyên; các sản phẩm khác giữ nguyên; API trả 2xx (EC26, EC28) | Web, API | xem 3.2 |
| FR15-BV-23 | Kiểm tra sửa sản phẩm id 5 thành công | EC21 (Sửa) – id 5 (UB) | Sửa | `5` | `Bàn␣phím␣cơ␣Keychron␣Q1` | `4100000` | `3` | Sửa thành công: sản phẩm id 5 mang Tên / Giá / Danh mục như cột dữ liệu, Mô tả / Ảnh giữ nguyên; các sản phẩm khác giữ nguyên; API trả 2xx (EC26, EC28) | Web, API | AI |
| FR15-BV-24 | Kiểm tra sửa sản phẩm bị từ chối khi id sản phẩm bằng 6 | EC21/EC22 (Sửa) – id 6 (UB+1) | Sửa | `6` | `San␣pham␣sua␣thu` | `1000000` | `1` | Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32) | API | AI |
| FR15-BV-25 | Kiểm tra xóa sản phẩm bị từ chối khi id sản phẩm bằng 0 | EC22/EC21 (Xóa) – id 0 (LB-1) | Xóa | `0` | – | – | – | Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32) | API | AI |
| FR15-BV-26 | Kiểm tra xóa sản phẩm id 1 thành công | EC21 (Xóa) – id 1 (LB) | Xóa | `1` | – | – | – | Xóa thành công: sản phẩm id 1 không còn trong danh sách; các sản phẩm khác giữ nguyên; API trả 2xx (EC27, EC28) | Web, API | AI |
| (FR15-DT-30) | Kiểm tra xóa sản phẩm thành công và các sản phẩm khác giữ nguyên | EC21 (Xóa) – id 5 (UB) | Xóa | `5` | – | – | – | Xóa thành công: sản phẩm id 5 không còn trong danh sách; các sản phẩm khác giữ nguyên; API trả 2xx (EC27, EC28) | Web, API | xem 3.2 |
| FR15-BV-27 | Kiểm tra xóa sản phẩm bị từ chối khi id sản phẩm bằng 6 | EC21/EC22 (Xóa) – id 6 (UB+1) | Xóa | `6` | – | – | – | Từ chối, báo không tìm thấy sản phẩm; danh sách sản phẩm không đổi; API trả 404 (EC32) | API | AI |

Tổng: 27 test case BVA mới (FR15-BV-01…FR15-BV-27); 5 dòng có ID trong ngoặc là điểm biên đã được phủ bởi test case Minimum Set (mục 3.2), chỉ dẫn chiếu, không chạy lại.
<!-- END:T42 -->

### 5. Bước 5 – Kết quả thực thi

#### 5.1 Môi trường và cách chạy

| Mục | Giá trị |
| --- | --- |
| Ngày chạy | 2026-10-20 |
| Người chạy | 23120031 (script tự động, kết quả được rà soát thủ công) |
| SUT | `eshop-sut-main` (trùng với `d1nhnguyen/eshop-sut`), Node 20.19.5 |
| Web | Web Admin `http://localhost:5174`, Chrome 155 (headless, Playwright) |
| API | `http://localhost:3000/api`, gọi bằng Python `urllib`, token admin |
| Dữ liệu | Backend được khởi động lại **trước mỗi test case** (`scripts/restart_backend.sh`) |
| Script | `scripts/fr15/cases.py` (dữ liệu), `run_web.mjs` (P-WEB), `run_api.py` (P-API), `report_tables.py` (sinh bảng) |
| Bằng chứng | `evidence/FR-15/web_results.json`, `api_results.json`; ảnh sau thao tác của từng test case `evidence/FR-15/web/<ID>.png` |

Cách kết luận (A6): chụp `GET /api/products` trước và sau thao tác. Test case "thành công" Pass khi sản phẩm được thao tác mang đúng giá trị (Thêm, Sửa) hoặc biến mất (Xóa) **và** các sản phẩm khác giữ nguyên. Test case "từ chối" Pass khi danh sách sản phẩm không đổi **và** có thông báo nêu đúng trường (hoặc API trả 4xx với thông báo đúng trường); "không tìm thấy" Pass khi API trả 404 và danh sách không đổi.

#### 5.2 Phát hiện chính

- **Server không kiểm tra dữ liệu sản phẩm:** mọi giá trị Tên / Giá / Danh mục không hợp lệ đều được lưu khi Thêm và khi Sửa (HTTP 200 "Product created" / "Product updated").
- **Web Admin chỉ chặn Tên rỗng** (thuộc tính `required` của trình duyệt). Tên toàn khoảng trắng, Tên > 255 ký tự, Giá 0 / âm / trống đều được gửi đi; khi Sửa còn hiện "Cập nhật thành công!".
- **Giá thập phân** (`99999.5`, `0.01`) được lưu cả qua Web lẫn API – đúng với A3; ghi nhận ở bước 1 rằng trình duyệt chặn `0.5` là chưa chính xác (xem mục 6).
- **Sửa / Xóa sản phẩm không tồn tại** (id `0`, `6`, `9999`, `abc`, sản phẩm vừa xóa) trả 200 "Product updated" / "Product deleted" thay vì 404; dữ liệu không đổi.
- Các thao tác hợp lệ đều đúng; khi Sửa / Xóa một sản phẩm, các sản phẩm khác giữ nguyên (đúng yêu cầu "chỉ sản phẩm đó bị thay đổi"). Tên chứa HTML được hiển thị nguyên văn.

#### 5.3 Kết quả theo test case

Mỗi test case một dòng. Bảng sinh từ `evidence/FR-15/web_results.json` và `api_results.json`.

<!-- BEGIN:T53 -->
| TC | Web | Kết quả thực tế – Web | API | Kết quả thực tế – API | Bằng chứng | Bug |
| --- | --- | --- | --- | --- | --- | --- |
| FR15-DT-01 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-DT-01.png) · `api_results.json` | – |
| FR15-DT-02 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-DT-02.png) · `api_results.json` | – |
| FR15-DT-03 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục, danh sách hiển thị nguyên văn “&lt;b&gt;Loa Bluetooth&lt;/b&gt; Mini” | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-DT-03.png) · `api_results.json` | – |
| FR15-DT-04 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-DT-04.png) · `api_results.json` | – |
| FR15-DT-05 | Pass | Trình duyệt chặn ô Tên sản phẩm: “Please fill out this field.”, không gửi request; danh sách sản phẩm không đổi | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “”, Giá 350000, Danh mục 3 | [ảnh Web](../evidence/FR-15/web/FR15-DT-05.png) · `api_results.json` | FR15-B4 |
| FR15-DT-06 | Fail | Form gửi request, HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “   ”, Giá 350000, Danh mục 3 | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “   ”, Giá 350000, Danh mục 3 | [ảnh Web](../evidence/FR-15/web/FR15-DT-06.png) · `api_results.json` | FR15-B4 |
| FR15-DT-07 | Fail | Form gửi request, HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB…”, Giá 350000, Danh mục 3 | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB…”, Giá 350000, Danh mục 3 | [ảnh Web](../evidence/FR-15/web/FR15-DT-07.png) · `api_results.json` | FR15-B3 |
| FR15-DT-08 | Fail | Form gửi request, HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá 0, Danh mục 3 | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá 0, Danh mục 3 | [ảnh Web](../evidence/FR-15/web/FR15-DT-08.png) · `api_results.json` | FR15-B1 |
| FR15-DT-09 | Fail | Form gửi request, HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá -50000, Danh mục 3 | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá -50000, Danh mục 3 | [ảnh Web](../evidence/FR-15/web/FR15-DT-09.png) · `api_results.json` | FR15-B1 |
| FR15-DT-10 | Fail | Form gửi request, HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá (rỗng), Danh mục 3 | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá (không có), Danh mục 3 | [ảnh Web](../evidence/FR-15/web/FR15-DT-10.png) · `api_results.json` | FR15-B2 |
| FR15-DT-11 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá abc, Danh mục 3 | `api_results.json` | FR15-B2 |
| FR15-DT-12 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá 350000, Danh mục (không có) | `api_results.json` | FR15-B5 |
| FR15-DT-13 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá 350000, Danh mục 99 | `api_results.json` | FR15-B5 |
| FR15-DT-14 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá 350000, Danh mục abc | `api_results.json` | FR15-B5 |
| FR15-DT-15 | Pass | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm id 3 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | Pass | HTTP 200 “Product updated”; sản phẩm id 3 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | [ảnh Web](../evidence/FR-15/web/FR15-DT-15.png) · `api_results.json` | – |
| FR15-DT-16 | Pass | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm id 4 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | Pass | HTTP 200 “Product updated”; sản phẩm id 4 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | [ảnh Web](../evidence/FR-15/web/FR15-DT-16.png) · `api_results.json` | – |
| FR15-DT-17 | Pass | Trình duyệt chặn ô Tên sản phẩm: “Please fill out this field.”, không gửi request; danh sách sản phẩm không đổi | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “”, Giá 28000000, Danh mục 1 | [ảnh Web](../evidence/FR-15/web/FR15-DT-17.png) · `api_results.json` | FR15-B4 |
| FR15-DT-18 | Fail | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm bị sửa thành: Tên “   ”, Giá 28000000, Danh mục 1 | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “   ”, Giá 28000000, Danh mục 1 | [ảnh Web](../evidence/FR-15/web/FR15-DT-18.png) · `api_results.json` | FR15-B4 |
| FR15-DT-19 | Fail | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm bị sửa thành: Tên “BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB…”, Giá 28000000, Danh mục 1 | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB…”, Giá 28000000, Danh mục 1 | [ảnh Web](../evidence/FR-15/web/FR15-DT-19.png) · `api_results.json` | FR15-B3 |
| FR15-DT-20 | Fail | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá 0, Danh mục 1 | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá 0, Danh mục 1 | [ảnh Web](../evidence/FR-15/web/FR15-DT-20.png) · `api_results.json` | FR15-B1 |
| FR15-DT-21 | Fail | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá -50000, Danh mục 1 | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá -50000, Danh mục 1 | [ảnh Web](../evidence/FR-15/web/FR15-DT-21.png) · `api_results.json` | FR15-B1 |
| FR15-DT-22 | Fail | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá (rỗng), Danh mục 1 | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá (không có), Danh mục 1 | [ảnh Web](../evidence/FR-15/web/FR15-DT-22.png) · `api_results.json` | FR15-B2 |
| FR15-DT-23 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá abc, Danh mục 1 | `api_results.json` | FR15-B2 |
| FR15-DT-24 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá 28000000, Danh mục (không có) | `api_results.json` | FR15-B5 |
| FR15-DT-25 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá 28000000, Danh mục 99 | `api_results.json` | FR15-B5 |
| FR15-DT-26 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá 28000000, Danh mục abc | `api_results.json` | FR15-B5 |
| FR15-DT-27 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product updated”; báo thành công thay vì 404; danh sách sản phẩm không đổi | `api_results.json` | FR15-B6 |
| FR15-DT-28 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product updated”; báo thành công thay vì 404; danh sách sản phẩm không đổi | `api_results.json` | FR15-B6 |
| FR15-DT-29 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product updated”; báo thành công thay vì 404; danh sách sản phẩm không đổi | `api_results.json` | FR15-B6 |
| FR15-DT-30 | Pass | Form gửi request, HTTP 200 “Product deleted”; sản phẩm id 5 đã bị xóa, các sản phẩm khác giữ nguyên | Pass | HTTP 200 “Product deleted”; sản phẩm id 5 đã bị xóa, các sản phẩm khác giữ nguyên | [ảnh Web](../evidence/FR-15/web/FR15-DT-30.png) · `api_results.json` | – |
| FR15-DT-31 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product deleted”; báo thành công thay vì 404; danh sách sản phẩm không đổi | `api_results.json` | FR15-B6 |
| FR15-DT-32 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product deleted”; báo thành công thay vì 404; danh sách sản phẩm không đổi | `api_results.json` | FR15-B6 |
| FR15-DT-33 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product deleted”; báo thành công thay vì 404; danh sách sản phẩm không đổi | `api_results.json` | FR15-B6 |
| FR15-BV-01 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-BV-01.png) · `api_results.json` | – |
| FR15-BV-02 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-BV-02.png) · `api_results.json` | – |
| FR15-BV-03 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-BV-03.png) · `api_results.json` | – |
| FR15-BV-04 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-BV-04.png) · `api_results.json` | – |
| FR15-BV-05 | Fail | Form gửi request, HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA…”, Giá 350000, Danh mục 3 | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA…”, Giá 350000, Danh mục 3 | [ảnh Web](../evidence/FR-15/web/FR15-BV-05.png) · `api_results.json` | FR15-B3 |
| FR15-BV-06 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-BV-06.png) · `api_results.json` | – |
| FR15-BV-07 | Fail | Form gửi request, HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “ỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐ…”, Giá 350000, Danh mục 3 | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “ỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐỐ…”, Giá 350000, Danh mục 3 | [ảnh Web](../evidence/FR-15/web/FR15-BV-07.png) · `api_results.json` | FR15-B3 |
| FR15-BV-08 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-BV-08.png) · `api_results.json` | – |
| FR15-BV-09 | Pass | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm id 2 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | Pass | HTTP 200 “Product updated”; sản phẩm id 2 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | [ảnh Web](../evidence/FR-15/web/FR15-BV-09.png) · `api_results.json` | – |
| FR15-BV-10 | Fail | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm bị sửa thành: Tên “AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA…”, Giá 28000000, Danh mục 1 | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA…”, Giá 28000000, Danh mục 1 | [ảnh Web](../evidence/FR-15/web/FR15-BV-10.png) · `api_results.json` | FR15-B3 |
| FR15-BV-11 | Fail | Form gửi request, HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá -1, Danh mục 3 | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá -1, Danh mục 3 | [ảnh Web](../evidence/FR-15/web/FR15-BV-11.png) · `api_results.json` | FR15-B1 |
| FR15-BV-12 | Fail | Form gửi request, HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá -0.01, Danh mục 3 | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá -0.01, Danh mục 3 | [ảnh Web](../evidence/FR-15/web/FR15-BV-12.png) · `api_results.json` | FR15-B1 |
| FR15-BV-13 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-BV-13.png) · `api_results.json` | – |
| FR15-BV-14 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-BV-14.png) · `api_results.json` | – |
| FR15-BV-15 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-BV-15.png) · `api_results.json` | – |
| FR15-BV-16 | Pass | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm id 2 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | Pass | HTTP 200 “Product updated”; sản phẩm id 2 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | [ảnh Web](../evidence/FR-15/web/FR15-BV-16.png) · `api_results.json` | – |
| FR15-BV-17 | Fail | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá -1, Danh mục 1 | Fail | HTTP 200 “Product updated”; sản phẩm bị sửa thành: Tên “Samsung Galaxy S24 Ultra”, Giá -1, Danh mục 1 | [ảnh Web](../evidence/FR-15/web/FR15-BV-17.png) · `api_results.json` | FR15-B1 |
| FR15-BV-18 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá 350000, Danh mục 0 | `api_results.json` | FR15-B5 |
| FR15-BV-19 | Pass | Form gửi request, HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | Pass | HTTP 200 “Product created”; sản phẩm mới lưu đúng Tên / Giá / Danh mục | [ảnh Web](../evidence/FR-15/web/FR15-BV-19.png) · `api_results.json` | – |
| FR15-BV-20 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product created”; vẫn tạo sản phẩm: Tên “Sac nhanh USB-C 20W”, Giá 350000, Danh mục 4 | `api_results.json` | FR15-B5 |
| FR15-BV-21 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product updated”; báo thành công thay vì 404; danh sách sản phẩm không đổi | `api_results.json` | FR15-B6 |
| FR15-BV-22 | Pass | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm id 1 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | Pass | HTTP 200 “Product updated”; sản phẩm id 1 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | [ảnh Web](../evidence/FR-15/web/FR15-BV-22.png) · `api_results.json` | – |
| FR15-BV-23 | Pass | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm id 5 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | Pass | HTTP 200 “Product updated”; sản phẩm id 5 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | [ảnh Web](../evidence/FR-15/web/FR15-BV-23.png) · `api_results.json` | – |
| FR15-BV-24 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product updated”; báo thành công thay vì 404; danh sách sản phẩm không đổi | `api_results.json` | FR15-B6 |
| FR15-BV-25 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product deleted”; báo thành công thay vì 404; danh sách sản phẩm không đổi | `api_results.json` | FR15-B6 |
| FR15-BV-26 | Pass | Form gửi request, HTTP 200 “Product deleted”; sản phẩm id 1 đã bị xóa, các sản phẩm khác giữ nguyên | Pass | HTTP 200 “Product deleted”; sản phẩm id 1 đã bị xóa, các sản phẩm khác giữ nguyên | [ảnh Web](../evidence/FR-15/web/FR15-BV-26.png) · `api_results.json` | – |
| FR15-BV-27 | – | Không áp dụng (giao diện không cho nhập giá trị này) | Fail | HTTP 200 “Product deleted”; báo thành công thay vì 404; danh sách sản phẩm không đổi | `api_results.json` | FR15-B6 |
| FR15-DT-34 | Pass | Form gửi request, HTTP 200 “Product updated”, hiện “Cập nhật thành công!”; sản phẩm id 3 lưu đúng giá trị mới, các sản phẩm khác giữ nguyên | – | Không áp dụng (giao diện không cho nhập giá trị này) | [ảnh Web](../evidence/FR-15/web/FR15-DT-34.png) | – |
<!-- END:T53 -->

#### 5.4 Tổng hợp

<!-- BEGIN:T55 -->
| Kênh | Thiết kế | Đã chạy | Pass | Fail | Blocked | Không áp dụng |
| --- | --- | --- | --- | --- | --- | --- |
| Web | 61 | 41 | 25 | 16 | 0 | 20 |
| API | 61 | 60 | 22 | 38 | 0 | 1 |
| **Tổng lượt chạy** | | **101** | **47** | **54** | **0** | |

61 test case = 33 Minimum Set (mục 3.2) + 27 BVA (mục 4.2) + 1 bổ sung sau rà soát (mục 6.2). Gộp các kênh theo test case (Fail nếu Fail ở bất kỳ kênh nào, Blocked nếu còn kênh bị Blocked): 23 Pass, 38 Fail, 0 Blocked.
<!-- END:T55 -->

### 6. Bước 6 – AI gap analysis

> G1–G5: AI (Claude Code) tự phát hiện trong lúc làm các bước 1–5 của FR-15. Sinh viên rà soát và bổ sung các điểm tự phát hiện ở commit `[FR-15][Bn-review]`.

#### 6.1 Những gì AI bỏ sót hoặc làm sai

| # | AI bỏ sót / làm sai | Loại | Nguyên nhân | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |
| G1 | Bước 1 ghi "trình duyệt chặn `0.5`" chỉ dựa vào thông báo `validationMessage` của ô Giá, không thử bấm Lưu; thực tế giá thập phân vẫn được gửi và lưu | Quan sát / giả định sai về SUT | **Giới hạn công cụ AI**: suy ra hành vi từ thuộc tính giao diện thay vì quan sát hành vi thật | FR15-DT-04, FR15-BV-13 Pass ở bước 5 trái với dự đoán; khảo sát lại `checkValidity()` | Đính chính mục 1.1 |
| G2 | Thiết kế ban đầu không có test case Sửa chỉ một ô trên Web: mọi test case Sửa đều chọn lại Danh mục, nên không kiểm tra được form Sửa có điền sẵn đúng Danh mục (A9) hay không – lần khảo sát chỉ xem sản phẩm danh mục 1, trùng giá trị mặc định | Test case thiếu | **Độ phức tạp feature**: hành vi phụ thuộc giá trị form điền sẵn; **giới hạn công cụ AI**: script luôn nhập đủ mọi ô nên không giống thao tác thật | AI rà soát bảng phủ và giả định A9 sau khi chạy | Bổ sung FR15-DT-34 (mục 6.2): Pass |
| G3 | Script Web bản đầu ghi thông báo "Please fill out this field." của form đã được xóa trắng sau khi lưu vào mọi test case → bằng chứng sai lệch, có thể khiến test case "từ chối" Pass giả | Oracle / bằng chứng | **Giới hạn công cụ AI**: lặp lại đúng lỗi G5 của FR-01 (đọc thông báo sau khi giao diện đã đổi trạng thái) – AI không tự chuyển bài học giữa các feature | Đọc output: test case thành công cũng có thông báo lỗi | Chỉ đọc thông báo trình duyệt khi form không gửi request |
| G4 | Runner API bản đầu treo ở test case đầu tiên (chờ pipe của tiến trình backend chạy nền); trong lúc kiểm tra, AI còn khởi động lại backend song song làm hỏng lượt chạy | Thực thi | **Giới hạn công cụ AI**: lỗi lập trình script và thao tác song song trên môi trường dùng chung | Không có dòng kết quả nào sau 400 giây | Không bắt output của script restart; chạy lại toàn bộ |
| G5 | Bảng kết quả bản đầu: ô API của FR15-DT-03 ghi "hiển thị nguyên văn None"; test case "không tìm thấy" Fail không nêu lý do; tên chứa `<b>` trong ô bảng sẽ bị hiển thị thành chữ đậm | Báo cáo kết quả | **Giới hạn công cụ AI**: sinh văn bản tự động không kiểm tra theo kênh và không escape | AI đọc lại bảng sinh ra | Sửa hàm diễn giải kết quả; escape `<`, `>`, `|` trong `report_lib.py` |

#### 6.2 Test case bổ sung

Kết quả thực thi nằm ở mục 5.3.

<!-- BEGIN:T62 -->
| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Thao tác | Sản phẩm (id) | Tên | Giá | Danh mục | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR15-DT-34 | Kiểm tra sửa chỉ Giá sản phẩm thành công mà Danh mục do form điền sẵn được giữ nguyên | EC3, EC11, EC17, EC21, EC26 (A9 – form Sửa điền sẵn đúng Danh mục khác giá trị mặc định 1) | Sửa | `3` | `MacBook␣Pro␣M3` (không chạm vào ô) | `43000000` | `2` (không chạm vào ô) | Sửa thành công: sản phẩm id 3 mang Tên / Giá / Danh mục như cột dữ liệu, Mô tả / Ảnh giữ nguyên; các sản phẩm khác giữ nguyên (EC26, EC28); A9 | Web | AI |
<!-- END:T62 -->

#### 6.3 Điểm còn mở (chưa xử lý)

- Giá gửi dạng chuỗi số (`"350000"`) qua API chưa được phân vùng: đặc tả không nói giá trị dạng chuỗi số có hợp lệ không (liên quan A4).
- A3 (giá thập phân hợp lệ) và A6 (404 khi sản phẩm không tồn tại) quyết định kết luận của FR15-DT-04, FR15-BV-13 và FR15-B6; cần TA xác nhận.

#### 6.4 Nhận xét

- **Do prompt:** prompt không yêu cầu đối chiếu bài học từ FR-01, nên AI lặp lại lỗi đọc thông báo sau khi giao diện đổi trạng thái (G3).
- **Do giới hạn công cụ AI:** AI dễ kết luận về hành vi SUT từ thuộc tính tĩnh (G1) và dễ viết oracle / script có lỗi ngầm (G3, G4); các lỗi này chỉ lộ ra khi đọc kỹ output thay vì chỉ nhìn số Pass / Fail.
- **Do độ phức tạp feature:** Sửa phụ thuộc trạng thái form điền sẵn (G2), một khía cạnh mà dữ liệu đầu vào trong bảng không thể hiện được.

### 7. Bước 7 – Bug

Chi tiết từng bug (các bước tái hiện, kết quả mong đợi / thực tế, phân tích, ảnh): `bugs/Bug_Report.md`. Cột GitHub Issue dẫn tới issue trên repo nhóm `d1nhnguyen/eshop-sut` (ảnh chụp trang issue ở cuối `bugs/Bug_Report.md`).

| Mã | Tiêu đề | Mức độ | Thành phần | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- | --- |
| FR15-B1 | Quản lý sản phẩm cho lưu Giá bằng 0 hoặc âm khi Thêm và Sửa | Major | Backend, Web Admin | FR15-DT-08, FR15-DT-09, FR15-DT-20, FR15-DT-21, FR15-BV-11, FR15-BV-12, FR15-BV-17 | [BUG-24](https://github.com/d1nhnguyen/eshop-sut/issues/24) |
| FR15-B2 | Quản lý sản phẩm cho lưu khi thiếu Giá hoặc Giá không phải số | Major | Backend, Web Admin | FR15-DT-10, FR15-DT-11, FR15-DT-22, FR15-DT-23 | [BUG-25](https://github.com/d1nhnguyen/eshop-sut/issues/25) |
| FR15-B3 | Quản lý sản phẩm cho lưu Tên dài hơn 255 ký tự | Major | Backend, Web Admin | FR15-DT-07, FR15-DT-19, FR15-BV-05, FR15-BV-07, FR15-BV-10 | [BUG-26](https://github.com/d1nhnguyen/eshop-sut/issues/26) |
| FR15-B4 | Quản lý sản phẩm cho lưu Tên rỗng (API) hoặc chỉ gồm khoảng trắng | Major | Backend, Web Admin | FR15-DT-05, FR15-DT-06, FR15-DT-17, FR15-DT-18 | [BUG-27](https://github.com/d1nhnguyen/eshop-sut/issues/27) |
| FR15-B5 | Quản lý sản phẩm cho lưu Danh mục thiếu hoặc không có trong danh sách | Major | Backend | FR15-DT-12…FR15-DT-14, FR15-DT-24…FR15-DT-26, FR15-BV-18, FR15-BV-20 | [BUG-28](https://github.com/d1nhnguyen/eshop-sut/issues/28) |
| FR15-B6 | Sửa / Xóa sản phẩm không tồn tại trả 200 "Product updated / deleted" thay vì 404 | Minor | Backend | FR15-DT-27…FR15-DT-29, FR15-DT-31…FR15-DT-33, FR15-BV-21, FR15-BV-24, FR15-BV-25, FR15-BV-27 | [BUG-29](https://github.com/d1nhnguyen/eshop-sut/issues/29) |

Tổng: 6 bug (5 Major, 1 Minor). Ngoài phạm vi FR-15 (ghi trong danh sách đối chiếu để báo người phụ trách): `GET /api/products/:id` trả giá dạng chuỗi với id chẵn (FR-06); giá trong danh sách Admin không có phân cách hàng nghìn (FR-21).

## Mobile – Đăng nhập · Domain Testing & Boundary Value Analysis

| Mục | Giá trị |
| --- | --- |
| Feature | Mobile – Đăng nhập (Pool D, FR-20) |
| Kênh kiểm thử | App mobile (Expo Go SDK 54 trên Android Emulator `eshop_api34`, Android 14), backend qua `http://10.0.2.2:3000/api` |
| Người thực hiện | 23120031 |
| Công cụ AI | Claude Code (VS Code extension) |
| Kỹ thuật | Domain Testing (S04 – bước 1–3), Boundary Value Analysis (S04 – bước 4) |

### 0. Đặc tả (trích nguyên văn README của SUT)

> ### FR-02: Đăng nhập & Khóa tài khoản
>
> - Người dùng nhập Email và Mật khẩu.
> - Sau mỗi lần đăng nhập sai, hệ thống tăng bộ đếm lên **đúng 1 đơn vị**.
> - Nếu đăng nhập sai từ **3 lần trở lên** liên tiếp, tài khoản bị tạm khóa **30 giây** (môi trường demo). Hệ thống trả về thông báo lỗi phù hợp; không để lộ chi tiết nguyên nhân.
> - Đăng nhập thành công trả về JWT Token. Token được lưu phía client và gửi kèm tất cả các yêu cầu có xác thực qua header `Authorization: Bearer <token>`.
> - Trường email phải dùng `type="email"` (có validate HTML5 format).

> ### FR-20: Tính năng Mobile
>
> - Đầy đủ các chức năng: Xem sản phẩm, Đăng nhập, Đăng xuất, Đăng ký, Giỏ hàng, Thanh toán, Hồ sơ, Lịch sử đơn hàng.
> - Chức năng Hủy đơn hàng tuân theo đúng State Machine ở FR-10 (chỉ được hủy khi `pending` hoặc `confirmed`).

### 1. Bước 1 – Xác định biến Input / Output

#### 1.1 Quan sát giao diện (hộp đen)

App EShop Mobile chạy bằng Expo Go (SDK 54) trên Android 14, backend qua `http://10.0.2.2:3000/api`. Điều khiển và quan sát bằng `adb` (cây giao diện `uiautomator dump`, chạm, nhập chữ, chụp màn hình).

| Thiết bị ảo | Thanh trạng thái | Quan sát |
| --- | --- | --- |
| Pixel 6 (`eshop_api34`, 1080×2400, có tai thỏ camera) | cao 128 px | Thanh tiêu đề của app (y = 37–108, chứa "Đăng nhập", "Giỏ (0)") nằm **dưới** thanh trạng thái; chạm vào "Đăng nhập" không có tác dụng; không có đường nào khác tới màn hình Đăng nhập (ảnh `evidence/Mobile/B1_pixel6_header_bi_che.png`) |
| Pixel 2 (`eshop_api34_pixel2`, 1080×1920, không tai thỏ) | cao 63 px | Phần dưới của "Đăng nhập" (y = 63–98) chạm được → mở màn hình Đăng nhập; mọi thực thi ở bước 5 dùng thiết bị này |

Màn hình Đăng nhập (Pixel 2, ảnh `B1_pixel2_man_hinh_dang_nhap.png`):

| Thành phần | Quan sát |
| --- | --- |
| Tiêu đề | "Đăng Nhập" |
| Nhãn + ô thứ nhất | nhãn **"Username"**, ô nhập placeholder "Email" |
| Nhãn + ô thứ hai | nhãn "Mật khẩu", ô nhập có thuộc tính `password` (che ký tự `•`) |
| Nút | **"Sign In"**; liên kết "Quên mật khẩu?", "Chưa có tài khoản? Đăng ký ngay", "Quay Lại" |
| Sai thông tin | dòng chữ "Đăng nhập thất bại. Vui lòng kiểm tra lại." hiện ngay trên màn hình |
| Đúng thông tin | về trang chủ, thanh tiêu đề hiện "Chào, Test User"; bấm vào mở trang Hồ sơ với dữ liệu tài khoản (ảnh `B1_pixel2_sau_dang_nhap.png`) |

API mà app gọi: `POST /api/login` (`{"email", "password"}` → `{"token", "user"}`); trạng thái khóa quan sát được qua `GET /api/admin/users` (trường `login_attempts`, `locked_until`).

#### 1.2 Biến đầu vào

| ID | Biến | Kênh nhập | Kiểu / miền giá trị | Ràng buộc theo đặc tả | Nguồn |
| --- | --- | --- | --- | --- | --- |
| I1 | Email | Mobile: ô "Email"; API: `email` | chuỗi | Email của tài khoản đã đăng ký | FR-02 |
| I2 | Mật khẩu | Mobile: ô "Mật khẩu"; API: `password` | chuỗi | Khớp mật khẩu của tài khoản | FR-02 |
| I3 | Số lần đăng nhập sai liên tiếp trước lần thử | Tiền điều kiện (chuỗi thao tác trước đó) | 0, 1, 2, … | Từ 3 lần trở lên → tài khoản bị khóa | FR-02 |
| I4 | Thời gian từ lúc bị khóa tới lần thử | Tiền điều kiện (chờ) | giây | Khóa 30 giây | FR-02 |
| I5 | Có lần đăng nhập đúng xen giữa các lần sai | Tiền điều kiện | có / không | "liên tiếp" | FR-02 |

#### 1.3 Biến đầu ra

| ID | Biến | Giá trị có thể có | Nguồn |
| --- | --- | --- | --- |
| O1 | Kết quả đăng nhập | Thành công: rời màn hình Đăng nhập, thanh tiêu đề chào người dùng, mở được trang Hồ sơ (token được lưu và gửi kèm); thất bại: ở lại màn hình Đăng nhập | FR-02, FR-20 |
| O2 | Thông báo | Thông báo lỗi chung, không lộ nguyên nhân (sai email / sai mật khẩu / bị khóa) | FR-02 |
| O3 | Bộ đếm sai (`login_attempts`) | tăng đúng 1 mỗi lần sai; về 0 khi đăng nhập đúng (A3) | FR-02 |
| O4 | Trạng thái khóa (`locked_until`) | không khóa / khóa tới thời điểm lần sai thứ 3 + 30 giây | FR-02 |
| O5 | Phản hồi API | `200` + `token` / `401` khi sai / mã lỗi khi bị khóa | `api_specification.md` 1.2 |

#### 1.4 Giả định cho những chỗ đặc tả chưa rõ

| ID | Giả định | Căn cứ |
| --- | --- | --- |
| A1 | Quy tắc đăng nhập trên Mobile là quy tắc của FR-02 | FR-20 chỉ nêu Mobile có chức năng Đăng nhập; nhóm thống nhất Pool D = các chức năng của FR-20. Cần TA xác nhận |
| A2 | Tài khoản bị khóa ngay sau lần sai thứ 3 liên tiếp; trong 30 giây sau đó mọi lần đăng nhập (kể cả mật khẩu đúng) bị từ chối; sau 2 lần sai vẫn đăng nhập đúng được | "sai từ 3 lần trở lên liên tiếp … tạm khóa 30 giây" |
| A3 | Đăng nhập thành công đặt bộ đếm về 0 | "liên tiếp" |
| A4 | Bộ đếm / thời điểm khóa quan sát qua `GET /api/admin/users` (`login_attempts`, `locked_until`) | API Admin có trong `api_specification.md` 6.1 |
| A5 | Cùng một thông báo cho sai email, sai mật khẩu, email không tồn tại; khi bị khóa thông báo có thể khác nhưng không cho đăng nhập | "không để lộ chi tiết nguyên nhân" |
| A6 | Email so khớp không phân biệt hoa / thường và bỏ khoảng trắng đầu / cuối; mật khẩu so khớp chính xác | Nhất quán với FR-01 (giả định A3, A4 của FR-01) |
| A7 | Đăng nhập với email không tồn tại không làm thay đổi bộ đếm của tài khoản nào | Không có tài khoản để đếm |
| A8 | "Token được lưu phía client và gửi kèm" kiểm chứng bằng việc mở được trang Hồ sơ (cần xác thực) sau khi đăng nhập; không yêu cầu giữ phiên sau khi tắt app | FR-02 |
| A9 | Ô Mật khẩu phải che ký tự (tương đương `type="password"` của FR-22 trên mobile) | FR-22 |

#### 1.5 Ngoài phạm vi

- Đăng xuất, Đăng ký, Quên mật khẩu trên Mobile (các chức năng khác của Pool D); đăng nhập trên Web (FR-02).

### 2. Bước 2 – Lớp tương đương (Complete Set of Partitions)

#### 2.1 Cách áp dụng guideline cho từng biến

| Biến | Điều kiện trong đặc tả | Guideline [S04] | Lớp tạo ra |
| --- | --- | --- | --- |
| I1 Email | email của tài khoản đã đăng ký | "Phải là" → đã đăng ký / không tồn tại; tách lớp (G5): khác hoa / thường, có khoảng trắng đầu / cuối (so khớp có thể khác nhau – A6), rỗng, sai định dạng | 3 valid, 3 invalid |
| I2 Mật khẩu | khớp mật khẩu | "Phải là" → đúng / sai; tách lớp (G5): rỗng, chỉ khác hoa / thường, thừa khoảng trắng cuối (so khớp có thể bỏ qua – A6) | 1 valid, 4 invalid |
| I3 Số lần sai liên tiếp trước đó | "từ 3 lần trở lên … bị khóa" | Khoảng giá trị: 0–2 (chưa khóa) / ≥ 3 (khóa) | 1 valid, 1 invalid |
| I4 Thời gian từ lúc khóa | "tạm khóa 30 giây" | Khoảng giá trị: < 30 giây (còn khóa) / ≥ 30 giây (hết khóa) | 1 valid, 1 invalid |
| I5 Đăng nhập đúng xen giữa | "liên tiếp" | "Phải là" chuỗi liên tiếp mới khóa → có lần đúng xen giữa thì bộ đếm làm mới (A3) | 1 valid |
| Đầu ra O1–O5 | thành công / thất bại / bộ đếm / khóa / hết khóa | Phân vùng đầu ra như ví dụ [UC] | 5 lớp đầu ra |

#### 2.2 Complete Set of Partitions

| EC | Biến | Phân vùng | Ví dụ đại diện | Valid / Invalid |
| --- | --- | --- | --- | --- |
| EC1 | I1 Email | Email đã đăng ký, đúng chính xác | `test@eshop.com` | Valid |
| EC2 | I1 Email | Email đã đăng ký, khác chữ hoa / thường (A6) | `TEST@eshop.com` | Valid |
| EC3 | I1 Email | Email đã đăng ký, có khoảng trắng đầu / cuối (A6) | `␣test@eshop.com␣` | Valid |
| EC4 | I1 Email | Email không tồn tại | `khongco@eshop.com` | Invalid |
| EC5 | I1 Email | Rỗng | `` | Invalid |
| EC6 | I1 Email | Sai định dạng | `test@eshop` | Invalid |
| EC7 | I2 Mật khẩu | Đúng | `Test1234!` | Valid |
| EC8 | I2 Mật khẩu | Sai | `Sai12345!` | Invalid |
| EC9 | I2 Mật khẩu | Rỗng | `` | Invalid |
| EC10 | I2 Mật khẩu | Chỉ khác chữ hoa / thường | `test1234!` | Invalid |
| EC11 | I2 Mật khẩu | Thừa khoảng trắng cuối (A6) | `Test1234!␣` | Invalid |
| EC12 | I3 | 0–2 lần sai liên tiếp trước đó (chưa khóa) | 0 | Valid |
| EC13 | I3 | ≥ 3 lần sai liên tiếp trước đó (bị khóa) | 3 | Invalid |
| EC14 | I4 | Thử lại khi chưa hết 30 giây khóa | ngay sau khi khóa | Invalid |
| EC15 | I4 | Thử lại khi đã hết 30 giây khóa | sau 35 giây | Valid |
| EC16 | I5 | Có lần đăng nhập đúng xen giữa các lần sai (A3) | sai, sai, đúng, sai, sai, đúng | Valid |
| EC17 | O1, O5 | Đăng nhập thành công: rời màn hình Đăng nhập, chào người dùng, mở được Hồ sơ; API `200` + `token` | | Output |
| EC18 | O1, O2, O5 | Thất bại: thông báo lỗi chung, giống nhau cho sai email / sai mật khẩu (A5); API `401` | | Output |
| EC19 | O3 | Bộ đếm `login_attempts` tăng đúng 1 sau mỗi lần sai | | Output |
| EC20 | O1, O4 | Bị khóa: từ chối cả mật khẩu đúng | | Output |
| EC21 | O1, O4 | Hết khóa: đăng nhập đúng thành công, bộ đếm về 0 | | Output |

Tổng: 16 lớp đầu vào (7 valid, 9 invalid) và 5 lớp đầu ra.

### 3. Bước 3 – Test case Domain Testing

#### 3.1 Thủ tục thực hiện

Mọi test case dùng chung thủ tục, chỉ dữ liệu thay đổi → dạng **data matrix** [DR]. ID có tiền tố `MOB-`. Mỗi test case gồm các **lần thử trước** (tiền điều kiện, thực hiện cùng kênh) và **lần thử được đánh giá** (cột Email, Mật khẩu). Trong bảng: `␣` là một dấu cách; `(rỗng)` là để trống ô.

**Tiền điều kiện chung (self-standing, self-cleaning):** khởi động lại backend trước mỗi test case → `test@eshop.com / Test1234!` có `login_attempts = 0`, chưa bị khóa.

**P-MOBILE** – Android Emulator Pixel 2, Expo Go:

| Bước | Hành động | Kết quả mong đợi của bước |
| --- | --- | --- |
| 1 | Mở lại app (trạng thái chưa đăng nhập), bấm "Đăng nhập" trên thanh tiêu đề | Màn hình "Đăng Nhập" với ô Email, Mật khẩu, nút đăng nhập |
| 2 | Thực hiện lần lượt các lần thử trước: nhập Email, Mật khẩu, bấm nút đăng nhập; nếu đăng nhập thành công thì quay lại màn hình Đăng nhập | Như thiết kế của tiền điều kiện |
| 3 | Chờ theo cột "Chờ trước lần thử" (tính từ lần thử trước cuối cùng) | – |
| 4 | Nhập Email, Mật khẩu theo cột dữ liệu, bấm nút đăng nhập | Như cột Kết quả mong đợi |
| 5 | Nếu đăng nhập thành công: bấm "Chào, …" trên thanh tiêu đề | Trang "Hồ sơ của bạn" hiện email `test@eshop.com` (token được dùng – A8) |
| 6 | Kiểm chứng bộ đếm: `GET /api/admin/users` → `login_attempts`, `locked_until` của `test@eshop.com` (A4) | Như cột Kết quả mong đợi |

**P-API** – các lần thử trước và lần thử được đánh giá là `POST /api/login` với `{"email", "password"}`; kiểm chứng mã HTTP, `token`, và bước 6 như trên.

#### 3.2 Minimum Set of Test Cases

Dữ liệu và kết quả mong đợi được sinh từ `scripts/mobile/cases.py` (cùng nguồn với script thực thi) bằng `scripts/mobile/report_tables.py`.

<!-- BEGIN:T32 -->
**Test case valid** – mỗi test case phủ nhiều lớp valid nhất có thể:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Email | Mật khẩu | Các lần thử trước (tiền điều kiện) | Chờ trước lần thử | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MOB-DT-01 | Kiểm tra đăng nhập thành công với email và mật khẩu đúng | EC1, EC7, EC12, EC17 | `test@eshop.com` | `Test1234!` | – | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17) | Mobile, API | AI |
| MOB-DT-02 | Kiểm tra đăng nhập thành công khi email khác chữ hoa / thường | EC2, EC7, EC12, EC17 | `TEST@eshop.com` | `Test1234!` | – | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); A6 | Mobile, API | AI |
| MOB-DT-03 | Kiểm tra đăng nhập thành công khi email có khoảng trắng đầu / cuối | EC3, EC7, EC12, EC17 | `␣test@eshop.com␣` | `Test1234!` | – | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); A6 | Mobile, API | AI |
| MOB-DT-04 | Kiểm tra đăng nhập thành công khi đã hết 30 giây khóa | EC15, EC21 | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | 35 giây | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); tiền điều kiện: 3 lần sai liên tiếp rồi chờ 35 giây | Mobile, API | AI |
| MOB-DT-05 | Kiểm tra đăng nhập đúng xen giữa làm mới chuỗi sai liên tiếp | EC16, EC12, EC17 | `test@eshop.com` | `Test1234!` | 2 × sai (`Sai12345!`) → 1 × đúng (`Test1234!`) → 2 × sai (`Sai12345!`) | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); A3; sau lần đúng thứ nhất chuỗi sai bắt đầu lại nên 2 lần sai sau không làm khóa tài khoản | Mobile, API | AI |

**Test case invalid** – mỗi test case phủ đúng một lớp invalid, các biến còn lại hợp lệ:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Email | Mật khẩu | Các lần thử trước (tiền điều kiện) | Chờ trước lần thử | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MOB-DT-06 | Kiểm tra đăng nhập bị từ chối khi sai mật khẩu | EC8, EC18, EC19 | `test@eshop.com` | `Sai12345!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19) | Mobile, API | AI |
| MOB-DT-07 | Kiểm tra đăng nhập bị từ chối với cùng thông báo khi email không tồn tại | EC4, EC18 | `khongco@eshop.com` | `Test1234!` | 1 × sai (`Sai12345!`) | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19); A5, A7: thông báo giống hệt lần sai mật khẩu ở tiền điều kiện; bộ đếm của `test@eshop.com` giữ 1 | Mobile, API | AI |
| MOB-DT-08 | Kiểm tra đăng nhập bị từ chối khi bỏ trống email | EC5, EC18 | (rỗng) | `Test1234!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 0 (EC18, EC19) | Mobile, API | AI |
| MOB-DT-09 | Kiểm tra đăng nhập bị từ chối khi email sai định dạng | EC6, EC18 | `test@eshop` | `Test1234!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 0 (EC18, EC19) | Mobile, API | AI |
| MOB-DT-10 | Kiểm tra đăng nhập bị từ chối khi bỏ trống mật khẩu | EC9, EC18 | `test@eshop.com` | (rỗng) | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19) | Mobile, API | AI |
| MOB-DT-11 | Kiểm tra đăng nhập bị từ chối khi mật khẩu chỉ khác chữ hoa / thường | EC10, EC18 | `test@eshop.com` | `test1234!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19) | Mobile, API | AI |
| MOB-DT-12 | Kiểm tra đăng nhập bị từ chối khi mật khẩu thừa khoảng trắng cuối | EC11, EC18 | `test@eshop.com` | `Test1234!␣` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19); A6 | Mobile, API | AI |
| MOB-DT-13 | Kiểm tra đăng nhập bị từ chối dù mật khẩu đúng khi đã sai 3 lần liên tiếp | EC13, EC14, EC20 | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | – | Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20); A2 | Mobile, API | AI |
<!-- END:T32 -->

#### 3.3 Bảng phủ phân vùng

<!-- BEGIN:T33 -->
| EC | Test case phủ | | EC | Test case phủ |
| --- | --- | --- | --- | --- |
| EC1 | MOB-DT-01 | | EC12 | MOB-DT-01…MOB-DT-03, MOB-DT-05 |
| EC2 | MOB-DT-02 | | EC13 | MOB-DT-13 |
| EC3 | MOB-DT-03 | | EC14 | MOB-DT-13 |
| EC4 | MOB-DT-07 | | EC15 | MOB-DT-04 |
| EC5 | MOB-DT-08 | | EC16 | MOB-DT-05; bổ sung: MOB-DT-14 (mục 6.2) |
| EC6 | MOB-DT-09 | | EC17 | MOB-DT-01…MOB-DT-03, MOB-DT-05; bổ sung: MOB-DT-14 (mục 6.2) |
| EC7 | MOB-DT-01…MOB-DT-03 | | EC18 | MOB-DT-06…MOB-DT-12 |
| EC8 | MOB-DT-06 | | EC19 | MOB-DT-06 |
| EC9 | MOB-DT-10 | | EC20 | MOB-DT-13 |
| EC10 | MOB-DT-11 | | EC21 | MOB-DT-04 |
| EC11 | MOB-DT-12 | |  |  |

21 / 21 lớp được phủ bởi 13 test case Minimum Set (5 valid, 8 invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp invalid có test case riêng. Các đại diện bổ sung sau rà soát (mục 6.2) ghi sau dấu `;`.
<!-- END:T33 -->

### 4. Bước 4 – Boundary Value Analysis

#### 4.1 Xác định biên

| Biến | Phân vùng | LB | UB | Bước nhảy | Điểm kiểm tra |
| --- | --- | --- | --- | --- | --- |
| I3 số lần sai liên tiếp trước lần thử | EC12 (0–2) / EC13 (≥ 3) | 0; 3 | 2; – | 1 lần | 0, 1, 2, 3, 4 |
| Bộ đếm `login_attempts` | tăng 1 mỗi lần sai, khóa khi đạt 3 | – | 3 | 1 | sau lần sai thứ 2 → 3 |
| I4 thời gian từ lúc khóa | EC14 (< 30 giây) / EC15 (≥ 30 giây) | 30 giây | – | 2 giây (sai số thao tác trên Mobile ~1 giây) | 0, 28, 32, 35 giây |
| Độ dài mật khẩu so với mật khẩu đúng | EC7 / EC8 | 9 ký tự (`Test1234!`) | 9 | 1 ký tự | 8, 9, 10 ký tự |
| Độ dài email so với email đúng | EC1 / EC4 | 14 ký tự (`test@eshop.com`) | 14 | 1 ký tự | 13, 14, 15 ký tự |

#### 4.2 Boundary Value Test Cases

Thủ tục: mục 3.1. Bảng giữ các cột dữ liệu của data matrix như mục 3.2. Dòng có ID trong ngoặc là điểm biên đã có trong Minimum Set, chỉ dẫn chiếu.

<!-- BEGIN:T42 -->
| ID | Tên test case (Action + Function + Condition) | Partition tested | Email | Mật khẩu | Các lần thử trước (tiền điều kiện) | Chờ trước lần thử | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| (MOB-DT-01) | Kiểm tra đăng nhập thành công với email và mật khẩu đúng | EC12 – 0 lần sai (LB) | `test@eshop.com` | `Test1234!` | – | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17) | Mobile, API | xem 3.2 |
| MOB-BV-01 | Kiểm tra đăng nhập thành công khi trước đó sai 1 lần | EC12 – 1 lần sai (LB+1) | `test@eshop.com` | `Test1234!` | 1 × sai (`Sai12345!`) | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17) | Mobile, API | AI |
| MOB-BV-02 | Kiểm tra đăng nhập thành công khi trước đó sai 2 lần liên tiếp | EC12/EC13 – 2 lần sai (UB của EC12) | `test@eshop.com` | `Test1234!` | 2 × sai (`Sai12345!`) | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); A2 | Mobile, API | AI |
| (MOB-DT-13) | Kiểm tra đăng nhập bị từ chối dù mật khẩu đúng khi đã sai 3 lần liên tiếp | EC13 – 3 lần sai (LB của EC13) | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | – | Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20); A2 | Mobile, API | xem 3.2 |
| MOB-BV-03 | Kiểm tra đăng nhập bị từ chối dù mật khẩu đúng khi trước đó sai 4 lần liên tiếp | EC13 – 4 lần sai (LB+1 của EC13) | `test@eshop.com` | `Test1234!` | 4 × sai (`Sai12345!`) | – | Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20) | Mobile, API | AI |
| MOB-BV-04 | Kiểm tra lần sai thứ 3 liên tiếp đưa bộ đếm lên 3 và khóa tài khoản | EC19 – bộ đếm 2 → 3 (biên khóa) | `test@eshop.com` | `Sai12345!` | 2 × sai (`Sai12345!`) | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 3 (EC18, EC19); sau lần này `locked_until` ≈ thời điểm hiện tại + 30 giây | Mobile, API | AI |
| (MOB-DT-13) | Kiểm tra đăng nhập bị từ chối dù mật khẩu đúng khi đã sai 3 lần liên tiếp | EC14 – 0 giây sau khi khóa | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | – | Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20); A2 | Mobile, API | xem 3.2 |
| MOB-BV-05 | Kiểm tra đăng nhập bị từ chối khi mới qua 28 giây khóa | EC14/EC15 – 28 giây (UB-1 của EC14, sai số thao tác ~1 giây) | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | 28 giây | Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20) | Mobile, API | AI |
| MOB-BV-06 | Kiểm tra đăng nhập thành công khi đã qua 32 giây khóa | EC14/EC15 – 32 giây (LB+1 của EC15, sai số thao tác ~1 giây) | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | 32 giây | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17) | Mobile, API | AI |
| (MOB-DT-04) | Kiểm tra đăng nhập thành công khi đã hết 30 giây khóa | EC15 – 35 giây | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | 35 giây | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); tiền điều kiện: 3 lần sai liên tiếp rồi chờ 35 giây | Mobile, API | xem 3.2 |
| (MOB-DT-01) | Kiểm tra đăng nhập thành công với email và mật khẩu đúng | EC7 – mật khẩu đúng độ dài | `test@eshop.com` | `Test1234!` | – | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17) | Mobile, API | xem 3.2 |
| MOB-BV-07 | Kiểm tra đăng nhập bị từ chối khi mật khẩu thiếu 1 ký tự cuối | EC7/EC8 – độ dài mật khẩu − 1 | `test@eshop.com` | `Test1234` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19) | Mobile, API | AI |
| MOB-BV-08 | Kiểm tra đăng nhập bị từ chối khi mật khẩu thừa 1 ký tự | EC7/EC8 – độ dài mật khẩu + 1 | `test@eshop.com` | `Test1234!!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19) | Mobile, API | AI |
| MOB-BV-09 | Kiểm tra đăng nhập bị từ chối khi email thiếu 1 ký tự cuối | EC1/EC4 – độ dài email − 1 | `test@eshop.co` | `Test1234!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 0 (EC18, EC19) | Mobile, API | AI |
| MOB-BV-10 | Kiểm tra đăng nhập bị từ chối khi email thừa 1 ký tự | EC1/EC4 – độ dài email + 1 | `test@eshop.comm` | `Test1234!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 0 (EC18, EC19) | Mobile, API | AI |

Tổng: 10 test case BVA mới (MOB-BV-01…MOB-BV-10); 5 dòng có ID trong ngoặc là điểm biên đã được phủ bởi test case Minimum Set (mục 3.2), chỉ dẫn chiếu, không chạy lại.
<!-- END:T42 -->

### 5. Bước 5 – Kết quả thực thi

#### 5.1 Môi trường và cách chạy

| Mục | Giá trị |
| --- | --- |
| Ngày chạy | 2026-10-21 |
| Người chạy | 23120031 (script tự động, kết quả được rà soát thủ công) |
| SUT | `eshop-sut-main` (trùng với `d1nhnguyen/eshop-sut`); `frontend-mobile/App.js:16` trỏ `API_URL` tới `http://10.0.2.2:3000/api` |
| Mobile | Expo Go SDK 54, Android Emulator **Pixel 2** (`eshop_api34_pixel2`, Android 14, 1080×1920); điều khiển qua `adb` (`scripts/mobile/adb_ui.py`) |
| API | `http://localhost:3000/api`, gọi bằng Python `urllib` |
| Dữ liệu | Backend được khởi động lại và app được mở lại trước mỗi test case |
| Script | `scripts/mobile/cases.py` (dữ liệu), `run_mobile.py` (P-MOBILE), `run_api.py` (P-API), `common.py` (kết luận chung cho 2 kênh), `report_tables.py` |
| Bằng chứng | `evidence/Mobile/web_results.json` (kênh Mobile), `api_results.json`; ảnh màn hình sau lần thử được đánh giá `evidence/Mobile/web/<ID>.png` |

Cách kết luận: "thành công" Pass khi rời màn hình Đăng nhập, thanh tiêu đề chào người dùng, mở được Hồ sơ (API: `200` + `token`) và bộ đếm về 0. "Từ chối" Pass khi ở lại màn hình Đăng nhập với thông báo lỗi (API 4xx, không có `token`), bộ đếm đúng giá trị mong đợi và tài khoản chỉ bị khóa khi đủ 3 lần sai. Test case có tiền điều kiện không dựng được (lần đăng nhập đúng trong chuỗi bị từ chối) là **Blocked**.

#### 5.2 Phát hiện chính

- **Pixel 6 không mở được màn hình Đăng nhập** (thanh tiêu đề bị thanh trạng thái che – mục 1.1); mọi thực thi trên Mobile dùng Pixel 2.
- **Bộ đếm tăng 2 mỗi lần sai:** gọi `POST /api/login` sai một lần → `login_attempts` từ 0 lên 2 (đã kiểm tra bằng đúng một request, loại trừ khả năng script gửi hai lần); vì vậy tài khoản bị khóa ngay sau lần sai thứ 2.
- **Thời gian khóa 180 giây:** `locked_until` = thời điểm khóa + 180 giây; sau 32–35 giây vẫn bị từ chối. Các lần thử trong lúc khóa không gia hạn khóa.
- Thông báo trên Mobile luôn là "Đăng nhập thất bại. Vui lòng kiểm tra lại." – giống nhau cho sai email / sai mật khẩu / bị khóa (không lộ nguyên nhân). API trả "Invalid email or password" (401) hoặc "Tài khoản đã bị khóa. Vui lòng thử lại sau." (403).
- Email khác chữ hoa / thường hoặc có khoảng trắng đầu / cuối bị từ chối (A6).
- Đăng nhập đúng làm mới bộ đếm (MOB-DT-14 Pass); MOB-DT-05 Blocked vì tài khoản đã bị khóa từ lần sai thứ 2 nên lần đăng nhập đúng ở giữa chuỗi không thực hiện được.

#### 5.3 Kết quả theo test case

Mỗi test case một dòng. Bảng sinh từ `evidence/Mobile/web_results.json` (cột Mobile) và `api_results.json`.

<!-- BEGIN:T53 -->
| TC | Mobile | Kết quả thực tế – Mobile | API | Kết quả thực tế – API | Bằng chứng | Bug |
| --- | --- | --- | --- | --- | --- | --- |
| MOB-DT-01 | Pass | Đăng nhập thành công, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; bộ đếm = 0 | Pass | HTTP 200 “Login successful”, có token; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-01.png) · `api_results.json` | – |
| MOB-DT-02 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-02.png) · `api_results.json` | MOB-B4 |
| MOB-DT-03 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-03.png) · `api_results.json` | MOB-B4 |
| MOB-DT-04 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:35:02 UTC | Fail | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:55:56 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-04.png) · `api_results.json` | MOB-B3 |
| MOB-DT-05 | Blocked | tiền điều kiện không dựng được: lần đăng nhập đúng trong chuỗi bị từ chối (“Đăng nhập thất bại. Vui lòng kiểm tra lại.”) | Blocked | tiền điều kiện không dựng được: lần đăng nhập đúng trong chuỗi bị từ chối (“Tài khoản đã bị khóa. Vui lòng thử lại sau.”) | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-05.png) · `api_results.json` | – |
| MOB-DT-06 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-06.png) · `api_results.json` | MOB-B2 |
| MOB-DT-07 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-07.png) · `api_results.json` | MOB-B2 |
| MOB-DT-08 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Pass | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-08.png) · `api_results.json` | – |
| MOB-DT-09 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Pass | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-09.png) · `api_results.json` | – |
| MOB-DT-10 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-10.png) · `api_results.json` | MOB-B2 |
| MOB-DT-11 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-11.png) · `api_results.json` | MOB-B2 |
| MOB-DT-12 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-12.png) · `api_results.json` | MOB-B2 |
| MOB-DT-13 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:45:04 UTC | Pass | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:56:40 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-13.png) · `api_results.json` | – |
| MOB-BV-01 | Pass | Đăng nhập thành công, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; bộ đếm = 0 | Pass | HTTP 200 “Login successful”, có token; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-01.png) · `api_results.json` | – |
| MOB-BV-02 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:48:33 UTC | Fail | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:56:42 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-02.png) · `api_results.json` | MOB-B2 |
| MOB-BV-03 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:50:15 UTC | Pass | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:56:43 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-03.png) · `api_results.json` | – |
| MOB-BV-04 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:52:50 UTC | Fail | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:56:44 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-04.png) · `api_results.json` | MOB-B2 |
| MOB-BV-05 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:54:33 UTC | Pass | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:56:44 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-05.png) · `api_results.json` | – |
| MOB-BV-06 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:56:48 UTC | Fail | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:57:13 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-06.png) · `api_results.json` | MOB-B3 |
| MOB-BV-07 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-07.png) · `api_results.json` | MOB-B2 |
| MOB-BV-08 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-08.png) · `api_results.json` | MOB-B2 |
| MOB-BV-09 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Pass | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-09.png) · `api_results.json` | – |
| MOB-BV-10 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Pass | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-10.png) · `api_results.json` | – |
| MOB-DT-14 | Pass | Đăng nhập thành công, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; bộ đếm = 0 | Pass | HTTP 200 “Login successful”, có token; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-14.png) · `api_results.json` | – |
<!-- END:T53 -->

#### 5.4 Tổng hợp

<!-- BEGIN:T55 -->
| Kênh | Thiết kế | Đã chạy | Pass | Fail | Blocked | Không áp dụng |
| --- | --- | --- | --- | --- | --- | --- |
| Mobile | 24 | 24 | 10 | 13 | 1 | 0 |
| API | 24 | 24 | 10 | 13 | 1 | 0 |
| **Tổng lượt chạy** | | **48** | **20** | **26** | **2** | |

24 test case = 13 Minimum Set (mục 3.2) + 10 BVA (mục 4.2) + 1 bổ sung sau rà soát (mục 6.2). Gộp các kênh theo test case (Fail nếu Fail ở bất kỳ kênh nào, Blocked nếu còn kênh bị Blocked): 10 Pass, 13 Fail, 1 Blocked.
<!-- END:T55 -->

### 6. Bước 6 – AI gap analysis

> G1–G5: AI (Claude Code) tự phát hiện trong lúc làm các bước 1–5. Sinh viên rà soát và bổ sung các điểm tự phát hiện ở commit `[Mobile][Bn-review]`.

#### 6.1 Những gì AI bỏ sót hoặc làm sai

| # | AI bỏ sót / làm sai | Loại | Nguyên nhân | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |
| G1 | Thiết kế không có biến "thiết bị / kích thước thanh trạng thái"; AI chỉ chuẩn bị một máy ảo (Pixel 6) và suýt kết luận cả feature bị chặn | Biến đầu vào thiếu (môi trường) | **Độ phức tạp feature**: hành vi giao diện phụ thuộc thiết bị; **do prompt**: đề không nêu thiết bị đích | Không chạm được "Đăng nhập" ở bước 1 | Tạo thêm máy Pixel 2, ghi bug MOB-B1, ghi điểm cần kiểm tra trên điện thoại thật |
| G2 | MOB-DT-05 (đăng nhập đúng xen giữa) phụ thuộc bộ đếm tăng đúng 1; khi bộ đếm tăng 2 thì tiền điều kiện không dựng được nên test case không trả lời được câu hỏi "có làm mới bộ đếm không" | Thiết kế test case | **Độ phức tạp feature**: hai quy tắc (đếm, làm mới) ràng buộc nhau; AI chọn chuỗi thao tác dài thay vì chuỗi ngắn nhất cô lập quy tắc | Kết quả API: lần đăng nhập đúng ở giữa bị 403 | Đánh Blocked; bổ sung MOB-DT-14 (sai → đúng → sai → đúng) |
| G3 | Bộ đếm tăng 2 lúc đầu có thể do script chạm nút hai lần | Nguy cơ kết luận sai | **Giới hạn công cụ AI**: tự động hoá giao diện qua `adb` không thấy được request mạng | AI kiểm tra lại bằng đúng một request API | Kết luận chỉ sau khi tái hiện bằng một request |
| G4 | Runner Mobile bản đầu: lỗi `KeyError` khi in kết quả Blocked; mở lại app ngay sau `force-stop` thất bại → 4 test case Blocked giả; phải dừng và chạy lại | Thực thi | **Giới hạn công cụ AI**: script chưa xử lý trạng thái không mong đợi của emulator / Expo Go | Ảnh chụp lúc Blocked là màn hình chính Android | Chỉ rõ package khi mở app, thử lại tối đa 3 lần, chờ trang chủ tải xong |
| G5 | Điểm biên thời gian 28 / 32 giây chỉ kiểm tra được biên theo đặc tả (30 giây); biên thực tế của SUT (180 giây) chỉ đo được qua `locked_until`, chưa chạy test case quanh 180 giây | Biên chưa phủ | **Giới hạn thời gian thực thi** (mỗi lần chờ 3 phút) | Khảo sát `locked_until` | Ghi trong bug MOB-B3; để mở |

#### 6.2 Test case bổ sung

Kết quả thực thi nằm ở mục 5.3.

<!-- BEGIN:T62 -->
| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Email | Mật khẩu | Các lần thử trước (tiền điều kiện) | Chờ trước lần thử | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MOB-DT-14 | Kiểm tra đăng nhập đúng sau một lần sai làm mới bộ đếm | EC16, EC17 | `test@eshop.com` | `Test1234!` | 1 × sai (`Sai12345!`) → 1 × đúng (`Test1234!`) → 1 × sai (`Sai12345!`) | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); A3; nếu bộ đếm không về 0 sau lần đúng thì 2 lần sai cộng dồn sẽ khóa tài khoản | Mobile, API | AI |
<!-- END:T62 -->

#### 6.3 Điểm còn mở (chưa xử lý)

- Kiểm tra lại MOB-B1 trên điện thoại thật có tai thỏ để xác nhận mức độ ảnh hưởng.
- A1 (Mobile kế thừa FR-02), A2 (khóa ngay sau lần sai thứ 3), A6 (email không phân biệt hoa / thường) cần TA xác nhận.

#### 6.4 Nhận xét

- **Do prompt:** đề và prompt không nêu thiết bị đích nên AI không phân vùng theo thiết bị (G1).
- **Do giới hạn công cụ AI:** tự động hoá mobile qua `adb` kém ổn định hơn Web; AI phải tự xác minh bằng kênh API để tránh kết luận sai (G3, G4).
- **Do độ phức tạp feature:** các quy tắc đếm / khóa / làm mới phụ thuộc trạng thái và thời gian; một lỗi (bộ đếm tăng 2) che các test case khác (G2).

### 7. Bước 7 – Bug

Chi tiết từng bug: `bugs/Bug_Report.md`. Tiêu đề issue dùng `[FR-20]`. Cột GitHub Issue dẫn tới issue trên repo nhóm `d1nhnguyen/eshop-sut` (ảnh chụp trang issue ở cuối `bugs/Bug_Report.md`).

| Mã | Tiêu đề | Mức độ | Thành phần | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- | --- |
| MOB-B1 | Thanh tiêu đề app Mobile bị thanh trạng thái che trên máy có thanh trạng thái cao, không mở được màn hình Đăng nhập | Critical | Mobile | Quan sát bước 1 (Pixel 6) | [BUG-32](https://github.com/d1nhnguyen/eshop-sut/issues/32) |
| MOB-B2 | Mỗi lần đăng nhập sai bộ đếm tăng 2, tài khoản bị khóa ngay sau lần sai thứ 2 | Major | Backend (ảnh hưởng Mobile) | MOB-DT-06, MOB-DT-07, MOB-DT-10…MOB-DT-12, MOB-BV-02, MOB-BV-04, MOB-BV-07, MOB-BV-08 | [BUG-33](https://github.com/d1nhnguyen/eshop-sut/issues/33) |
| MOB-B3 | Tài khoản bị khóa 180 giây thay vì 30 giây | Major | Backend (ảnh hưởng Mobile) | MOB-DT-04, MOB-BV-06 | [BUG-34](https://github.com/d1nhnguyen/eshop-sut/issues/34) |
| MOB-B4 | Đăng nhập thất bại khi email khác chữ hoa / thường hoặc có khoảng trắng đầu / cuối | Minor | Backend (ảnh hưởng Mobile) | MOB-DT-02, MOB-DT-03 | [BUG-35](https://github.com/d1nhnguyen/eshop-sut/issues/35) |
| MOB-B5 | Màn hình Đăng nhập Mobile dùng nhãn tiếng Anh "Username" cho ô Email và nút "Sign In" | Minor | Mobile | Quan sát bước 1 | [BUG-36](https://github.com/d1nhnguyen/eshop-sut/issues/36) |

Tổng: 5 bug (1 Critical, 2 Major, 2 Minor). Ngoài phạm vi (đã ghi trong danh sách đối chiếu): nút đăng xuất ghi "Thoát" (FR-23).

## Khai báo sử dụng AI (Mandatory Disclosure)

Các test case, script, bảng kết quả, nháp bug report và báo cáo Domain Testing + BVA của 4 feature (FR-01, FR-10, FR-15, Mobile – Đăng nhập) trong bài này được sinh phiên bản đầu bởi Claude Code (Claude Opus 5.5); báo cáo FR-01 và 22 bug được rà soát chéo bằng Google Antigravity (Gemini 4 Argon). Tôi đã rà soát và quyết định các chỉnh sửa cho báo cáo FR-01 (cấu trúc bảng BVA, dữ liệu test case, ID, bảng kết quả – Claude Code thực hiện theo nhận xét rà soát), duyệt các test case bổ sung FR01-DT-29…32, FR15-DT-34, MOB-DT-14 do AI đề xuất, và tự tạo 22 issue BUG-15…BUG-36 trên GitHub kèm ảnh bằng chứng. AI Critique, cột lý do, kết luận và đoạn khai báo này cũng do Claude Code nháp theo yêu cầu của tôi và đã được tôi đọc, duyệt. Mô tả bug do AI nháp: đề HW02 §11 không đặt ràng buộc chống dùng AI (Anti-AI-Cheat: None) nên tôi khai báo rõ tại đây thay cho kỳ vọng "bug report 100% sinh viên viết" của AI-01 §11. AI Audit Report chi tiết ở trên, prompt log có thời gian ở Phụ lục A (`ai/prompt_log.md`). Ngoài phần mô tả bug đã nêu, tôi cam đoan không dùng AI để sinh bất kỳ artifact nào thuộc danh mục bị cấm của AI-01 §10 (video demo có giọng nói của tôi do tôi tự quay).

Hồ sơ đi kèm: `ai/AI_Audit_Report.md` (AI Audit Report), `ai/AI_Disclosure_Form.md`, `ai/AI_Critique.md`, `ai/AI_Privacy_Checklist.md`, `ai/prompt_log.md` (Phụ lục A – prompt log có thời gian).
