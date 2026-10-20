# Quy tắc phương pháp (tóm tắt tài liệu môn học)

| Ký hiệu | Nguồn |
| --- | --- |
| [S04] | S04_Domain Testing.pdf |
| [KB] | Refs/EN.DOMAIN TESTING.pdf (Kaner & Bach) |
| [UC] | Refs/EN.DOMAIN TESTING - UC Analysis.pdf |
| [S07] | S07_Test Case.pdf, EN.Test_Cases_AI_First.pdf |
| [DR] | Refs/How to write better testcases.pdf (Runnels) |
| [TPL] | Templates/Test Cases (Test cases_Template_En.xlsx, Testcase Checklist.xlsx) |

## 4 bước Domain Testing [S04]

1. Xác định biến Input và Output (cả thông báo lỗi là output).
2. Xác định lớp tương đương cho mỗi Input / Output.
3. Chọn "best representative" cho mỗi lớp [KB]: giá trị có khả năng lộ lỗi cao nhất – theo **rủi ro**, không phải giá trị "điển hình".
4. Đại diện tốt nhất của biến có thứ tự thường là giá trị biên → BVA.

## Guideline lớp tương đương [S04], [KB]

| Điều kiện | Valid | Invalid |
| --- | --- | --- |
| Khoảng giá trị (1–999) | 1 | 2 (dưới, trên) |
| Số lượng giá trị (1–6 phần tử) | 1 | 2 (0, quá nhiều) |
| Tập giá trị xử lý khác nhau | 1 / giá trị | 1 (ngoài tập) |
| "Phải là" | 1 | 1 |
| G5 – có lý do tin các phần tử được xử lý khác nhau | tách lớp | tách lớp |

Thêm lớp kiểu dữ liệu (rỗng, chỉ khoảng trắng, sai kiểu, sai độ chính xác) như [UC] thêm "alphabetic string", "three decimal places". Có lớp cho **đầu ra**.

## Chọn test case [S04], [UC]

- Mỗi lớp ít nhất một test case.
- Valid: một test case phủ càng nhiều lớp valid càng tốt.
- Invalid: mỗi test case phủ **đúng một** lớp invalid (biến khác hợp lệ) để khi Fail biết ngay nguyên nhân.
- Trình bày: Complete Set of Partitions → Test cases providing coverage → Minimum Set → Boundary Value Test Cases (cột "Partition tested" dạng `EC3/EC4`).

## BVA [S04]

- Mỗi phân vùng tối đa 9 điểm: đại diện, LB-1, LB, LB+1, UB-1, UB, UB+1, nhỏ nhất / lớn nhất nhập được qua UI.
- Bước nhảy = độ chính xác nhỏ nhất của biến (1 ký tự, 1 đơn vị, 0.01, 1 mã ký tự…).
- Giá trị biên bắt được cả lỗi viết sai bất đẳng thức (`<=` thay `<`) lẫn sai hằng số; giá trị không phải biên có thể bỏ sót cả hai.

## Test case [S07], [DR], [TPL]

- Tiêu đề: **Action + Function + Condition** ("Kiểm tra đăng ký bị từ chối khi Mật khẩu không có chữ hoa").
- Thủ tục giống nhau, chỉ dữ liệu khác → **data matrix**: một thủ tục step-by-step + mỗi dòng là một test case.
- Dữ liệu cụ thể, kết quả mong đợi kiểm chứng được; ≤ 15 bước; matrix chạy ≤ 20 phút.
- 7 thuộc tính: Accurate, Economical, Repeatable, Traceable, Appropriate, Self-standing, Self-cleaning.
- Kết quả: Actual, Status (Pass / Fail / Blocked), Tester, Date, Bug ID, bằng chứng.

## Bug report (Kaner TCS ch.5)

Số hiệu, chương trình / phiên bản, loại, mức độ, tái hiện được không, tóm tắt, các bước tái hiện **ít nhất**, kết quả mong đợi / thực tế, phân tích (hậu quả nghiêm trọng nhất, điều kiện đơn giản nhất, đường khác dẫn tới lỗi, lỗi liên quan), người báo, ngày, đính kèm. Viết đơn giản, tái hiện được, không phán xét.
