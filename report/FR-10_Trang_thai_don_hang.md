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

Trạng thái `pending (0) < confirmed (1) < shipping (2) < delivered (3)` có thứ tự, nên BVA áp dụng cho khoảng cách **d = thứ tự đích − thứ tự hiện tại**: chuyển tiến hợp lệ chỉ khi d = +1 (vừa là LB vừa là UB), nên các điểm biên là d = 0 (UB−1), d = +1, d = +2 (UB+1), cùng d âm (lùi) và giá trị lớn nhất. Ngoài ra xét vùng "được hủy" `{pending, confirmed}` (UB = `confirmed`, UB+1 = `shipping`), độ dài chuỗi `status` quanh giá trị hợp lệ `confirmed`, và mã đơn của bộ dữ liệu (#1–#7).

| Biến | Phân vùng | LB | UB | Bước nhảy | Điểm kiểm tra |
| --- | --- | --- | --- | --- | --- |
| d từ `pending` | EC12 (d = 0) / EC1 (d = +1) / EC10 (d ≥ 2) | +1 | +1 | 1 trạng thái | 0, +1, +2, +3 |
| d từ `confirmed` | EC11 (d < 0) / EC12 / EC2 / EC10 | +1 | +1 | 1 trạng thái | −1, 0, +1, +2 |
| d từ `shipping` | EC11 / EC12 / EC3 | +1 | +1 | 1 trạng thái | −2, −1, 0, +1 |
| d từ `delivered` (kết thúc) | EC8 | – | – | 1 trạng thái | −1, 0 |
| `canceled` (kết thúc) | EC9 | – | – | – | → `canceled`, → `pending` |
| Vùng được hủy (Admin, User) | EC4/EC5, EC6/EC7 (valid) / EC13, EC14 (invalid) | `pending` | `confirmed` | 1 trạng thái | `confirmed` (UB), `shipping` (UB+1) |
| Chuỗi `status` | EC18 / EC19 | `confirmed` (9 ký tự) | `confirmed` | 1 ký tự | thiếu 1 ký tự, thừa 1 ký tự, thừa 1 khoảng trắng đầu / cuối |
| Mã đơn Admin | EC24 / EC23 (#1–#7) | 1 | 7 | 1 | 0, 1, 7, 8 |
| Mã đơn User (đơn của mình #1–#6) | EC24 / EC23 | 1 | 6 | 1 | 0, 6, 8 |

### 4.2 Boundary Value Test Cases

Thủ tục: mục 3.1 (chỉ chạy P-API – giao diện không có thao tác cho các điểm biên này). Dòng có ID trong ngoặc là điểm biên đã có trong Minimum Set, chỉ dẫn chiếu.

<!-- BEGIN:T42 -->
| ID | Tên test case (Action + Function + Condition) | Partition tested | Tác nhân | Thao tác | Đơn | Trạng thái hiện tại | Giá trị `status` | Kết quả mong đợi | Kênh | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR10-BV-01 | Kiểm tra Admin chuyển đơn chờ xác nhận sang chính nó bị từ chối | `pending`: d = 0 (UB-1) | Admin | Đổi trạng thái | #1 | `pending` | `pending` | Từ chối, báo chuyển đổi không hợp lệ; đơn #1 giữ `pending`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | AI |
| (FR10-DT-01) | Kiểm tra Admin xác nhận đơn đang chờ xác nhận thành công | `pending`: d = +1 (UB – cạnh hợp lệ) | Admin | Đổi trạng thái | #1 | `pending` | `confirmed` | Đơn #1 chuyển `pending` → `confirmed`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| (FR10-DT-10) | Kiểm tra Admin chuyển đơn chờ xác nhận thẳng sang đang giao bị từ chối | `pending`: d = +2 (UB+1) | Admin | Đổi trạng thái | #1 | `pending` | `shipping` | Từ chối, báo chuyển đổi không hợp lệ; đơn #1 giữ `pending`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | xem 3.2 |
| FR10-BV-02 | Kiểm tra Admin chuyển đơn chờ xác nhận thẳng sang đã giao bị từ chối | `pending`: d = +3 (lớn nhất) | Admin | Đổi trạng thái | #1 | `pending` | `delivered` | Từ chối, báo chuyển đổi không hợp lệ; đơn #1 giữ `pending`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| FR10-BV-03 | Kiểm tra Admin chuyển đơn đã xác nhận lùi về chờ xác nhận bị từ chối | `confirmed`: d = −1 | Admin | Đổi trạng thái | #2 | `confirmed` | `pending` | Từ chối, báo chuyển đổi không hợp lệ; đơn #2 giữ `confirmed`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| (FR10-DT-12) | Kiểm tra Admin chuyển đơn đã xác nhận sang chính trạng thái đã xác nhận bị từ chối | `confirmed`: d = 0 (UB-1) | Admin | Đổi trạng thái | #2 | `confirmed` | `confirmed` | Từ chối, báo chuyển đổi không hợp lệ; đơn #2 giữ `confirmed`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | xem 3.2 |
| (FR10-DT-02) | Kiểm tra Admin chuyển đơn đã xác nhận sang đang giao thành công | `confirmed`: d = +1 (UB) | Admin | Đổi trạng thái | #2 | `confirmed` | `shipping` | Đơn #2 chuyển `confirmed` → `shipping`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| FR10-BV-04 | Kiểm tra Admin chuyển đơn đã xác nhận thẳng sang đã giao bị từ chối | `confirmed`: d = +2 (UB+1) | Admin | Đổi trạng thái | #2 | `confirmed` | `delivered` | Từ chối, báo chuyển đổi không hợp lệ; đơn #2 giữ `confirmed`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| FR10-BV-05 | Kiểm tra Admin chuyển đơn đang giao lùi về chờ xác nhận bị từ chối | `shipping`: d = −2 | Admin | Đổi trạng thái | #3 | `shipping` | `pending` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | AI |
| (FR10-DT-11) | Kiểm tra Admin chuyển đơn đang giao lùi về đã xác nhận bị từ chối | `shipping`: d = −1 (UB-2) | Admin | Đổi trạng thái | #3 | `shipping` | `confirmed` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A3 | API | xem 3.2 |
| FR10-BV-06 | Kiểm tra Admin chuyển đơn đang giao sang chính nó bị từ chối | `shipping`: d = 0 | Admin | Đổi trạng thái | #3 | `shipping` | `shipping` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | AI |
| (FR10-DT-03) | Kiểm tra Admin hoàn tất đơn đang giao thành công | `shipping`: d = +1 (UB) | Admin | Đổi trạng thái | #3 | `shipping` | `delivered` | Đơn #3 chuyển `shipping` → `delivered`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| FR10-BV-07 | Kiểm tra Admin chuyển đơn đã giao lùi về đang giao bị từ chối | `delivered` (kết thúc): d = −1 | Admin | Đổi trạng thái | #4 | `delivered` | `shipping` | Từ chối, báo chuyển đổi không hợp lệ; đơn #4 giữ `delivered`; các đơn khác giữ nguyên; API trả 4xx (EC27) | API | AI |
| FR10-BV-08 | Kiểm tra Admin chuyển đơn đã giao sang chính nó bị từ chối | `delivered` (kết thúc): d = 0 | Admin | Đổi trạng thái | #4 | `delivered` | `delivered` | Từ chối, báo chuyển đổi không hợp lệ; đơn #4 giữ `delivered`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | AI |
| (FR10-DT-05) | Kiểm tra Admin hủy đơn đã xác nhận thành công | Vùng được hủy {pending, confirmed} – Admin hủy `confirmed` (UB) | Admin | Đổi trạng thái | #2 | `confirmed` | `canceled` | Đơn #2 chuyển `confirmed` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| (FR10-DT-13) | Kiểm tra Admin hủy đơn đang giao bị từ chối | Admin hủy `shipping` (UB+1, A1) | Admin | Đổi trạng thái | #3 | `shipping` | `canceled` | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); A1 | API | xem 3.2 |
| (FR10-DT-07) | Kiểm tra User hủy đơn đã xác nhận của mình thành công | User hủy `confirmed` (UB) | User chủ đơn | Hủy đơn | #2 | `confirmed` | – | Đơn #2 chuyển `confirmed` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| (FR10-DT-14) | Kiểm tra User hủy đơn đang giao bị từ chối | User hủy `shipping` (UB+1) | User chủ đơn | Hủy đơn | #3 | `shipping` | – | Từ chối, báo chuyển đổi không hợp lệ; đơn #3 giữ `shipping`; các đơn khác giữ nguyên; API trả 4xx (EC27); trên Web bấm nút "Hủy đơn" có sẵn ở đơn đang giao | Web, API | xem 3.2 |
| FR10-BV-09 | Kiểm tra Admin hủy lại đơn đã hủy bị từ chối | `canceled` (kết thúc) → `canceled` | Admin | Đổi trạng thái | #5 | `canceled` | `canceled` | Từ chối, báo chuyển đổi không hợp lệ; đơn #5 giữ `canceled`; các đơn khác giữ nguyên; API trả 4xx (EC27); A2 | API | AI |
| FR10-BV-10 | Kiểm tra Admin khôi phục đơn đã hủy về chờ xác nhận bị từ chối | `canceled` (kết thúc) → `pending` | Admin | Đổi trạng thái | #5 | `canceled` | `pending` | Từ chối, báo chuyển đổi không hợp lệ; đơn #5 giữ `canceled`; các đơn khác giữ nguyên; API trả 4xx (EC27) | API | AI |
| FR10-BV-11 | Kiểm tra Admin đổi trạng thái bị từ chối khi status thừa 1 khoảng trắng đầu | `confirmed` + 1 ký tự ở đầu | Admin | Đổi trạng thái | #1 | `pending` | `␣confirmed` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28); A4 | API | AI |
| FR10-BV-12 | Kiểm tra Admin đổi trạng thái bị từ chối khi status thừa 1 khoảng trắng cuối | `confirmed` + 1 ký tự ở cuối | Admin | Đổi trạng thái | #1 | `pending` | `confirmed␣` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28); A4 | API | AI |
| FR10-BV-13 | Kiểm tra Admin đổi trạng thái bị từ chối khi status thiếu 1 ký tự | độ dài `confirmed` − 1 | Admin | Đổi trạng thái | #1 | `pending` | `confirme` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28); A4 | API | AI |
| FR10-BV-14 | Kiểm tra Admin đổi trạng thái bị từ chối khi status thừa 1 ký tự | độ dài `confirmed` + 1 | Admin | Đổi trạng thái | #1 | `pending` | `confirmedd` | Từ chối, báo trạng thái không hợp lệ; đơn #1 giữ `pending`; API trả 4xx (EC28); A4 | API | AI |
| FR10-BV-15 | Kiểm tra Admin đổi trạng thái đơn mã 0 bị từ chối | mã đơn 0 (LB-1) | Admin | Đổi trạng thái | #0 | – | `confirmed` | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| (FR10-DT-01) | Kiểm tra Admin xác nhận đơn đang chờ xác nhận thành công | mã đơn 1 (LB) | Admin | Đổi trạng thái | #1 | `pending` | `confirmed` | Đơn #1 chuyển `pending` → `confirmed`; các đơn khác giữ nguyên; API trả 2xx (EC26) | Web, API | xem 3.2 |
| FR10-BV-16 | Kiểm tra Admin xác nhận đơn có mã lớn nhất đang tồn tại thành công | mã đơn 7 (UB) | Admin | Đổi trạng thái | #7 | `pending` | `confirmed` | Đơn #7 chuyển `pending` → `confirmed`; các đơn khác giữ nguyên; API trả 2xx (EC26) | API | AI |
| FR10-BV-17 | Kiểm tra Admin đổi trạng thái đơn mã 8 bị từ chối | mã đơn 8 (UB+1) | Admin | Đổi trạng thái | #8 | – | `confirmed` | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| FR10-BV-18 | Kiểm tra User hủy đơn mã 0 bị từ chối | mã đơn 0 (LB-1) | User chủ đơn | Hủy đơn | #0 | – | – | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |
| FR10-BV-19 | Kiểm tra User hủy đơn có mã lớn nhất của mình thành công | mã đơn 6 (UB của User) | User chủ đơn | Hủy đơn | #6 | `pending` | – | Đơn #6 chuyển `pending` → `canceled`; các đơn khác giữ nguyên; API trả 2xx (EC26) | API | AI |
| FR10-BV-20 | Kiểm tra User hủy đơn mã 8 bị từ chối | mã đơn 8 (UB+1) | User chủ đơn | Hủy đơn | #8 | – | – | Từ chối, báo không tìm thấy đơn; API trả 404; các đơn giữ nguyên (EC29) | API | AI |

Tổng: 20 test case BVA mới (FR10-BV-01…FR10-BV-20); 11 dòng có ID trong ngoặc là điểm biên đã được phủ bởi test case Minimum Set (mục 3.2), chỉ dẫn chiếu, không chạy lại.
<!-- END:T42 -->

## 5. Bước 5 – Kết quả thực thi

### 5.1 Môi trường và cách chạy

| Mục | Giá trị |
| --- | --- |
| Ngày chạy | 2026-10-20 |
| Người chạy | 23120031 (script tự động, kết quả được rà soát thủ công) |
| SUT | `eshop-sut-main` (trùng với `d1nhnguyen/eshop-sut`), Node 20.19.5 |
| Web | Web Admin `http://localhost:5174`, Web `http://localhost:5173`, Chrome 155 (headless, Playwright) |
| API | `http://localhost:3000/api`, gọi bằng Python `urllib` với token Admin / `test@eshop.com` |
| Dữ liệu | Bộ dữ liệu 7 đơn (mục 3.1) được dựng lại **trước mỗi test case** (`scripts/fr10/fixture.py`) |
| Script | `scripts/fr10/cases.py` (dữ liệu), `fixture.py`, `run_web.mjs` (P-WEB-ADMIN / P-WEB-USER), `run_api.py` (P-API), `report_tables.py` |
| Bằng chứng | `evidence/FR-10/web_results.json`, `api_results.json`; ảnh sau thao tác của từng test case `evidence/FR-10/web/<ID>.png` |

Cách kết luận (A5): so trạng thái mọi đơn trước / sau. "Thành công" Pass khi chỉ đơn được thao tác đổi sang đúng trạng thái đích. "Từ chối" Pass khi không đơn nào đổi trạng thái **và** API trả 4xx kèm thông báo (trên Web: không có nút cho thao tác, hoặc có thông báo lỗi). "Không tìm thấy" Pass khi API trả 404.

### 5.2 Phát hiện chính

- API thực thi đúng phần lớn sơ đồ: 5 cạnh hợp lệ chạy được; bỏ bước, lùi, giữ nguyên, đi ra từ `delivered`, `shipping → canceled`, giá trị `status` sai đều bị từ chối (400 "Invalid state transition from … to …"); đơn không tồn tại / của người khác trả 404.
- **Hai lỗ hổng của sơ đồ:** Admin chuyển được `canceled → delivered` (Web Admin còn hiện sẵn nút "Đánh dấu Đã giao" cho đơn đã hủy); User hủy được đơn `shipping` (trang Hồ sơ hiện nút "Hủy đơn" cho đơn đang giao).
- Thông báo lỗi cho giá trị `status` không hợp lệ dùng chung câu "Invalid state transition from pending to abc"; đặc tả chỉ yêu cầu "thông báo phù hợp" nên không tính là lỗi.

### 5.3 Kết quả theo test case

Mỗi test case một dòng. Bảng sinh từ `evidence/FR-10/web_results.json` và `api_results.json`.

<!-- BEGIN:T53 -->
| TC | Web | Kết quả thực tế – Web | API | Kết quả thực tế – API | Bằng chứng | Bug |
| --- | --- | --- | --- | --- | --- | --- |
| FR10-DT-01 | Pass | Bấm “Xác nhận”, không có thông báo lỗi; đơn #1 chuyển `pending` → `confirmed` | Pass | HTTP 200 “Order status updated”; đơn #1 chuyển `pending` → `confirmed` | [ảnh Web](../evidence/FR-10/web/FR10-DT-01.png) · `api_results.json` | – |
| FR10-DT-02 | Pass | Bấm “Giao hàng”, không có thông báo lỗi; đơn #2 chuyển `confirmed` → `shipping` | Pass | HTTP 200 “Order status updated”; đơn #2 chuyển `confirmed` → `shipping` | [ảnh Web](../evidence/FR-10/web/FR10-DT-02.png) · `api_results.json` | – |
| FR10-DT-03 | Pass | Bấm “Hoàn thành”, không có thông báo lỗi; đơn #3 chuyển `shipping` → `delivered` | Pass | HTTP 200 “Order status updated”; đơn #3 chuyển `shipping` → `delivered` | [ảnh Web](../evidence/FR-10/web/FR10-DT-03.png) · `api_results.json` | – |
| FR10-DT-04 | Pass | Bấm “Hủy”, không có thông báo lỗi; đơn #1 chuyển `pending` → `canceled` | Pass | HTTP 200 “Order status updated”; đơn #1 chuyển `pending` → `canceled` | [ảnh Web](../evidence/FR-10/web/FR10-DT-04.png) · `api_results.json` | – |
| FR10-DT-05 | Pass | Bấm “Hủy”, không có thông báo lỗi; đơn #2 chuyển `confirmed` → `canceled` | Pass | HTTP 200 “Order status updated”; đơn #2 chuyển `confirmed` → `canceled` | [ảnh Web](../evidence/FR-10/web/FR10-DT-05.png) · `api_results.json` | – |
| FR10-DT-06 | Pass | Bấm “Hủy đơn”, hiện “Hủy đơn thành công!”; đơn #1 chuyển `pending` → `canceled` | Pass | HTTP 200 “Order canceled successfully”; đơn #1 chuyển `pending` → `canceled` | [ảnh Web](../evidence/FR-10/web/FR10-DT-06.png) · `api_results.json` | – |
| FR10-DT-07 | Pass | Bấm “Hủy đơn”, hiện “Hủy đơn thành công!”; đơn #2 chuyển `confirmed` → `canceled` | Pass | HTTP 200 “Order canceled successfully”; đơn #2 chuyển `confirmed` → `canceled` | [ảnh Web](../evidence/FR-10/web/FR10-DT-07.png) · `api_results.json` | – |
| FR10-DT-08 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from delivered to canceled”; đơn #4 giữ nguyên `delivered` | `api_results.json` | – |
| FR10-DT-09 | Fail | Bấm “Đánh dấu Đã giao”, không có thông báo lỗi; đơn #5 chuyển `canceled` → `delivered` | Fail | HTTP 200 “Order status updated”; đơn #5 chuyển `canceled` → `delivered` | [ảnh Web](../evidence/FR-10/web/FR10-DT-09.png) · `api_results.json` | FR10-B1 |
| FR10-DT-10 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to shipping”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-11 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from shipping to confirmed”; đơn #3 giữ nguyên `shipping` | `api_results.json` | – |
| FR10-DT-12 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from confirmed to confirmed”; đơn #2 giữ nguyên `confirmed` | `api_results.json` | – |
| FR10-DT-13 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from shipping to canceled”; đơn #3 giữ nguyên `shipping` | `api_results.json` | – |
| FR10-DT-14 | Fail | Bấm “Hủy đơn”, hiện “Hủy đơn thành công!”; đơn #3 chuyển `shipping` → `canceled` | Fail | HTTP 200 “Order canceled successfully”; đơn #3 chuyển `shipping` → `canceled` | [ảnh Web](../evidence/FR-10/web/FR10-DT-14.png) · `api_results.json` | FR10-B2 |
| FR10-DT-15 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Cannot cancel this order.”; đơn #4 giữ nguyên `delivered` | `api_results.json` | – |
| FR10-DT-16 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Cannot cancel this order.”; đơn #5 giữ nguyên `canceled` | `api_results.json` | – |
| FR10-DT-17 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; đơn #7 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-18 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to abc”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-19 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to Confirmed”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-20 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to ”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-21 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to undefined”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-DT-22 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-DT-23 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-DT-24 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-DT-25 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-DT-26 | Fail | #1 Chờ xác nhận: Xác nhận, Hủy; #2 Đã xác nhận: Giao hàng, Hủy; #3 Đang giao: Hoàn thành; #4 Đã giao: không có nút; #5 Đã hủy: Đánh dấu Đã giao – sai: #5 Đã hủy: có [Đánh dấu Đã giao], mong đợi [không có] | – | Không áp dụng (giao diện không có thao tác này) | [ảnh Web](../evidence/FR-10/web/FR10-DT-26.png) | FR10-B1 |
| FR10-DT-27 | Fail | #1 Chờ xác nhận: Hủy đơn; #2 Đã xác nhận: Hủy đơn; #3 Đang giao: Hủy đơn; #4 Đã giao: không có nút; #5 Đã hủy: không có nút – sai: #3 Đang giao: có [Hủy đơn], mong đợi [không có] | – | Không áp dụng (giao diện không có thao tác này) | [ảnh Web](../evidence/FR-10/web/FR10-DT-27.png) | FR10-B2 |
| FR10-BV-01 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to pending”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-02 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to delivered”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-03 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from confirmed to pending”; đơn #2 giữ nguyên `confirmed` | `api_results.json` | – |
| FR10-BV-04 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from confirmed to delivered”; đơn #2 giữ nguyên `confirmed` | `api_results.json` | – |
| FR10-BV-05 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from shipping to pending”; đơn #3 giữ nguyên `shipping` | `api_results.json` | – |
| FR10-BV-06 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from shipping to shipping”; đơn #3 giữ nguyên `shipping` | `api_results.json` | – |
| FR10-BV-07 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from delivered to shipping”; đơn #4 giữ nguyên `delivered` | `api_results.json` | – |
| FR10-BV-08 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from delivered to delivered”; đơn #4 giữ nguyên `delivered` | `api_results.json` | – |
| FR10-BV-09 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from canceled to canceled”; đơn #5 giữ nguyên `canceled` | `api_results.json` | – |
| FR10-BV-10 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from canceled to pending”; đơn #5 giữ nguyên `canceled` | `api_results.json` | – |
| FR10-BV-11 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to  confirmed”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-12 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to confirmed ”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-13 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to confirme”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-14 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 400 “Invalid state transition from pending to confirmedd”; đơn #1 giữ nguyên `pending` | `api_results.json` | – |
| FR10-BV-15 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-BV-16 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 200 “Order status updated”; đơn #7 chuyển `pending` → `confirmed` | `api_results.json` | – |
| FR10-BV-17 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-BV-18 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
| FR10-BV-19 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 200 “Order canceled successfully”; đơn #6 chuyển `pending` → `canceled` | `api_results.json` | – |
| FR10-BV-20 | – | Không áp dụng (giao diện không có thao tác này) | Pass | HTTP 404 “Order not found”; không đơn nào thay đổi | `api_results.json` | – |
<!-- END:T53 -->

### 5.4 Tổng hợp

<!-- BEGIN:T55 -->
| Kênh | Thiết kế | Đã chạy | Pass | Fail | Blocked | Không áp dụng |
| --- | --- | --- | --- | --- | --- | --- |
| Web | 47 | 11 | 7 | 4 | 0 | 36 |
| API | 47 | 45 | 43 | 2 | 0 | 2 |
| **Tổng lượt chạy** | | **56** | **50** | **6** | **0** | |

47 test case = 27 Minimum Set (mục 3.2) + 20 BVA (mục 4.2). Gộp các kênh theo test case (Fail nếu Fail ở bất kỳ kênh nào, Blocked nếu còn kênh bị Blocked): 43 Pass, 4 Fail, 0 Blocked.
<!-- END:T55 -->

## 6. Bước 6 – AI gap analysis

> G1–G3: AI (Claude Code) tự phát hiện trong lúc làm các bước 1–5 của FR-10. Sinh viên rà soát và bổ sung các điểm tự phát hiện ở commit `[FR-10][Bn-review]`.

### 6.1 Những gì AI bỏ sót hoặc làm sai

| # | AI bỏ sót / làm sai | Loại | Nguyên nhân | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |
| G1 | Script Web bản đầu tìm dòng đơn bằng biểu thức `#<id>(\D|$)` trên `textContent` của cả dòng; ở trang Hồ sơ các ô nối liền (`#110/20/2026…`) nên không tìm thấy dòng nào → FR10-DT-06, FR10-DT-07 **Fail giả**, FR10-DT-14 **Pass giả** ("không có nút Hủy đơn" bị hiểu là giao diện đã chặn) | Oracle / script | **Giới hạn công cụ AI**: giả định văn bản các ô có khoảng cách; không đối chiếu với quan sát ở bước 1 trước khi kết luận | Kết quả mâu thuẫn với ảnh bước 1 (trang Hồ sơ có nút "Hủy đơn" ở #1, #2, #3) | Tìm dòng theo ô mã đơn khớp chính xác; chạy lại toàn bộ |
| G2 | Oracle của test case "từ chối" chỉ kiểm tra có thông báo, không đánh giá thông báo có "phù hợp" (đặc tả) hay không – vd `status = abc` nhận "Invalid state transition from pending to abc" | Kết quả mong đợi chưa đủ chặt | **Đặc tả mơ hồ**: "thông báo phù hợp" không định nghĩa; AI chọn tiêu chí lỏng | AI rà soát kết quả bước 5 | Ghi nhận ở 6.3, không tính là lỗi |
| G3 | Ghi nhận thông báo trên Web lấy cả dòng đơn vừa đổi trạng thái (`#1 … Đã hủy`) như một "thông báo" | Bằng chứng | **Giới hạn công cụ AI**: so khác biệt văn bản trang trước / sau mà không lọc phần dữ liệu | Đọc output | Lọc khi diễn giải kết quả (mục 5.3) |

### 6.2 Test case bổ sung

Không bổ sung test case sau rà soát của AI: các lỗi tìm thấy nằm trong phạm vi các lớp đã thiết kế (EC9, EC14, EC30).

### 6.3 Điểm còn mở (chưa xử lý)

- A1 (Admin không được hủy đơn `shipping`): SUT từ chối `shipping → canceled` đúng theo A1; nếu TA xác nhận Admin được hủy đơn đang giao thì FR10-DT-13 phải đổi kết quả mong đợi.
- Mức độ "phù hợp" của thông báo lỗi (G2) và ngôn ngữ thông báo (API trả tiếng Anh trong khi FR-21 yêu cầu giao diện tiếng Việt – thuộc FR-21).

### 6.4 Nhận xét

- **Do prompt:** không có yêu cầu đối chiếu kết quả với quan sát bước 1, nên AI suýt chấp nhận kết quả sai của G1; chỉ phát hiện vì kết quả mâu thuẫn rõ với ảnh đã chụp.
- **Do giới hạn công cụ AI:** lỗi lặp lại ở cả 3 feature là oracle / bộ chọn phần tử của script (FR-01 G2, G5; FR-15 G3; FR-10 G1) – AI viết test tự động nhanh nhưng dễ sinh Pass / Fail giả.
- **Do độ phức tạp feature:** lỗi của FR-10 nằm ở hai cạnh lạ (`canceled → delivered`, User hủy `shipping`) mà cả giao diện lẫn API đều cho phép – chỉ phát hiện được nhờ phân vùng tách riêng "đi ra từ `canceled`" và "User hủy `shipping`" (G5).

## 7. Bước 7 – Bug

Chi tiết từng bug: `bugs/Bug_Report.md`. Cột GitHub Issue dẫn tới issue trên repo nhóm `d1nhnguyen/eshop-sut` (ảnh chụp trang issue ở cuối `bugs/Bug_Report.md`).

| Mã | Tiêu đề | Mức độ | Thành phần | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- | --- |
| FR10-B1 | Đơn đã hủy chuyển được sang "Đã giao"; Web Admin hiện nút "Đánh dấu Đã giao" cho đơn đã hủy | Critical | Backend, Web Admin | FR10-DT-09, FR10-DT-26 | [BUG-30](https://github.com/d1nhnguyen/eshop-sut/issues/30) |
| FR10-B2 | User hủy được đơn đang giao; trang Hồ sơ hiện nút "Hủy đơn" cho đơn đang giao | Major | Backend, Web | FR10-DT-14, FR10-DT-27 | [BUG-31](https://github.com/d1nhnguyen/eshop-sut/issues/31) |

Tổng: 2 bug (1 Critical, 1 Major).
