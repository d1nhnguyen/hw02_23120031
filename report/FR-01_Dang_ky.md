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

### 3.2 Minimum Set of Test Cases

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Dữ liệu | Kết quả mong đợi | Origin |
| --- | --- | --- | --- | --- | --- |

### 3.3 Bảng phủ phân vùng

| EC | Test case phủ |
| --- | --- |

## 4. Bước 4 – Boundary Value Analysis

### 4.1 Xác định biên

| Biến | Phân vùng | LB | UB | Bước nhảy | Nhỏ nhất nhập được | Lớn nhất nhập được |
| --- | --- | --- | --- | --- | --- | --- |

### 4.2 Boundary Value Test Cases

| ID | Tên test case (Action + Function + Condition) | Partition tested | Giá trị | Kết quả mong đợi | Origin |
| --- | --- | --- | --- | --- | --- |

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
