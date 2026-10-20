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

Mọi test case dùng chung thủ tục, chỉ dữ liệu thay đổi, nên được viết dạng **data matrix** [DR]: thủ tục dưới đây + mỗi dòng ở mục 3.2 là một test case.

**Tiền điều kiện chung**

- Backend `http://localhost:3000` vừa được khởi động lại (dữ liệu seed, có sẵn `test@eshop.com / Test1234!`, `admin@eshop.com / Admin123!`).
- Web `http://localhost:5173` đang chạy; Chrome, chưa đăng nhập.
- Email trong mỗi test case là duy nhất (`fr01.<id>@example.com`) để các test case độc lập nhau, trừ khi test case ghi khác.

**P-WEB – Thực hiện trên giao diện Web**

| Bước | Hành động | Kết quả mong đợi của bước |
| --- | --- | --- |
| 1 | Mở `http://localhost:5173/register` | Trang "Đăng Ký Tài Khoản" hiện các ô Họ Tên, Email, Mật khẩu, Xác nhận mật khẩu và nút "Đăng Ký" |
| 2 | Nhập Họ Tên, Email, Mật khẩu theo cột dữ liệu | Giá trị hiện đúng như nhập; ô Mật khẩu che ký tự |
| 3 | Nhập Xác nhận mật khẩu theo cột dữ liệu (`= MK` nghĩa là giống Mật khẩu) | Ô che ký tự |
| 4 | Bấm "Đăng Ký" | Như cột Kết quả mong đợi |
| 5 | Kiểm chứng tài khoản: gửi `POST /api/login` với Email (đã bỏ khoảng trắng đầu/cuối) + Mật khẩu của test case | Có token nếu mong đợi đăng ký thành công; bị từ chối nếu mong đợi đăng ký bị từ chối |

**P-API – Thực hiện trên API**

| Bước | Hành động | Kết quả mong đợi của bước |
| --- | --- | --- |
| 1 | Gửi `POST http://localhost:3000/api/register`, `Content-Type: application/json`, body `{"name": <Họ Tên>, "email": <Email>, "password": <Mật khẩu>}` | Như cột Kết quả mong đợi: `200` + `{"message": "User registered successfully", "id"}` khi hợp lệ, mã 4xx + thông báo lỗi khi không hợp lệ (A7) |
| 2 | Kiểm chứng tài khoản như bước 5 của P-WEB | như trên |

Test case thuộc biến Xác nhận mật khẩu (I4) chỉ chạy P-WEB (A8). Ký hiệu `␣` là một dấu cách.

**Hậu điều kiện (self cleaning):** khởi động lại backend sau phiên thực thi để xóa các tài khoản đã tạo.

### 3.2 Minimum Set of Test Cases

Giá trị mặc định cho các biến không phải đối tượng của test case: Họ Tên `Nguyen Van A`, Email `fr01.<id>@example.com`, Mật khẩu `Abcdef1@`, Xác nhận `= MK`.

**Test case valid** – mỗi test case phủ nhiều lớp valid nhất có thể:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Họ Tên | Email | Mật khẩu | Xác nhận | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DT-01 | Kiểm tra đăng ký thành công với dữ liệu hợp lệ điển hình | EC1, EC5, EC14, EC18, EC20, EC22, EC24, EC26, EC29, EC37, EC41 | `Nguyen Van A` | `fr01.dt01@example.com` | `Abcdef1@` | `= MK` | Đăng ký thành công, chuyển tới trang Đăng nhập; API `200` + `id`; đăng nhập được | Web, API | AI |
| DT-02 | Kiểm tra đăng ký thành công khi Họ Tên có dấu, email có khoảng trắng đầu/cuối và mật khẩu có ký tự ngoài tập | EC2, EC6, EC30, EC36, EC41 | `Nguyễn Thị Ánh` | `␣fr01.dt02@example.com␣` | `Abc#def1$` | `= MK` | Như DT-01; email được lưu là `fr01.dt02@example.com` (A4) | Web, API | AI |
| DT-03 | Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất là `!` | EC31, EC41 | mặc định | `fr01.dt03@example.com` | `Abcdef1!` | `= MK` | Như DT-01 | Web, API | AI |
| DT-04 | Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất là `%` | EC32, EC41 | mặc định | `fr01.dt04@example.com` | `Abcdef1%` | `= MK` | Như DT-01 | Web, API | AI |
| DT-05 | Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất là `*` | EC33, EC41 | mặc định | `fr01.dt05@example.com` | `Abcdef1*` | `= MK` | Như DT-01 | Web, API | AI |
| DT-06 | Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất là `?` | EC34, EC41 | mặc định | `fr01.dt06@example.com` | `Abcdef1?` | `= MK` | Như DT-01 | Web, API | AI |
| DT-07 | Kiểm tra đăng ký thành công khi ký tự đặc biệt duy nhất là `&` | EC35, EC41 | mặc định | `fr01.dt07@example.com` | `Abcdef1&` | `= MK` | Như DT-01 | Web, API | AI |

**Test case invalid** – mỗi test case phủ đúng một lớp invalid, các biến còn lại hợp lệ. Kết quả mong đợi chung khi bị từ chối (A7): không tạo tài khoản, ở lại trang Đăng ký, hiện thông báo lỗi đúng lý do; API trả 4xx kèm thông báo; bước kiểm chứng đăng nhập thất bại.

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Họ Tên | Email | Mật khẩu | Xác nhận | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DT-08 | Kiểm tra đăng ký bị từ chối khi bỏ trống Họ Tên | EC3, EC42 | `` | `fr01.dt08@example.com` | mặc định | `= MK` | Từ chối, báo thiếu Họ Tên | Web, API | AI |
| DT-09 | Kiểm tra đăng ký bị từ chối khi Họ Tên chỉ gồm khoảng trắng | EC4, EC42 | `␣␣␣` | `fr01.dt09@example.com` | mặc định | `= MK` | Từ chối, báo thiếu Họ Tên (A4) | Web, API | AI |
| DT-10 | Kiểm tra đăng ký bị từ chối khi bỏ trống Email | EC7, EC42 | mặc định | `` | mặc định | `= MK` | Từ chối, báo thiếu Email | Web, API | AI |
| DT-11 | Kiểm tra đăng ký bị từ chối khi Email thiếu ký tự `@` | EC8, EC43 | mặc định | `fr01.dt11example.com` | mặc định | `= MK` | Từ chối, báo email sai định dạng | Web, API | AI |
| DT-12 | Kiểm tra đăng ký bị từ chối khi Email thiếu phần trước `@` | EC9, EC43 | mặc định | `@example.com` | mặc định | `= MK` | Từ chối, báo email sai định dạng | Web, API | AI |
| DT-13 | Kiểm tra đăng ký bị từ chối khi Email thiếu phần domain sau `@` | EC10, EC43 | mặc định | `fr01.dt13@` | mặc định | `= MK` | Từ chối, báo email sai định dạng | Web, API | AI |
| DT-14 | Kiểm tra đăng ký bị từ chối khi domain của Email không có dấu `.` | EC11, EC43 | mặc định | `fr01.dt14@example` | mặc định | `= MK` | Từ chối, báo email sai định dạng (A2) | Web, API | AI |
| DT-15 | Kiểm tra đăng ký bị từ chối khi Email có hai ký tự `@` | EC12, EC43 | mặc định | `fr01@dt15@example.com` | mặc định | `= MK` | Từ chối, báo email sai định dạng | Web, API | AI |
| DT-16 | Kiểm tra đăng ký bị từ chối khi Email có khoảng trắng ở giữa | EC13, EC43 | mặc định | `fr01␣dt16@example.com` | mặc định | `= MK` | Từ chối, báo email sai định dạng | Web, API | AI |
| DT-17 | Kiểm tra đăng ký bị từ chối khi Email đã tồn tại | EC15, EC44 | mặc định | `test@eshop.com` | `Newpass1@` | `= MK` | Từ chối, báo email đã tồn tại; đăng nhập `test@eshop.com / Test1234!` vẫn thành công (tài khoản cũ không bị ghi đè); đăng nhập bằng `Newpass1@` thất bại | Web, API | AI |
| DT-18 | Kiểm tra đăng ký bị từ chối khi Email trùng tài khoản có sẵn nhưng khác chữ hoa / thường | EC16, EC44 | mặc định | `TEST@eshop.com` | `Newpass1@` | `= MK` | Như DT-17 (A3) | Web, API | AI |
| DT-19 | Kiểm tra đăng ký bị từ chối khi bỏ trống Mật khẩu | EC17, EC42 | mặc định | `fr01.dt19@example.com` | `` | `= MK` | Từ chối, báo thiếu Mật khẩu | Web, API | AI |
| DT-20 | Kiểm tra đăng ký bị từ chối khi Mật khẩu ngắn hơn 8 ký tự | EC19, EC45 | mặc định | `fr01.dt20@example.com` | `Abcd1@` (6) | `= MK` | Từ chối, báo mật khẩu không đủ mạnh | Web, API | AI |
| DT-21 | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ hoa | EC21, EC45 | mặc định | `fr01.dt21@example.com` | `abcdef1@` | `= MK` | Từ chối, báo mật khẩu không đủ mạnh | Web, API | AI |
| DT-22 | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ thường | EC23, EC45 | mặc định | `fr01.dt22@example.com` | `ABCDEF1@` | `= MK` | Từ chối, báo mật khẩu không đủ mạnh | Web, API | AI |
| DT-23 | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ số | EC25, EC45 | mặc định | `fr01.dt23@example.com` | `Abcdefg@` | `= MK` | Từ chối, báo mật khẩu không đủ mạnh | Web, API | AI |
| DT-24 | Kiểm tra đăng ký bị từ chối khi Mật khẩu không có ký tự đặc biệt | EC27, EC45 | mặc định | `fr01.dt24@example.com` | `Abcdefg1` | `= MK` | Từ chối, báo mật khẩu không đủ mạnh | Web, API | AI |
| DT-25 | Kiểm tra đăng ký bị từ chối khi ký tự đặc biệt của Mật khẩu nằm ngoài tập `@ $ ! % * ? &` | EC28, EC45 | mặc định | `fr01.dt25@example.com` | `Abcdef1#` | `= MK` | Từ chối, báo mật khẩu không đủ mạnh (A1) | Web, API | AI |
| DT-26 | Kiểm tra đăng ký bị từ chối khi bỏ trống Xác nhận mật khẩu | EC38, EC42 | mặc định | `fr01.dt26@example.com` | mặc định | `` | Từ chối, báo thiếu Xác nhận mật khẩu hoặc không khớp | Web | AI |
| DT-27 | Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu khác Mật khẩu | EC39, EC46 | mặc định | `fr01.dt27@example.com` | `Abcdef1@` | `Abcdef2@` | Từ chối, báo xác nhận mật khẩu không khớp | Web | AI |
| DT-28 | Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu chỉ khác Mật khẩu ở chữ hoa / thường | EC40, EC46 | mặc định | `fr01.dt28@example.com` | `Abcdef1@` | `abcdef1@` | Từ chối, báo xác nhận mật khẩu không khớp | Web | AI |

### 3.3 Bảng phủ phân vùng

| EC | Test case phủ | | EC | Test case phủ |
| --- | --- | --- | --- | --- |
| EC1 | DT-01, DT-03…DT-07 | | EC24 | DT-01…DT-07 |
| EC2 | DT-02 | | EC25 | DT-23 |
| EC3 | DT-08 | | EC26 | DT-01…DT-07 |
| EC4 | DT-09 | | EC27 | DT-24 |
| EC5 | DT-01, DT-03…DT-07 | | EC28 | DT-25 |
| EC6 | DT-02 | | EC29 | DT-01 |
| EC7 | DT-10 | | EC30 | DT-02 |
| EC8 | DT-11 | | EC31 | DT-03 |
| EC9 | DT-12 | | EC32 | DT-04 |
| EC10 | DT-13 | | EC33 | DT-05 |
| EC11 | DT-14 | | EC34 | DT-06 |
| EC12 | DT-15 | | EC35 | DT-07 |
| EC13 | DT-16 | | EC36 | DT-02 |
| EC14 | DT-01…DT-07 | | EC37 | DT-01…DT-07 |
| EC15 | DT-17 | | EC38 | DT-26 |
| EC16 | DT-18 | | EC39 | DT-27 |
| EC17 | DT-19 | | EC40 | DT-28 |
| EC18 | DT-01…DT-07 | | EC41 | DT-01…DT-07 |
| EC19 | DT-20 | | EC42 | DT-08, DT-09, DT-10, DT-19, DT-26 |
| EC20 | DT-01…DT-07 | | EC43 | DT-11…DT-16 |
| EC21 | DT-21 | | EC44 | DT-17, DT-18 |
| EC22 | DT-01…DT-07 | | EC45 | DT-20…DT-25 |
| EC23 | DT-22 | | EC46 | DT-27, DT-28 |

46 / 46 lớp được phủ bởi 28 test case (7 valid, 21 invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp invalid có đúng một test case riêng.

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
| I2 khoảng trắng đầu email × trùng email | EC6 / EC15 | – | – | – | 1 khoảng trắng + email đã tồn tại |
| I4 so với I3 | EC37 (khớp) / EC39 (khác) | độ dài = độ dài MK | | 1 ký tự | MK thiếu 1 ký tự cuối, MK thừa 1 ký tự |

### 4.2 Boundary Value Test Cases

Thủ tục: P-WEB / P-API ở mục 3.1. Giá trị mặc định như mục 3.2; email mỗi test case là `fr01.<id>@example.com` trừ khi ghi khác.

| ID | Tên test case (Action + Function + Condition) | Partition tested | Giá trị | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- |
| (DT-19) | Mật khẩu độ dài 0 | EC17 | `` | Từ chối | | |
| BV-01 | Kiểm tra đăng ký bị từ chối khi Mật khẩu dài 1 ký tự | EC17/EC19 (LB) | `@` | Từ chối, mật khẩu không đủ mạnh | Web, API | AI |
| BV-02 | Kiểm tra đăng ký bị từ chối khi Mật khẩu dài 2 ký tự | EC19 (LB+1) | `A1` | Từ chối, mật khẩu không đủ mạnh | Web, API | AI |
| (DT-20) | Mật khẩu dài 6 ký tự | EC19 (UB-1) | `Abcd1@` | Từ chối | | |
| BV-03 | Kiểm tra đăng ký bị từ chối khi Mật khẩu dài 7 ký tự và đủ 4 loại ký tự | EC19/EC18 (UB của EC19) | `Abcde1@` | Từ chối, mật khẩu không đủ mạnh | Web, API | AI |
| (DT-01) | Mật khẩu dài 8 ký tự | EC19/EC18 (LB của EC18) | `Abcdef1@` | Thành công | | |
| BV-04 | Kiểm tra đăng ký thành công khi Mật khẩu dài 9 ký tự | EC18 (LB+1) | `Abcdefg1@` | Thành công, đăng nhập được | Web, API | AI |
| BV-05 | Kiểm tra đăng ký thành công khi Mật khẩu dài 1000 ký tự | EC18 (lớn nhất nhập được) | `Abcdef1@` + 992 × `a` | Thành công, đăng nhập được bằng đúng mật khẩu 1000 ký tự (A5) | Web, API | AI |
| (DT-21…DT-24) | Mỗi loại ký tự có 0 ký tự | EC21, EC23, EC25, EC27 | | Từ chối | | |
| (DT-01) | Có đúng 1 chữ hoa, 1 chữ số, 1 ký tự đặc biệt | EC20, EC24, EC26 (LB) | `Abcdef1@` | Thành công | | |
| BV-06 | Kiểm tra đăng ký thành công khi Mật khẩu có đúng 1 chữ thường | EC22 (LB) | `ABCDEa1@` | Thành công, đăng nhập được | Web, API | AI |
| BV-07 | Kiểm tra đăng ký thành công khi chữ hoa duy nhất là `Z`, chữ thường duy nhất là `a`, chữ số duy nhất là `9` | `Z` (UB chữ hoa), `a` (LB chữ thường), `9` (UB chữ số) | `Zaaaaa9@` | Thành công, đăng nhập được | Web, API | AI |
| BV-08 | Kiểm tra đăng ký thành công khi chữ hoa duy nhất là `A`, chữ thường duy nhất là `z`, chữ số duy nhất là `0` | `A` (LB chữ hoa), `z` (UB chữ thường), `0` (LB chữ số) | `Azzzzz0@` | Thành công, đăng nhập được | Web, API | AI |
| (DT-21) | Ký tự liền trước `A` là `@` – mật khẩu không có chữ hoa nhưng có `@` | `@`/`A` | `abcdef1@` | Từ chối | | |
| BV-09 | Kiểm tra đăng ký bị từ chối khi ký tự liền sau `Z` (`[`) thay cho chữ hoa | `Z`/`[` (UB+1 chữ hoa) | `[bcdef1@` | Từ chối, mật khẩu không đủ mạnh (không có chữ hoa) | Web, API | AI |
| BV-10 | Kiểm tra đăng ký bị từ chối khi ký tự liền trước `a` (`` ` ``) thay cho chữ thường | `` ` ``/`a` (LB-1 chữ thường) | ``A`````1@`` | Từ chối, mật khẩu không đủ mạnh (không có chữ thường) | Web, API | AI |
| BV-11 | Kiểm tra đăng ký bị từ chối khi ký tự liền sau `z` (`{`) thay cho chữ thường | `z`/`{` (UB+1 chữ thường) | `A{{{{{1@` | Từ chối, mật khẩu không đủ mạnh (không có chữ thường) | Web, API | AI |
| BV-12 | Kiểm tra đăng ký bị từ chối khi ký tự liền trước `0` (`/`) thay cho chữ số | `/`/`0` (LB-1 chữ số) | `Abcdef/@` | Từ chối, mật khẩu không đủ mạnh (không có chữ số) | Web, API | AI |
| BV-13 | Kiểm tra đăng ký bị từ chối khi ký tự liền sau `9` (`:`) thay cho chữ số | `9`/`:` (UB+1 chữ số) | `Abcdef:@` | Từ chối, mật khẩu không đủ mạnh (không có chữ số) | Web, API | AI |
| (DT-08) | Họ Tên độ dài 0 | EC3 | `` | Từ chối | | |
| BV-14 | Kiểm tra đăng ký thành công khi Họ Tên dài 1 ký tự | EC3/EC1 (LB) | `A` | Thành công | Web, API | AI |
| BV-15 | Kiểm tra đăng ký thành công khi Họ Tên có 1 ký tự giữa các khoảng trắng | EC4/EC1 | `␣A␣` | Thành công (A4) | Web, API | AI |
| BV-16 | Kiểm tra đăng ký thành công khi Họ Tên dài 1000 ký tự | EC1 (lớn nhất nhập được) | 1000 × `A` | Thành công (A5) | Web, API | AI |
| BV-17 | Kiểm tra đăng ký thành công với Email ngắn nhất hợp lệ | EC5 (LB) | `a@b.c` | Thành công, đăng nhập được | Web, API | AI |
| BV-18 | Kiểm tra đăng ký thành công với Email dài 254 ký tự | EC5 (UB) | phần local 64 ký tự + `@` + domain 189 ký tự (các nhãn ≤ 63 ký tự, kết thúc `.com`) | Thành công, đăng nhập được | Web, API | AI |
| BV-19 | Kiểm tra đăng ký bị từ chối khi Email đã tồn tại có thêm khoảng trắng ở đầu | EC6/EC15 | `␣test@eshop.com`, Mật khẩu `Newpass1@` | Từ chối, email đã tồn tại; `test@eshop.com / Test1234!` vẫn đăng nhập được (A4) | Web, API | AI |
| BV-20 | Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu thiếu ký tự cuối | EC37/EC39 (độ dài - 1) | MK `Abcdef1@`, Xác nhận `Abcdef1` | Từ chối, xác nhận mật khẩu không khớp | Web | AI |
| BV-21 | Kiểm tra đăng ký bị từ chối khi Xác nhận mật khẩu thừa 1 ký tự | EC37/EC39 (độ dài + 1) | MK `Abcdef1@`, Xác nhận `Abcdef1@1` | Từ chối, xác nhận mật khẩu không khớp | Web | AI |

Tổng: 21 test case BVA mới (BV-01…BV-21); 7 điểm biên khác đã được phủ bởi test case Domain Testing (dòng có ID trong ngoặc).

## 5. Bước 5 – Kết quả thực thi

| TC | Kênh | Kết quả thực tế | Status | Bug ID |
| --- | --- | --- | --- | --- |

| Thiết kế | Đã chạy | Pass | Fail | Blocked / chưa chạy | Số bug |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 6. Bước 6 – AI gap analysis

| # | AI bỏ sót / làm sai | Loại (EC / TC / biên / expected sai / bug) | Nguyên nhân (prompt / giới hạn công cụ AI / độ phức tạp feature) | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |

## 7. Bước 7 – Bug

| Bug ID | Tiêu đề | Mức độ | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- |
