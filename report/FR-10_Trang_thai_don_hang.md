# FR-10 – Máy trạng thái đơn hàng · Domain Testing & Boundary Value Analysis

| Mục | Giá trị |
| --- | --- |
| Feature | FR-10 – Máy trạng thái đơn hàng (Pool B) |
| Kênh kiểm thử | Web Admin – tab Đơn hàng (http://localhost:5174) + Web khách hàng – hủy đơn ở trang Hồ sơ + API `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel` |
| Người thực hiện | 23120031 |
| Công cụ AI | Claude Code (VS Code extension) |
| Kỹ thuật | Domain Testing (S04 – bước 1–3), Boundary Value Analysis (S04 – bước 4) |

## 0. Đặc tả (trích nguyên văn README của SUT)

> ### FR-10: Trạng thái Đơn hàng (Order State Machine)
>
> Đơn hàng có **5 trạng thái** và phải tuân theo sơ đồ chuyển đổi sau:
>
> ```
>                  [Admin xác nhận]          [Admin giao hàng]      [Admin hoàn tất]
>   ┌──────────┐ ─────────────────► ┌───────────┐ ──────────────► ┌──────────┐ ──────────► ┌───────────┐
>   │ pending  │                    │ confirmed │                  │ shipping │             │ delivered │
>   └──────────┘                    └───────────┘                  └──────────┘             └───────────┘
>        │                               │
>        │ [User/Admin hủy]              │ [User/Admin hủy]
>        ▼                               ▼
>   ┌──────────┐                    ┌──────────┐
>   │ canceled │                    │ canceled │
>   └──────────┘                    └──────────┘
> ```
>
> **Ràng buộc trạng thái kết thúc (Final States):**
>
> - Trạng thái `delivered` và `canceled` là **trạng thái kết thúc** — không được phép chuyển sang bất kỳ trạng thái nào khác.
> - Khi đơn hàng đã ở trạng thái `shipping`, **User không được phép tự hủy** — chỉ Admin mới có thể thao tác.
> - Mọi chuyển đổi không hợp lệ phải trả về lỗi với thông báo phù hợp.

## 1. Bước 1 – Xác định biến Input / Output

### 1.1 Quan sát giao diện và API (hộp đen)

Tạo 5 đơn của `test@eshop.com` bằng `POST /api/checkout` rồi đưa mỗi đơn về một trạng thái bằng các chuyển đổi hợp lệ (`PUT /api/admin/orders/:id/status`). Ảnh: `evidence/FR-10/B1_admin_don_hang.png`, `B1_web_ho_so.png`.

| Trạng thái (nhãn hiển thị) | Nút trên Web Admin – tab "Đơn hàng" | Nút trên Web – trang Hồ sơ, "Lịch sử đơn hàng" |
| --- | --- | --- |
| `pending` ("Chờ xác nhận") | Xác nhận, Hủy | Hủy đơn |
| `confirmed` ("Đã xác nhận") | Giao hàng, Hủy | Hủy đơn |
| `shipping` ("Đang giao") | Hoàn thành | Hủy đơn |
| `delivered` ("Đã giao") | – | – |
| `canceled` ("Đã hủy") | Đánh dấu Đã giao | – |

API (`api_specification.md` 4.3, 4.6, 6.2): tạo đơn `POST /api/checkout` (`{"total_amount", "shipping_address"}` → `{"orderId"}`); Admin đổi trạng thái `PUT /api/admin/orders/:id/status` body `{"status": "<pending|confirmed|shipping|delivered|canceled>"}`; User hủy `PUT /api/orders/:id/cancel`; xem `GET /api/admin/orders`, `GET /api/orders/my-orders`.

### 1.2 Biến đầu vào

| ID | Biến | Kênh nhập | Kiểu / miền giá trị | Ràng buộc theo đặc tả | Nguồn |
| --- | --- | --- | --- | --- | --- |
| I1 | Trạng thái hiện tại của đơn | Tiền điều kiện (dữ liệu) | {`pending`, `confirmed`, `shipping`, `delivered`, `canceled`} | Xác định các chuyển đổi được phép | FR-10 |
| I2 | Trạng thái đích Admin yêu cầu | Web Admin: nút thao tác; API: trường `status` | chuỗi | Phải là chuyển đổi có trên sơ đồ; giá trị thuộc 5 trạng thái | FR-10, `api_specification.md` 6.2 |
| I3 | Yêu cầu hủy của User | Web: nút "Hủy đơn"; API: `PUT /api/orders/:id/cancel` | thao tác | Chỉ khi đơn `pending` / `confirmed`; không được khi `shipping` | FR-10 |
| I4 | Tác nhân | Tài khoản thực hiện | {Admin, User chủ đơn, User khác} | Admin xác nhận / giao / hoàn tất / hủy; User hủy | FR-10 (sơ đồ) |
| I5 | Mã đơn | Dòng được bấm; `:id` trên URL | số nguyên | Phải là đơn đang tồn tại | FR-10 |

Vì trạng thái có thứ tự `pending (0) < confirmed (1) < shipping (2) < delivered (3)` (`canceled` là nhánh riêng), chuyển đổi tiến hợp lệ là **khoảng cách d = thứ tự đích − thứ tự hiện tại = +1**; đại lượng d dùng cho phân tích biên ở bước 4.

### 1.3 Biến đầu ra

| ID | Biến | Giá trị có thể có | Nguồn |
| --- | --- | --- | --- |
| O1 | Trạng thái đơn sau thao tác | trạng thái mới (thành công) / giữ nguyên (bị từ chối) | FR-10 |
| O2 | Phản hồi | Thành công; lỗi kèm thông báo phù hợp (4xx); không tìm thấy (404) | FR-10 ("Mọi chuyển đổi không hợp lệ phải trả về lỗi với thông báo phù hợp"); A5 |
| O3 | Các đơn khác | Giữ nguyên / bị thay đổi | A5 |
| O4 | Thao tác giao diện hiển thị cho từng trạng thái | Tập nút trên Web Admin / trang Hồ sơ | A7 |

### 1.4 Giả định cho những chỗ đặc tả chưa rõ

| ID | Giả định | Căn cứ |
| --- | --- | --- |
| A1 | Admin **không** được chuyển `shipping → canceled`; câu "khi shipping … chỉ Admin mới có thể thao tác" hiểu là Admin tiếp tục chuyển `shipping → delivered` | Sơ đồ không có cạnh `shipping → canceled`; "mọi chuyển đổi không hợp lệ phải trả về lỗi". Cần TA xác nhận |
| A2 | Chuyển sang chính trạng thái hiện tại (vd `pending → pending`) không hợp lệ | Không có trên sơ đồ |
| A3 | Bỏ bước (`pending → shipping`, `pending → delivered`, `confirmed → delivered`) và lùi trạng thái không hợp lệ | Không có trên sơ đồ |
| A4 | `status` phải đúng một trong 5 chuỗi chữ thường; giá trị khác (sai hoa / thường, có khoảng trắng, rỗng, thiếu trường) không hợp lệ | `api_specification.md` 6.2 liệt kê đúng 5 giá trị |
| A5 | Bị từ chối: trả 4xx kèm thông báo, trạng thái đơn và các đơn khác giữ nguyên; đơn không tồn tại: 404 | Quy ước REST; FR-10 |
| A6 | User chỉ hủy được đơn của chính mình | FR-11 ("chỉ xem được đơn hàng của chính mình") |
| A7 | Giao diện chỉ hiển thị thao tác tương ứng chuyển đổi hợp lệ của trạng thái hiện tại | Giao diện là một kênh nhập của miền I2 / I3 |
| A8 | Kênh API dùng token đúng vai trò (Admin / User) | Kiểm soát truy cập thuộc FR-12 (ngoài phạm vi) |

### 1.5 Ngoài phạm vi

- Gọi API Admin bằng token User hoặc không có token (FR-12); hủy đơn trên Mobile (Pool D – FR-20); hiển thị lịch sử đơn (FR-11), tính doanh thu (FR-13).

## 2. Bước 2 – Lớp tương đương (Complete Set of Partitions)

### 2.1 Cách áp dụng guideline cho từng biến

| Biến | Điều kiện trong đặc tả | Guideline [S04] | Lớp tạo ra |
| --- | --- | --- | --- |
| I1 × I2 (Admin đổi trạng thái) | Sơ đồ có 5 cạnh: `pending→confirmed`, `confirmed→shipping`, `shipping→delivered`, `pending→canceled`, `confirmed→canceled` | Tập giá trị được xử lý khác nhau (mỗi cạnh là một thao tác riêng: Xác nhận / Giao hàng / Hoàn thành / Hủy) → mỗi cạnh 1 lớp valid | 5 lớp valid |
| | "`delivered` và `canceled` là trạng thái kết thúc"; "mọi chuyển đổi không hợp lệ phải trả về lỗi" | "Phải là" cạnh trên sơ đồ → lớp invalid; tách lớp (G5) theo kiểu sai vì mỗi kiểu có thể bị một điều kiện khác bỏ sót: đi ra từ `delivered`, đi ra từ `canceled` (giao diện còn hiện nút cho đơn đã hủy), bỏ bước (d ≥ 2), lùi (d ≤ −1), giữ nguyên (d = 0), `shipping→canceled` (A1) | 6 lớp invalid |
| I3 (User hủy) | "User/Admin hủy" từ `pending`, `confirmed`; "khi `shipping` User không được tự hủy" | "Phải là" đơn `pending` / `confirmed`; tách lớp (G5) theo trạng thái hiện tại vì mỗi trạng thái có thể được kiểm tra riêng | 2 lớp valid; `shipping`, `delivered`, `canceled` (3 lớp invalid) |
| I4 (Tác nhân) | User hủy đơn của mình (A6) | "Phải là" chủ đơn | User khác hủy (invalid) |
| I2 giá trị `status` | 5 giá trị (`api_specification.md` 6.2) | "Phải là" một trong tập → 1 valid + 1 invalid (ngoài tập); tách lớp (G5): sai hoa / thường, rỗng, thiếu trường (A4) | 1 valid, 4 invalid |
| I5 Mã đơn | Đơn đang tồn tại | "Phải là" → tồn tại / không tồn tại; tách lớp (G5): id không phải số | 1 valid, 2 invalid |
| Đầu ra O1–O4 | thành công / từ chối / không tìm thấy / thao tác giao diện | Phân vùng đầu ra như ví dụ [UC] | 5 lớp đầu ra |

### 2.2 Complete Set of Partitions

| EC | Biến | Phân vùng | Ví dụ đại diện | Valid / Invalid |
| --- | --- | --- | --- | --- |
| EC1 | I1 × I2 Admin | `pending → confirmed` (Xác nhận) | đơn `pending`, `status = confirmed` | Valid |
| EC2 | I1 × I2 Admin | `confirmed → shipping` (Giao hàng) | | Valid |
| EC3 | I1 × I2 Admin | `shipping → delivered` (Hoàn thành) | | Valid |
| EC4 | I1 × I2 Admin | `pending → canceled` (Hủy) | | Valid |
| EC5 | I1 × I2 Admin | `confirmed → canceled` (Hủy) | | Valid |
| EC6 | I3 User | Hủy đơn `pending` của mình | | Valid |
| EC7 | I3 User | Hủy đơn `confirmed` của mình | | Valid |
| EC8 | I1 × I2 Admin | Đi ra từ `delivered` (trạng thái kết thúc) | `delivered → canceled` | Invalid |
| EC9 | I1 × I2 Admin | Đi ra từ `canceled` (trạng thái kết thúc) | `canceled → delivered` | Invalid |
| EC10 | I1 × I2 Admin | Bỏ bước tiến (d ≥ 2) (A3) | `pending → shipping` | Invalid |
| EC11 | I1 × I2 Admin | Lùi trạng thái (d ≤ −1) (A3) | `shipping → confirmed` | Invalid |
| EC12 | I1 × I2 Admin | Giữ nguyên trạng thái (d = 0) (A2) | `confirmed → confirmed` | Invalid |
| EC13 | I1 × I2 Admin | `shipping → canceled` (A1) | | Invalid |
| EC14 | I3 User | Hủy đơn `shipping` | | Invalid |
| EC15 | I3 User | Hủy đơn `delivered` | | Invalid |
| EC16 | I3 User | Hủy đơn `canceled` | | Invalid |
| EC17 | I4 | User hủy đơn của người khác (A6) | | Invalid |
| EC18 | I2 `status` | Một trong 5 giá trị chữ thường | `confirmed` | Valid |
| EC19 | I2 `status` | Ngoài tập (A4) | `abc` | Invalid |
| EC20 | I2 `status` | Sai chữ hoa / thường (A4) | `Confirmed` | Invalid |
| EC21 | I2 `status` | Rỗng (A4) | `` | Invalid |
| EC22 | I2 `status` | Thiếu trường `status` (A4) | `{}` | Invalid |
| EC23 | I5 Mã đơn | Đơn đang tồn tại | id `1` | Valid |
| EC24 | I5 Mã đơn | Không tồn tại | `9999` | Invalid |
| EC25 | I5 Mã đơn | Không phải số | `abc` | Invalid |
| EC26 | O1, O3 | Chuyển thành công: đơn có trạng thái mới, các đơn khác giữ nguyên | | Output |
| EC27 | O1, O2 | Từ chối chuyển đổi không hợp lệ: 4xx + thông báo, trạng thái giữ nguyên | | Output |
| EC28 | O1, O2 | Từ chối giá trị `status` không hợp lệ: 4xx, trạng thái giữ nguyên | | Output |
| EC29 | O2 | Không tìm thấy đơn: 404 | | Output |
| EC30 | O4 | Giao diện chỉ hiện thao tác của chuyển đổi hợp lệ cho trạng thái hiện tại (A7) | | Output |

Tổng: 25 lớp đầu vào (9 valid, 16 invalid) và 5 lớp đầu ra.

## 3. Bước 3 – Test case Domain Testing

### 3.1 Thủ tục thực hiện

Mọi test case dùng chung thủ tục, chỉ dữ liệu thay đổi → dạng **data matrix** [DR]. ID có tiền tố `FR10-`. Trong bảng: `(bỏ trống / không gửi)` là không gửi trường `status`; `(rỗng)` là chuỗi rỗng; `␣` là một dấu cách.

**Tiền điều kiện chung – dựng trước mỗi test case (self-standing, self-cleaning)**

1. Khởi động lại backend (dữ liệu seed, chưa có đơn).
2. Đăng ký User B `fr10.userb@example.com / Abcdef1@` (`POST /api/register`).
3. Tạo đơn bằng `POST /api/checkout` và đưa về trạng thái bằng các chuyển đổi hợp lệ của Admin:

| Đơn | Chủ đơn | Trạng thái | Cách dựng |
| --- | --- | --- | --- |
| #1 | `test@eshop.com` | `pending` | tạo mới |
| #2 | `test@eshop.com` | `confirmed` | `pending → confirmed` |
| #3 | `test@eshop.com` | `shipping` | `pending → confirmed → shipping` |
| #4 | `test@eshop.com` | `delivered` | `pending → confirmed → shipping → delivered` |
| #5 | `test@eshop.com` | `canceled` | `pending → canceled` |
| #6 | `test@eshop.com` | `pending` | tạo mới |
| #7 | User B | `pending` | tạo mới |

4. Đọc `GET /api/admin/orders`, kiểm tra đúng bảng trên; nếu không dựng được, test case **Blocked**.

**P-WEB-ADMIN** – Web Admin `http://localhost:5174` (đăng nhập `admin@eshop.com`) → tab "Đơn hàng" → ở dòng đơn theo cột dữ liệu bấm nút ứng với trạng thái đích (Xác nhận → `confirmed`, Giao hàng → `shipping`, Hoàn thành → `delivered`, Hủy → `canceled`, Đánh dấu Đã giao → `delivered`), chấp nhận hộp thoại nếu có.

**P-WEB-USER** – Web `http://localhost:5173` đăng nhập `test@eshop.com / Test1234!` → trang Hồ sơ → "Lịch sử đơn hàng" → bấm "Hủy đơn" ở đơn theo cột dữ liệu, chấp nhận hộp thoại nếu có.

**P-API** – Admin: `PUT /api/admin/orders/<đơn>/status` body `{"status": <giá trị>}` với token Admin. User: `PUT /api/orders/<đơn>/cancel` với token của tác nhân.

**Kiểm chứng (mọi kênh):** so `GET /api/admin/orders` trước / sau – trạng thái đơn được thao tác và các đơn khác; với kênh API kiểm tra thêm mã HTTP và thông báo.

Chuyển đổi không có nút trên giao diện chỉ chạy P-API; việc giao diện không có nút được kiểm tra riêng ở FR10-DT-26, FR10-DT-27.

### 3.2 Minimum Set of Test Cases

Dữ liệu và kết quả mong đợi được sinh từ `scripts/fr10/cases.py` (cùng nguồn với script thực thi) bằng `scripts/fr10/report_tables.py`.

<!-- BEGIN:T32 -->
**Test case valid** – mỗi test case phủ nhiều lớp valid nhất có thể:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Tác nhân | Thao tác | Đơn | Trạng thái hiện tại | Giá trị `status` | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR10-DT-01 | Kiểm tra Admin xác nhận đơn đang chờ xác nhận thành công | EC1, EC18, EC23, EC26 | Admin | Đổi trạng thái | #1 | `pending` | `confirmed` | Đơn #1 chuyển `pending` → `confirmed`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-02 | Kiểm tra Admin chuyển đơn đã xác nhận sang đang giao thành công | EC2, EC18, EC23, EC26 | Admin | Đổi trạng thái | #2 | `confirmed` | `shipping` | Đơn #2 chuyển `confirmed` → `shipping`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-03 | Kiểm tra Admin hoàn tất đơn đang giao thành công | EC3, EC18, EC23, EC26 | Admin | Đổi trạng thái | #3 | `shipping` | `delivered` | Đơn #3 chuyển `shipping` → `delivered`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-04 | Kiểm tra Admin hủy đơn đang chờ xác nhận thành công | EC4, EC18, EC23, EC26 | Admin | Đổi trạng thái | #1 | `pending` | `canceled` | Đơn #1 chuyển `pending` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-05 | Kiểm tra Admin hủy đơn đã xác nhận thành công | EC5, EC18, EC23, EC26 | Admin | Đổi trạng thái | #2 | `confirmed` | `canceled` | Đơn #2 chuyển `confirmed` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-06 | Kiểm tra User hủy đơn đang chờ xác nhận của mình thành công | EC6, EC23, EC26 | User chủ đơn | Hủy đơn | #1 | `pending` | – | Đơn #1 chuyển `pending` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-07 | Kiểm tra User hủy đơn đã xác nhận của mình thành công | EC7, EC23, EC26 | User chủ đơn | Hủy đơn | #2 | `confirmed` | – | Đơn #2 chuyển `confirmed` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | AI |
| FR10-DT-26 | Kiểm tra Web Admin chỉ hiện thao tác hợp lệ cho từng trạng thái đơn | EC30 (Admin) | Admin | Xem tab Đơn hàng | #1–#5 | – | – | Web Admin hiện: Chờ xác nhận – Xác nhận, Hủy; Đã xác nhận – Giao hàng, Hủy; Đang giao – Hoàn thành; Đã giao, Đã hủy – không có nút (EC30) | Web | AI |
| FR10-DT-27 | Kiểm tra trang Hồ sơ chỉ hiện nút Hủy đơn cho đơn được phép hủy | EC30 (User) | User chủ đơn | Xem Lịch sử đơn hàng | #1–#5 | – | – | Trang Hồ sơ hiện nút "Hủy đơn" chỉ ở đơn Chờ xác nhận, Đã xác nhận; không có ở Đang giao, Đã giao, Đã hủy (EC30) | Web | AI |

**Test case invalid** – mỗi test case phủ đúng một lớp invalid, các biến còn lại hợp lệ:

| ID | Tên test case (Action + Function + Condition) | Phân vùng phủ | Tác nhân | Thao tác | Đơn | Trạng thái hiện tại | Giá trị `status` | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR10-DT-08 | Kiểm tra Admin chuyển đơn đã giao sang đã hủy bị từ chối | EC8, EC27 | Admin | Đổi trạng thái | #4 | `delivered` | `canceled` | Từ chối, báo chuyển đổi không hợp lệ; đơn #4 giữ `delivered`; các đơn khác giữ nguyên; API trả 4xx (EC27) | API | AI |
| FR10-DT-09 | Kiểm tra Admin chuyển đơn đã hủy sang đã giao bị từ chối | EC9, EC27 | Admin | Đổi trạng thái | #5 | `canceled` | `delivered` | Từ chối, báo chuyển đổi không hợp lệ; đơn #5 giữ `canceled`; các đơn khác giữ nguyên; API trả 4xx (EC27); trên Web Admin bấm nút "Đánh dấu Đã giao" có sẵn ở đơn đã hủy | Web, API | AI |
| FR10-DT-10 | Kiểm tra Admin chuyển đơn chờ xác nhận thẳng sang đang giao bị từ chối | EC10, EC27 | Admin | Đổi trạng thái | #1 | `pending` | `shipping` | Từ chối, báo chuyển đổi không hợp lệ; đơn #1 giữ `pending`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| FR10-DT-11 | Kiểm tra Admin chuyển đơn đang giao lùi về đã xác nhận bị từ chối | EC11, EC27 | Admin | Đổi trạng thái | #3 | `shipping` | `confirmed` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| FR10-DT-12 | Kiểm tra Admin chuyển đơn đã xác nhận sang chính trạng thái đã xác nhận bị từ chối | EC12, EC27 | Admin | Đổi trạng thái | #2 | `confirmed` | `confirmed` | Từ chối, báo chuyển đổi không hợp lệ; đơn #2 giữ `confirmed`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | AI |
| FR10-DT-13 | Kiểm tra Admin hủy đơn đang giao bị từ chối | EC13, EC27 | Admin | Đổi trạng thái | #3 | `shipping` | `canceled` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A1 | API | AI |
| FR10-DT-14 | Kiểm tra User hủy đơn đang giao bị từ chối | EC14, EC27 | User chủ đơn | Hủy đơn | #3 | `shipping` | – | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); trên Web bấm nút "Hủy đơn" có sẵn ở đơn đang giao | Web, API | AI |
| FR10-DT-15 | Kiểm tra User hủy đơn đã giao bị từ chối | EC15, EC27 | User chủ đơn | Hủy đơn | #4 | `delivered` | – | Từ chối, báo chuyển đổi không hợp lệ; đơn #4 giữ `delivered`; các đơn khác giữ nguyên; API trả 4xx (EC27) | API | AI |
| FR10-DT-16 | Kiểm tra User hủy đơn đã hủy bị từ chối | EC16, EC27 | User chủ đơn | Hủy đơn | #5 | `canceled` | – | Từ chối, báo chuyển đổi không hợp lệ; đơn #5 giữ `canceled`; các đơn khác giữ nguyên; API trả 4xx (EC27) | API | AI |
| FR10-DT-17 | Kiểm tra User hủy đơn của người dùng khác bị từ chối | EC17, EC27 | User khác (test@eshop.com hủy đơn của User B) | Hủy đơn | #7 | `pending` | – | Từ chối, báo chuyển đổi không hợp lệ; đơn #7 giữ `pending`; các đơn khác giữ nguyên; API trả 4xx (EC27); A6; đơn #7 của User B giữ `pending` | API | AI |
| FR10-DT-18 | Kiểm tra Admin đổi trạng thái bị từ chối khi status ngoài tập | EC19, EC28 | Admin | Đổi trạng thái | #1 | `pending` | `abc` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28) | API | AI |
| FR10-DT-19 | Kiểm tra Admin đổi trạng thái bị từ chối khi status sai chữ hoa / thường | EC20, EC28 | Admin | Đổi trạng thái | #1 | `pending` | `Confirmed` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28) | API | AI |
| FR10-DT-20 | Kiểm tra Admin đổi trạng thái bị từ chối khi status rỗng | EC21, EC28 | Admin | Đổi trạng thái | #1 | `pending` | (rỗng) | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28) | API | AI |
| FR10-DT-21 | Kiểm tra Admin đổi trạng thái bị từ chối khi không gửi status | EC22, EC28 | Admin | Đổi trạng thái | #1 | `pending` | (bỏ trống / không gửi) | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28) | API | AI |
| FR10-DT-22 | Kiểm tra Admin đổi trạng thái đơn không tồn tại bị từ chối | EC24 (Admin), EC29 | Admin | Đổi trạng thái | #9999 | – | `confirmed` | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| FR10-DT-23 | Kiểm tra Admin đổi trạng thái bị từ chối khi mã đơn không phải số | EC25 (Admin), EC29 | Admin | Đổi trạng thái | `abc` | – | `confirmed` | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| FR10-DT-24 | Kiểm tra User hủy đơn không tồn tại bị từ chối | EC24 (User), EC29 | User chủ đơn | Hủy đơn | #9999 | – | – | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| FR10-DT-25 | Kiểm tra User hủy đơn bị từ chối khi mã đơn không phải số | EC25 (User), EC29 | User chủ đơn | Hủy đơn | `abc` | – | – | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
<!-- END:T32 -->

### 3.3 Bảng phủ phân vùng

<!-- BEGIN:T33 -->
| EC | Test case phủ | | EC | Test case phủ |
| --- | --- | --- | --- | --- |
| EC1 | FR10-DT-01 | | EC16 | FR10-DT-16 |
| EC2 | FR10-DT-02 | | EC17 | FR10-DT-17 |
| EC3 | FR10-DT-03 | | EC18 | FR10-DT-01…FR10-DT-05 |
| EC4 | FR10-DT-04 | | EC19 | FR10-DT-18 |
| EC5 | FR10-DT-05 | | EC20 | FR10-DT-19 |
| EC6 | FR10-DT-06 | | EC21 | FR10-DT-20 |
| EC7 | FR10-DT-07 | | EC22 | FR10-DT-21 |
| EC8 | FR10-DT-08 | | EC23 | FR10-DT-01…FR10-DT-07 |
| EC9 | FR10-DT-09 | | EC24 | FR10-DT-22, FR10-DT-24 |
| EC10 | FR10-DT-10 | | EC25 | FR10-DT-23, FR10-DT-25 |
| EC11 | FR10-DT-11 | | EC26 | FR10-DT-01…FR10-DT-07 |
| EC12 | FR10-DT-12 | | EC27 | FR10-DT-08…FR10-DT-17 |
| EC13 | FR10-DT-13 | | EC28 | FR10-DT-18…FR10-DT-21 |
| EC14 | FR10-DT-14 | | EC29 | FR10-DT-22…FR10-DT-25 |
| EC15 | FR10-DT-15 | | EC30 | FR10-DT-26, FR10-DT-27 |

30 / 30 lớp được phủ bởi 27 test case Minimum Set (9 valid, 18 invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp invalid có test case riêng.
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
