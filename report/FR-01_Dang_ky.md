# FR-01 – Đăng ký tài khoản · Domain Testing & Boundary Value Analysis

| Mục | Giá trị |
| --- | --- |
| Feature | FR-01 – Đăng ký tài khoản (Pool A) |
| Kênh kiểm thử | Web khách hàng (`/register`, http://localhost:5173) + API `POST /api/register` |
| Người thực hiện | 23120031 |
| Công cụ AI | Claude Code (VS Code extension) |
| Kỹ thuật | Domain Testing (S04 – bước 1–3), Boundary Value Analysis (S04 – bước 4) |

## 0. Đặc tả (trích nguyên văn README của SUT)

> ### FR-01: Đăng ký tài khoản
>
> - Người dùng phải cung cấp: **Họ Tên**, **Email**, **Mật khẩu**.
> - Email phải có định dạng hợp lệ (`user@domain.com`) và là duy nhất trong hệ thống.
> - **Yêu cầu mật khẩu mạnh**: Tối thiểu 8 ký tự, có ít nhất 1 chữ hoa, 1 chữ thường, 1 chữ số và 1 ký tự đặc biệt (`@`, `$`, `!`, `%`, `*`, `?`, `&`).
> - Phải có trường **Xác nhận mật khẩu** — hệ thống từ chối nếu hai trường không khớp.
> - Sau khi đăng ký thành công, người dùng được chuyển tới trang Đăng nhập.

## 1. Bước 1 – Xác định biến Input / Output

### 1.1 Quan sát giao diện (hộp đen)

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

### 1.2 Biến đầu vào

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

### 1.3 Biến đầu ra

| ID | Biến | Giá trị có thể có | Nguồn |
| --- | --- | --- | --- |
| O1 | Kết quả đăng ký | (a) Thành công: tài khoản được tạo và người dùng được chuyển tới trang Đăng nhập; (b) Bị từ chối: không tạo tài khoản, ở lại trang Đăng ký | FR-01 |
| O2 | Thông báo lỗi | thiếu trường bắt buộc / email sai định dạng / email đã tồn tại / mật khẩu không đủ mạnh / xác nhận mật khẩu không khớp | FR-01 (nội dung câu chữ không được quy định) |
| O3 | Phản hồi API | `200` + `{"message": "User registered successfully", "id"}` khi thành công; mã lỗi kèm thông báo khi bị từ chối | `api_specification.md` 1.1; giả định A7 |
| O4 | Trạng thái dữ liệu | tài khoản mới tồn tại / không tồn tại; kiểm chứng bằng cách đăng nhập (`POST /api/login`) với email + mật khẩu vừa dùng | FR-01, FR-02 |

### 1.4 Giả định cho những chỗ đặc tả chưa rõ

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

### 1.5 Ngoài phạm vi

- Yêu cầu giao diện chung (màu nút, thẻ `<h1>`, dấu `*` cạnh nhãn, vị trí thông báo lỗi – FR-21, FR-22) và lưu trữ mật khẩu (SEC-01): không phải miền dữ liệu đầu vào của FR-01.
- Đăng ký trên Mobile: thuộc Pool D, không nằm trong feature này.

## 2. Bước 2 – Lớp tương đương (Complete Set of Partitions)

### 2.1 Cách áp dụng guideline cho từng biến

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

### 2.2 Complete Set of Partitions

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

## 3. Bước 3 – Test case Domain Testing

### 3.1 Thủ tục thực hiện

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

### 3.2 Minimum Set of Test Cases

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

### 3.3 Bảng phủ phân vùng

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

46 / 46 lớp được phủ bởi 28 test case Minimum Set (7 valid, 21 invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp invalid có đúng một test case riêng. Các đại diện bổ sung sau rà soát (mục 6.2) ghi sau dấu `;`.
<!-- END:T33 -->

## 4. Bước 4 – Boundary Value Analysis

### 4.1 Xác định biên

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

### 4.2 Boundary Value Test Cases

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

## 5. Bước 5 – Kết quả thực thi

### 5.1 Môi trường và cách chạy

| Mục | Giá trị |
| --- | --- |
| Ngày chạy | 2026-10-20 |
| Người chạy | 23120031 (script tự động, kết quả được rà soát thủ công) |
| SUT | `eshop-sut-main` (trùng với `d1nhnguyen/eshop-sut`), Node 20.19.5 |
| Web | Chrome 155 (headless, Playwright), `http://localhost:5173` |
| API | `http://localhost:3000/api`, gọi bằng Python `urllib` |
| Dữ liệu | Backend được khởi động lại trước mỗi lượt chạy (`scripts/restart_backend.sh`) |
| Script | `scripts/fr01/cases.py` (dữ liệu), `run_web.mjs` (P-WEB), `run_api.py` (P-API), `explore_web_password.mjs` (khảo sát) |
| Bằng chứng | `evidence/FR-01/web_results.json`, `api_results.json`, `web_results_workaround.json`, `explore_web_password.json`, ảnh `evidence/FR-01/web/<ID>.png` |

Cách kết luận (A7): test case "thành công" Pass khi chuyển tới trang Đăng nhập (Web) / HTTP 200 (API), tài khoản xuất hiện trong danh sách người dùng (`GET /api/admin/users`) và đăng nhập được. Test case "từ chối" Pass khi không tạo tài khoản **và** thông báo lỗi nói đúng lý do mong đợi; bị từ chối nhưng sai lý do là Fail. Test case email trùng còn kiểm tra tài khoản gốc `test@eshop.com / Test1234!` vẫn đăng nhập được.

### 5.2 Phát hiện chặn khi chạy trên Web

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

### 5.3 Kết quả theo test case

Web = lượt chính thức (P-WEB, dữ liệu đúng thiết kế). Ảnh: `evidence/FR-01/web/<ID>.png`.

| TC | Web | API | Kết quả thực tế | Bug |
| --- | --- | --- | --- | --- |
| DT-01 | Fail | Pass | Web: "Mật khẩu quá yếu!", không gửi request. API: 200, đăng nhập được | FR01-B1 |
| DT-02 | Fail | Fail | Web: "Mật khẩu quá yếu!" (`$`). API: 200 nhưng email lưu nguyên `' fr01.dt02@example.com '`, đăng nhập bằng email đã bỏ khoảng trắng thất bại | FR01-B1, FR01-B8 |
| DT-03…DT-07 | Fail | Pass | Web: "Mật khẩu quá yếu!" với `!`, `%`, `*`, `?`, `&`. API: 200, đăng nhập được | FR01-B1 |
| DT-08 | Pass | Fail | Web: trình duyệt chặn ô Họ Tên trống ("Please fill out this field."). API: 200, tạo tài khoản không có tên | FR01-B3 |
| DT-09 | Blocked | Fail | Web: bị chặn vì mật khẩu. API: 200, tạo tài khoản tên `'   '` | FR01-B9 |
| DT-10 | Pass | Fail | Web: trình duyệt chặn ô Email trống. API: 200, tạo tài khoản không có email | FR01-B3 |
| DT-11…DT-16 | Blocked | Fail | Web: bị chặn vì mật khẩu. API: 200 với cả 6 kiểu email sai định dạng | FR01-B4 |
| DT-17 | Blocked | Fail | API: 200, tạo **tài khoản thứ hai** `test@eshop.com`; đăng nhập `Test1234!` vẫn vào tài khoản cũ, `Newpass1@` không đăng nhập được | FR01-B6 |
| DT-18 | Blocked | Fail | API: 200, tạo thêm tài khoản `TEST@eshop.com` | FR01-B6 |
| DT-19 | Pass | Fail | Web: trình duyệt chặn ô Mật khẩu trống. API: 200, tạo tài khoản mật khẩu rỗng | FR01-B3 |
| DT-20…DT-25 | Pass | Fail | Web: "Mật khẩu quá yếu!" (đúng lý do). API: 200 với mật khẩu 6 ký tự, thiếu chữ hoa / chữ thường / chữ số / ký tự đặc biệt, chỉ có `#` | FR01-B5 |
| DT-26…DT-28 | Fail | – | Giao diện không có ô Xác nhận mật khẩu | FR01-B2 |
| BV-01…BV-03 | Pass | Fail | Web: "Mật khẩu quá yếu!". API: 200 với mật khẩu dài 1, 2, 7 ký tự | FR01-B5 |
| BV-04…BV-08 | Fail | Pass | Web: "Mật khẩu quá yếu!" với mật khẩu 9, 1000 ký tự, 1 chữ thường, biên `A/Z/a/z/0/9`. API: 200, đăng nhập được | FR01-B1 |
| BV-09…BV-13 | Pass | Fail | Web: "Mật khẩu quá yếu!". API: 200 với `[`, `` ` ``, `{`, `/`, `:` thay cho chữ hoa / chữ thường / chữ số | FR01-B5 |
| BV-14…BV-18 | Blocked | Pass | API: 200 và đăng nhập được với Họ Tên 1 ký tự, `␣A␣`, 1000 ký tự, email `a@b.c`, email 254 ký tự | – |
| BV-19 | Blocked | Fail | API: 200, tạo tài khoản email `' test@eshop.com'` (không bỏ khoảng trắng nên không phát hiện trùng) | FR01-B6, FR01-B8 |
| BV-20, BV-21 | Fail | – | Giao diện không có ô Xác nhận mật khẩu | FR01-B2 |

### 5.4 Quan sát từ lượt khảo sát trên Web (không tính verdict)

Với mật khẩu `Abcdef1␣` form Web gửi request; `web_results_workaround.json`, ảnh `evidence/FR-01/web/<ID>_wa.png`:

- Họ Tên `␣␣␣` (DT-09) qua được thuộc tính `required` của trình duyệt và được server chấp nhận → FR01-B9.
- Cả 6 email sai định dạng (DT-11…DT-16) được form gửi đi mà không cảnh báo (ô Email là `type="text"`) và được server chấp nhận → FR01-B7, FR01-B4.
- Email trùng `test@eshop.com`, `TEST@eshop.com`, `␣test@eshop.com` (DT-17, DT-18, BV-19) được chấp nhận → FR01-B6.
- Họ Tên / Email ở biên (BV-14…BV-18) đăng ký và đăng nhập được, khớp kết quả API.
- Bản thân việc mật khẩu `Abcdef1␣` (không có ký tự nào thuộc tập `@ $ ! % * ? &`) được chấp nhận ở cả Web và API là vi phạm A1 → FR01-B1, FR01-B5.

### 5.5 Tổng hợp

| Kênh | Thiết kế | Đã chạy | Pass | Fail | Blocked | Không áp dụng |
| --- | --- | --- | --- | --- | --- | --- |
| Web | 49 | 49 | 17 | 17 | 15 | 0 |
| API | 49 | 44 | 16 | 28 | 0 | 5 (biến Xác nhận mật khẩu, A8) |
| **Tổng lượt chạy** | | **93** | **33** | **45** | **15** | |

Theo test case (gộp 2 kênh: Fail nếu Fail ở bất kỳ kênh nào, Blocked nếu còn kênh bị Blocked): 49 test case, 0 Pass, 44 Fail, 5 Blocked (BV-14…BV-18 Pass ở API nhưng Blocked ở Web).

## 6. Bước 6 – AI gap analysis

> Bản nháp do AI (Claude Code) tự liệt kê những chỗ nó làm sai / bỏ sót trong các bước 1–5 của FR-01. Sinh viên rà soát và bổ sung các điểm tự phát hiện (commit `[FR-01][B6-review]`).

### 6.1 Những gì AI bỏ sót hoặc làm sai

| # | AI bỏ sót / làm sai | Loại | Nguyên nhân | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |
| G1 | Lớp EC28 "chỉ có ký tự đặc biệt ngoài tập" dùng `#` làm đại diện; không xét dấu cách – đúng ký tự mà form Web coi là "ký tự đặc biệt". Thiết kế ban đầu không có test case phát hiện việc Web / API chấp nhận mật khẩu không có ký tự nào thuộc tập | Test case / chọn best representative | **Giới hạn công cụ AI**: chọn đại diện "điển hình" thay vì theo rủi ro; trước khi chạy không quan sát được cách SUT xử lý từng ký tự. **Độ phức tạp feature**: các phần tử của cùng một lớp lại được SUT xử lý khác nhau – đúng trường hợp guideline G5 yêu cầu tách lớp | Khảo sát 43 mật khẩu ở bước 5 | Bổ sung DT-29 (mục 6.2) |
| G2 | Bản đầu của script Web coi "bị từ chối với bất kỳ thông báo nào" là Pass → 10 test case Email / Họ Tên / email trùng được báo Pass trong khi thật ra bị từ chối vì "Mật khẩu quá yếu!" | Kết quả mong đợi / oracle quá lỏng | **Giới hạn công cụ AI**: tự động hoá kiểm tra không bám đúng giả định A7 ("thông báo chỉ đúng lý do") mà chính nó đã đặt ra | Rà soát output lượt chạy đầu: mọi test case từ chối đều cùng một câu thông báo | Kiểm tra lý do từ chối theo trường; thêm trạng thái Blocked |
| G3 | Bản đầu của script không đánh Fail 5 test case Xác nhận mật khẩu khi ô này không tồn tại (chúng "Pass" vì bị từ chối do mật khẩu) | Oracle | Như G2 | Rà soát output | Kiểm tra sự tồn tại của ô trước khi kết luận |
| G4 | Giả định đường vòng `Abcdef1@␣` sẽ qua được form vì `Abcdef1␣` qua được – khái quát hoá từ một mẫu | Giả định sai | **Giới hạn công cụ AI**: suy luận quá đà từ dữ liệu khảo sát ít | Lượt chạy lại vẫn bị chặn | Khảo sát thêm 10 mật khẩu; chuyển lượt chạy lại thành khảo sát, không tính verdict |
| G5 | Script đọc thông báo validation của form Đăng nhập sau khi đã chuyển trang, ghi vào bằng chứng như thông báo của form Đăng ký | Bằng chứng sai lệch | **Giới hạn công cụ AI**: không lường trước việc chuyển trang làm thay đổi phần tử được chọn | Đọc output: test case thành công lại có "Please fill out this field." | Chỉ đọc thông báo khi còn ở `/register` |
| G6 | Kiểm tra "tài khoản gốc bị ảnh hưởng" dựa vào số tài khoản trùng email = 1, bị nhiễm trạng thái do test case trước tạo ra → kết luận sai cho DT-18, BV-19 | Oracle / test case không độc lập | **Độ phức tạp feature**: một lỗi (cho trùng email) làm thay đổi trạng thái dùng chung giữa các test case | Đối chiếu thủ công bằng `curl` | Chỉ dựa vào việc tài khoản gốc còn đăng nhập được |
| G7 | Email 254 ký tự bị tính thành 255 | Dữ liệu test | Lỗi tính toán của AI | `assert` trong `cases.py` | Sửa |
| G8 | Trước khi commit B3, bảng phủ tính cả test case invalid là phủ lớp valid; DT-19 ghi ô Xác nhận rỗng thay vì `= MK` | Bảng phủ / dữ liệu | AI áp dụng quy tắc Minimum Set chưa chặt | AI tự rà soát trước khi commit (không có trong lịch sử commit) | Sửa trước commit |

### 6.2 Test case bổ sung

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Mật khẩu | Kết quả mong đợi | Web | API | Bug | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DT-29 | Kiểm tra đăng ký bị từ chối khi ký tự đặc biệt duy nhất của Mật khẩu là dấu cách | EC28 (đại diện thứ hai), EC45 | `Abcdef1␣` | Từ chối, mật khẩu không đủ mạnh (A1) | Fail – đăng ký thành công | Fail – 200, tạo tài khoản | FR01-B1, FR01-B5 | AI (sau khảo sát) |

Bằng chứng: `evidence/FR-01/web_results_DT-29.json`, `api_results_DT-29.json`, ảnh `evidence/FR-01/web/DT-29.png`.

### 6.3 Điểm còn mở (chưa xử lý)

- Đặc tả không nói "chữ hoa / chữ thường" có gồm chữ có dấu (`Đ`, `Ă`, `ê`…) hay không; thiết kế hiện chỉ xét `A–Z`, `a–z`. Cần hỏi TA trước khi thêm lớp.
- Các giả định A1–A5 ảnh hưởng trực tiếp tới kết quả mong đợi (đặc biệt A3, A4 liên quan FR01-B6, FR01-B8); nên xác nhận với TA.

### 6.4 Nhận xét

- **Do prompt:** prompt "tiếp tục làm các bước" không quy định cách xử lý test case bị một lỗi khác che, nên AI tự chọn cách xử lý (Blocked + lượt khảo sát); sinh viên cần xác nhận lựa chọn này.
- **Do giới hạn công cụ AI:** phần lớn sai sót (G2–G7) nằm ở script tự động hoá và oracle, không phải ở bảng phân vùng; AI viết oracle lỏng hơn chính giả định nó đặt ra.
- **Do độ phức tạp feature:** hai lỗi chồng nhau (Web chặn mật khẩu hợp lệ, server không kiểm tra gì) khiến kết quả "Pass" trên Web dễ là Pass giả nếu không kiểm tra lý do từ chối.

## 7. Bước 7 – Bug

Chi tiết từng bug (các bước tái hiện, kết quả mong đợi / thực tế, phân tích, ảnh): `bugs/Bug_Report.md`. Cột Issue điền số `BUG-NN` sau khi tạo issue trên repo nhóm.

| Mã | Tiêu đề | Mức độ | Thành phần | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- | --- |
| FR01-B1 | Form Đăng ký trên Web báo "Mật khẩu quá yếu" với mọi mật khẩu hợp lệ có ký tự đặc biệt `@ $ ! % * ? &` | Critical | Web | DT-01…DT-07, BV-04…BV-08, DT-29 | |
| FR01-B2 | Form Đăng ký thiếu ô "Xác nhận mật khẩu" | Major | Web | DT-26…DT-28, BV-20, BV-21 | |
| FR01-B3 | API đăng ký chấp nhận Họ Tên, Email hoặc Mật khẩu rỗng | Major | Backend | DT-08, DT-10, DT-19 | |
| FR01-B4 | API đăng ký chấp nhận email sai định dạng | Major | Backend | DT-11…DT-16 | |
| FR01-B5 | API đăng ký chấp nhận mật khẩu không đủ mạnh | Major | Backend | DT-20…DT-25, BV-01…BV-03, BV-09…BV-13, DT-29 | |
| FR01-B6 | Hệ thống cho đăng ký bằng email đã tồn tại, tạo tài khoản trùng | Critical | Backend | DT-17, DT-18, BV-19 | |
| FR01-B7 | Ô Email ở form Đăng ký dùng `type="text"`, không kiểm tra định dạng email | Minor | Web | Quan sát B1; DT-11…DT-16 (khảo sát) | |
| FR01-B8 | Email đăng ký được lưu kèm khoảng trắng đầu/cuối | Minor | Backend | DT-02, BV-19 | |
| FR01-B9 | Hệ thống chấp nhận Họ Tên chỉ gồm khoảng trắng | Minor | Web, Backend | DT-09 | |

Tổng: 9 bug (2 Critical, 4 Major, 3 Minor). Ngoài phạm vi FR-01 (không báo ở đây): trang Đăng ký không có thẻ `<h1>` và nút "Đăng Ký" màu đỏ (FR-21).
