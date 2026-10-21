---
name: domain-testing-bva
description: Apply Domain Testing (equivalence partitioning) and Boundary Value Analysis to one feature of a system under test, step by step as taught in CSC13003 (S04, UC Analysis, S07, Runnels), producing a Vietnamese Markdown report with data-matrix test cases, executable test scripts, execution evidence, AI gap analysis and bug report drafts. By default a single invocation runs all seven steps in order (one git commit per step, self-checks between steps) and ends with a results summary; it can also run one step at a time for review. Use when the user asks to design or run domain / boundary test cases for a feature from its specification (e.g. "làm domain testing cho FR-xx", "BVA cho chức năng đăng nhập").
---

# Domain Testing + Boundary Value Analysis cho một feature

Skill này dẫn agent đi qua **7 bước**, mỗi bước là **một commit** `[<FEATURE>][B<n>]`. Không gộp các bước thành một lần "sinh test case": làm xong một bước, tự kiểm tra kết quả theo mục "Kiểm tra trước khi sang bước sau", rồi mới làm bước kế.

## Hai chế độ chạy

| Chế độ | Khi nào | Cách làm |
| --- | --- | --- |
| **Liền mạch** (mặc định) | Người dùng gọi skill một lần, vd `/domain-testing-bva FR-02` | Làm tuần tự B1 → B7 không dừng hỏi; mỗi bước một commit; thông tin thiếu thì tự suy ra (mục "Đầu vào") và ghi thành giả định; cuối cùng in **Tóm tắt kết quả** |
| Từng bước | Người dùng yêu cầu duyệt từng bước ("làm B1 rồi dừng") | Làm đúng bước được yêu cầu rồi dừng chờ duyệt |

Chỉ dừng giữa chừng khi bị chặn thật sự: không tìm thấy đặc tả, SUT không chạy và không tự khởi động được, đặc tả mâu thuẫn đến mức không đặt được giả định.

Trước khi bắt đầu, đọc `reference/method.md` (quy tắc của môn học) và `reference/lessons.md` (các lỗi đã gặp khi tự động hóa – bắt buộc tránh).

## Đầu vào cần có

| Mục | Ví dụ |
| --- | --- |
| Mã feature + đặc tả nguyên văn | FR-15 trong README của SUT |
| Kênh kiểm thử | Web / Web Admin / Mobile + API |
| Cách khởi động lại dữ liệu sạch | `scripts/restart_backend.sh` |
| Tiền tố ID | `FR15`, `MOB` |

Thiếu mục nào thì tự suy ra và ghi vào mục 1.4 (giả định):

- Đặc tả: tìm mục `FR-xx` trong README / tài liệu đặc tả của SUT (vd `eshop-sut-main/README.md`, `api_specification.md`); trích **nguyên văn** vào mục 0.
- Kênh: theo đặc tả (Web / Web Admin / Mobile) + endpoint API tương ứng; kiểm tra SUT đang chạy (vd `curl` trang và API).
- Tiền tố ID: mã feature bỏ dấu gạch (`FR-02` → `FR02`).
- Reset dữ liệu: `scripts/restart_backend.sh` nếu dự án có.

Đặc tả mơ hồ → đặt giả định có mã (A1, A2…) và ghi vào danh sách điểm cần hỏi (`DOI_CHIEU_TRUOC_KHI_NOP.md` nếu dự án có). Chế độ từng bước: thiếu thông tin hoặc mâu thuẫn thì hỏi người dùng.

## Bố cục sản phẩm

```
scripts/report_lib.py               # chép scripts/report_lib.py của skill (dùng chung cho mọi feature)
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
5. **Không tự tạo GitHub issue** trừ khi người dùng yêu cầu rõ ràng – mặc định sinh viên duyệt nháp rồi tự tạo issue (đính ảnh trong `bugs/screenshots/`). Sau khi có issue, điền số `BUG-NN` + link vào `bugs/Bug_Report.md` và mục 7 của báo cáo.
6. Commit `[<F>][B7]`; cập nhật prompt log nếu dự án có (`[ai-log]`).

## Kiểm tra trước khi sang bước sau

| Bước | Tự kiểm tra |
| --- | --- |
| B1 | Đặc tả trích nguyên văn; có cả biến đầu ra; mỗi chỗ mơ hồ có giả định |
| B2 | Mỗi điều kiện trong đặc tả có lớp valid + invalid; đếm lại số lớp bằng script |
| B3 | T33 đạt 100%; mỗi TC invalid phủ đúng 1 lớp invalid; không có ô "mặc định" / "như TC khác" |
| B4 | Mỗi biến có thứ tự có LB-1…UB+1; điểm trùng Minimum Set chỉ dẫn chiếu |
| B5 | Mỗi TC có verdict + bằng chứng; kết quả bất ngờ đã xác minh bằng một request API; runner dài chạy nền và theo dõi đến khi xong (lessons 9–11) |
| B6 | Mỗi điểm có nguyên nhân + cách phát hiện; TC bổ sung đã chạy |
| B7 | TC của mỗi bug khớp cột Bug của T53 |

## Tóm tắt kết quả (cuối chế độ liền mạch)

In ra cho người dùng, ngắn gọn:

1. Bảng 7 bước → commit tương ứng (`git log --oneline`).
2. Số lớp tương đương, số TC (Minimum Set / BVA / bổ sung) và bảng T55 (Pass / Fail / Blocked theo kênh).
3. Danh sách bug nháp: mã, tiêu đề, mức độ, TC phát hiện.
4. Các điểm AI gap analysis chính.
5. **Điểm cần người duyệt**: giả định đã đặt, mức độ bug, kết quả bất ngờ.
6. File nên mở để xem: báo cáo, `evidence/<F>/`, `bugs/Bug_Report.md`.

## Rà soát của sinh viên

Mỗi chỉnh sửa sau khi sinh viên rà soát là commit `[<F>][B<n>-review]`; test case được sửa đổi Origin thành `AI-sửa`, test case sinh viên thêm là `SV`. Nếu bản rà soát do công cụ AI khác tạo, phải khai báo trong AI Audit Report.
