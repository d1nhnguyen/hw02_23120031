# Mobile – Đăng nhập · Domain Testing & Boundary Value Analysis

| Mục | Giá trị |
| --- | --- |
| Feature | Mobile – Đăng nhập (Pool D, FR-20) |
| Kênh kiểm thử | App mobile (Expo Go SDK 54 trên Android Emulator `eshop_api34`, Android 14), backend qua `http://10.0.2.2:3000/api` |
| Người thực hiện | 23120031 |
| Công cụ AI | Claude Code (VS Code extension) |
| Kỹ thuật | Domain Testing (S04 – bước 1–3), Boundary Value Analysis (S04 – bước 4) |

## 0. Đặc tả (trích nguyên văn README của SUT)

> ### FR-02: Đăng nhập & Khóa tài khoản
>
> - Người dùng nhập Email và Mật khẩu.
> - Sau mỗi lần đăng nhập sai, hệ thống tăng bộ đếm lên **đúng 1 đơn vị**.
> - Nếu đăng nhập sai từ **3 lần trở lên** liên tiếp, tài khoản bị tạm khóa **30 giây** (môi trường demo). Hệ thống trả về thông báo lỗi phù hợp; không để lộ chi tiết nguyên nhân.
> - Đăng nhập thành công trả về JWT Token. Token được lưu phía client và gửi kèm tất cả các yêu cầu có xác thực qua header `Authorization: Bearer <token>`.
> - Trường email phải dùng `type="email"` (có validate HTML5 format).

> ### FR-20: Tính năng Mobile
>
> - Đầy đủ các chức năng: Xem sản phẩm, Đăng nhập, Đăng xuất, Đăng ký, Giỏ hàng, Thanh toán, Hồ sơ, Lịch sử đơn hàng.
> - Chức năng Hủy đơn hàng tuân theo đúng State Machine ở FR-10 (chỉ được hủy khi `pending` hoặc `confirmed`).

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
