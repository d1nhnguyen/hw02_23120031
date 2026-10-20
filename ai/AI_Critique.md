# AI Critique · HW02 · 23120031

<!--
200–300 từ, trả lời 3 câu hỏi của đề (mục 10):
1. AI đã sai, thiên lệch hoặc thiếu sót ở đâu?
2. Vì sao AI không phát hiện được vấn đề đó?
3. Bạn rút ra nguyên tắc gì về cách cộng tác với AI qua bài này?
Dẫn ví dụ cụ thể từ phần AI gap analysis của 4 feature.

Ví dụ có sẵn trong mục 6.1 các báo cáo (sinh viên chọn, tự diễn đạt, xóa khối chú thích này trước khi nộp):
- Oracle quá dễ dãi: FR-01 G2–G3 (từ chối vì bất kỳ lý do nào cũng tính Pass → 10 + 5 test case Pass giả).
- Suy luận quá đà từ một mẫu: FR-01 G4 (đường vòng mật khẩu), FR-15 G1 (kết luận "trình duyệt chặn 0.5" chỉ từ validationMessage).
- Bằng chứng sai lệch: FR-01 G5, FR-15 G3, FR-10 G1 (regex tìm dòng đơn → Fail / Pass giả), FR-10 G3.
- Thiếu biến môi trường: Mobile G1 (chỉ thử Pixel 6); test case phụ thuộc chuỗi trạng thái: Mobile G2.
- Lỗi do bản rà soát chéo FR-01 (Google Antigravity – Gemini 4 Argon, lượt #13) phát hiện (G9–G16): bảng BVA lệch data matrix, test case không self-standing, ID trùng khi gộp, tổng số lệch, thiếu test case chữ tiếng Việt có dấu trong mật khẩu.
- Điểm AI làm tốt: tự kiểm tra lại bằng API trước khi kết luận (Mobile G3), assert độ dài dữ liệu (FR-01 G7).
-->

Số từ:
