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
