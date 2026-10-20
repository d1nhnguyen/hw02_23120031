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

### 1.1 Biến đầu vào

| Biến | Kênh nhập | Kiểu / miền giá trị | Ràng buộc theo đặc tả | Nguồn |
| --- | --- | --- | --- | --- |

### 1.2 Biến đầu ra

| Biến | Giá trị có thể có | Nguồn |
| --- | --- | --- |

### 1.3 Giả định cho những chỗ đặc tả chưa rõ

| ID | Giả định | Căn cứ |
| --- | --- | --- |

### 1.4 Ngoài phạm vi

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
