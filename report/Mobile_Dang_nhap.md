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

### 2.1 Cách áp dụng guideline cho từng biến

| Biến | Điều kiện trong đặc tả | Guideline [S04] | Lớp tạo ra |
| --- | --- | --- | --- |
| I1 Email | email của tài khoản đã đăng ký | "Phải là" → đã đăng ký / không tồn tại; tách lớp (G5): khác hoa / thường, có khoảng trắng đầu / cuối (so khớp có thể khác nhau – A6), rỗng, sai định dạng | 3 valid, 3 invalid |
| I2 Mật khẩu | khớp mật khẩu | "Phải là" → đúng / sai; tách lớp (G5): rỗng, chỉ khác hoa / thường, thừa khoảng trắng cuối (so khớp có thể bỏ qua – A6) | 1 valid, 4 invalid |
| I3 Số lần sai liên tiếp trước đó | "từ 3 lần trở lên … bị khóa" | Khoảng giá trị: 0–2 (chưa khóa) / ≥ 3 (khóa) | 1 valid, 1 invalid |
| I4 Thời gian từ lúc khóa | "tạm khóa 30 giây" | Khoảng giá trị: < 30 giây (còn khóa) / ≥ 30 giây (hết khóa) | 1 valid, 1 invalid |
| I5 Đăng nhập đúng xen giữa | "liên tiếp" | "Phải là" chuỗi liên tiếp mới khóa → có lần đúng xen giữa thì bộ đếm làm mới (A3) | 1 valid |
| Đầu ra O1–O5 | thành công / thất bại / bộ đếm / khóa / hết khóa | Phân vùng đầu ra như ví dụ [UC] | 5 lớp đầu ra |

### 2.2 Complete Set of Partitions

| EC | Biến | Phân vùng | Ví dụ đại diện | Valid / Invalid |
| --- | --- | --- | --- | --- |
| EC1 | I1 Email | Email đã đăng ký, đúng chính xác | `test@eshop.com` | Valid |
| EC2 | I1 Email | Email đã đăng ký, khác chữ hoa / thường (A6) | `TEST@eshop.com` | Valid |
| EC3 | I1 Email | Email đã đăng ký, có khoảng trắng đầu / cuối (A6) | `␣test@eshop.com␣` | Valid |
| EC4 | I1 Email | Email không tồn tại | `khongco@eshop.com` | Invalid |
| EC5 | I1 Email | Rỗng | `` | Invalid |
| EC6 | I1 Email | Sai định dạng | `test@eshop` | Invalid |
| EC7 | I2 Mật khẩu | Đúng | `Test1234!` | Valid |
| EC8 | I2 Mật khẩu | Sai | `Sai12345!` | Invalid |
| EC9 | I2 Mật khẩu | Rỗng | `` | Invalid |
| EC10 | I2 Mật khẩu | Chỉ khác chữ hoa / thường | `test1234!` | Invalid |
| EC11 | I2 Mật khẩu | Thừa khoảng trắng cuối (A6) | `Test1234!␣` | Invalid |
| EC12 | I3 | 0–2 lần sai liên tiếp trước đó (chưa khóa) | 0 | Valid |
| EC13 | I3 | ≥ 3 lần sai liên tiếp trước đó (bị khóa) | 3 | Invalid |
| EC14 | I4 | Thử lại khi chưa hết 30 giây khóa | ngay sau khi khóa | Invalid |
| EC15 | I4 | Thử lại khi đã hết 30 giây khóa | sau 35 giây | Valid |
| EC16 | I5 | Có lần đăng nhập đúng xen giữa các lần sai (A3) | sai, sai, đúng, sai, sai, đúng | Valid |
| EC17 | O1, O5 | Đăng nhập thành công: rời màn hình Đăng nhập, chào người dùng, mở được Hồ sơ; API `200` + `token` | | Output |
| EC18 | O1, O2, O5 | Thất bại: thông báo lỗi chung, giống nhau cho sai email / sai mật khẩu (A5); API `401` | | Output |
| EC19 | O3 | Bộ đếm `login_attempts` tăng đúng 1 sau mỗi lần sai | | Output |
| EC20 | O1, O4 | Bị khóa: từ chối cả mật khẩu đúng | | Output |
| EC21 | O1, O4 | Hết khóa: đăng nhập đúng thành công, bộ đếm về 0 | | Output |

Tổng: 16 lớp đầu vào (7 valid, 9 invalid) và 5 lớp đầu ra.

## 3. Bước 3 – Test case Domain Testing

### 3.1 Thủ tục thực hiện

Mọi test case dùng chung thủ tục, chỉ dữ liệu thay đổi → dạng **data matrix** [DR]. ID có tiền tố `MOB-`. Mỗi test case gồm các **lần thử trước** (tiền điều kiện, thực hiện cùng kênh) và **lần thử được đánh giá** (cột Email, Mật khẩu). Trong bảng: `␣` là một dấu cách; `(rỗng)` là để trống ô.

**Tiền điều kiện chung (self-standing, self-cleaning):** khởi động lại backend trước mỗi test case → `test@eshop.com / Test1234!` có `login_attempts = 0`, chưa bị khóa.

**P-MOBILE** – Android Emulator Pixel 2, Expo Go:

| Bước | Hành động | Kết quả mong đợi của bước |
| --- | --- | --- |
| 1 | Mở lại app (trạng thái chưa đăng nhập), bấm "Đăng nhập" trên thanh tiêu đề | Màn hình "Đăng Nhập" với ô Email, Mật khẩu, nút đăng nhập |
| 2 | Thực hiện lần lượt các lần thử trước: nhập Email, Mật khẩu, bấm nút đăng nhập; nếu đăng nhập thành công thì quay lại màn hình Đăng nhập | Như thiết kế của tiền điều kiện |
| 3 | Chờ theo cột "Chờ trước lần thử" (tính từ lần thử trước cuối cùng) | – |
| 4 | Nhập Email, Mật khẩu theo cột dữ liệu, bấm nút đăng nhập | Như cột Kết quả mong đợi |
| 5 | Nếu đăng nhập thành công: bấm "Chào, …" trên thanh tiêu đề | Trang "Hồ sơ của bạn" hiện email `test@eshop.com` (token được dùng – A8) |
| 6 | Kiểm chứng bộ đếm: `GET /api/admin/users` → `login_attempts`, `locked_until` của `test@eshop.com` (A4) | Như cột Kết quả mong đợi |

**P-API** – các lần thử trước và lần thử được đánh giá là `POST /api/login` với `{"email", "password"}`; kiểm chứng mã HTTP, `token`, và bước 6 như trên.

### 3.2 Minimum Set of Test Cases

Dữ liệu và kết quả mong đợi được sinh từ `scripts/mobile/cases.py` (cùng nguồn với script thực thi) bằng `scripts/mobile/report_tables.py`.

<!-- BEGIN:T32 -->
**Test case valid** – mỗi test case phủ nhiều lớp valid nhất có thể:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Email | Mật khẩu | Các lần thử trước (tiền điều kiện) | Chờ trước lần thử | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MOB-DT-01 | Kiểm tra đăng nhập thành công với email và mật khẩu đúng | EC1, EC7, EC12, EC17 | `test@eshop.com` | `Test1234!` | – | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17) | Mobile, API | AI |
| MOB-DT-02 | Kiểm tra đăng nhập thành công khi email khác chữ hoa / thường | EC2, EC7, EC12, EC17 | `TEST@eshop.com` | `Test1234!` | – | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); A6 | Mobile, API | AI |
| MOB-DT-03 | Kiểm tra đăng nhập thành công khi email có khoảng trắng đầu / cuối | EC3, EC7, EC12, EC17 | `␣test@eshop.com␣` | `Test1234!` | – | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); A6 | Mobile, API | AI |
| MOB-DT-04 | Kiểm tra đăng nhập thành công khi đã hết 30 giây khóa | EC15, EC21 | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | 35 giây | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); tiền điều kiện: 3 lần sai liên tiếp rồi chờ 35 giây | Mobile, API | AI |
| MOB-DT-05 | Kiểm tra đăng nhập đúng xen giữa làm mới chuỗi sai liên tiếp | EC16, EC12, EC17 | `test@eshop.com` | `Test1234!` | 2 × sai (`Sai12345!`) → 1 × đúng (`Test1234!`) → 2 × sai (`Sai12345!`) | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); A3; sau lần đúng thứ nhất chuỗi sai bắt đầu lại nên 2 lần sai sau không làm khóa tài khoản | Mobile, API | AI |

**Test case invalid** – mỗi test case phủ đúng một lớp invalid, các biến còn lại hợp lệ:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Email | Mật khẩu | Các lần thử trước (tiền điều kiện) | Chờ trước lần thử | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MOB-DT-06 | Kiểm tra đăng nhập bị từ chối khi sai mật khẩu | EC8, EC18, EC19 | `test@eshop.com` | `Sai12345!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19) | Mobile, API | AI |
| MOB-DT-07 | Kiểm tra đăng nhập bị từ chối với cùng thông báo khi email không tồn tại | EC4, EC18 | `khongco@eshop.com` | `Test1234!` | 1 × sai (`Sai12345!`) | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19); A5, A7: thông báo giống hệt lần sai mật khẩu ở tiền điều kiện; bộ đếm của `test@eshop.com` giữ 1 | Mobile, API | AI |
| MOB-DT-08 | Kiểm tra đăng nhập bị từ chối khi bỏ trống email | EC5, EC18 | (rỗng) | `Test1234!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 0 (EC18, EC19) | Mobile, API | AI |
| MOB-DT-09 | Kiểm tra đăng nhập bị từ chối khi email sai định dạng | EC6, EC18 | `test@eshop` | `Test1234!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 0 (EC18, EC19) | Mobile, API | AI |
| MOB-DT-10 | Kiểm tra đăng nhập bị từ chối khi bỏ trống mật khẩu | EC9, EC18 | `test@eshop.com` | (rỗng) | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19) | Mobile, API | AI |
| MOB-DT-11 | Kiểm tra đăng nhập bị từ chối khi mật khẩu chỉ khác chữ hoa / thường | EC10, EC18 | `test@eshop.com` | `test1234!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19) | Mobile, API | AI |
| MOB-DT-12 | Kiểm tra đăng nhập bị từ chối khi mật khẩu thừa khoảng trắng cuối | EC11, EC18 | `test@eshop.com` | `Test1234!␣` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19); A6 | Mobile, API | AI |
| MOB-DT-13 | Kiểm tra đăng nhập bị từ chối dù mật khẩu đúng khi đã sai 3 lần liên tiếp | EC13, EC14, EC20 | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | – | Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20); A2 | Mobile, API | AI |
<!-- END:T32 -->

### 3.3 Bảng phủ phân vùng

<!-- BEGIN:T33 -->
| EC | Test case phủ | | EC | Test case phủ |
| --- | --- | --- | --- | --- |
| EC1 | MOB-DT-01 | | EC12 | MOB-DT-01…MOB-DT-03, MOB-DT-05 |
| EC2 | MOB-DT-02 | | EC13 | MOB-DT-13 |
| EC3 | MOB-DT-03 | | EC14 | MOB-DT-13 |
| EC4 | MOB-DT-07 | | EC15 | MOB-DT-04 |
| EC5 | MOB-DT-08 | | EC16 | MOB-DT-05; bổ sung: MOB-DT-14 (mục 6.2) |
| EC6 | MOB-DT-09 | | EC17 | MOB-DT-01…MOB-DT-03, MOB-DT-05; bổ sung: MOB-DT-14 (mục 6.2) |
| EC7 | MOB-DT-01…MOB-DT-03 | | EC18 | MOB-DT-06…MOB-DT-12 |
| EC8 | MOB-DT-06 | | EC19 | MOB-DT-06 |
| EC9 | MOB-DT-10 | | EC20 | MOB-DT-13 |
| EC10 | MOB-DT-11 | | EC21 | MOB-DT-04 |
| EC11 | MOB-DT-12 | |  |  |

21 / 21 lớp được phủ bởi 13 test case Minimum Set (5 valid, 8 invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp invalid có test case riêng. Các đại diện bổ sung sau rà soát (mục 6.2) ghi sau dấu `;`.
<!-- END:T33 -->

## 4. Bước 4 – Boundary Value Analysis

### 4.1 Xác định biên

| Biến | Phân vùng | LB | UB | Bước nhảy | Điểm kiểm tra |
| --- | --- | --- | --- | --- | --- |
| I3 số lần sai liên tiếp trước lần thử | EC12 (0–2) / EC13 (≥ 3) | 0; 3 | 2; – | 1 lần | 0, 1, 2, 3, 4 |
| Bộ đếm `login_attempts` | tăng 1 mỗi lần sai, khóa khi đạt 3 | – | 3 | 1 | sau lần sai thứ 2 → 3 |
| I4 thời gian từ lúc khóa | EC14 (< 30 giây) / EC15 (≥ 30 giây) | 30 giây | – | 2 giây (sai số thao tác trên Mobile ~1 giây) | 0, 28, 32, 35 giây |
| Độ dài mật khẩu so với mật khẩu đúng | EC7 / EC8 | 9 ký tự (`Test1234!`) | 9 | 1 ký tự | 8, 9, 10 ký tự |
| Độ dài email so với email đúng | EC1 / EC4 | 14 ký tự (`test@eshop.com`) | 14 | 1 ký tự | 13, 14, 15 ký tự |

### 4.2 Boundary Value Test Cases

Thủ tục: mục 3.1. Bảng giữ các cột dữ liệu của data matrix như mục 3.2. Dòng có ID trong ngoặc là điểm biên đã có trong Minimum Set, chỉ dẫn chiếu.

<!-- BEGIN:T42 -->
| ID | Tên test case (Action + Function + Condition) | Partition tested | Email | Mật khẩu | Các lần thử trước (tiền điều kiện) | Chờ trước lần thử | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| (MOB-DT-01) | Kiểm tra đăng nhập thành công với email và mật khẩu đúng | EC12 – 0 lần sai (LB) | `test@eshop.com` | `Test1234!` | – | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17) | Mobile, API | xem 3.2 |
| MOB-BV-01 | Kiểm tra đăng nhập thành công khi trước đó sai 1 lần | EC12 – 1 lần sai (LB+1) | `test@eshop.com` | `Test1234!` | 1 × sai (`Sai12345!`) | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17) | Mobile, API | AI |
| MOB-BV-02 | Kiểm tra đăng nhập thành công khi trước đó sai 2 lần liên tiếp | EC12/EC13 – 2 lần sai (UB của EC12) | `test@eshop.com` | `Test1234!` | 2 × sai (`Sai12345!`) | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); A2 | Mobile, API | AI |
| (MOB-DT-13) | Kiểm tra đăng nhập bị từ chối dù mật khẩu đúng khi đã sai 3 lần liên tiếp | EC13 – 3 lần sai (LB của EC13) | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | – | Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20); A2 | Mobile, API | xem 3.2 |
| MOB-BV-03 | Kiểm tra đăng nhập bị từ chối dù mật khẩu đúng khi trước đó sai 4 lần liên tiếp | EC13 – 4 lần sai (LB+1 của EC13) | `test@eshop.com` | `Test1234!` | 4 × sai (`Sai12345!`) | – | Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20) | Mobile, API | AI |
| MOB-BV-04 | Kiểm tra lần sai thứ 3 liên tiếp đưa bộ đếm lên 3 và khóa tài khoản | EC19 – bộ đếm 2 → 3 (biên khóa) | `test@eshop.com` | `Sai12345!` | 2 × sai (`Sai12345!`) | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 3 (EC18, EC19); sau lần này `locked_until` ≈ thời điểm hiện tại + 30 giây | Mobile, API | AI |
| (MOB-DT-13) | Kiểm tra đăng nhập bị từ chối dù mật khẩu đúng khi đã sai 3 lần liên tiếp | EC14 – 0 giây sau khi khóa | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | – | Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20); A2 | Mobile, API | xem 3.2 |
| MOB-BV-05 | Kiểm tra đăng nhập bị từ chối khi mới qua 28 giây khóa | EC14/EC15 – 28 giây (UB-1 của EC14, sai số thao tác ~1 giây) | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | 28 giây | Từ chối dù mật khẩu đúng (tài khoản đang bị khóa), ở lại màn hình Đăng nhập; API trả 4xx, không có `token` (EC20) | Mobile, API | AI |
| MOB-BV-06 | Kiểm tra đăng nhập thành công khi đã qua 32 giây khóa | EC14/EC15 – 32 giây (LB+1 của EC15, sai số thao tác ~1 giây) | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | 32 giây | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17) | Mobile, API | AI |
| (MOB-DT-04) | Kiểm tra đăng nhập thành công khi đã hết 30 giây khóa | EC15 – 35 giây | `test@eshop.com` | `Test1234!` | 3 × sai (`Sai12345!`) | 35 giây | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); tiền điều kiện: 3 lần sai liên tiếp rồi chờ 35 giây | Mobile, API | xem 3.2 |
| (MOB-DT-01) | Kiểm tra đăng nhập thành công với email và mật khẩu đúng | EC7 – mật khẩu đúng độ dài | `test@eshop.com` | `Test1234!` | – | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17) | Mobile, API | xem 3.2 |
| MOB-BV-07 | Kiểm tra đăng nhập bị từ chối khi mật khẩu thiếu 1 ký tự cuối | EC7/EC8 – độ dài mật khẩu − 1 | `test@eshop.com` | `Test1234` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19) | Mobile, API | AI |
| MOB-BV-08 | Kiểm tra đăng nhập bị từ chối khi mật khẩu thừa 1 ký tự | EC7/EC8 – độ dài mật khẩu + 1 | `test@eshop.com` | `Test1234!!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 1 (EC18, EC19) | Mobile, API | AI |
| MOB-BV-09 | Kiểm tra đăng nhập bị từ chối khi email thiếu 1 ký tự cuối | EC1/EC4 – độ dài email − 1 | `test@eshop.co` | `Test1234!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 0 (EC18, EC19) | Mobile, API | AI |
| MOB-BV-10 | Kiểm tra đăng nhập bị từ chối khi email thừa 1 ký tự | EC1/EC4 – độ dài email + 1 | `test@eshop.comm` | `Test1234!` | – | – | Từ chối, hiện thông báo lỗi chung (không nêu trường sai), ở lại màn hình Đăng nhập; API trả 4xx; bộ đếm = 0 (EC18, EC19) | Mobile, API | AI |

Tổng: 10 test case BVA mới (MOB-BV-01…MOB-BV-10); 5 dòng có ID trong ngoặc là điểm biên đã được phủ bởi test case Minimum Set (mục 3.2), chỉ dẫn chiếu, không chạy lại.
<!-- END:T42 -->

## 5. Bước 5 – Kết quả thực thi

### 5.1 Môi trường và cách chạy

| Mục | Giá trị |
| --- | --- |
| Ngày chạy | 2026-10-21 |
| Người chạy | 23120031 (script tự động, kết quả được rà soát thủ công) |
| SUT | `eshop-sut-main` (trùng với `d1nhnguyen/eshop-sut`); `frontend-mobile/App.js:16` trỏ `API_URL` tới `http://10.0.2.2:3000/api` |
| Mobile | Expo Go SDK 54, Android Emulator **Pixel 2** (`eshop_api34_pixel2`, Android 14, 1080×1920); điều khiển qua `adb` (`scripts/mobile/adb_ui.py`) |
| API | `http://localhost:3000/api`, gọi bằng Python `urllib` |
| Dữ liệu | Backend được khởi động lại và app được mở lại trước mỗi test case |
| Script | `scripts/mobile/cases.py` (dữ liệu), `run_mobile.py` (P-MOBILE), `run_api.py` (P-API), `common.py` (kết luận chung cho 2 kênh), `report_tables.py` |
| Bằng chứng | `evidence/Mobile/web_results.json` (kênh Mobile), `api_results.json`; ảnh màn hình sau lần thử được đánh giá `evidence/Mobile/web/<ID>.png` |

Cách kết luận: "thành công" Pass khi rời màn hình Đăng nhập, thanh tiêu đề chào người dùng, mở được Hồ sơ (API: `200` + `token`) và bộ đếm về 0. "Từ chối" Pass khi ở lại màn hình Đăng nhập với thông báo lỗi (API 4xx, không có `token`), bộ đếm đúng giá trị mong đợi và tài khoản chỉ bị khóa khi đủ 3 lần sai. Test case có tiền điều kiện không dựng được (lần đăng nhập đúng trong chuỗi bị từ chối) là **Blocked**.

### 5.2 Phát hiện chính

- **Pixel 6 không mở được màn hình Đăng nhập** (thanh tiêu đề bị thanh trạng thái che – mục 1.1); mọi thực thi trên Mobile dùng Pixel 2.
- **Bộ đếm tăng 2 mỗi lần sai:** gọi `POST /api/login` sai một lần → `login_attempts` từ 0 lên 2 (đã kiểm tra bằng đúng một request, loại trừ khả năng script gửi hai lần); vì vậy tài khoản bị khóa ngay sau lần sai thứ 2.
- **Thời gian khóa 180 giây:** `locked_until` = thời điểm khóa + 180 giây; sau 32–35 giây vẫn bị từ chối. Các lần thử trong lúc khóa không gia hạn khóa.
- Thông báo trên Mobile luôn là "Đăng nhập thất bại. Vui lòng kiểm tra lại." – giống nhau cho sai email / sai mật khẩu / bị khóa (không lộ nguyên nhân). API trả "Invalid email or password" (401) hoặc "Tài khoản đã bị khóa. Vui lòng thử lại sau." (403).
- Email khác chữ hoa / thường hoặc có khoảng trắng đầu / cuối bị từ chối (A6).
- Đăng nhập đúng làm mới bộ đếm (MOB-DT-14 Pass); MOB-DT-05 Blocked vì tài khoản đã bị khóa từ lần sai thứ 2 nên lần đăng nhập đúng ở giữa chuỗi không thực hiện được.

### 5.3 Kết quả theo test case

Mỗi test case một dòng. Bảng sinh từ `evidence/Mobile/web_results.json` (cột Mobile) và `api_results.json`.

<!-- BEGIN:T53 -->
| TC | Mobile | Kết quả thực tế – Mobile | API | Kết quả thực tế – API | Bằng chứng | Bug |
| --- | --- | --- | --- | --- | --- | --- |
| MOB-DT-01 | Pass | Đăng nhập thành công, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; bộ đếm = 0 | Pass | HTTP 200 “Login successful”, có token; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-01.png) · `api_results.json` | – |
| MOB-DT-02 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-02.png) · `api_results.json` | MOB-B4 |
| MOB-DT-03 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-03.png) · `api_results.json` | MOB-B4 |
| MOB-DT-04 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:35:02 UTC | Fail | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:55:56 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-04.png) · `api_results.json` | MOB-B3 |
| MOB-DT-05 | Blocked | tiền điều kiện không dựng được: lần đăng nhập đúng trong chuỗi bị từ chối (“Đăng nhập thất bại. Vui lòng kiểm tra lại.”) | Blocked | tiền điều kiện không dựng được: lần đăng nhập đúng trong chuỗi bị từ chối (“Tài khoản đã bị khóa. Vui lòng thử lại sau.”) | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-05.png) · `api_results.json` | – |
| MOB-DT-06 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-06.png) · `api_results.json` | MOB-B2 |
| MOB-DT-07 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-07.png) · `api_results.json` | MOB-B2 |
| MOB-DT-08 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Pass | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-08.png) · `api_results.json` | – |
| MOB-DT-09 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Pass | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-09.png) · `api_results.json` | – |
| MOB-DT-10 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-10.png) · `api_results.json` | MOB-B2 |
| MOB-DT-11 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-11.png) · `api_results.json` | MOB-B2 |
| MOB-DT-12 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-12.png) · `api_results.json` | MOB-B2 |
| MOB-DT-13 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:45:04 UTC | Pass | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:56:40 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-13.png) · `api_results.json` | – |
| MOB-BV-01 | Pass | Đăng nhập thành công, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; bộ đếm = 0 | Pass | HTTP 200 “Login successful”, có token; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-01.png) · `api_results.json` | – |
| MOB-BV-02 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:48:33 UTC | Fail | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:56:42 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-02.png) · `api_results.json` | MOB-B2 |
| MOB-BV-03 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:50:15 UTC | Pass | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:56:43 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-03.png) · `api_results.json` | – |
| MOB-BV-04 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:52:50 UTC | Fail | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:56:44 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-04.png) · `api_results.json` | MOB-B2 |
| MOB-BV-05 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:54:33 UTC | Pass | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:56:44 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-05.png) · `api_results.json` | – |
| MOB-BV-06 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 4, bị khóa đến 17:56:48 UTC | Fail | HTTP 403 “Tài khoản đã bị khóa. Vui lòng thử lại sau.”; bộ đếm = 4, bị khóa đến 16:57:13 UTC | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-06.png) · `api_results.json` | MOB-B3 |
| MOB-BV-07 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-07.png) · `api_results.json` | MOB-B2 |
| MOB-BV-08 | Fail | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 2 | Fail | HTTP 401 “Invalid email or password”; bộ đếm = 2 | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-08.png) · `api_results.json` | MOB-B2 |
| MOB-BV-09 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Pass | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-09.png) · `api_results.json` | – |
| MOB-BV-10 | Pass | Ở lại màn hình Đăng nhập, hiện “Đăng nhập thất bại. Vui lòng kiểm tra lại.”; bộ đếm = 0 | Pass | HTTP 401 “Invalid email or password”; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-BV-10.png) · `api_results.json` | – |
| MOB-DT-14 | Pass | Đăng nhập thành công, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; bộ đếm = 0 | Pass | HTTP 200 “Login successful”, có token; bộ đếm = 0 | [ảnh Mobile](../evidence/Mobile/web/MOB-DT-14.png) · `api_results.json` | – |
<!-- END:T53 -->

### 5.4 Tổng hợp

<!-- BEGIN:T55 -->
| Kênh | Thiết kế | Đã chạy | Pass | Fail | Blocked | Không áp dụng |
| --- | --- | --- | --- | --- | --- | --- |
| Mobile | 24 | 24 | 10 | 13 | 1 | 0 |
| API | 24 | 24 | 10 | 13 | 1 | 0 |
| **Tổng lượt chạy** | | **48** | **20** | **26** | **2** | |

24 test case = 13 Minimum Set (mục 3.2) + 10 BVA (mục 4.2) + 1 bổ sung sau rà soát (mục 6.2). Gộp các kênh theo test case (Fail nếu Fail ở bất kỳ kênh nào, Blocked nếu còn kênh bị Blocked): 10 Pass, 13 Fail, 1 Blocked.
<!-- END:T55 -->

## 6. Bước 6 – AI gap analysis

> G1–G5: AI (Claude Code) tự phát hiện trong lúc làm các bước 1–5. Sinh viên rà soát và bổ sung các điểm tự phát hiện ở commit `[Mobile][Bn-review]`.

### 6.1 Những gì AI bỏ sót hoặc làm sai

| # | AI bỏ sót / làm sai | Loại | Nguyên nhân | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |
| G1 | Thiết kế không có biến "thiết bị / kích thước thanh trạng thái"; AI chỉ chuẩn bị một máy ảo (Pixel 6) và suýt kết luận cả feature bị chặn | Biến đầu vào thiếu (môi trường) | **Độ phức tạp feature**: hành vi giao diện phụ thuộc thiết bị; **do prompt**: đề không nêu thiết bị đích | Không chạm được "Đăng nhập" ở bước 1 | Tạo thêm máy Pixel 2, ghi bug MOB-B1, ghi điểm cần kiểm tra trên điện thoại thật |
| G2 | MOB-DT-05 (đăng nhập đúng xen giữa) phụ thuộc bộ đếm tăng đúng 1; khi bộ đếm tăng 2 thì tiền điều kiện không dựng được nên test case không trả lời được câu hỏi "có làm mới bộ đếm không" | Thiết kế test case | **Độ phức tạp feature**: hai quy tắc (đếm, làm mới) ràng buộc nhau; AI chọn chuỗi thao tác dài thay vì chuỗi ngắn nhất cô lập quy tắc | Kết quả API: lần đăng nhập đúng ở giữa bị 403 | Đánh Blocked; bổ sung MOB-DT-14 (sai → đúng → sai → đúng) |
| G3 | Bộ đếm tăng 2 lúc đầu có thể do script chạm nút hai lần | Nguy cơ kết luận sai | **Giới hạn công cụ AI**: tự động hoá giao diện qua `adb` không thấy được request mạng | AI kiểm tra lại bằng đúng một request API | Kết luận chỉ sau khi tái hiện bằng một request |
| G4 | Runner Mobile bản đầu: lỗi `KeyError` khi in kết quả Blocked; mở lại app ngay sau `force-stop` thất bại → 4 test case Blocked giả; phải dừng và chạy lại | Thực thi | **Giới hạn công cụ AI**: script chưa xử lý trạng thái không mong đợi của emulator / Expo Go | Ảnh chụp lúc Blocked là màn hình chính Android | Chỉ rõ package khi mở app, thử lại tối đa 3 lần, chờ trang chủ tải xong |
| G5 | Điểm biên thời gian 28 / 32 giây chỉ kiểm tra được biên theo đặc tả (30 giây); biên thực tế của SUT (180 giây) chỉ đo được qua `locked_until`, chưa chạy test case quanh 180 giây | Biên chưa phủ | **Giới hạn thời gian thực thi** (mỗi lần chờ 3 phút) | Khảo sát `locked_until` | Ghi trong bug MOB-B3; để mở |

### 6.2 Test case bổ sung

Kết quả thực thi nằm ở mục 5.3.

<!-- BEGIN:T62 -->
| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Email | Mật khẩu | Các lần thử trước (tiền điều kiện) | Chờ trước lần thử | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MOB-DT-14 | Kiểm tra đăng nhập đúng sau một lần sai làm mới bộ đếm | EC16, EC17 | `test@eshop.com` | `Test1234!` | 1 × sai (`Sai12345!`) → 1 × đúng (`Test1234!`) → 1 × sai (`Sai12345!`) | – | Đăng nhập thành công: rời màn hình Đăng nhập, thanh tiêu đề hiện “Chào, Test User”, mở được Hồ sơ; API trả `200` + `token`; bộ đếm = 0 (EC17); A3; nếu bộ đếm không về 0 sau lần đúng thì 2 lần sai cộng dồn sẽ khóa tài khoản | Mobile, API | AI |
<!-- END:T62 -->

### 6.3 Điểm còn mở (chưa xử lý)

- Kiểm tra lại MOB-B1 trên điện thoại thật có tai thỏ để xác nhận mức độ ảnh hưởng.
- A1 (Mobile kế thừa FR-02), A2 (khóa ngay sau lần sai thứ 3), A6 (email không phân biệt hoa / thường) cần TA xác nhận.

### 6.4 Nhận xét

- **Do prompt:** đề và prompt không nêu thiết bị đích nên AI không phân vùng theo thiết bị (G1).
- **Do giới hạn công cụ AI:** tự động hoá mobile qua `adb` kém ổn định hơn Web; AI phải tự xác minh bằng kênh API để tránh kết luận sai (G3, G4).
- **Do độ phức tạp feature:** các quy tắc đếm / khóa / làm mới phụ thuộc trạng thái và thời gian; một lỗi (bộ đếm tăng 2) che các test case khác (G2).

## 7. Bước 7 – Bug

Chi tiết từng bug: `bugs/Bug_Report.md`. Tiêu đề issue dùng `[FR-20]`. Cột GitHub Issue dẫn tới issue trên repo nhóm `d1nhnguyen/eshop-sut` (ảnh chụp trang issue ở cuối `bugs/Bug_Report.md`).

| Mã | Tiêu đề | Mức độ | Thành phần | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- | --- |
| MOB-B1 | Thanh tiêu đề app Mobile bị thanh trạng thái che trên máy có thanh trạng thái cao, không mở được màn hình Đăng nhập | Critical | Mobile | Quan sát bước 1 (Pixel 6) | [BUG-32](https://github.com/d1nhnguyen/eshop-sut/issues/32) |
| MOB-B2 | Mỗi lần đăng nhập sai bộ đếm tăng 2, tài khoản bị khóa ngay sau lần sai thứ 2 | Major | Backend (ảnh hưởng Mobile) | MOB-DT-06, MOB-DT-07, MOB-DT-10…MOB-DT-12, MOB-BV-02, MOB-BV-04, MOB-BV-07, MOB-BV-08 | [BUG-33](https://github.com/d1nhnguyen/eshop-sut/issues/33) |
| MOB-B3 | Tài khoản bị khóa 180 giây thay vì 30 giây | Major | Backend (ảnh hưởng Mobile) | MOB-DT-04, MOB-BV-06 | [BUG-34](https://github.com/d1nhnguyen/eshop-sut/issues/34) |
| MOB-B4 | Đăng nhập thất bại khi email khác chữ hoa / thường hoặc có khoảng trắng đầu / cuối | Minor | Backend (ảnh hưởng Mobile) | MOB-DT-02, MOB-DT-03 | [BUG-35](https://github.com/d1nhnguyen/eshop-sut/issues/35) |
| MOB-B5 | Màn hình Đăng nhập Mobile dùng nhãn tiếng Anh "Username" cho ô Email và nút "Sign In" | Minor | Mobile | Quan sát bước 1 | [BUG-36](https://github.com/d1nhnguyen/eshop-sut/issues/36) |

Tổng: 5 bug (1 Critical, 2 Major, 2 Minor). Ngoài phạm vi (đã ghi trong danh sách đối chiếu): nút đăng xuất ghi "Thoát" (FR-23).
