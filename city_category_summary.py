import sqlite3
import csv
import os

OUTDIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.abspath("urban_service.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""SELECT city, category, COUNT(*) bookings_count,
SUM(amount_inr) revenue_inr, SUM(sla_breach_flag) sla_breaches
FROM bookings
GROUP BY city, category
ORDER BY city, category""")

data = cur.fetchall()

def write_csv(filename, rows, headers):
  file_path = os.path.join(OUTDIR, filename)
  with open(file_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(headers)
    w.writerows(rows)

write_csv("city_category_summary.csv",
          data,
          [
            "city",
            "category",
            "bookings_count",
            "revenue_inr",
            "sla_breaches"
          ]
        )

conn.close()