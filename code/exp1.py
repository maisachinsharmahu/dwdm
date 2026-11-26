import json
import sqlite3
from datetime import datetime

sales_rows = [
    "1001, rahul sharma ,india,Laptop,1,55000,05-01-2025",
    "1002,PRIYA VERMA,IN,Mobile,2,18000,2025/01/07",
    "1003,john  smith,U.S.A,Laptop,1,62000,2025-01-09",
    "1004,aman gupta,India,Tablet,,21000,10-01-2025",
    "1005,sara khan,united states,Mobile,1,-500,2025-01-12",
    "1006,Rahul Sharma,INDIA,Mobile,3,18000,2025-01-15",
]
crm_json = json.loads("""[
  {"name": "Rahul Sharma", "segment": "Gold"},
  {"name": "Priya Verma",  "segment": "Silver"},
  {"name": "John Smith",   "segment": "Silver"},
  {"name": "Aman Gupta",   "segment": "Bronze"}
]""")
print(f"[EXTRACT] {len(sales_rows)} rows from flat file, "
      f"{len(crm_json)} records from CRM json")

COUNTRY = {"india": "India", "in": "India", "u.s.a": "USA",
           "united states": "USA", "usa": "USA"}

def to_date(text):
    for fmt in ("%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None

segment = {c["name"]: c["segment"] for c in crm_json}
clean, rejected = [], []
for line in sales_rows:
    parts = [x.strip() for x in line.split(",")]
    oid, name, ctry, prod, qty, price, dt = parts
    name = " ".join(name.split()).title()
    ctry = COUNTRY[ctry.lower()]
    qty = int(qty) if qty else 1
    price = float(price)
    if price <= 0:
        rejected.append((oid, "price <= 0"))
        continue
    clean.append((int(oid), name, ctry, prod, qty, price, to_date(dt),
                  segment.get(name, "Unknown"), qty * price))
print(f"[TRANSFORM] {len(clean)} rows cleaned, {len(rejected)} rejected "
      f"{rejected}")

db = sqlite3.connect(":memory:")
db.execute("""CREATE TABLE fact_sales(order_id INT, customer TEXT,
              country TEXT, product TEXT, qty INT, price REAL,
              order_date TEXT, segment TEXT, amount REAL)""")
db.executemany("INSERT INTO fact_sales VALUES (?,?,?,?,?,?,?,?,?)", clean)
db.commit()
print("[LOAD] rows in warehouse table fact_sales:",
      db.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0])

print("\nWarehouse check: sales by country")
for row in db.execute("""SELECT country, COUNT(*), SUM(amount)
                         FROM fact_sales GROUP BY country"""):
    print(f"  {row[0]:<6} orders = {row[1]}   revenue = {row[2]:>10,.0f}")
print("\nSample of loaded data:")
for row in db.execute("SELECT order_id, customer, country, order_date, "
                      "segment, amount FROM fact_sales LIMIT 4"):
    print(" ", row)
