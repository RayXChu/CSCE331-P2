#!/usr/bin/env python3
import csv
import random
from datetime import datetime, date, time, timedelta

OUTFILE = "saleshistory.csv"
TARGET_REVENUE = 750_000.00

MIN_ORDERS_PER_DAY = 100
MAX_ORDERS_PER_DAY = 300
PEAK_ORDERS_MIN = 3000
PEAK_ORDERS_MAX = 6000

PRICE_MIN = 8.00
PRICE_MAX = 12.00

END_DATE = datetime.today().date()
START_DATE = END_DATE - timedelta(days=365)

def iter_days(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)

def pick_peak_day(start: date, end: date) -> date:
    aug_start = date(end.year, 8, 15)
    aug_end = date(end.year, 9, 10)
    jan_start = date(end.year, 1, 10)
    jan_end = date(end.year, 1, 25)

    def choose_in_range(a: date, b: date):
        lo = max(start, a)
        hi = min(end, b)
        if lo <= hi:
            delta = (hi - lo).days
            return lo + timedelta(days=random.randint(0, delta))
        return None

    c1 = choose_in_range(aug_start, aug_end)
    if c1: return c1
    c2 = choose_in_range(jan_start, jan_end)
    if c2: return c2
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

PEAK_DAY = pick_peak_day(START_DATE, END_DATE)
PEAK_ORDERS = random.randint(PEAK_ORDERS_MIN, PEAK_ORDERS_MAX)

def rand_time_in_day(d: date) -> datetime:
    open_dt = datetime.combine(d, time(8, 0, 0))
    close_dt = datetime.combine(d, time(21, 30, 0))
    span = int((close_dt - open_dt).total_seconds())
    return open_dt + timedelta(seconds=random.randint(0, span))

def choose_unit_price() -> float:
    return round(random.uniform(PRICE_MIN, PRICE_MAX), 2)

def choose_drink_id() -> int:
    return random.randint(1, 16)

def choose_topping_id() -> int:
    return random.randint(0, 4)

def main():
    sale_id = 1
    total_revenue = 0.0
    rows = []
    day_order_counter = {}

    for d in iter_days(START_DATE, END_DATE):
        day_key = d.isoformat()
        day_order_counter[day_key] = 0
        planned_orders = PEAK_ORDERS if d == PEAK_DAY else random.randint(MIN_ORDERS_PER_DAY, MAX_ORDERS_PER_DAY)
        for _ in range(planned_orders):
            day_order_counter[day_key] += 1
            order_id = day_order_counter[day_key]
            order_time = rand_time_in_day(d)
            drink_id = choose_drink_id()
            topping_id = choose_topping_id()
            price = choose_unit_price()
            rows.append([
                sale_id,
                order_id,
                order_time.strftime("%Y-%m-%d %H:%M:%S"),
                drink_id,
                topping_id,
                f"{price:.2f}",
            ])
            total_revenue += price
            sale_id += 1

    while total_revenue < TARGET_REVENUE:
        d = END_DATE
        day_key = d.isoformat()
        if day_key not in day_order_counter:
            day_order_counter[day_key] = 0
        day_order_counter[day_key] += 1
        order_id = day_order_counter[day_key]
        order_time = rand_time_in_day(d)
        drink_id = choose_drink_id()
        topping_id = choose_topping_id()
        price = choose_unit_price()
        rows.append([
            sale_id,
            order_id,
            order_time.strftime("%Y-%m-%d %H:%M:%S"),
            drink_id,
            topping_id,
            f"{price:.2f}",
        ])
        total_revenue += price
        sale_id += 1

    with open(OUTFILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "sale_id",
            "order_id",
            "time",
            "drink_id",
            "topping_id",
            "price",
        ])
        writer.writerows(rows)

    print(f"Wrote {len(rows):,} rows to {OUTFILE}.")
    print(f"Total revenue: ${total_revenue:,.2f}")
    print(f"Date range: {START_DATE} to {END_DATE}")
    # print(f"Peak day: {PEAK_DAY} with {PEAK_ORDERS} orders")
    # print("order_id resets to 1 each day; sale_id is globally unique.")

if __name__ == "__main__":
    main()
