import sqlite3
import os

sample_bookings = [
 {"booking_id": "B0005", "category": "AC Repair & Service", "amount_inr": 1316},
 {"booking_id": "B0019", "category": "AC Repair & Service", "amount_inr": 538},
 {"booking_id": "B0027", "category": "AC Repair & Service", "amount_inr": 1016},
 {"booking_id": "B0055", "category": "AC Repair & Service", "amount_inr": 1505},
 {"booking_id": "B0001", "category": "Plumbing", "amount_inr": 1369},
 {"booking_id": "B0003", "category": "Plumbing", "amount_inr": 772},
 {"booking_id": "B0004", "category": "Plumbing", "amount_inr": 1133},
 {"booking_id": "B0006", "category": "Plumbing", "amount_inr": 805},
 {"booking_id": "B0018", "category": "Salon for Men", "amount_inr": 1414},
 {"booking_id": "B0024", "category": "Salon for Men", "amount_inr": 1176},
 {"booking_id": "B0029", "category": "Salon for Men", "amount_inr": 858},
 {"booking_id": "B0032", "category": "Salon for Men", "amount_inr": 638},
]

BOOKINGS_BY_CATEGORY = {}

for b in sample_bookings:
  data = BOOKINGS_BY_CATEGORY.setdefault(b["category"], {"no_of_bookings": 0, "total_amount_inr": 0})
  data["no_of_bookings"] += 1
  data["total_amount_inr"] += b["amount_inr"]

print("Python Results:")
print("-"*15)
for category, data in BOOKINGS_BY_CATEGORY.items():
  print(f"({category}, {data["no_of_bookings"]}, {data["total_amount_inr"]})")

db_path = os.path.abspath("urban_service.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""SELECT category, COUNT(*), SUM(amount_inr)
FROM bookings
WHERE booking_id IN("B0005", "B0019", "B0027", "B0055", "B0001", "B0003",
"B0004", "B0006", "B0018", "B0024", "B0029", "B0032") 
GROUP BY category""")

results = cur.fetchall()
print("-"*85)
print("SQL Results:")
print("-"*12)
print(results)