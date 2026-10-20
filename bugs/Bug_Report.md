# Báo cáo bug · HW02 · 23120031

Bug được báo trên GitHub Issues của repo nhóm `d1nhnguyen/eshop-sut`, tiêu đề dạng `[BUG-NN] [FR-xx] <tóm tắt>`. Mỗi bug dưới đây có mã tạm (vd `FR01-B1`) dùng trong báo cáo feature; cột **Issue** ghi số `BUG-NN` sau khi tạo issue. Nội dung theo mẫu Problem Report [Kaner, TCS ch.5]: tái hiện được, ít bước nhất, không phán xét, nêu hậu quả nghiêm trọng nhất và các đường khác dẫn tới cùng lỗi.

**Môi trường chung:** EShop SUT (`d1nhnguyen/eshop-sut`, commit `85af3ba`), backend Node 20.19.5 khởi động lại trước khi tái hiện (dữ liệu seed), Web `http://localhost:5173`, Chrome 155, Ubuntu 24.04. Người báo: 23120031. Ngày: 2026-10-20.

**Mức độ:** Critical (chặn chức năng chính / hỏng dữ liệu) · Major (vi phạm yêu cầu, có cách khác dùng được) · Minor (ảnh hưởng nhỏ hoặc phụ thuộc giả định) · Trivial.

## Tổng hợp

| Mã | Issue | Feature | Tiêu đề issue đề xuất | Mức độ | Thành phần | TC phát hiện |
| --- | --- | --- | --- | --- | --- | --- |
| FR01-B1 | | FR-01 | Form Đăng ký trên Web báo "Mật khẩu quá yếu" với mọi mật khẩu hợp lệ có ký tự đặc biệt `@ $ ! % * ? &` | Critical | Web | FR01-DT-01…FR01-DT-07, FR01-BV-04…FR01-BV-08, FR01-DT-29, FR01-DT-32 |
| FR01-B2 | | FR-01 | Form Đăng ký thiếu ô "Xác nhận mật khẩu" | Major | Web | FR01-DT-26…FR01-DT-28, FR01-BV-20, FR01-BV-21 |
| FR01-B3 | | FR-01 | API đăng ký chấp nhận Họ Tên, Email hoặc Mật khẩu rỗng | Major | Backend | FR01-DT-08, FR01-DT-10, FR01-DT-19 |
| FR01-B4 | | FR-01 | API đăng ký chấp nhận email sai định dạng | Major | Backend | FR01-DT-11…FR01-DT-16 |
| FR01-B5 | | FR-01 | API đăng ký chấp nhận mật khẩu không đủ mạnh | Major | Backend | FR01-DT-20…FR01-DT-25, FR01-BV-01…FR01-BV-03, FR01-BV-09…FR01-BV-13, FR01-DT-29…FR01-DT-31 |
| FR01-B6 | | FR-01 | Hệ thống cho đăng ký bằng email đã tồn tại, tạo tài khoản trùng | Critical | Backend | FR01-DT-17, FR01-DT-18, FR01-BV-19 |
| FR01-B7 | | FR-01 | Ô Email ở form Đăng ký dùng `type="text"`, không kiểm tra định dạng email | Minor | Web | Quan sát B1; FR01-DT-11…FR01-DT-16 (lượt khảo sát Web) |
| FR01-B8 | | FR-01 | Email đăng ký được lưu kèm khoảng trắng đầu/cuối, không đăng nhập được bằng email bình thường | Minor | Backend | FR01-DT-02, FR01-BV-19 |
| FR01-B9 | | FR-01 | Hệ thống chấp nhận Họ Tên chỉ gồm khoảng trắng | Minor | Web, Backend | FR01-DT-09 |
| FR15-B1 | | FR-15 | Quản lý sản phẩm cho lưu Giá bằng 0 hoặc âm khi Thêm và Sửa | Major | Backend, Web Admin | FR15-DT-08, FR15-DT-09, FR15-DT-20, FR15-DT-21, FR15-BV-11, FR15-BV-12, FR15-BV-17 |
| FR15-B2 | | FR-15 | Quản lý sản phẩm cho lưu khi thiếu Giá hoặc Giá không phải số | Major | Backend, Web Admin | FR15-DT-10, FR15-DT-11, FR15-DT-22, FR15-DT-23 |
| FR15-B3 | | FR-15 | Quản lý sản phẩm cho lưu Tên dài hơn 255 ký tự | Major | Backend, Web Admin | FR15-DT-07, FR15-DT-19, FR15-BV-05, FR15-BV-07, FR15-BV-10 |
| FR15-B4 | | FR-15 | Quản lý sản phẩm cho lưu Tên rỗng (API) hoặc chỉ gồm khoảng trắng | Major | Backend, Web Admin | FR15-DT-05, FR15-DT-06, FR15-DT-17, FR15-DT-18 |
| FR15-B5 | | FR-15 | Quản lý sản phẩm cho lưu Danh mục thiếu hoặc không có trong danh sách | Major | Backend | FR15-DT-12…FR15-DT-14, FR15-DT-24…FR15-DT-26, FR15-BV-18, FR15-BV-20 |
| FR15-B6 | | FR-15 | Sửa / Xóa sản phẩm không tồn tại trả 200 "Product updated / deleted" thay vì 404 | Minor | Backend | FR15-DT-27…FR15-DT-29, FR15-DT-31…FR15-DT-33, FR15-BV-21, FR15-BV-24, FR15-BV-25, FR15-BV-27 |
| FR10-B1 | | FR-10 | Đơn đã hủy chuyển được sang "Đã giao"; Web Admin hiện nút "Đánh dấu Đã giao" cho đơn đã hủy | Critical | Backend, Web Admin | FR10-DT-09, FR10-DT-26 |
| FR10-B2 | | FR-10 | User hủy được đơn đang giao; trang Hồ sơ hiện nút "Hủy đơn" cho đơn đang giao | Major | Backend, Web | FR10-DT-14, FR10-DT-27 |

## Chi tiết

### FR01-B1 – Form Đăng ký trên Web báo "Mật khẩu quá yếu" với mọi mật khẩu hợp lệ có ký tự đặc biệt `@ $ ! % * ? &`

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-01 Đăng ký tài khoản (yêu cầu mật khẩu mạnh) |
| Thành phần | Web – trang `/register` |
| Loại | Lỗi lập trình (kiểm tra phía client sai) |
| Mức độ / Ưu tiên | Critical / Cao |
| Tái hiện được | Luôn luôn (7/7 ký tự trong tập; 13/13 test case Web có mật khẩu hợp lệ) |
| TC phát hiện | FR01-DT-01…FR01-DT-07, FR01-BV-04…FR01-BV-08, FR01-DT-29, FR01-DT-32 (kênh Web) |

**Các bước tái hiện**

1. Mở `http://localhost:5173/register`.
2. Nhập Họ Tên `Nguyen Van A`, Email `fr01.b1@example.com`, Mật khẩu `Abcdef1@`.
3. Bấm "Đăng Ký".

**Kết quả mong đợi** (FR-01): mật khẩu có 8 ký tự, có chữ hoa, chữ thường, chữ số và `@` → đăng ký thành công, chuyển tới trang Đăng nhập.

**Kết quả thực tế:** form hiện "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT.", không gửi request. Kết quả giống hệt với `Mậtkhẩu1@` (có thêm chữ có dấu), `Abcdef1$`, `Abcdef1!`, `Abcdef1%`, `Abcdef1*`, `Abcdef1?`, `Abcdef1&` và 25 ký tự đặc biệt khác. Ngược lại, `Abcdef1␣` (ký tự đặc biệt duy nhất là dấu cách, không thuộc tập của đặc tả) lại được chấp nhận và đăng ký thành công.

**Phân tích:** form chỉ coi dấu cách là ký tự đặc biệt. Hậu quả: không người dùng nào đăng ký được trên Web bằng mật khẩu đúng đặc tả, đồng thời mật khẩu không có ký tự đặc biệt hợp lệ lại lọt qua. Đường khác: gọi trực tiếp `POST /api/register` vẫn đăng ký được (xem FR01-B5). Liên quan: FR01-B5.

**Bằng chứng:** `bugs/screenshots/FR01-B1.png`; `evidence/FR-01/explore_web_password.json` (43 mật khẩu khảo sát); ảnh từng test case `evidence/FR-01/web/FR01-DT-01.png`…

![FR01-B1](screenshots/FR01-B1.png)

### FR01-B2 – Form Đăng ký thiếu ô "Xác nhận mật khẩu"

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-01 ("Phải có trường Xác nhận mật khẩu") |
| Thành phần | Web – trang `/register` |
| Loại | Lỗi lập trình (thiếu chức năng) |
| Mức độ / Ưu tiên | Major / Cao |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR01-DT-26, FR01-DT-27, FR01-DT-28, FR01-BV-20, FR01-BV-21 |

**Các bước tái hiện**

1. Mở `http://localhost:5173/register`.

**Kết quả mong đợi** (FR-01): form có ô "Xác nhận mật khẩu"; hệ thống từ chối nếu hai ô mật khẩu không khớp.

**Kết quả thực tế:** form chỉ có Họ Tên, Email, Mật khẩu.

**Phân tích:** người dùng gõ nhầm mật khẩu (ô bị che) sẽ không được phát hiện và không đăng nhập được bằng mật khẩu mình định đặt.

**Bằng chứng:** `bugs/screenshots/FR01-B2.png`

![FR01-B2](screenshots/FR01-B2.png)

### FR01-B3 – API đăng ký chấp nhận Họ Tên, Email hoặc Mật khẩu rỗng

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-01 ("Người dùng phải cung cấp Họ Tên, Email, Mật khẩu") |
| Thành phần | Backend – `POST /api/register` |
| Loại | Lỗi lập trình (thiếu kiểm tra phía server) |
| Mức độ / Ưu tiên | Major / Cao |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR01-DT-08, FR01-DT-10, FR01-DT-19 (kênh API) |

**Các bước tái hiện**

1. Gửi `POST http://localhost:3000/api/register` với body `{"name": "", "email": "fr01.dt08@example.com", "password": "Abcdef1@"}`.
2. Lặp lại với `"email": ""` và với `"password": ""` (các trường còn lại hợp lệ).

**Kết quả mong đợi:** mã lỗi 4xx kèm thông báo thiếu trường; không tạo tài khoản.

**Kết quả thực tế:** cả 3 request trả `200 {"message": "User registered successfully"}`; tài khoản được tạo (trang Quản lý Người dùng của Web Admin có tài khoản ID 5 không có email).

**Phân tích:** form Web chặn ô trống bằng thuộc tính `required` của trình duyệt, nhưng mọi client gọi API trực tiếp (Postman, app mobile…) đều tạo được tài khoản thiếu thông tin. Liên quan: FR01-B4, FR01-B5, FR01-B9.

**Bằng chứng:** `bugs/screenshots/FR01-B3.png`, `bugs/screenshots/FR01-admin-users.png`

![FR01-B3](screenshots/FR01-B3.png)

### FR01-B4 – API đăng ký chấp nhận email sai định dạng

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-01 ("Email phải có định dạng hợp lệ `user@domain.com`") |
| Thành phần | Backend – `POST /api/register` |
| Loại | Lỗi lập trình (thiếu kiểm tra phía server) |
| Mức độ / Ưu tiên | Major / Cao |
| Tái hiện được | Luôn luôn (6/6 kiểu sai định dạng) |
| TC phát hiện | FR01-DT-11…FR01-DT-16 (kênh API) |

**Các bước tái hiện**

1. Gửi `POST /api/register` với `{"name": "Nguyen Van A", "email": "fr01.dt11example.com", "password": "Abcdef1@"}`.
2. Lặp lại với email `@example.com`, `fr01.dt13@`, `fr01.dt14@example`, `fr01@dt15@example.com`, `fr01 dt16@example.com`.

**Kết quả mong đợi:** từ chối với thông báo email sai định dạng.

**Kết quả thực tế:** cả 6 request trả 200 và tạo tài khoản với email sai định dạng (hiển thị trong Quản lý Người dùng).

**Phân tích:** form Web cũng không kiểm tra định dạng (FR01-B7), nên lỗi xảy ra cả qua giao diện. Tài khoản có email không dùng được cho chức năng Quên mật khẩu (FR-03).

**Bằng chứng:** `bugs/screenshots/FR01-B4.png`, `bugs/screenshots/FR01-admin-users.png`

![FR01-B4](screenshots/FR01-B4.png)

### FR01-B5 – API đăng ký chấp nhận mật khẩu không đủ mạnh

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-01 (mật khẩu ≥ 8 ký tự, có chữ hoa, chữ thường, chữ số, ký tự đặc biệt `@ $ ! % * ? &`) |
| Thành phần | Backend – `POST /api/register` |
| Loại | Lỗi lập trình (thiếu kiểm tra phía server) |
| Mức độ / Ưu tiên | Major / Cao |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR01-DT-20…FR01-DT-25, FR01-BV-01…FR01-BV-03, FR01-BV-09…FR01-BV-13, FR01-DT-29…FR01-DT-31 (kênh API) |

**Các bước tái hiện**

1. Gửi `POST /api/register` với `{"name": "Nguyen Van A", "email": "fr01.b5.0@example.com", "password": "@"}`.
2. Lặp lại với mật khẩu `Abcde1@` (7 ký tự), `abcdef1@` (không chữ hoa), `ABCDEF1@` (không chữ thường), `Abcdefg@` (không chữ số), `Abcdefg1` (không ký tự đặc biệt), `Abcdef1#`, `Abcdef1␣` (ký tự đặc biệt ngoài tập), `Đbcdef1@`, `ABCDEă1@` (chữ hoa / chữ thường duy nhất là chữ có dấu – A10).

**Kết quả mong đợi:** từ chối với thông báo mật khẩu không đủ mạnh.

**Kết quả thực tế:** mọi request trả 200 và tạo tài khoản; đăng nhập được bằng mật khẩu 1 ký tự.

**Phân tích:** chính sách mật khẩu chỉ tồn tại ở form Web (và form đó cũng sai – FR01-B1); gọi API trực tiếp bỏ qua hoàn toàn. Hậu quả bảo mật: tài khoản có mật khẩu dễ đoán.

**Bằng chứng:** `bugs/screenshots/FR01-B5.png`

![FR01-B5](screenshots/FR01-B5.png)

### FR01-B6 – Hệ thống cho đăng ký bằng email đã tồn tại, tạo tài khoản trùng

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-01 ("Email … là duy nhất trong hệ thống") |
| Thành phần | Backend – `POST /api/register` (xảy ra cả khi đăng ký qua Web) |
| Loại | Lỗi lập trình (thiếu kiểm tra trùng / ràng buộc duy nhất) |
| Mức độ / Ưu tiên | Critical / Cao |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR01-DT-17, FR01-DT-18, FR01-BV-19 (kênh API; lượt khảo sát Web cho kết quả giống) |

**Các bước tái hiện**

1. Gửi `POST /api/register` với `{"name": "Nguyen Van B", "email": "test@eshop.com", "password": "Newpass1@"}` (`test@eshop.com` là tài khoản có sẵn).
2. Đăng nhập `test@eshop.com / Test1234!`, rồi `test@eshop.com / Newpass1@`.

**Kết quả mong đợi:** bước 1 bị từ chối với thông báo email đã tồn tại.

**Kết quả thực tế:** bước 1 trả 200 và tạo **tài khoản thứ hai** cùng email `test@eshop.com` (Quản lý Người dùng hiện ID 2 và ID 22 cùng email). Đăng nhập bằng `Test1234!` vẫn vào tài khoản cũ, còn `Newpass1@` báo "Invalid email or password" – tài khoản mới tạo không dùng được. Email `TEST@eshop.com` và `␣test@eshop.com` cũng được chấp nhận.

**Phân tích:** vi phạm tính duy nhất của email – dữ liệu người dùng bị trùng, người đăng ký sau được báo thành công nhưng không bao giờ đăng nhập được; các chức năng tra cứu theo email (đăng nhập, quên mật khẩu) trở nên mơ hồ. Liên quan: FR01-B8.

**Bằng chứng:** `bugs/screenshots/FR01-B6.png`, `bugs/screenshots/FR01-admin-users.png`

![FR01-B6](screenshots/FR01-B6.png)

### FR01-B7 – Ô Email ở form Đăng ký dùng `type="text"`, không kiểm tra định dạng email

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-01 (định dạng email), FR-22 ("Trường Email phải dùng `type="email"`") |
| Thành phần | Web – trang `/register` |
| Loại | Lỗi lập trình |
| Mức độ / Ưu tiên | Minor / Trung bình |
| Tái hiện được | Luôn luôn |
| TC phát hiện | Quan sát giao diện ở bước 1; FR01-DT-11…FR01-DT-16 (lượt khảo sát Web) |

**Các bước tái hiện**

1. Mở `http://localhost:5173/register`, kiểm tra thuộc tính của ô Email (DevTools): `type="text"`.
2. Nhập Họ Tên `Nguyen Van A`, Email `fr01.b7example.com`, Mật khẩu `Abcdef1␣` (mật khẩu duy nhất form cho qua – FR01-B1), bấm "Đăng Ký".

**Kết quả mong đợi:** ô Email là `type="email"`, trình duyệt / form báo email sai định dạng và không gửi đi.

**Kết quả thực tế:** form gửi request ngay, server trả 200, chuyển tới trang Đăng nhập.

**Bằng chứng:** `bugs/screenshots/FR01-B7.png`

![FR01-B7](screenshots/FR01-B7.png)

### FR01-B8 – Email đăng ký được lưu kèm khoảng trắng đầu/cuối

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-01 (định dạng email); giả định A4 (bỏ khoảng trắng đầu/cuối như `type="email"` của HTML5) |
| Thành phần | Backend – `POST /api/register` |
| Loại | Lỗi lập trình |
| Mức độ / Ưu tiên | Minor / Thấp |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR01-DT-02, FR01-BV-19 (kênh API) |

**Các bước tái hiện**

1. Gửi `POST /api/register` với `{"name": "Nguyen Van A", "email": "␣fr01.b8@example.com␣", "password": "Abcdef1@"}`.
2. Đăng nhập với `fr01.b8@example.com / Abcdef1@`.

**Kết quả mong đợi:** email được lưu là `fr01.b8@example.com`; bước 2 đăng nhập thành công.

**Kết quả thực tế:** bước 1 trả 200 nhưng email được lưu nguyên kèm khoảng trắng; bước 2 báo "Invalid email or password". Với `␣test@eshop.com`, hệ thống còn không phát hiện email đã tồn tại (FR01-B6).

**Bằng chứng:** `bugs/screenshots/FR01-B8.png`

![FR01-B8](screenshots/FR01-B8.png)

### FR01-B9 – Hệ thống chấp nhận Họ Tên chỉ gồm khoảng trắng

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-01 ("phải cung cấp Họ Tên"); giả định A4 |
| Thành phần | Web (`required` chỉ chặn ô trống) và Backend |
| Loại | Lỗi lập trình |
| Mức độ / Ưu tiên | Minor / Thấp |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR01-DT-09 (kênh API; lượt khảo sát Web cho kết quả giống) |

**Các bước tái hiện**

1. Gửi `POST /api/register` với `{"name": "␣␣␣", "email": "fr01.dt09@example.com", "password": "Abcdef1@"}`.

**Kết quả mong đợi:** từ chối, báo thiếu Họ Tên.

**Kết quả thực tế:** 200, tạo tài khoản có tên chỉ gồm khoảng trắng. Trên Web, ô Họ Tên `␣␣␣` cũng qua được thuộc tính `required`.

**Bằng chứng:** `bugs/screenshots/FR01-B9.png`

![FR01-B9](screenshots/FR01-B9.png)

### FR-15 – Quản lý sản phẩm

Môi trường: như FR-01; Web Admin `http://localhost:5174` đăng nhập `admin@eshop.com`; API gửi kèm token admin. Dữ liệu seed: 5 sản phẩm id 1–5, danh mục id 1–3.

### FR15-B1 – Quản lý sản phẩm cho lưu Giá bằng 0 hoặc âm khi Thêm và Sửa

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-15 ("Giá: bắt buộc, phải là số dương (> 0)") |
| Thành phần | Backend `POST` / `PUT /api/products`; Web Admin tab Sản phẩm (ô Giá không đặt `min`) |
| Loại | Lỗi lập trình (thiếu kiểm tra) |
| Mức độ / Ưu tiên | Major / Cao |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR15-DT-08, FR15-DT-09, FR15-DT-20, FR15-DT-21, FR15-BV-11, FR15-BV-12, FR15-BV-17 (Web và API) |

**Các bước tái hiện**

1. Web Admin → tab "Sản phẩm" → nhập Tên `Gia am tu Web Admin`, Giá `-50000`, Danh mục `Điện thoại` → bấm "Lưu sản phẩm".
2. Hoặc gửi `POST /api/products` với `{"name": "Sac nhanh USB-C 20W", "price": 0, "category_id": 3}`; `PUT /api/products/2` với Giá `-1`.

**Kết quả mong đợi:** từ chối, báo Giá phải lớn hơn 0; không tạo / không sửa sản phẩm.

**Kết quả thực tế:** sản phẩm được tạo / sửa với Giá `-50000`, `0`, `-1`, `-0.01`; danh sách Admin hiện `-50000 ₫`. Khi Sửa, Web còn hiện "Cập nhật thành công!".

**Phân tích:** sản phẩm giá âm / bằng 0 xuất hiện trong cửa hàng, ảnh hưởng tổng tiền giỏ hàng và doanh thu (FR-07, FR-08, FR-13). Liên quan: FR15-B2.

**Bằng chứng:** `bugs/screenshots/FR15-B1.png`, `bugs/screenshots/FR15-admin-products.png`

![FR15-B1](screenshots/FR15-B1.png)

### FR15-B2 – Quản lý sản phẩm cho lưu khi thiếu Giá hoặc Giá không phải số

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-15 ("Giá: bắt buộc, phải là số") |
| Thành phần | Backend `POST` / `PUT /api/products`; Web Admin (ô Giá không `required`) |
| Loại | Lỗi lập trình (thiếu kiểm tra) |
| Mức độ / Ưu tiên | Major / Cao |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR15-DT-10, FR15-DT-22 (Web và API), FR15-DT-11, FR15-DT-23 (API) |

**Các bước tái hiện**

1. Web Admin → tab "Sản phẩm" → nhập Tên `Sac nhanh USB-C 20W`, để trống Giá → bấm "Lưu sản phẩm".
2. Hoặc gửi `POST /api/products` không có trường `price`, hoặc với `"price": "abc"`; `PUT /api/products/3` với `"price": "abc"`.

**Kết quả mong đợi:** từ chối, báo thiếu Giá / Giá không hợp lệ.

**Kết quả thực tế:** sản phẩm được tạo / sửa với Giá rỗng, `null` hoặc `"abc"`.

**Bằng chứng:** `bugs/screenshots/FR15-B2.png`

![FR15-B2](screenshots/FR15-B2.png)

### FR15-B3 – Quản lý sản phẩm cho lưu Tên dài hơn 255 ký tự

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-15 ("Tên sản phẩm: bắt buộc, tối đa 255 ký tự") |
| Thành phần | Backend `POST` / `PUT /api/products`; Web Admin (ô Tên không đặt `maxlength`) |
| Loại | Lỗi lập trình (thiếu kiểm tra) |
| Mức độ / Ưu tiên | Major / Trung bình |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR15-DT-07, FR15-DT-19, FR15-BV-05, FR15-BV-07, FR15-BV-10 (Web và API) |

**Các bước tái hiện**

1. Gửi `POST /api/products` với Tên `"A" * 256` (256 ký tự), Giá `350000`, Danh mục `3`.
2. Lặp lại với Tên `"Ố" * 256`; `PUT /api/products/4` với Tên `"B" * 300`. Trên Web Admin dán chuỗi 256 ký tự vào ô Tên cũng lưu được.

**Kết quả mong đợi:** từ chối, báo Tên vượt quá 255 ký tự.

**Kết quả thực tế:** lưu thành công Tên 256 và 300 ký tự. Biên 255 ký tự (kể cả chữ có dấu) được chấp nhận đúng.

**Bằng chứng:** `bugs/screenshots/FR15-B3.png`

![FR15-B3](screenshots/FR15-B3.png)

### FR15-B4 – Quản lý sản phẩm cho lưu Tên rỗng (API) hoặc chỉ gồm khoảng trắng

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-15 ("Tên sản phẩm: bắt buộc"); giả định A2 (Tên chỉ có khoảng trắng coi như bỏ trống) |
| Thành phần | Backend `POST` / `PUT /api/products`; Web Admin (thuộc tính `required` chỉ chặn ô trống) |
| Loại | Lỗi lập trình (thiếu kiểm tra phía server) |
| Mức độ / Ưu tiên | Major / Cao |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR15-DT-05, FR15-DT-17 (API), FR15-DT-06, FR15-DT-18 (Web và API) |

**Các bước tái hiện**

1. Web Admin → tab "Sản phẩm" → nhập Tên `␣␣␣` (3 dấu cách), Giá `350000` → bấm "Lưu sản phẩm".
2. Hoặc gửi `POST /api/products` với `"name": ""`; `PUT /api/products/5` với `"name": ""`.

**Kết quả mong đợi:** từ chối, báo thiếu Tên sản phẩm.

**Kết quả thực tế:** sản phẩm được tạo / sửa với Tên rỗng hoặc chỉ có khoảng trắng; danh sách Admin hiện dòng sản phẩm không có tên. Trên Web, Tên rỗng bị trình duyệt chặn nhưng Tên toàn khoảng trắng thì không.

**Bằng chứng:** `bugs/screenshots/FR15-B4.png`

![FR15-B4](screenshots/FR15-B4.png)

### FR15-B5 – Quản lý sản phẩm cho lưu Danh mục thiếu hoặc không có trong danh sách

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-15 ("Danh mục: bắt buộc, phải chọn từ danh sách có sẵn") |
| Thành phần | Backend `POST` / `PUT /api/products` (Web Admin dùng ô chọn nên không nhập được giá trị ngoài danh sách) |
| Loại | Lỗi lập trình (thiếu kiểm tra phía server) |
| Mức độ / Ưu tiên | Major / Trung bình |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR15-DT-12…FR15-DT-14, FR15-DT-24…FR15-DT-26, FR15-BV-18, FR15-BV-20 (API) |

**Các bước tái hiện**

1. Gửi `POST /api/products` với `{"name": "Sac nhanh USB-C 20W", "price": 350000}` (không có `category_id`).
2. Lặp lại với `"category_id": 99`, `0`, `"abc"`; `PUT /api/products/1` với `"category_id": 4` (danh mục có sẵn: 1, 2, 3).

**Kết quả mong đợi:** từ chối, báo Danh mục không hợp lệ.

**Kết quả thực tế:** sản phẩm được lưu với `category_id` `null`, `99`, `0`, `"abc"`, `4`.

**Phân tích:** sản phẩm không thuộc danh mục nào; lọc / xóa danh mục (FR-14) và hiển thị danh mục ở chi tiết sản phẩm (FR-06) có thể sai.

**Bằng chứng:** `bugs/screenshots/FR15-B5.png`

![FR15-B5](screenshots/FR15-B5.png)

### FR15-B6 – Sửa / Xóa sản phẩm không tồn tại trả 200 thay vì 404

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-15 (Sửa / Xóa một sản phẩm); giả định A6 (404 khi không tồn tại) |
| Thành phần | Backend `PUT` / `DELETE /api/products/:id` |
| Loại | Lỗi lập trình |
| Mức độ / Ưu tiên | Minor / Thấp |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR15-DT-27…FR15-DT-29, FR15-DT-31…FR15-DT-33, FR15-BV-21, FR15-BV-24, FR15-BV-25, FR15-BV-27 (API) |

**Các bước tái hiện**

1. Gửi `PUT /api/products/9999` với body hợp lệ; `DELETE /api/products/9999`.
2. Lặp lại với id `0`, `abc` và với sản phẩm vừa bị xóa.

**Kết quả mong đợi:** HTTP 404, báo không tìm thấy sản phẩm.

**Kết quả thực tế:** HTTP 200 `{"message": "Product updated"}` / `{"message": "Product deleted"}`; dữ liệu không đổi.

**Phân tích:** client (Web Admin) báo thao tác thành công dù không có gì xảy ra, che giấu lỗi khi hai admin cùng thao tác trên một sản phẩm.

**Bằng chứng:** `bugs/screenshots/FR15-B6.png`

![FR15-B6](screenshots/FR15-B6.png)

### FR-10 – Máy trạng thái đơn hàng

Môi trường: như FR-01; bộ dữ liệu 7 đơn của `test@eshop.com` / User B dựng bằng `scripts/fr10/fixture.py` (đơn #3 `shipping`, #5 `canceled`).

### FR10-B1 – Đơn đã hủy chuyển được sang "Đã giao"; Web Admin hiện nút "Đánh dấu Đã giao" cho đơn đã hủy

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-10 ("`delivered` và `canceled` là trạng thái kết thúc — không được phép chuyển sang bất kỳ trạng thái nào khác") |
| Thành phần | Backend `PUT /api/admin/orders/:id/status`; Web Admin tab "Đơn hàng" |
| Loại | Lỗi lập trình (thiếu ràng buộc trạng thái kết thúc) |
| Mức độ / Ưu tiên | Critical / Cao |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR10-DT-09 (Web, API), FR10-DT-26 (Web) |

**Các bước tái hiện**

1. Tạo đơn (`POST /api/checkout` bằng `test@eshop.com`), Admin hủy đơn (`status = canceled`) → đơn "Đã hủy".
2. Web Admin → tab "Đơn hàng": dòng đơn "Đã hủy" có nút "Đánh dấu Đã giao" → bấm nút.
3. Hoặc gửi `PUT /api/admin/orders/<id>/status` với `{"status": "delivered"}`.

**Kết quả mong đợi:** đơn đã hủy không có thao tác nào; API trả 4xx "chuyển đổi không hợp lệ"; đơn giữ "Đã hủy".

**Kết quả thực tế:** HTTP 200 "Order status updated"; đơn chuyển sang "Đã giao". Các chuyển đổi khác ra khỏi `canceled` (`→ pending`, `→ canceled`) và ra khỏi `delivered` đều bị từ chối đúng – chỉ cạnh `canceled → delivered` bị lọt.

**Phân tích:** đơn đã hủy được tính vào doanh thu (FR-13 chỉ tính đơn `delivered`); giao diện Admin chủ động mời thao tác sai.

**Bằng chứng:** `bugs/screenshots/FR10-B1.png`

![FR10-B1](screenshots/FR10-B1.png)

### FR10-B2 – User hủy được đơn đang giao; trang Hồ sơ hiện nút "Hủy đơn" cho đơn đang giao

| Trường | Nội dung |
| --- | --- |
| Feature / FR | FR-10 ("Khi đơn hàng đã ở trạng thái `shipping`, User không được phép tự hủy"); FR-20 nêu cùng quy tắc |
| Thành phần | Backend `PUT /api/orders/:id/cancel`; Web trang Hồ sơ – "Lịch sử đơn hàng" |
| Loại | Lỗi lập trình |
| Mức độ / Ưu tiên | Major / Cao |
| Tái hiện được | Luôn luôn |
| TC phát hiện | FR10-DT-14 (Web, API), FR10-DT-27 (Web) |

**Các bước tái hiện**

1. Tạo đơn của `test@eshop.com`; Admin chuyển `pending → confirmed → shipping`.
2. Đăng nhập Web bằng `test@eshop.com / Test1234!` → trang Hồ sơ: đơn "Đang giao" có nút "Hủy đơn" → bấm nút.
3. Hoặc gửi `PUT /api/orders/<id>/cancel` bằng token của `test@eshop.com`.

**Kết quả mong đợi:** không có nút hủy ở đơn đang giao; API trả 4xx; đơn giữ "Đang giao".

**Kết quả thực tế:** HTTP 200 "Order canceled successfully", Web hiện "Hủy đơn thành công!", đơn chuyển "Đã hủy". Hủy đơn "Đã giao" / "Đã hủy" thì bị từ chối đúng (400 "Cannot cancel this order.").

**Phân tích:** khách hủy được đơn khi hàng đã rời kho; Mobile dùng cùng API nên nhiều khả năng cũng bị (thuộc người làm Pool D – Lịch sử đơn hàng).

**Bằng chứng:** `bugs/screenshots/FR10-B2.png`

![FR10-B2](screenshots/FR10-B2.png)

## Ảnh trang GitHub Issues

<!-- Sau khi tạo issue: chụp trang issue, lưu bugs/screenshots/BUG-NN_issue.png và chèn vào đây. -->
