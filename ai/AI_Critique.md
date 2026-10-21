# AI Critique · HW02 · 23120031

<!-- NHÁP do Claude Code viết theo yêu cầu của sinh viên (lượt #26), dựa trên mục 6 (AI gap analysis) của 4 báo cáo. Sinh viên đọc, chỉnh theo ý mình rồi xóa dòng này. -->

**AI đã sai ở đâu?** Lỗi nguy hiểm nhất nằm ở oracle. Ở FR-01, script đầu tiên coi mọi lần form từ chối là Pass, nên 15 test case thực chất bị từ chối vì một lỗi khác: form báo "Mật khẩu quá yếu" với mọi mật khẩu hợp lệ. AI còn khái quát từ một quan sát: kết luận ô Giá chặn `0.5` chỉ nhờ thông báo của trình duyệt dù giá vẫn được lưu (FR-15), tìm sai dòng đơn hàng nên ra Fail / Pass giả (FR-10), chỉ thử máy Pixel 6 nên suýt kết luận Mobile không đăng nhập được. Antigravity khi rà soát chéo chỉ ra test case chưa self-standing, nhưng khi đối chiếu bug lại dẫn mã test case không tồn tại.

**Vì sao AI không tự phát hiện?** AI tối ưu cho việc script chạy ra kết quả, không tự hỏi kết quả đúng vì đúng lý do hay không. Nó tin quan sát đầu tiên và không thấy điều công cụ không quan sát được (`adb` không thấy request mạng). Prompt của tôi cũng thiếu ngữ cảnh: không nêu thiết bị đích, không nói bốn báo cáo sẽ được gộp. Khi viết nhanh, AI rút gọn dữ liệu thành "mặc định", "như test case khác".

**Nguyên tắc rút ra.** Output của AI là giả thuyết: mỗi verdict cần bằng chứng từ một kênh độc lập (dữ liệu đọc qua API trước và sau thao tác), và oracle phải kiểm tra lý do bị từ chối chứ không chỉ việc bị từ chối. AI thứ hai giúp kiểm tra chéo nhưng không thay được việc tự đối chiếu với đặc tả. Giả định, mức độ nghiêm trọng và quyết định cuối cùng vẫn là của tôi.

Số từ: 291
