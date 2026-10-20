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
