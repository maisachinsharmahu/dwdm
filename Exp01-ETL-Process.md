# Experiment 1: Study of ETL process and its tools

> **File:** `exp1.py`  |  **Tools:** Python 3.13 (json, sqlite3, datetime), MacOS

## 🎯 Aim

Study the ETL (Extract, Transform, Load) process and its tools, and demonstrate a small ETL pipeline.

## 📘 Theory

ETL is the process that fills a data warehouse. Data is first extracted from different source systems, then transformed into one clean and consistent format, and finally loaded into the warehouse where it can be used for reporting and mining. The data is first kept in a staging area so that a bad source can never damage the warehouse itself.

- **Extract**: read data from databases, flat files, spreadsheets, JSON/XML feeds and APIs into a staging area.
- **Transform**: clean (fix or remove wrong values), standardise (one format for dates, countries and names), join, split, filter, sort and calculate new fields.
- **Load**: write the final data into the warehouse tables, either as a full load or as an incremental load of only the new records.
- **ETL tools**: Informatica PowerCenter, Talend, Microsoft SSIS, Pentaho Data Integration, Apache NiFi, Apache Airflow and cloud services such as AWS Glue and Fivetran.
- **Choosing a tool**: check the number of supported connectors, the ease of customisation, speed, cost and the skills of the team.

## 🪜 Algorithm / Steps

1. Prepare two source datasets: a messy flat file of sales orders and a CRM file in JSON format.
2. Extract: read all rows of both sources into Python lists.
3. Transform: trim names, give a single spelling to countries, convert three date formats into one, fill a missing quantity, reject rows with a wrong price and add the customer segment from the CRM.
4. Load: create the fact_sales table in an SQLite database and insert the clean rows.
5. Verify the load by running SQL queries on the warehouse table.

## 💻 Code

```python
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
```

## 🖥️ Output

```text
[EXTRACT] 6 rows from flat file, 4 records from CRM json
[TRANSFORM] 5 rows cleaned, 1 rejected [('1005', 'price <= 0')]
[LOAD] rows in warehouse table fact_sales: 5

Warehouse check: sales by country
  India  orders = 4   revenue =    166,000
  USA    orders = 1   revenue =     62,000

Sample of loaded data:
  (1001, 'Rahul Sharma', 'India', '2025-01-05', 'Gold', 55000.0)
  (1002, 'Priya Verma', 'India', '2025-01-07', 'Silver', 36000.0)
  (1003, 'John Smith', 'USA', '2025-01-09', 'Silver', 62000.0)
  (1004, 'Aman Gupta', 'India', '2025-01-10', 'Bronze', 21000.0)
```

## ✅ Result

The pipeline extracted 6 sales rows and 4 CRM records. After transformation 5 rows were clean and 1 row (order 1005, price below zero) was rejected. The 5 rows were loaded into the warehouse and the query shows India with 4 orders (revenue 166,000) and USA with 1 order (revenue 62,000).

## 🎤 Viva Questions

**Q. What does ETL stand for?**  
A. Extract, Transform, Load.

**Q. What happens in the transform step?**  
A. The data is cleaned, converted to a common format, validated and combined with reference data.

**Q. Name some ETL tools.**  
A. Informatica PowerCenter, Talend, Microsoft SSIS, Pentaho Data Integration and Apache NiFi.

**Q. What is a fact table?**  
A. The central table of a star schema that stores the measurable events, such as fees or sales.

**Q. What is a dimension table?**  
A. A table that describes the facts, such as course, customer or date.

---
[⬅ Back to index](README.md)
