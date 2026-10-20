---
name: domain-testing-bva
description: Apply Domain Testing (equivalence partitioning) and Boundary Value Analysis to one feature of a system under test, step by step as taught in CSC13003 (S04, UC Analysis, S07, Runnels), producing a Vietnamese Markdown report with data-matrix test cases, executable test scripts, execution evidence, AI gap analysis and bug report drafts. Use when the user asks to design or run domain / boundary test cases for a feature from its specification (e.g. "làm domain testing cho FR-xx", "BVA cho chức năng đăng nhập").
---

# Domain Testing + Boundary Value Analysis cho một feature

Skill này dẫn agent đi qua **7 bước**, mỗi bước là **một commit** `[<FEATURE>][B<n>]`. Không bao giờ dùng một prompt "sinh test case" duy nhất: làm từng bước, đọc lại kết quả, rồi mới sang bước sau.

Trước khi bắt đầu, đọc `reference/method.md` (quy tắc của môn học) và `reference/lessons.md` (các lỗi đã gặp khi tự động hóa – bắt buộc tránh).

## Đầu vào cần có

| Mục | Ví dụ |
| --- | --- |
| Mã feature + đặc tả nguyên văn | FR-15 trong README của SUT |
| Kênh kiểm thử | Web / Web Admin / Mobile + API |
| Cách khởi động lại dữ liệu sạch | `scripts/restart_backend.sh` |
| Tiền tố ID | `FR15`, `MOB` |

Thiếu mục nào hoặc đặc tả mâu thuẫn → **dừng và hỏi người dùng**. Chỗ đặc tả chỉ mơ hồ → đặt giả định có mã (A1, A2…) và ghi vào danh sách điểm cần hỏi TA (`DOI_CHIEU_TRUOC_KHI_NOP.md` nếu dự án có).

## Bố cục sản phẩm

```
report/<Feature>.md                 # chép templates/report_template.md, điền mục 0 bằng đặc tả nguyên văn
scripts/<feature>/cases.py          # NGUỒN DUY NHẤT: tiêu đề, phân vùng phủ, dữ liệu, kết quả mong đợi, Origin
scripts/<feature>/report_tables.py  # sinh bảng 3.2, 3.3, 4.2, 5.3, 5.5, 6.2 (dùng scripts/report_lib.py)
scripts/<feature>/run_<kênh>.*      # runner từng kênh, ghi evidence/<Feature>/<kênh>_results.json
evidence/<Feature>/                 # kết quả JSON + ảnh từng test case
bugs/Bug_Report.md                  # nháp bug theo mẫu Problem Report (Kaner)
```

Bảng trong báo cáo **không viết tay**: đặt mốc `<!-- BEGIN:T32 --> … <!-- END:T32 -->` và chạy `python3 report_tables.py T32 …`. Như vậy báo cáo và script không bao giờ lệch nhau.

## Các bước

### B1 – Biến Input / Output (mục 1)
1. Quan sát hộp đen giao diện thật (trường, kiểu, `required`, `maxlength`, nút theo trạng thái) và API trong đặc tả. Chụp ảnh `evidence/<Feature>/B1_*.png`. **Không đọc mã nguồn SUT.**
2. Bảng biến đầu vào (ID, biến, kênh nhập, miền, ràng buộc, nguồn), biến dẫn xuất có thứ tự (độ dài, số ký tự mỗi loại, thứ tự trạng thái…), biến đầu ra (kể cả từng loại thông báo, dữ liệu sau thao tác).
3. Giả định A1…An cho chỗ mơ hồ; mục "Ngoài phạm vi".
4. Commit `[<F>][B1] Xác định biến Input/Output, giả định và phạm vi`.

### B2 – Lớp tương đương (mục 2)
1. Bảng 2.1: với từng biến, ghi điều kiện trong đặc tả → guideline áp dụng (khoảng giá trị / số lượng / tập giá trị / "phải là" / tách lớp G5) → lớp tạo ra. Tách lớp khi có **lý do rủi ro** cụ thể (ghi lý do).
2. Bảng 2.2 Complete Set of Partitions: EC, biến, phân vùng, ví dụ đại diện, Valid / Invalid / Output. Có cả **lớp đầu ra**.
3. Đếm lại số lớp bằng script trước khi ghi tổng.
4. Commit `[<F>][B2]`.

### B3 – Minimum Set (mục 3)
1. Mục 3.1: thủ tục step-by-step chung cho từng kênh + tiền điều kiện + hậu điều kiện (self-cleaning). Ghi quy ước ký hiệu (`␣`, `(rỗng)`, công thức chuỗi dài).
2. Viết `cases.py` (chép `templates/cases_template.py`): mỗi test case có ID `<PREFIX>-DT-nn`, tiêu đề **Action + Function + Condition**, phân vùng phủ, dữ liệu cụ thể (không "mặc định", không "như TC khác"), kết quả mong đợi tường minh kèm mã lớp đầu ra, kênh, Origin.
3. Test case valid phủ nhiều lớp valid nhất có thể (liệt kê đủ mọi lớp valid mà dữ liệu phủ); mỗi test case invalid phủ **đúng một** lớp invalid.
4. Sinh T32, T33; kiểm tra bảng phủ đạt 100%.
5. Commit `[<F>][B3]`.

### B4 – BVA (mục 4)
1. Bảng 4.1: với mỗi biến có thứ tự: phân vùng, LB, UB, bước nhảy (độ chính xác nhỏ nhất), điểm kiểm tra (LB-1, LB, LB+1, UB-1, UB, UB+1, lớn nhất nhập được). Nghĩ cả biến "ẩn" có thứ tự: mã ký tự (`@`/`A`/`Z`/`[`), thứ tự trạng thái, số lần thử, thời gian, id.
2. Thêm test case `<PREFIX>-BV-nn` vào `cases.py`; điểm biên đã có trong Minimum Set thì đưa vào `BV_ORDER` dạng dẫn chiếu `(DT-xx, "partition")`, không tạo test case trùng.
3. Bảng 4.2 giữ **đủ cột dữ liệu** như 3.2. Sinh T42.
4. Commit `[<F>][B4]`.

### B5 – Thực thi (mục 5)
1. Viết runner cho từng kênh: khởi động lại dữ liệu **trước mỗi test case**, kiểm chứng bằng ảnh chụp dữ liệu trước / sau qua API (oracle không có tác dụng phụ), ghi kết quả + ghi chú, chụp ảnh mỗi test case. Áp dụng toàn bộ `reference/lessons.md`.
2. Kết quả bất ngờ → khảo sát thêm (exploratory) và **xác minh bằng một request API** trước khi kết luận là lỗi SUT.
3. Test case bị một lỗi khác che (chưa tới được điều kiện cần kiểm tra) → **Blocked**, ghi lý do; có thể thêm lượt khảo sát không tính verdict.
4. Mục 5.1 môi trường + cách kết luận, 5.2 phát hiện chính, sinh T53 (mỗi test case một dòng, có cột Bằng chứng, Bug ID), T55.
5. Commit `[<F>][B5]` kèm `evidence/`.

### B6 – AI gap analysis (mục 6)
1. Liệt kê trung thực mọi chỗ AI làm sai / bỏ sót ở B1–B5 (dự đoán sai về SUT, oracle lỏng, thiếu lớp, dữ liệu sai…), mỗi dòng có **nguyên nhân**: do prompt / giới hạn công cụ AI / độ phức tạp feature, cách phát hiện, cách xử lý.
2. Test case bổ sung (`added=True`, Origin `AI` hoặc `SV`) → chạy, sinh T62 và các bảng kết quả.
3. Điểm còn mở; nhận xét theo 3 nhóm nguyên nhân.
4. Commit `[<F>][B6]`.

### B7 – Bug (mục 7)
1. Gom các test case Fail theo **điều khoản đặc tả bị vi phạm** (mỗi điều khoản / mỗi chỗ cần sửa riêng = một bug; không thổi phồng).
2. Viết `bug_evidence.*`: tái hiện từng bug, chụp "thẻ bằng chứng" (request, response, dữ liệu lưu) + ảnh giao diện.
3. Nháp trong `bugs/Bug_Report.md` theo mẫu Problem Report: trường, mức độ / ưu tiên, các bước tái hiện ngắn nhất, mong đợi (trích đặc tả), thực tế, phân tích (hậu quả nghiêm trọng nhất, đường khác dẫn tới lỗi), bằng chứng. Tiêu đề issue `[BUG-NN] [FR-xx] …`.
4. Đối chiếu bằng script: danh sách TC của mỗi bug phải khớp cột Bug của T53.
5. **Không tự tạo GitHub issue** – sinh viên duyệt và tạo.
6. Commit `[<F>][B7]`; cập nhật prompt log (`[ai-log]`).

## Rà soát của sinh viên

Mỗi chỉnh sửa sau khi sinh viên rà soát là commit `[<F>][B<n>-review]`; test case được sửa đổi Origin thành `AI-sửa`, test case sinh viên thêm là `SV`. Nếu bản rà soát do công cụ AI khác tạo, phải khai báo trong AI Audit Report.
