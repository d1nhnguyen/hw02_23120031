# FR-15 – Quản lý sản phẩm (CRUD) · Domain Testing & Boundary Value Analysis

| Mục | Giá trị |
| --- | --- |
| Feature | FR-15 – Quản lý sản phẩm (CRUD) (Pool C) |
| Kênh kiểm thử | Web Admin – tab Sản phẩm (http://localhost:5174) + API `POST/PUT/DELETE /api/products` |
| Người thực hiện | 23120031 |
| Công cụ AI | Claude Code (VS Code extension) |
| Kỹ thuật | Domain Testing (S04 – bước 1–3), Boundary Value Analysis (S04 – bước 4) |

## 0. Đặc tả (trích nguyên văn README của SUT)

> ### FR-15: Quản lý Sản phẩm (Product CRUD)
>
> - Admin có thể Thêm / Xem / Sửa / Xóa sản phẩm.
> - **Ràng buộc đầu vào:**
>   - Tên sản phẩm: bắt buộc, tối đa 255 ký tự.
>   - Giá: bắt buộc, phải là số **dương** (> 0).
>   - Danh mục: bắt buộc, phải chọn từ danh sách có sẵn.
> - Khi Sửa một sản phẩm, chỉ sản phẩm đó bị thay đổi — các sản phẩm khác giữ nguyên.

## 1. Bước 1 – Xác định biến Input / Output

### 1.1 Quan sát giao diện (hộp đen)

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

### 1.2 Biến đầu vào

| ID | Biến | Kênh nhập | Kiểu / miền giá trị | Ràng buộc theo đặc tả | Nguồn |
| --- | --- | --- | --- | --- | --- |
| I1 | Thao tác | Web: form Thêm / nút Sửa / nút Xóa / danh sách; API: method | {Thêm, Xem, Sửa, Xóa} | Admin thực hiện được cả 4 thao tác | FR-15 |
| I2 | Tên sản phẩm | Web: ô "Tên sản phẩm"; API: `name` | chuỗi ký tự | Bắt buộc; tối đa 255 ký tự | FR-15 |
| I3 | Giá | Web: ô "Giá tiền"; API: `price` | số | Bắt buộc; > 0 | FR-15 |
| I4 | Danh mục | Web: ô chọn danh mục; API: `category_id` | id danh mục | Bắt buộc; thuộc danh sách có sẵn (seed: 1, 2, 3) | FR-15 |
| I5 | Sản phẩm được Sửa / Xóa | Web: dòng được bấm; API: `:id` trên URL | id sản phẩm | Phải là sản phẩm đang tồn tại (seed: 1–5) | FR-15 (Sửa / Xóa một sản phẩm) |
| I6 | Mô tả, URL Ảnh | Web: ô "Mô tả", "URL Ảnh"; API: `description`, `imageUrl` | chuỗi | Không có ràng buộc (A5) | – |

### 1.3 Biến đầu ra

| ID | Biến | Giá trị có thể có | Nguồn |
| --- | --- | --- | --- |
| O1 | Kết quả thao tác | Thêm / Sửa / Xóa thành công; bị từ chối kèm thông báo lỗi | FR-15 |
| O2 | Phản hồi API | 2xx khi thành công; 4xx khi dữ liệu không hợp lệ; 404 khi sản phẩm không tồn tại (A6) | `api_specification.md`; A6 |
| O3 | Dữ liệu sản phẩm được thao tác | Giá trị Tên / Giá / Danh mục lưu trong hệ thống (`GET /api/products`) và hiển thị trên danh sách Admin | FR-15 (Xem) |
| O4 | Dữ liệu các sản phẩm khác | Giữ nguyên / bị thay đổi | FR-15 ("chỉ sản phẩm đó bị thay đổi") |

### 1.4 Giả định cho những chỗ đặc tả chưa rõ

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

### 1.5 Ngoài phạm vi

- Kiểm soát truy cập API sản phẩm (token / role) – FR-12; Import CSV – FR-16; hiển thị sản phẩm phía người dùng – FR-05, FR-06.
- Yêu cầu giao diện chung (nhãn, `*` bắt buộc, định dạng `₫` có phân cách hàng nghìn – FR-21, FR-22).

## 2. Bước 2 – Lớp tương đương (Complete Set of Partitions)

### 2.1 Cách áp dụng guideline cho từng biến

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

### 2.2 Complete Set of Partitions

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

## 3. Bước 3 – Test case Domain Testing

### 3.1 Thủ tục thực hiện

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

### 3.2 Minimum Set of Test Cases

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

### 3.3 Bảng phủ phân vùng

<!-- BEGIN:T33 -->
| EC | Test case phủ | | EC | Test case phủ |
| --- | --- | --- | --- | --- |
| EC1 | FR15-DT-01…FR15-DT-04 | | EC17 | FR15-DT-01…FR15-DT-04, FR15-DT-15, FR15-DT-16 |
| EC2 | FR15-DT-01…FR15-DT-04, FR15-DT-15, FR15-DT-16, FR15-DT-30 | | EC18 | FR15-DT-12, FR15-DT-24 |
| EC3 | FR15-DT-15, FR15-DT-16 | | EC19 | FR15-DT-13, FR15-DT-25 |
| EC4 | FR15-DT-30 | | EC20 | FR15-DT-14, FR15-DT-26 |
| EC5 | FR15-DT-01, FR15-DT-04, FR15-DT-15 | | EC21 | FR15-DT-15, FR15-DT-16, FR15-DT-30 |
| EC6 | FR15-DT-02, FR15-DT-16 | | EC22 | FR15-DT-27, FR15-DT-31 |
| EC7 | FR15-DT-03 | | EC23 | FR15-DT-28, FR15-DT-32 |
| EC8 | FR15-DT-05, FR15-DT-17 | | EC24 | FR15-DT-29, FR15-DT-33 |
| EC9 | FR15-DT-06, FR15-DT-18 | | EC25 | FR15-DT-01…FR15-DT-04 |
| EC10 | FR15-DT-07, FR15-DT-19 | | EC26 | FR15-DT-15, FR15-DT-16 |
| EC11 | FR15-DT-01…FR15-DT-03, FR15-DT-15, FR15-DT-16 | | EC27 | FR15-DT-30 |
| EC12 | FR15-DT-04 | | EC28 | FR15-DT-15, FR15-DT-16, FR15-DT-30 |
| EC13 | FR15-DT-08, FR15-DT-20 | | EC29 | FR15-DT-05…FR15-DT-07, FR15-DT-17…FR15-DT-19 |
| EC14 | FR15-DT-09, FR15-DT-21 | | EC30 | FR15-DT-08…FR15-DT-11, FR15-DT-20…FR15-DT-23 |
| EC15 | FR15-DT-10, FR15-DT-22 | | EC31 | FR15-DT-12…FR15-DT-14, FR15-DT-24…FR15-DT-26 |
| EC16 | FR15-DT-11, FR15-DT-23 | | EC32 | FR15-DT-27…FR15-DT-29, FR15-DT-31…FR15-DT-33 |

32 / 32 lớp được phủ bởi 33 test case Minimum Set (7 valid, 26 invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp invalid có test case riêng.
<!-- END:T33 -->

## 4. Bước 4 – Boundary Value Analysis

### 4.1 Xác định biên

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

### 4.2 Boundary Value Test Cases

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

## 5. Bước 5 – Kết quả thực thi

### 5.1 Môi trường và cách chạy

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

### 5.2 Phát hiện chính

- **Server không kiểm tra dữ liệu sản phẩm:** mọi giá trị Tên / Giá / Danh mục không hợp lệ đều được lưu khi Thêm và khi Sửa (HTTP 200 "Product created" / "Product updated").
- **Web Admin chỉ chặn Tên rỗng** (thuộc tính `required` của trình duyệt). Tên toàn khoảng trắng, Tên > 255 ký tự, Giá 0 / âm / trống đều được gửi đi; khi Sửa còn hiện "Cập nhật thành công!".
- **Giá thập phân** (`99999.5`, `0.01`) được lưu cả qua Web lẫn API – đúng với A3; ghi nhận ở bước 1 rằng trình duyệt chặn `0.5` là chưa chính xác (xem mục 6).
- **Sửa / Xóa sản phẩm không tồn tại** (id `0`, `6`, `9999`, `abc`, sản phẩm vừa xóa) trả 200 "Product updated" / "Product deleted" thay vì 404; dữ liệu không đổi.
- Các thao tác hợp lệ đều đúng; khi Sửa / Xóa một sản phẩm, các sản phẩm khác giữ nguyên (đúng yêu cầu "chỉ sản phẩm đó bị thay đổi"). Tên chứa HTML được hiển thị nguyên văn.

### 5.3 Kết quả theo test case

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

### 5.4 Tổng hợp

<!-- BEGIN:T55 -->
| Kênh | Thiết kế | Đã chạy | Pass | Fail | Blocked | Không áp dụng |
| --- | --- | --- | --- | --- | --- | --- |
| Web | 61 | 41 | 25 | 16 | 0 | 20 |
| API | 61 | 60 | 22 | 38 | 0 | 1 |
| **Tổng lượt chạy** | | **101** | **47** | **54** | **0** | |

61 test case = 33 Minimum Set (mục 3.2) + 27 BVA (mục 4.2) + 1 bổ sung sau rà soát (mục 6.2). Gộp các kênh theo test case (Fail nếu Fail ở bất kỳ kênh nào, Blocked nếu còn kênh bị Blocked): 23 Pass, 38 Fail, 0 Blocked.
<!-- END:T55 -->

## 6. Bước 6 – AI gap analysis

> G1–G5: AI (Claude Code) tự phát hiện trong lúc làm các bước 1–5 của FR-15. Sinh viên rà soát và bổ sung các điểm tự phát hiện ở commit `[FR-15][Bn-review]`.

### 6.1 Những gì AI bỏ sót hoặc làm sai

| # | AI bỏ sót / làm sai | Loại | Nguyên nhân | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |
| G1 | Bước 1 ghi "trình duyệt chặn `0.5`" chỉ dựa vào thông báo `validationMessage` của ô Giá, không thử bấm Lưu; thực tế giá thập phân vẫn được gửi và lưu | Quan sát / giả định sai về SUT | **Giới hạn công cụ AI**: suy ra hành vi từ thuộc tính giao diện thay vì quan sát hành vi thật | FR15-DT-04, FR15-BV-13 Pass ở bước 5 trái với dự đoán; khảo sát lại `checkValidity()` | Đính chính mục 1.1 |
| G2 | Thiết kế ban đầu không có test case Sửa chỉ một ô trên Web: mọi test case Sửa đều chọn lại Danh mục, nên không kiểm tra được form Sửa có điền sẵn đúng Danh mục (A9) hay không – lần khảo sát chỉ xem sản phẩm danh mục 1, trùng giá trị mặc định | Test case thiếu | **Độ phức tạp feature**: hành vi phụ thuộc giá trị form điền sẵn; **giới hạn công cụ AI**: script luôn nhập đủ mọi ô nên không giống thao tác thật | AI rà soát bảng phủ và giả định A9 sau khi chạy | Bổ sung FR15-DT-34 (mục 6.2): Pass |
| G3 | Script Web bản đầu ghi thông báo "Please fill out this field." của form đã được xóa trắng sau khi lưu vào mọi test case → bằng chứng sai lệch, có thể khiến test case "từ chối" Pass giả | Oracle / bằng chứng | **Giới hạn công cụ AI**: lặp lại đúng lỗi G5 của FR-01 (đọc thông báo sau khi giao diện đã đổi trạng thái) – AI không tự chuyển bài học giữa các feature | Đọc output: test case thành công cũng có thông báo lỗi | Chỉ đọc thông báo trình duyệt khi form không gửi request |
| G4 | Runner API bản đầu treo ở test case đầu tiên (chờ pipe của tiến trình backend chạy nền); trong lúc kiểm tra, AI còn khởi động lại backend song song làm hỏng lượt chạy | Thực thi | **Giới hạn công cụ AI**: lỗi lập trình script và thao tác song song trên môi trường dùng chung | Không có dòng kết quả nào sau 400 giây | Không bắt output của script restart; chạy lại toàn bộ |
| G5 | Bảng kết quả bản đầu: ô API của FR15-DT-03 ghi "hiển thị nguyên văn None"; test case "không tìm thấy" Fail không nêu lý do; tên chứa `<b>` trong ô bảng sẽ bị hiển thị thành chữ đậm | Báo cáo kết quả | **Giới hạn công cụ AI**: sinh văn bản tự động không kiểm tra theo kênh và không escape | AI đọc lại bảng sinh ra | Sửa hàm diễn giải kết quả; escape `<`, `>`, `|` trong `report_lib.py` |

### 6.2 Test case bổ sung

Kết quả thực thi nằm ở mục 5.3.

<!-- BEGIN:T62 -->
| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Thao tác | Sản phẩm (id) | Tên | Giá | Danh mục | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR15-DT-34 | Kiểm tra sửa chỉ Giá sản phẩm thành công mà Danh mục do form điền sẵn được giữ nguyên | EC3, EC11, EC17, EC21, EC26 (A9 – form Sửa điền sẵn đúng Danh mục khác giá trị mặc định 1) | Sửa | `3` | `MacBook␣Pro␣M3` (không chạm vào ô) | `43000000` | `2` (không chạm vào ô) | Sửa thành công: sản phẩm id 3 mang Tên / Giá / Danh mục như cột dữ liệu, Mô tả / Ảnh giữ nguyên; các sản phẩm khác giữ nguyên (EC26, EC28); A9 | Web | AI |
<!-- END:T62 -->

### 6.3 Điểm còn mở (chưa xử lý)

- Giá gửi dạng chuỗi số (`"350000"`) qua API chưa được phân vùng: đặc tả không nói giá trị dạng chuỗi số có hợp lệ không (liên quan A4).
- A3 (giá thập phân hợp lệ) và A6 (404 khi sản phẩm không tồn tại) quyết định kết luận của FR15-DT-04, FR15-BV-13 và FR15-B6; cần TA xác nhận.

### 6.4 Nhận xét

- **Do prompt:** prompt không yêu cầu đối chiếu bài học từ FR-01, nên AI lặp lại lỗi đọc thông báo sau khi giao diện đổi trạng thái (G3).
- **Do giới hạn công cụ AI:** AI dễ kết luận về hành vi SUT từ thuộc tính tĩnh (G1) và dễ viết oracle / script có lỗi ngầm (G3, G4); các lỗi này chỉ lộ ra khi đọc kỹ output thay vì chỉ nhìn số Pass / Fail.
- **Do độ phức tạp feature:** Sửa phụ thuộc trạng thái form điền sẵn (G2), một khía cạnh mà dữ liệu đầu vào trong bảng không thể hiện được.

## 7. Bước 7 – Bug

| Bug ID | Tiêu đề | Mức độ | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- |
