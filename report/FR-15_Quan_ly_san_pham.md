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
| Ô "Giá tiền" | `type="number"`, **không** `required`, không đặt `min` / `step`. Trình duyệt chặn `0.5` ("The two nearest valid values are 0 and 1" – bước mặc định 1) nhưng cho qua `0`, `-1`, `1e3` |
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
