"""Writes one CSV file per table into projects/db/data/ for VicFly.

Run from the root of the repository:
    uv run python projects/db/make_data.py
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(2026)  # same files every run

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

AS_OF = date(2026, 11, 5)            # the as_of date: data covers the 12 months up to it
START = AS_OF - timedelta(days=364)
LAST_BOOKED = AS_OF + timedelta(days=35)   # a few trips already booked after as_of


def write(name, header, rows):
    with open(DATA / f"{name}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}.csv: {len(rows)} rows")


# ---------- rivers (8 rivers, 6 states) ----------
rivers = [
    (1, "Deerfield River", "Western Massachusetts", "MA"),
    (2, "Swift River", "Central Massachusetts", "MA"),
    (3, "Farmington River", "Northwest Connecticut", "CT"),
    (4, "Battenkill", "Southwest Vermont", "VT"),
    (5, "Kennebec River", "Western Maine", "ME"),
    (6, "Deschutes River", "Central Oregon", "OR"),
    (7, "Yakima River", "Central Washington", "WA"),
    (8, "Skagit River", "Northwest Washington", "WA"),
]
species_by_river = {
    1: ["Brown trout", "Rainbow trout", "Brook trout"],
    2: ["Brown trout", "Rainbow trout", "Brook trout"],
    3: ["Brown trout", "Rainbow trout"],
    4: ["Brown trout", "Rainbow trout"],
    5: ["Landlocked salmon", "Brook trout", "Brown trout"],
    6: ["Redband trout", "Rainbow trout", "Brown trout"],
    7: ["Rainbow trout", "Cutthroat trout", "Brown trout"],
    8: ["Steelhead", "Cutthroat trout", "Rainbow trout"],
}

# ---------- guides (4) ----------
guides = [
    (1, "Mara", "Lindqvist", "GD-MA-1021", date(2019, 4, 2)),
    (2, "Theo", "Ramsey", "GD-CT-2210", date(2020, 3, 15)),
    (3, "Josie", "Okafor", "GD-OR-3307", date(2021, 5, 1)),
    (4, "Walt", "Brennan", "GD-WA-4415", date(2022, 4, 10)),
]

# ---------- flies (20) ----------
flies = [
    (1, "Adams", "14", "dry", 1.75), (2, "Parachute Adams", "16", "dry", 1.85),
    (3, "Elk Hair Caddis", "16", "dry", 1.90), (4, "Royal Wulff", "14", "dry", 2.10),
    (5, "Stimulator", "10", "dry", 2.40), (6, "Blue-Winged Olive", "18", "dry", 1.80),
    (7, "Griffith's Gnat", "20", "dry", 1.60), (8, "Hopper", "10", "dry", 2.50),
    (9, "Pheasant Tail", "18", "nymph", 1.70), (10, "Hare's Ear", "16", "nymph", 1.70),
    (11, "Prince Nymph", "14", "nymph", 1.95), (12, "Copper John", "16", "nymph", 2.20),
    (13, "San Juan Worm", "12", "nymph", 1.40), (14, "Pat's Rubber Legs", "8", "nymph", 2.30),
    (15, "Egg Pattern", "14", "nymph", 1.30), (16, "Woolly Bugger", "8", "streamer", 2.25),
    (17, "Zonker", "6", "streamer", 2.60), (18, "Clouser Minnow", "4", "streamer", 2.80),
    (19, "Mickey Finn", "8", "streamer", 2.20), (20, "Sculpin", "6", "streamer", 2.90),
]
UNUSED_FLIES = {19, 20}   # two flies the guides never used, so "nothing attached" has an answer
used_flies = [f[0] for f in flies if f[0] not in UNUSED_FLIES]

# ---------- clients (40) ----------
first = ["Alex", "Priya", "Marcus", "Elena", "Jordan", "Sam", "Nina", "Owen", "Dana", "Luis",
         "Hannah", "Victor", "Grace", "Isaac", "Mei", "Ben", "Tara", "Noah", "Rosa", "Eli"]
last = ["Carter", "Shah", "Bennett", "Vargas", "Nguyen", "Foster", "Ibrahim", "Reyes",
        "Walsh", "Kim", "Moreau", "Duarte", "Hale", "Sutton", "Park", "Mercer", "Quinn", "Boyd"]
names = set()
clients_base = []
while len(clients_base) < 40:
    fn, ln = random.choice(first), random.choice(last)
    if (fn, ln) in names:
        continue
    names.add((fn, ln))
    clients_base.append((fn, ln))
NEVER_BOOKED = set(random.sample(range(1, 41), 6))   # 6 clients who have never booked
weights = [0 if (i + 1) in NEVER_BOOKED else random.choice([1, 1, 2, 3, 5]) for i in range(40)]

# ---------- trips ----------
month_weight = {1: 0.3, 2: 0.3, 3: 0.6, 4: 1.2, 5: 1.5, 6: 1.6, 7: 1.2,
                8: 1.2, 9: 1.4, 10: 1.4, 11: 0.6, 12: 0.4}
days = [START + timedelta(days=i) for i in range((LAST_BOOKED - START).days + 1)]
day_w = [month_weight[d.month] * (1.6 if d.weekday() >= 5 else 1.0) for d in days]

trips = []
busy = set()   # (guide_id, date): a guide leads at most one trip a day
trip_id = 0
while len(trips) < 300:
    d = random.choices(days, weights=day_w)[0]
    g = random.choice(guides)[0]
    if (g, d) in busy:
        continue
    busy.add((g, d))
    trip_id += 1
    hours = random.choice([4, 6, 8])
    if d > AS_OF:
        status = "booked"
    else:
        status = random.choices(["completed", "cancelled"], weights=[88, 12])[0]
    river = random.choice(rivers)[0]
    trips.append([trip_id, g, river, d, f"{random.choice([5, 6, 7, 8, 9])}:00",
                  hours, random.choice([2, 3, 4]), 100 + 25 * hours, status])
trips.sort(key=lambda t: (t[3], t[0]))
for new_id, t in enumerate(trips, start=1):   # renumber in date order
    t[0] = new_id

# ---------- bookings: party sizes never pass max_anglers ----------
bookings = []
for t in trips:
    tid, cap, hours = t[0], t[6], t[5]
    rate = 60 + 40 * hours           # price per angler for this trip length
    k = random.choices([1, 2, 3], weights=[35, 45, 20])[0]
    left, chosen = cap, set()
    while left > 0 and len(chosen) < k:
        c = random.choices(range(1, 41), weights=weights)[0]
        if c in chosen:
            continue
        size = random.randint(1, min(left, 2))
        chosen.add(c)
        left -= size
        bookings.append([tid, c, size, rate * size])

# ---------- break the capacity rule in exactly two trips ----------
total_by_trip = {}
for b in bookings:
    total_by_trip[b[0]] = total_by_trip.get(b[0], 0) + b[2]
candidates = [t for t in trips if t[6] == 2 and t[8] == "completed" and total_by_trip.get(t[0]) == 2]
broken = random.sample(candidates, 2)
for t in broken:
    in_trip = {b[1] for b in bookings if b[0] == t[0]}
    extra = random.choice([c for c in range(1, 41) if c not in in_trip and c not in NEVER_BOOKED])
    bookings.append([t[0], extra, 1, 60 + 40 * t[5]])
print("Rule broken on purpose (booked party sizes above max_anglers):")
for t in broken:
    tot = sum(b[2] for b in bookings if b[0] == t[0])
    print(f"  trip_id {t[0]}: max_anglers {t[6]}, booked {tot}")
bookings.sort(key=lambda b: (b[0], b[1]))

# ---------- clients (join date before the first booking) ----------
first_trip_date = {}
trip_date = {t[0]: t[3] for t in trips}
for b in bookings:
    d = trip_date[b[0]]
    if b[1] not in first_trip_date or d < first_trip_date[b[1]]:
        first_trip_date[b[1]] = d
clients = []
for i, (fn, ln) in enumerate(clients_base, start=1):
    if i in first_trip_date:
        join = first_trip_date[i] - timedelta(days=random.randint(0, 90))
    else:
        join = START + timedelta(days=random.randint(0, 364))
    clients.append((i, fn, ln, f"{fn.lower()}.{ln.lower()}{i}@example.com",
                    f"555-01{i:02d}", join))

# ---------- trip_flies and catches (completed trips only) ----------
trip_flies, catches = [], []
catch_id = 0
for t in trips:
    if t[8] != "completed":
        continue
    tid, river = t[0], t[2]
    used = random.sample(used_flies, random.randint(1, 4))
    for f in used:
        trip_flies.append([tid, f, random.randint(1, 6)])
    if random.random() < 0.12:          # some completed trips caught nothing
        continue
    for _ in range(random.randint(1, 7)):
        catch_id += 1
        fly = random.choice(used) if random.random() > 0.15 else ""   # 15%: fly not recorded
        catches.append([catch_id, tid, fly, random.choice(species_by_river[river])])

# ---------- write ----------
write("clients", ["client_id", "first_name", "last_name", "email", "phone", "join_date"], clients)
write("guides", ["guide_id", "first_name", "last_name", "license_number", "hire_date"], guides)
write("rivers", ["river_id", "name", "region", "state"], rivers)
write("flies", ["fly_id", "pattern_name", "size", "fly_type", "cost"], flies)
write("trips", ["trip_id", "guide_id", "river_id", "trip_date", "start_time", "hours",
                "max_anglers", "guide_pay", "status"], trips)
write("bookings", ["trip_id", "client_id", "party_size", "price_charged"], bookings)
write("trip_flies", ["trip_id", "fly_id", "quantity_used"], trip_flies)
write("catches", ["catch_id", "trip_id", "fly_id", "species"], catches)