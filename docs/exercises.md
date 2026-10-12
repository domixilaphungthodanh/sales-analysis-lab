# Bài tập

## Cơ bản

1. Đếm đơn hoàn tất và đơn hủy. Tính tỷ lệ hủy trên toàn bộ đơn.
2. Tìm ba sản phẩm bán nhiều nhất theo số lượng; so sánh với thứ hạng doanh thu.
3. Tính doanh thu theo tháng bằng SQL rồi bằng pandas, kiểm tra hai kết quả bằng nhau.

## Trung cấp

4. Tính doanh thu, số khách mua và doanh thu trên mỗi khách theo khu vực.
5. Dùng CTE tìm khách có ít nhất ba đơn hoàn tất.
6. Dùng LAG tính thay đổi doanh thu theo tháng. Vì sao tháng đầu có NULL?
7. So sánh mean và median giá trị đơn; dùng histogram và boxplot giải thích.

## Nâng cao

8. Xếp hạng sản phẩm theo doanh thu trong từng danh mục bằng DENSE_RANK.
9. Tạo heatmap cohort: hàng = tháng mua đầu, cột = số tháng từ lần mua đầu; giá trị = tỷ lệ khách quay lại. Để trống các tháng chưa quan sát, không điền 0.
10. Viết báo cáo gồm câu hỏi, phương pháp, ba phát hiện, hai đề xuất và giới hạn dữ liệu. Không suy ra quan hệ nhân quả từ tương quan.

## Tiêu chí tự kiểm tra

- Chỉ đơn hoàn tất được tính doanh thu.
- Không đếm số dòng hàng như số đơn.
- Tổng doanh thu theo tháng, sản phẩm và đơn phải bằng nhau.
- Biểu đồ có tiêu đề, đơn vị và trục rõ ràng.
- Phân biệt phát hiện trên dữ liệu giả lập với kết luận về thực tế.
