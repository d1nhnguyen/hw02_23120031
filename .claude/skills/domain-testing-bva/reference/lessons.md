# Bài học khi tự động hóa (rút từ AI gap analysis của FR-01, FR-15, FR-10, Mobile – Đăng nhập)

Mỗi mục là một lỗi AI đã thực sự mắc; runner mới phải tránh từ đầu.

## Oracle (điều kiện Pass / Fail)

1. **Bị từ chối chưa đủ để Pass.** Phải kiểm tra thông báo nói đúng lý do mong đợi (trường / loại lỗi); bị từ chối vì lý do khác → Fail, hoặc **Blocked** nếu một lỗi khác chặn trước (FR-01: mọi test case Email "Pass" vì bị chặn bởi lỗi mật khẩu).
2. **Không có phần tử ≠ hệ thống đã chặn.** Trước khi kết luận "giao diện không cho thao tác", đối chiếu với ảnh quan sát ở bước 1; bộ chọn sai cũng cho kết quả "không có" (FR-10: Pass giả vì không tìm thấy dòng).
3. **Kiểm chứng bằng ảnh chụp dữ liệu trước / sau** qua API (danh sách sản phẩm, đơn hàng, người dùng) – bắt được cả việc tạo thêm bản ghi trùng, sửa nhầm bản ghi khác.
4. **Không suy hành vi từ thuộc tính tĩnh** (vd `validationMessage` của ô số) – phải thực hiện thao tác thật (FR-15: tưởng trình duyệt chặn giá thập phân).
5. **Test case độc lập:** khởi động lại dữ liệu trước mỗi test case; kiểm tra "bản ghi gốc bị ảnh hưởng" bằng hành vi của chính bản ghi đó, không bằng số lượng bị nhiễm từ test case trước (FR-01).

## Bộ chọn phần tử / bằng chứng

6. Không đọc thông báo sau khi giao diện đã đổi trạng thái (chuyển trang, form bị xóa trắng sau khi lưu) – chỉ đọc khi thao tác bị chặn tại chỗ (FR-01, lặp lại ở FR-15).
7. Tìm dòng bảng theo **ô** khớp chính xác (`td` = `#12`), không theo `textContent` cả dòng – các ô nối liền nhau (`#110/20/2026…`) (FR-10).
8. Escape `<`, `>`, `|` khi đưa văn bản tự do vào ô bảng Markdown; bằng chứng chứa HTML sẽ bị hiển thị sai (FR-15).

## Thực thi

9. Gọi script con (khởi động lại backend) **không bắt output** (`stdout=DEVNULL`) – tiến trình chạy nền giữ pipe làm runner treo (FR-15).
10. Không chạy song song hai runner dùng chung backend; không tự khởi động lại backend khi một runner đang chạy.
11. Chạy runner dài bằng `setsid nohup` và ghi kết quả sau từng test case (chế độ `RESUME`) để không mất tiến độ khi IDE / phiên bị dừng.
12. Mobile qua `adb`: chỉ rõ package khi mở app, thử lại khi mở thất bại, chờ màn hình tải xong; vùng thanh trạng thái không nhận chạm (thử nhiều thiết bị).
13. Kết quả bất thường (vd bộ đếm tăng 2) → tái hiện bằng **một request API** trước khi kết luận là lỗi SUT, để loại trừ lỗi của script (Mobile).
14. Tính toán dữ liệu dài bằng code + `assert` (độ dài email 254 – AI từng tính thành 255).
