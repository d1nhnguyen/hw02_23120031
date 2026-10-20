# <FEATURE> – <Tên feature> · Domain Testing & Boundary Value Analysis

| Mục | Giá trị |
| --- | --- |
| Feature | <FEATURE> – <Tên> (Pool <X>) |
| Kênh kiểm thử | <Web / Web Admin / Mobile> + API <endpoint> |
| Người thực hiện | <MSSV> |
| Công cụ AI | <công cụ> |
| Kỹ thuật | Domain Testing (S04 – bước 1–3), Boundary Value Analysis (S04 – bước 4) |

## 0. Đặc tả (trích nguyên văn)

> <dán nguyên văn đoạn đặc tả>

## 1. Bước 1 – Xác định biến Input / Output

### 1.1 Quan sát giao diện (hộp đen)

| Thành phần | Quan sát |
| --- | --- |

### 1.2 Biến đầu vào

| ID | Biến | Kênh nhập | Kiểu / miền giá trị | Ràng buộc theo đặc tả | Nguồn |
| --- | --- | --- | --- | --- | --- |

### 1.3 Biến đầu ra

| ID | Biến | Giá trị có thể có | Nguồn |
| --- | --- | --- | --- |

### 1.4 Giả định cho những chỗ đặc tả chưa rõ

| ID | Giả định | Căn cứ |
| --- | --- | --- |

### 1.5 Ngoài phạm vi

## 2. Bước 2 – Lớp tương đương (Complete Set of Partitions)

### 2.1 Cách áp dụng guideline cho từng biến

| Biến | Điều kiện trong đặc tả | Guideline [S04] | Lớp tạo ra |
| --- | --- | --- | --- |

### 2.2 Complete Set of Partitions

| EC | Biến | Phân vùng | Ví dụ đại diện | Valid / Invalid |
| --- | --- | --- | --- | --- |

## 3. Bước 3 – Test case Domain Testing

### 3.1 Thủ tục thực hiện

### 3.2 Minimum Set of Test Cases

<!-- BEGIN:T32 -->
<!-- END:T32 -->

### 3.3 Bảng phủ phân vùng

<!-- BEGIN:T33 -->
<!-- END:T33 -->

## 4. Bước 4 – Boundary Value Analysis

### 4.1 Xác định biên

| Biến | Phân vùng | LB | UB | Bước nhảy | Điểm kiểm tra |
| --- | --- | --- | --- | --- | --- |

### 4.2 Boundary Value Test Cases

<!-- BEGIN:T42 -->
<!-- END:T42 -->

## 5. Bước 5 – Kết quả thực thi

### 5.1 Môi trường và cách chạy

### 5.2 Phát hiện chính

### 5.3 Kết quả theo test case

<!-- BEGIN:T53 -->
<!-- END:T53 -->

### 5.4 Tổng hợp

<!-- BEGIN:T55 -->
<!-- END:T55 -->

## 6. Bước 6 – AI gap analysis

### 6.1 Những gì AI bỏ sót hoặc làm sai

| # | AI bỏ sót / làm sai | Loại | Nguyên nhân | Phát hiện bằng cách nào | Đã xử lý |
| --- | --- | --- | --- | --- | --- |

### 6.2 Test case bổ sung

<!-- BEGIN:T62 -->
<!-- END:T62 -->

### 6.3 Điểm còn mở

### 6.4 Nhận xét

## 7. Bước 7 – Bug

| Mã | Tiêu đề | Mức độ | Thành phần | TC liên quan | GitHub Issue |
| --- | --- | --- | --- | --- | --- |
