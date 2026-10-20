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

| Biến | Kiểu / miền giá trị | Ràng buộc theo đặc tả | Nguồn (FR) |
| --- | --- | --- | --- |

### 1.2 Biến đầu ra

| Biến | Giá trị có thể có | Nguồn (FR) |
| --- | --- | --- |

### 1.3 Giả định cho những chỗ đặc tả chưa rõ

| ID | Giả định | Lý do | Đã hỏi TA? |
| --- | --- | --- | --- |

## 2. Bước 2 – Lớp tương đương

| ID | Biến | Điều kiện | Lớp tương đương | Valid / Invalid | Origin | Verdict output AI |
| --- | --- | --- | --- | --- | --- | --- |

## 3. Bước 3 – Test case Domain Testing

### 3.1 Bảng phủ lớp tương đương

| Lớp (EC) | Test case phủ |
| --- | --- |

### 3.2 Danh sách test case

| ID | Tiêu đề (Action + Function + Condition) | Lớp phủ | Tiền điều kiện | Các bước | Dữ liệu | Kết quả mong đợi | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 4. Bước 4 – Boundary Value Analysis

### 4.1 Xác định biên

| Biến | Phân vùng | LB | UB | Giá trị nhỏ nhất nhập được (UI/API) | Giá trị lớn nhất nhập được (UI/API) |
| --- | --- | --- | --- | --- | --- |

### 4.2 Danh sách test case BVA

| ID | Tiêu đề (Action + Function + Condition) | Biến / biên | Giá trị | Tiền điều kiện | Kết quả mong đợi | Origin |
| --- | --- | --- | --- | --- | --- | --- |

## 5. Bước 5 – Kết quả thực thi

| TC ID | Kênh (UI / API) | Kết quả thực tế | Trạng thái | Bằng chứng | Bug ID |
| --- | --- | --- | --- | --- | --- |

| Thiết kế | Đã chạy | Pass | Fail | Chưa chạy | Số bug |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 6. Bước 6 – AI gap analysis

| # | AI bỏ sót / làm sai | Loại (EC / TC / biên / expected sai / bug) | Nguyên nhân (prompt / giới hạn công cụ AI / độ phức tạp feature) | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |

## 7. Bước 7 – Bug

| Bug ID | Tiêu đề | Mức độ | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- |
