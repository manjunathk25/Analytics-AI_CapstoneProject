import sqlite3
import os

OUTDIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(OUTDIR, "urban_service.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM categories")
categories_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM partners_import")
partners_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM bookings")
bookings_count = cur.fetchone()[0]

conn.close()

output_content = f"""#Verification Results:
#categories: {categories_count}
#partners_import: {partners_count}
#bookings: {bookings_count}"""

output_path = os.path.join(OUTDIR, "verify_output.txt")
with open(output_path, "w") as f:
  f.write(output_content)

print(f"Results written to {output_path}")