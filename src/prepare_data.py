"""Create deterministic synthetic sales CSVs and rebuild a SQLite database."""
from pathlib import Path
import csv
import random
import sqlite3
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]


def main():
    rng = random.Random(42)
    raw = ROOT / 'data' / 'raw'
    raw.mkdir(parents=True, exist_ok=True)
    (ROOT / 'database').mkdir(exist_ok=True)
    products = [
        (1, 'Notebook', 'Stationery', 35000),
        (2, 'Pen set', 'Stationery', 25000),
        (3, 'Desk lamp', 'Home', 220000),
        (4, 'Water bottle', 'Home', 150000),
        (5, 'Mouse', 'Electronics', 180000),
        (6, 'Keyboard', 'Electronics', 450000),
    ]
    customers = [(i, f'Customer {i:03d}', rng.choice(['North', 'Central', 'South'])) for i in range(1, 121)]
    orders, items = [], []
    for order_id in range(1, 1001):
        day = date(2025, 1, 1) + timedelta(days=rng.randrange(365))
        status = 'cancelled' if rng.random() < 0.08 else 'completed'
        orders.append((order_id, rng.randrange(1, 121), day.isoformat(), status))
        for product in rng.sample(products, rng.randint(1, 3)):
            items.append((len(items) + 1, order_id, product[0], rng.randint(1, 4), product[3]))
    datasets = {
        'customers': (['customer_id', 'customer_name', 'region'], customers),
        'products': (['product_id', 'product_name', 'category', 'list_price_vnd'], products),
        'orders': (['order_id', 'customer_id', 'order_date', 'status'], orders),
        'order_items': (['item_id', 'order_id', 'product_id', 'quantity', 'unit_price_vnd'], items),
    }
    for name, (columns, rows) in datasets.items():
        with (raw / f'{name}.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)
    with sqlite3.connect(ROOT / 'database' / 'analysis.db') as conn:
        conn.execute('PRAGMA foreign_keys = ON')
        conn.executescript((ROOT / 'sql' / 'schema.sql').read_text(encoding='utf-8'))
        for table, (columns, _) in datasets.items():
            with (raw / f'{table}.csv').open(newline='', encoding='utf-8') as f:
                rows = csv.reader(f)
                next(rows)
                marks = ','.join('?' for _ in columns)
                conn.executemany(f'INSERT INTO {table} VALUES ({marks})', rows)
        assert not conn.execute('PRAGMA foreign_key_check').fetchall()
        assert conn.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    print('Created 1,000 synthetic orders and database/analysis.db')


if __name__ == '__main__':
    main()
