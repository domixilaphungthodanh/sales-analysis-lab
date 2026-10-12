# Sales Analysis Lab

Dự án học phân tích doanh thu cửa hàng với **SQLite + Python + pandas + Seaborn + Matplotlib**. Kết quả gồm notebook, bảng tổng hợp, năm biểu đồ và báo cáo Markdown.

## Bắt đầu

Cần Python 3.10 trở lên. Mở terminal tại thư mục repo.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe src/prepare_data.py
.venv\Scripts\python.exe src/analyze.py
.venv\Scripts\python.exe -m jupyter notebook
```

Trên macOS/Linux, thay `.venv\Scripts\python.exe` bằng `.venv/bin/python`.
Trong VS Code, mở `notebooks/02_analysis.ipynb` và chọn kernel của `.venv`.

## Dữ liệu và định nghĩa

- 120 khách, 6 sản phẩm, 1.000 đơn giả lập trong năm 2025; seed 42 để tái lập.
- `customers` → `orders` → `order_items` ← `products`.
- View `sales` chỉ gồm đơn `completed`; đơn `cancelled` không đóng góp doanh thu.
- Doanh thu = số lượng × đơn giá tại thời điểm mua; đơn vị VND, lưu số nguyên.
- Giá trị trung bình mỗi đơn = tổng doanh thu / số đơn hoàn tất, không phải trung bình dòng hàng.
- Dữ liệu giả lập để học; không dùng kết quả để kết luận về thị trường. Chưa có chi phí, hoàn trả, thuế hoặc chiết khấu.

`prepare_data.py` tạo lại CSV và dựng lại các bảng trong `database/analysis.db` mỗi lần chạy. Để giữ dữ liệu thật, hãy sử dụng database khác và viết bước nhập riêng.

## Cấu trúc

```text
data/raw/                   CSV mẫu được tạo bằng seed cố định
database/                   SQLite database được tạo khi chạy
sql/schema.sql              Schema, constraints, view và indexes
sql/analysis.sql            Ví dụ GROUP BY, JOIN, CTE và LAG
src/prepare_data.py         Tạo dữ liệu và nhập SQLite
src/analyze.py              Xuất bảng, biểu đồ và báo cáo
notebooks/02_analysis.ipynb  Hướng dẫn phân tích từng bước
outputs/                    Kết quả chạy; không đưa vào Git
docs/exercises.md           Bài tập từ cơ bản đến nâng cao
```

## Lộ trình học

1. Đọc schema, xác định khóa chính/khóa ngoại và mức chi tiết của mỗi bảng.
2. Chạy notebook; kiểm tra null, trùng lặp và tổng doanh thu.
3. Viết lại truy vấn trong `sql/analysis.sql` trước khi xem lời giải.
4. Giải thích năm biểu đồ bằng số liệu, rồi làm bài tập trong `docs/exercises.md`.
5. Thay dữ liệu giả lập bằng dữ liệu thật và ghi rõ các giới hạn mới.

## Đưa lên GitHub

Repo local dùng nhánh `main`. Sau khi có kết nối GitHub, có thể tạo remote và đẩy mã. Nếu đã cài, đăng nhập GitHub CLI và đứng tại repo:

```bash
gh repo create sales-analysis-lab --private --source=. --remote=origin --push
```

Mặc định ví dụ dùng repo riêng tư; chuyển `--private` thành `--public` nếu muốn chia sẻ portfolio công khai.
