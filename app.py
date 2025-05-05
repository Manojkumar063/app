# app.py

import streamlit as st
from datetime import datetime, timedelta
import calendar
from collections import defaultdict

# ---------- Function to calculate monthly bill ----------
def generate_monthly_bill(item_list: list, target_month: str) -> dict:
    year, month = map(int, target_month.split('-'))
    month_start = datetime(year, month, 1)
    month_end = datetime(year, month, calendar.monthrange(year, month)[1])
    days_in_month = (month_end - month_start).days + 1

    grouped_items = defaultdict(lambda: {"qty": 0, "amount": 0.0})
    
    for item in item_list:
        try:
            item_start = datetime.strptime(item["start_date"], "%Y-%m-%d")
            item_stop = datetime.strptime(item["stop_date"], "%Y-%m-%d")
        except:
            continue  # Skip invalid dates

        # Check if active during target month
        if item_start > month_end or item_stop < month_start:
            continue

        # Compute overlapping billing period
        bill_start = max(item_start, month_start)
        bill_end = min(item_stop, month_end)
        active_days = (bill_end - bill_start).days + 1
        if active_days <= 0:
            continue

        try:
            rate = float(item["rate"])
            qty = int(item["qty"])
        except:
            continue

        # Pro-rate the amount
        amount = round((active_days / days_in_month) * rate * qty, 2)
        billing_period = f"{bill_start.strftime('%Y-%m-%d')} to {bill_end.strftime('%Y-%m-%d')}"
        key = (item["item_code"], rate, billing_period)

        grouped_items[key]["qty"] += qty
        grouped_items[key]["amount"] += amount

    line_items = []
    total_revenue = 0.0
    for (item_code, rate, billing_period), values in grouped_items.items():
        line = {
            "item_code": item_code,
            "rate": rate,
            "qty": values["qty"],
            "amount": round(values["amount"], 2),
            "billing_period": billing_period
        }
        line_items.append(line)
        total_revenue += line["amount"]

    return {
        "line_items": line_items,
        "total_revenue": round(total_revenue, 2)
    }

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Monthly Bill Generator", layout="wide")
st.title("📅 Monthly Bill Generator")

# Sample item list (can replace with uploaded file or DB)
item_list = [  # Use the full item_list you provided
    {
        "idx": 1,
        "item_code": "Executive Desk (4*2)",
        "sales_description": "Dedicated Executive Desk",
        "qty": 10,
        "rate": "1000",
        "amount": "10000",
        "start_date": "2023-11-01",
        "stop_date": "2024-10-17",
    },
    {
        "idx": 2,
        "item_code": "Executive Desk (4*2)",
        "qty": "10",
        "rate": "1080",
        "amount": "10800",
        "start_date": "2024-10-18",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 3,
        "item_code": "Executive Desk (4*2)",
        "qty": 15,
        "rate": "1080",
        "amount": "16200",
        "start_date": "2024-11-01",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 4,
        "item_code": "Executive Desk (4*2)",
        "qty": 5,
        "rate": "1000",
        "amount": "5000",
        "start_date": "2024-11-01",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 5,
        "item_code": "Manager Cabin",
        "qty": 5,
        "rate": 5000,
        "amount": 25000,
        "start_date": "2024-11-01",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 6,
        "item_code": "Manager Cabin",
        "qty": 7,
        "rate": "5000",
        "amount": 35000,
        "start_date": "2024-12-15",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 7,
        "item_code": "Manager Cabin",
        "qty": 10,
        "rate": 4600,
        "amount": 46000,
        "start_date": "2023-11-01",
        "stop_date": "2024-10-17",
    },
    {
        "idx": 8,
        "item_code": "Parking (2S)",
        "qty": 10,
        "rate": 1000,
        "amount": 10000,
        "start_date": "2024-11-01",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 9,
        "item_code": "Parking (2S)",
        "qty": 10,
        "rate": 0,
        "amount": 0,
        "start_date": "2024-11-01",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 10,
        "item_code": "Executive Desk (4*2)",
        "qty": "8",
        "rate": "1100",
        "amount": "8800",
        "start_date": "2024-11-15",
        "stop_date": "2025-01-31",
    },
    {
        "idx": 11,
        "item_code": "Manager Cabin",
        "qty": "3",
        "rate": "5200",
        "amount": "15600",
        "start_date": "2024-10-10",
        "stop_date": "2024-11-10",
    },
    {
        "idx": 12,
        "item_code": "Conference Table",
        "qty": 1,
        "rate": "20000",
        "amount": "20000",
        "start_date": "2024-11-05",
        "stop_date": "2024-11-20",
    },
    {
        "idx": 13,
        "item_code": "Parking (2S)",
        "qty": 5,
        "rate": "1000",
        "amount": "5000",
        "start_date": "2024-11-15",
        "stop_date": "2025-02-28",
    },
    {
        "idx": 14,
        "item_code": "Reception Desk",
        "qty": 2,
        "rate": "7000",
        "amount": "14000",
        "start_date": "2024-11-01",
        "stop_date": "2025-03-31",
    },
    {
        "idx": 15,
        "item_code": "Reception Desk",
        "qty": 1,
        "rate": "7000",
        "amount": "7000",
        "start_date": "2024-11-10",
        "stop_date": "2024-11-25",
    },
    {
        "idx": 16,
        "item_code": "Breakout Area",
        "qty": 3,
        "rate": "3000",
        "amount": "9000",
        "start_date": "2024-01-01",
        "stop_date": "2024-01-31",
    }
]

# Streamlit input
target_month = st.text_input("Enter target month (YYYY-MM):", "2024-11")

if st.button("Generate Bill"):
    bill = generate_monthly_bill(item_list, target_month)

    st.subheader("📋 Line Items")
    st.dataframe(bill["line_items"])

    st.subheader("💰 Total Revenue")
    st.success(f"₹ {bill['total_revenue']:.2f}")
