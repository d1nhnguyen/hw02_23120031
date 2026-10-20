# Phương pháp áp dụng – Domain Testing & Boundary Value Analysis

Phần này mô tả cách bài làm áp dụng kỹ thuật theo tài liệu môn học; mọi feature (FR-01, FR-10, FR-15, Mobile – Đăng nhập) đều làm theo đúng các bước dưới đây.

## Tài liệu tham chiếu

| Ký hiệu | Tài liệu |
| --- | --- |
| [S04] | S04_Domain Testing.pdf – quy trình 4 bước, guideline lớp tương đương, BVA 9 điểm |
| [KB] | Refs/EN.DOMAIN TESTING.pdf (Cem Kaner & James Bach) – 4 quan niệm về "tương đương", best representative |
| [UC] | Refs/EN.DOMAIN TESTING - UC Analysis.pdf – ví dụ mẫu: Complete Set of Partitions, Minimum Set, Boundary Value Test Cases |
| [S07] | S07_Test Case.pdf, EN.Test_Cases_AI_First.pdf – cấu trúc test case, tiêu đề Action + Function + Condition |
| [DR] | Refs/How to write better testcases.pdf (Dianne Runnels) – step-by-step vs data matrix, 7 lỗi thường gặp |
| [TPL] | Templates/Test Cases – Test cases_Template_En.xlsx, Testcase Checklist.xlsx |

## Bước 1 – Xác định biến Input / Output [S04]

- Đọc đặc tả (README của SUT, `api_specification.md`) và giao diện thật (quan sát hộp đen: các trường nhập, kiểu trường) để liệt kê **biến đầu vào** và **biến đầu ra**.
- Biến đầu ra gồm cả kết quả thành công lẫn từng loại thông báo lỗi, vì [UC] phân vùng cả output (vd. "Insufficient Funds", "Invalid Input").
- Chỗ đặc tả không nói rõ được ghi thành **giả định** có mã (A1, A2…), mỗi test case phụ thuộc giả định sẽ dẫn chiếu mã đó.

## Bước 2 – Xác định lớp tương đương [S04], [KB]

Áp dụng 5 guideline:

| Loại điều kiện | Lớp valid | Lớp invalid |
| --- | --- | --- |
| Khoảng giá trị (vd 1–999) | 1 | 2 (dưới, trên) |
| Số lượng giá trị (vd 1–6 phần tử) | 1 | 2 (không có, quá nhiều) |
| Tập giá trị được xử lý khác nhau | mỗi giá trị 1 lớp | 1 (giá trị ngoài tập) |
| Điều kiện "phải là" | 1 | 1 |
| Có lý do tin rằng các phần tử trong lớp được xử lý khác nhau | tách lớp | tách lớp |

- Ngoài ràng buộc nghiệp vụ, mỗi biến có thêm các lớp về **kiểu** (sai kiểu dữ liệu, rỗng, chỉ có khoảng trắng) như cách [UC] thêm "alphabetic string", "three decimal places".
- Kết quả trình bày thành bảng **Complete Set of Partitions** [UC]: mỗi lớp có mã EC, biến, điều kiện, Valid / Invalid.

## Bước 3 – Chọn test case [S04], [UC]

- Mỗi lớp chọn một **best representative** [KB]: giá trị có khả năng lộ lỗi cao nhất trong lớp.
- **Minimum Set**: test case valid phủ càng nhiều lớp valid càng tốt; mỗi test case invalid phủ **đúng một** lớp invalid (các biến còn lại giữ giá trị valid) để khi fail biết ngay nguyên nhân.
- Bảng **phủ phân vùng** chỉ ra mỗi EC được test case nào phủ, chứng minh 100% lớp được phủ.

## Bước 4 – Boundary Value Analysis [S04], [UC]

- Áp dụng cho biến có thứ tự (độ dài chuỗi, số tiền, số lần, thời gian, thứ tự trạng thái…).
- Mỗi phân vùng xét tối đa 9 điểm: giá trị đại diện, LB-1, LB, LB+1, UB-1, UB, UB+1, giá trị nhỏ nhất và lớn nhất nhập được qua UI/API.
- Bước nhảy giữa các điểm bằng độ chính xác nhỏ nhất của biến (1 ký tự, 1 đơn vị, 0.01…), như [UC] dùng 0.01 vì hệ thống xử lý 2 chữ số thập phân.
- Cột **Partition tested** ghi biên giữa hai phân vùng dạng `EC3/EC4`.

## Định dạng test case [S07], [DR], [TPL]

- Tiêu đề theo cú pháp **Action + Function + Condition**, ví dụ "Verify đăng ký bị từ chối khi mật khẩu thiếu chữ hoa".
- Với form nhập liệu, mọi test case có cùng thủ tục, chỉ dữ liệu thay đổi → dùng dạng **data matrix** [DR]: mỗi feature có một thủ tục step-by-step (Precondition + Steps) cho từng kênh (Web UI, API), mỗi dòng của ma trận là một test case có ID, tiêu đề, dữ liệu và kết quả mong đợi kiểm chứng được.
- Kết quả thực thi ghi theo mẫu [TPL]: Actual Result, Status (Pass / Fail / Blocked), Tester, Tested Date, Bug ID.
- Tự rà soát bằng *Testcase Checklist* [TPL] (Accurate, Economical, Repeatable, Traceable, Appropriate, Self standing, Self cleaning; ≤ 15 bước; matrix chạy ≤ 20 phút).

## Kênh kiểm thử

- Mỗi test case được thực thi trên giao diện người dùng (Web / Web Admin / Mobile) và, khi có API tương ứng, gọi trực tiếp API để kiểm tra phía server có tự kiểm tra dữ liệu hay chỉ dựa vào kiểm tra phía client.
- Dữ liệu được reset bằng cách khởi động lại backend trước mỗi phiên thực thi (Self cleaning).

## Vai trò của AI

- Mỗi bước được thực hiện với Claude Code theo đúng thứ tự trên (không dùng một prompt "sinh test case" duy nhất).
- Output AI của mỗi bước là một commit riêng `[<FR>][B<n>]`; phần sinh viên rà soát, sửa và bổ sung là commit tiếp theo, nên `git diff` giữa hai commit chính là bằng chứng chỉnh sửa cho AI Audit Report và AI gap analysis.
