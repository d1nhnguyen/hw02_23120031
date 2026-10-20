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

| EC | Biến | Guideline | Phân vùng | Valid / Invalid |
| --- | --- | --- | --- | --- |

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
