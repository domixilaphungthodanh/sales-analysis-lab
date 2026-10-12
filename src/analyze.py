"""Query SQLite, export result tables, and draw five Seaborn figures."""
from pathlib import Path
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]


def main():
    db = ROOT / 'database' / 'analysis.db'
    if not db.exists():
        raise SystemExit('Run python src/prepare_data.py first.')
    output = ROOT / 'outputs'
    for folder in ['figures', 'tables']:
        (output / folder).mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(f'{db.as_uri()}?mode=ro', uri=True) as conn:
        sales = pd.read_sql_query('SELECT * FROM sales', conn, parse_dates=['order_date'])
        monthly = pd.read_sql_query("SELECT strftime('%Y-%m', order_date) AS month, SUM(revenue_vnd) AS revenue_vnd FROM sales GROUP BY month ORDER BY month", conn)
        products = pd.read_sql_query('SELECT product_name, SUM(revenue_vnd) AS revenue_vnd FROM sales GROUP BY product_name ORDER BY revenue_vnd DESC', conn)
        orders = pd.read_sql_query('SELECT order_id, region, SUM(revenue_vnd) AS total_vnd FROM sales GROUP BY order_id, region', conn)
    if sales.empty:
        raise SystemExit('No completed sales found.')
    assert sales['revenue_vnd'].sum() == monthly['revenue_vnd'].sum() == orders['total_vnd'].sum()
    for name, frame in [('monthly_revenue', monthly), ('product_revenue', products), ('order_totals', orders)]:
        frame.to_csv(output / 'tables' / f'{name}.csv', index=False)
    sns.set_theme(style='whitegrid')

    def save(name):
        plt.tight_layout()
        plt.savefig(output / 'figures' / f'{name}.png', dpi=160)
        plt.close()

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly, x='month', y=monthly['revenue_vnd'] / 1e6, marker='o')
    plt.ylabel('Revenue (million VND)')
    plt.title('Monthly revenue — synthetic data, 2025')
    plt.xticks(rotation=45)
    save('01_monthly_revenue')

    plt.figure(figsize=(9, 5))
    sns.barplot(data=products, x=products['revenue_vnd'] / 1e6, y='product_name', color='#3282b8')
    plt.xlabel('Revenue (million VND)')
    plt.ylabel('Product')
    plt.title('Revenue by product')
    save('02_product_revenue')

    plt.figure(figsize=(9, 5))
    sns.histplot(orders['total_vnd'] / 1e6, bins=25)
    plt.xlabel('Order value (million VND)')
    plt.title('Distribution of completed order values')
    save('03_order_distribution')

    plt.figure(figsize=(9, 5))
    sns.boxplot(data=orders, x='region', y=orders['total_vnd'] / 1e6)
    plt.ylabel('Order value (million VND)')
    plt.title('Order value by customer region')
    save('04_region_comparison')

    sales['month'] = sales['order_date'].dt.strftime('%Y-%m')
    grid = sales.pivot_table(index='category', columns='month', values='revenue_vnd', aggfunc='sum', fill_value=0) / 1e6
    plt.figure(figsize=(12, 4))
    sns.heatmap(grid, annot=True, fmt='.1f', cmap='Blues', cbar_kws={'label': 'Million VND'})
    plt.title('Revenue by category and month')
    save('05_category_heatmap')

    best = monthly.loc[monthly['revenue_vnd'].idxmax()]
    report = f'''# Báo cáo dữ liệu giả lập\n\nDữ liệu năm 2025, seed 42. Chỉ tính đơn hoàn tất; giá trị tiền là VND.\n\n- Doanh thu: {int(orders.total_vnd.sum()):,} VND.\n- Đơn hoàn tất: {len(orders):,}.\n- Giá trị trung bình một đơn: {orders.total_vnd.mean():,.0f} VND.\n- Tháng doanh thu cao nhất: {best['month']}, {int(best['revenue_vnd']):,} VND.\n- Sản phẩm doanh thu cao nhất: {products.iloc[0]['product_name']}.\n\n## Bài tập tiếp theo\n\n1. Giải thích vì sao sản phẩm dẫn đầu doanh thu có thể không dẫn đầu số lượng.\n2. So sánh tổng doanh thu và doanh thu trung bình trên mỗi khách theo khu vực.\n3. Viết ba nhận xét có số liệu và hai đề xuất cần kiểm chứng bằng dữ liệu thật.\n\n## Giới hạn\n\nDữ liệu ngẫu nhiên phục vụ học tập, không phản ánh thị trường. Không có chi phí, thuế, hoàn trả hay chiết khấu; doanh thu không phải lợi nhuận. Một năm dữ liệu không đủ xác nhận tính mùa vụ.\n'''
    (output / 'report.md').write_text(report, encoding='utf-8')
    print('Exported 5 figures, 3 tables and outputs/report.md')


if __name__ == '__main__':
    main()
