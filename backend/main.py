from datetime import date
from typing import Optional

import pandas as pd
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.anomaly import flag_anomalies
from src.data import load_data
from src.forecast import forecast_next_month

app = FastAPI(title="Spend Analytics API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# A straight-line trend needs at least this many months of data to mean anything.
MIN_FORECAST_MONTHS = 3 

# Load the CSV and flag unusual orders ONCE, when the server starts.
# df = flag_anomalies(load_data())
df = flag_anomalies(load_data(), contamination=0.015)


def filter_data(
    vendor: Optional[str] = None,
    category: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    """Return only the rows that match the filters the caller sent."""
    data = df
    if vendor:
        data = data[data["vendor"] == vendor]
    if category:
        data = data[data["category"] == category]
    if department:
        data = data[data["department"] == department]
    if status:
        data = data[data["status"] == status]
    if start_date:
        data = data[data["po_date"] >= pd.Timestamp(start_date)]
    if end_date:
        data = data[data["po_date"] <= pd.Timestamp(end_date)]
    return data


def spend_by(data, column):
    """Add up total_amount for each value of `column`, biggest first."""
    grouped = (
        data.groupby(column)["total_amount"]
        .sum() 
        .round(2)
    )
    return [{column: name, "total_spend": float(value)} for name, value in grouped.items()]


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/filters")
def filters():
    """The real values to show in the dropdowns (always from the full data)."""
    return {
        "vendors": sorted(df["vendor"].unique().tolist()),
        "categories": sorted(df["category"].unique().tolist()),
        "departments": sorted(df["department"].unique().tolist()),
        "statuses": sorted(df["status"].unique().tolist()),
        "min_date": df["po_date"].min().strftime("%Y-%m-%d"),
        "max_date": df["po_date"].max().strftime("%Y-%m-%d"),
    }


@app.get("/api/summary")
def summary(data: pd.DataFrame = Depends(filter_data)):
    return {
        "total_spend": round(float(data["total_amount"].sum()), 2),
        "orders": int(len(data)),
        "vendors": int(data["vendor"].nunique()),
        "flagged_orders": int(data["is_anomaly"].sum()),
    }


@app.get("/api/spend/vendor")
def spend_by_vendor(data: pd.DataFrame = Depends(filter_data)):
    return spend_by(data, "vendor")


@app.get("/api/spend/category")
def spend_by_category(data: pd.DataFrame = Depends(filter_data)):
    return spend_by(data, "category")


@app.get("/api/spend/monthly")
def spend_by_month(data: pd.DataFrame = Depends(filter_data)):
    grouped = data.groupby("month")["total_amount"].sum().round(2)
    return [
        {"month": month.strftime("%Y-%m"), "total_spend": float(value)}
        for month, value in grouped.items()
    ]


@app.get("/api/anomalies")
def anomalies(data: pd.DataFrame = Depends(filter_data)):
    """Orders the Isolation Forest flagged as unusual, biggest first."""
    columns = ["po_number", "po_date", "vendor", "category", "item",
               "quantity", "unit_price", "total_amount"]
    flagged = data[data["is_anomaly"]].sort_values("total_amount", ascending=False)
    rows = flagged[columns].copy()
    rows["po_date"] = rows["po_date"].dt.strftime("%Y-%m-%d")
    return rows.to_dict(orient="records")


# @app.get("/api/forecast")
# def forecast(data: pd.DataFrame = Depends(filter_data)):
#     """Next month's predicted spend per category (flagged orders left out)."""
#     normal_orders = data[~data["is_anomaly"]]
#     if normal_orders["month"].nunique() < MIN_FORECAST_MONTHS:
#         return {
#             "next_month": None,
#             "forecast": [],
#             "message": f"Need at least {MIN_FORECAST_MONTHS} months of data to forecast.",
#         }
#     result, next_month = forecast_next_month(normal_orders)
#     result = result.sort_values(ascending=False).round(0)
#     return {
#         "next_month": next_month.strftime("%Y-%m"),
#         "forecast": [
#             {"category": category, "forecast_spend": float(value)}
#             for category, value in result.items()
#         ],
#         "message": None,
#     }

@app.get("/api/forecast")
def forecast(data: pd.DataFrame = Depends(filter_data)):

    normal_orders = data[~data["is_anomaly"]]

    if normal_orders["month"].nunique() < MIN_FORECAST_MONTHS:
        return {
            "next_month": None,
            "forecast": [],
            "message": f"Need at least {MIN_FORECAST_MONTHS} months of data to forecast."
        }

    result, next_month = forecast_next_month(normal_orders)

    result = result.sort_values(ascending=False).round(0)

    return {
        "next_month": next_month.strftime("%Y-%m"),
        "forecast": [
            {
                "category": category,
                "forecast_spend": float(value)
            }
            for category, value in result.items()
        ],
        "message": None
    }


@app.get("/")
def home():
    return {
        "message": "Spend Analytics Dashboard API is running successfully!"
    }