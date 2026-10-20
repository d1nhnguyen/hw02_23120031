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
