import random
import sqlite3
import csv
import os

random.seed(2604)

OUTDIR = os.path.dirname(os.path.abspath(__file__))

CITIES = ["Bengaluru", "Mumbai", "Delhi NCR", "Pune", "Hyderabad", "Chennai"]
ACTIVE_CATEGORIES = ["AC Repair & Service",
                     "Salon for Women",
                     "Salon for Men",
                     "Deep Home Cleaning",
                     "Plumbing",
                     "Electrical Repair"
                    ]
HELD_OUT_CATEGORY = "Pest Control"
ALL_CATEGORIES = ACTIVE_CATEGORIES + [HELD_OUT_CATEGORY]
CATEGORY_PRICE_RANGE = {"AC Repair & Service": (499, 2499),
                        "Salon for Women": (699, 3499),
                        "Salon for Men": (349, 1499),
                        "Deep Home Cleaning": (999, 4999),
                        "Plumbing": (199, 1499),
                        "Electrical Repair": (199, 1999)
                      }
CATEGORY_WEIGHTS = [0.22, 0.20, 0.14, 0.18, 0.14, 0.12]

PARTNERS = []
partner_seq = 1

for city in CITIES:
  for _ in range(8):
    pid = f"P{partner_seq:03d}"
    cat = random.choices(ACTIVE_CATEGORIES, weights=CATEGORY_WEIGHTS, k=1)[0]
    rating = round(random.uniform(3.4, 5.0), 1)
    PARTNERS.append({
      "partner_id": pid,
      "city": city,
      "primary_category": cat,
      "rating": rating,
      "active": True,
      "days_since_onboarding": random.randint(30, 500)
    })
    partner_seq += 1

IDLE_PARTNER_ID = f"P{partner_seq:03d}"
PARTNERS.append({
  "partner_id": IDLE_PARTNER_ID,
  "city": "Pune",
  "primary_category": "Plumbing",
  "rating": 0.0,
  "active": True,
  "days_since_onboarding": 4
})
partner_seq += 1

PARTNER_BY_ID = {p["partner_id"]: p for p in PARTNERS}
PARTNERS_BY_CITY = {}
for p in PARTNERS:
  if p["partner_id"] == IDLE_PARTNER_ID:
    continue
  else:
    PARTNERS_BY_CITY.setdefault(p["city"], []).append(p["partner_id"])

N_BOOKINGS = 600
BOOKINGS = []
STATUS_CHOICES = ["Paid", "Refunded", "Pending"]
STATUS_WEIGHTS = [0.82, 0.10, 0.08]

for booking_seq in range(1, N_BOOKINGS + 1):
  city = random.choice(CITIES)
  partner_id = random.choice(PARTNERS_BY_CITY[city])
  partner = PARTNER_BY_ID[partner_id]
  category = partner["primary_category"]
  lo, hi = CATEGORY_PRICE_RANGE[category]
  amount = random.randint(lo, hi)
  year = 2026
  day = random.randint(1, 90)
  month_days = [31, 29 if(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28, 31]
  day_in_month = day
  for m in range(1, 4):
    if day_in_month <= month_days[m-1]:
      break
    else:
      day_in_month -= month_days[m-1]
  booking_date = f"{year}-{m:02d}-{day_in_month:02d}"
  status = random.choices(STATUS_CHOICES, weights=STATUS_WEIGHTS, k=1)[0]
  complaint_flag = 1 if random.random() < 0.12 else 0
  sla_breach_flag = 1 if random.random() < 0.15 else 0
  
  if status == "Pending":
    customer_rating = None
  else:
    base = 4.3 - (1.4 if complaint_flag else 0) - (0.6 if sla_breach_flag else 0)
    customer_rating = max(1, min(5, round(base + random.uniform(-0.6, 0.6))))

  is_test = 1 if booking_seq in (37, 214, 507) else 0

  BOOKINGS.append({
    "booking_id": f"B{booking_seq:04d}",
    "partner_id": partner_id,
    "city": city,
    "category": category,
    "booking_date": booking_date,
    "amount_inr": amount,
    "complaint_flag": complaint_flag,
    "sla_breach_flag": sla_breach_flag,
    "is_test": is_test
  })

DUPLICATED_IDS = ["P003", "P017", "P031"]
import_rows = list(PARTNERS)

for pid in DUPLICATED_IDS:
  import_rows.append(dict(PARTNER_BY_ID[pid]))
random.shuffle(import_rows)

def write_csv(filename, rows, fieldnames):
  with open(os.path.join(OUTDIR, filename), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

write_csv("cities.csv", [{"city": c} for c in CITIES], ["city"])
write_csv("categories.csv", [{"category": c} for c in ALL_CATEGORIES], ["category"])
write_csv("partners_import.csv",
          import_rows,
          ["partner_id",
           "city",
           "primary_category",
           "rating",
           "active",
           "days_since_onboarding"
          ])
write_csv("bookings.csv",
          BOOKINGS,
          ["booking_id",
           "partner_id",
           "city",
           "category",
           "booking_date",
           "amount_inr",
           "complaint_flag",
           "sla_breach_flag",
           "is_test"])

db_path = os.path.join(OUTDIR, "urban_service.db")
if os.path.exists(db_path):
  os.remove(db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("CREATE TABLE categories(category TEXT PRIMARY KEY)")
cur.executemany("INSERT INTO categories VALUES(?)", [(c,) for c in ALL_CATEGORIES])

cur.execute("""CREATE TABLE partners_import(partner_id TEXT, city TEXT,
primary_category TEXT, rating REAL, active INTEGER, days_since_onboarding INTEGER)""")
cur.executemany("INSERT INTO partners_import VALUES(?,?,?,?,?,?)",
                [
                  (
                    r["partner_id"],
                    r["city"],
                    r["primary_category"],
                    r["rating"],
                    1 if r["active"] else 0,
                    r["days_since_onboarding"]
                  )
                  for r in import_rows
                ])

cur.execute("""CREATE TABLE bookings(booking_id TEXT PRIMARY KEY, partner_id TEXT,
city TEXT, category TEXT, booking_date TEXT, amount_inr INTEGER, complaint_flag INTEGER,
sla_breach_flag INTEGER, is_test INTEGER)""")
cur.executemany("INSERT INTO bookings VALUES(?,?,?,?,?,?,?,?,?)",
                [
                  (
                    b["booking_id"],
                    b["partner_id"],
                    b["city"],
                    b["category"],
                    b["booking_date"],
                    b["amount_inr"],
                    b["complaint_flag"],
                    b["sla_breach_flag"],
                    b["is_test"]
                  )
                  for b in BOOKINGS
                ])

conn.commit()
conn.close()

print("urban_service.db created with categories, partners_import, bookings tables.")