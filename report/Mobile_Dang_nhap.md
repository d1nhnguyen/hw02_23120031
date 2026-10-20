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

### 1.1 Quan sát giao diện (hộp đen)

App EShop Mobile chạy bằng Expo Go (SDK 54) trên Android 14, backend qua `http://10.0.2.2:3000/api`. Điều khiển và quan sát bằng `adb` (cây giao diện `uiautomator dump`, chạm, nhập chữ, chụp màn hình).

| Thiết bị ảo | Thanh trạng thái | Quan sát |
| --- | --- | --- |
| Pixel 6 (`eshop_api34`, 1080×2400, có tai thỏ camera) | cao 128 px | Thanh tiêu đề của app (y = 37–108, chứa "Đăng nhập", "Giỏ (0)") nằm **dưới** thanh trạng thái; chạm vào "Đăng nhập" không có tác dụng; không có đường nào khác tới màn hình Đăng nhập (ảnh `evidence/Mobile/B1_pixel6_header_bi_che.png`) |
| Pixel 2 (`eshop_api34_pixel2`, 1080×1920, không tai thỏ) | cao 63 px | Phần dưới của "Đăng nhập" (y = 63–98) chạm được → mở màn hình Đăng nhập; mọi thực thi ở bước 5 dùng thiết bị này |

Màn hình Đăng nhập (Pixel 2, ảnh `B1_pixel2_man_hinh_dang_nhap.png`):

| Thành phần | Quan sát |
| --- | --- |
| Tiêu đề | "Đăng Nhập" |
| Nhãn + ô thứ nhất | nhãn **"Username"**, ô nhập placeholder "Email" |
| Nhãn + ô thứ hai | nhãn "Mật khẩu", ô nhập có thuộc tính `password` (che ký tự `•`) |
| Nút | **"Sign In"**; liên kết "Quên mật khẩu?", "Chưa có tài khoản? Đăng ký ngay", "Quay Lại" |
| Sai thông tin | dòng chữ "Đăng nhập thất bại. Vui lòng kiểm tra lại." hiện ngay trên màn hình |
| Đúng thông tin | về trang chủ, thanh tiêu đề hiện "Chào, Test User"; bấm vào mở trang Hồ sơ với dữ liệu tài khoản (ảnh `B1_pixel2_sau_dang_nhap.png`) |

API mà app gọi: `POST /api/login` (`{"email", "password"}` → `{"token", "user"}`); trạng thái khóa quan sát được qua `GET /api/admin/users` (trường `login_attempts`, `locked_until`).

### 1.2 Biến đầu vào

| ID | Biến | Kênh nhập | Kiểu / miền giá trị | Ràng buộc theo đặc tả | Nguồn |
| --- | --- | --- | --- | --- | --- |
| I1 | Email | Mobile: ô "Email"; API: `email` | chuỗi | Email của tài khoản đã đăng ký | FR-02 |
| I2 | Mật khẩu | Mobile: ô "Mật khẩu"; API: `password` | chuỗi | Khớp mật khẩu của tài khoản | FR-02 |
| I3 | Số lần đăng nhập sai liên tiếp trước lần thử | Tiền điều kiện (chuỗi thao tác trước đó) | 0, 1, 2, … | Từ 3 lần trở lên → tài khoản bị khóa | FR-02 |
| I4 | Thời gian từ lúc bị khóa tới lần thử | Tiền điều kiện (chờ) | giây | Khóa 30 giây | FR-02 |
| I5 | Có lần đăng nhập đúng xen giữa các lần sai | Tiền điều kiện | có / không | "liên tiếp" | FR-02 |

### 1.3 Biến đầu ra

| ID | Biến | Giá trị có thể có | Nguồn |
| --- | --- | --- | --- |
| O1 | Kết quả đăng nhập | Thành công: rời màn hình Đăng nhập, thanh tiêu đề chào người dùng, mở được trang Hồ sơ (token được lưu và gửi kèm); thất bại: ở lại màn hình Đăng nhập | FR-02, FR-20 |
| O2 | Thông báo | Thông báo lỗi chung, không lộ nguyên nhân (sai email / sai mật khẩu / bị khóa) | FR-02 |
| O3 | Bộ đếm sai (`login_attempts`) | tăng đúng 1 mỗi lần sai; về 0 khi đăng nhập đúng (A3) | FR-02 |
| O4 | Trạng thái khóa (`locked_until`) | không khóa / khóa tới thời điểm lần sai thứ 3 + 30 giây | FR-02 |
| O5 | Phản hồi API | `200` + `token` / `401` khi sai / mã lỗi khi bị khóa | `api_specification.md` 1.2 |

### 1.4 Giả định cho những chỗ đặc tả chưa rõ

| ID | Giả định | Căn cứ |
| --- | --- | --- |
| A1 | Quy tắc đăng nhập trên Mobile là quy tắc của FR-02 | FR-20 chỉ nêu Mobile có chức năng Đăng nhập; nhóm thống nhất Pool D = các chức năng của FR-20. Cần TA xác nhận |
| A2 | Tài khoản bị khóa ngay sau lần sai thứ 3 liên tiếp; trong 30 giây sau đó mọi lần đăng nhập (kể cả mật khẩu đúng) bị từ chối; sau 2 lần sai vẫn đăng nhập đúng được | "sai từ 3 lần trở lên liên tiếp … tạm khóa 30 giây" |
| A3 | Đăng nhập thành công đặt bộ đếm về 0 | "liên tiếp" |
| A4 | Bộ đếm / thời điểm khóa quan sát qua `GET /api/admin/users` (`login_attempts`, `locked_until`) | API Admin có trong `api_specification.md` 6.1 |
| A5 | Cùng một thông báo cho sai email, sai mật khẩu, email không tồn tại; khi bị khóa thông báo có thể khác nhưng không cho đăng nhập | "không để lộ chi tiết nguyên nhân" |
| A6 | Email so khớp không phân biệt hoa / thường và bỏ khoảng trắng đầu / cuối; mật khẩu so khớp chính xác | Nhất quán với FR-01 (giả định A3, A4 của FR-01) |
| A7 | Đăng nhập với email không tồn tại không làm thay đổi bộ đếm của tài khoản nào | Không có tài khoản để đếm |
| A8 | "Token được lưu phía client và gửi kèm" kiểm chứng bằng việc mở được trang Hồ sơ (cần xác thực) sau khi đăng nhập; không yêu cầu giữ phiên sau khi tắt app | FR-02 |
| A9 | Ô Mật khẩu phải che ký tự (tương đương `type="password"` của FR-22 trên mobile) | FR-22 |

### 1.5 Ngoài phạm vi

- Đăng xuất, Đăng ký, Quên mật khẩu trên Mobile (các chức năng khác của Pool D); đăng nhập trên Web (FR-02).

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
