import streamlit as st

from src.data import load_data
from src.anomaly import flag_anomalies
from src.forecast import forecast_next_month

st.set_page_config(page_title="Spend Analytics", layout="wide")
st.title("Spend Analytics Dashboard")


@st.cache_data
def get_data():
    return load_data()


df = get_data()
df = flag_anomalies(df, contamination=0.015)

# ---------- HEADLINE NUMBERS ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total spend", f"{df['total_amount'].sum():,.0f}")
c2.metric("Orders", f"{len(df):,}")
c3.metric("Vendors", df["vendor"].nunique())
c4.metric("Flagged orders", int(df["is_anomaly"].sum()))

# ---------- SPEND CHARTS ----------
st.header("1. Spend Chart")
left, right = st.columns(2)
with left:
    st.subheader("By Vendor")
    st.bar_chart(df.groupby("vendor")["total_amount"].sum().sort_values(ascending=False))
with right:
    st.subheader("By Category")
    st.bar_chart(df.groupby("category")["total_amount"].sum().sort_values(ascending=False))

st.subheader("By Month")
st.bar_chart(df.groupby("month")["total_amount"].sum())

# ---------- ANOMALIES ----------
st.header("2. Unusual orders")
flagged = df[df["is_anomaly"]].sort_values("total_amount", ascending=False)
st.write(f"{len(flagged)} orders look unusual for their category.")
st.dataframe(
    flagged[["po_number", "po_date", "vendor", "category", "item",
             "quantity", "unit_price", "total_amount"]],
    width="stretch",
)

# ---------- FORECAST ----------
st.header("3. Forecast: next month's spend by category.")
# Leave out flagged orders so one huge order doesn't distort the trend
forecast, next_month = forecast_next_month(df[~df["is_anomaly"]])
st.write(f"Predicted spend for **{next_month:%B %Y}**")
st.bar_chart(forecast)
# st.dataframe(forecast.round(0).to_frame("forecast spend"))
# st.caption("Simple straight-line trend. It does not account for seasonal busy months.")

with st.expander("Show raw data"):
    st.dataframe(df)






















# import numpy as np
# import pandas as pd
# import streamlit as st
# from sklearn.ensemble import IsolationForest

# st.set_page_config(page_title="Spend Analytics", layout="wide")
# st.title("Spend Analytics Dashboard")


# # ---------- 1. LOAD DATA ----------
# @st.cache_data
# def load_data():
#     df = pd.read_csv("data/purchase_orders.csv", parse_dates=["po_date"])
#     # Turn each date into the first day of its month, e.g. 2025-03-17 -> 2025-03-01
#     df["month"] = df["po_date"].dt.to_period("M").dt.to_timestamp()
#     return df


# # ---------- 2. ANOMALY DETECTION ----------
# def flag_anomalies(df, contamination):
#     """Mark unusual orders. Each category is checked separately,
#     because a normal laptop order looks very different from a normal pen order."""
#     df = df.copy()
#     df["is_anomaly"] = False
#     for category, group in df.groupby("category"):
#         # log1p squashes big numbers so the model compares sizes fairly
#         features = np.log1p(group[["quantity", "unit_price"]])
#         model = IsolationForest(contamination=contamination, random_state=42)
#         model.fit(features)
#         df.loc[group.index, "is_anomaly"] = model.predict(features) == -1
#     return df


# # ---------- 3. FORECAST ----------
# def forecast_next_month(df):
#     """Draw a straight trend line through each category's monthly spend
#     and read off where it lands next month."""
#     monthly = df.pivot_table(
#         index="month", columns="category", values="total_amount", aggfunc="sum"
#     ).fillna(0)
#     x = np.arange(len(monthly))
#     results = {}
#     for category in monthly.columns:
#         slope, intercept = np.polyfit(x, monthly[category].values, 1)
#         results[category] = max(slope * len(monthly) + intercept, 0)
#     next_month = monthly.index[-1] + pd.offsets.MonthBegin(1)
#     return pd.Series(results, name="forecast"), next_month


# df = load_data()

# contamination = 0.015
# df = flag_anomalies(df, contamination)

# # # Sidebar control
# # st.sidebar.header("Settings")
# # contamination = st.sidebar.slider(
# #     "Share of orders to flag as unusual", 0.005, 0.05, 0.015, step=0.005,
# #     help="Higher = more orders get flagged",
# # )
# # df = flag_anomalies(df, contamination)

# # ---------- HEADLINE NUMBERS ----------
# c1, c2, c3, c4 = st.columns(4)
# c1.metric("Total spend", f"{df['total_amount'].sum():,.0f}")
# c2.metric("Orders", f"{len(df):,}")
# c3.metric("Vendors", df["vendor"].nunique())
# c4.metric("Flagged orders", int(df["is_anomaly"].sum()))

# # ---------- SPEND CHARTS ----------
# st.header("1. Spend breakdown")
# left, right = st.columns(2)
# with left:
#     st.subheader("By vendor")
#     st.bar_chart(df.groupby("vendor")["total_amount"].sum().sort_values(ascending=False))
# with right:
#     st.subheader("By category")
#     st.bar_chart(df.groupby("category")["total_amount"].sum().sort_values(ascending=False))

# st.subheader("By month")
# st.line_chart(df.groupby("month")["total_amount"].sum())

# # ---------- ANOMALIES ----------
# st.header("2. Unusual orders")
# flagged = df[df["is_anomaly"]].sort_values("total_amount", ascending=False)
# st.write(f"{len(flagged)} orders look unusual for their category.")
# st.dataframe(
#     flagged[["po_number", "po_date", "vendor", "category", "item",
#              "quantity", "unit_price", "total_amount"]],
#     width="stretch",
# )

# # ---------- FORECAST ----------
# st.header("3. Forecast: next month's spend by category")
# # Leave out flagged orders so one huge order doesn't distort the trend
# forecast, next_month = forecast_next_month(df[~df["is_anomaly"]])
# st.write(f"Predicted spend for **{next_month:%B %Y}**")
# st.bar_chart(forecast)
# st.dataframe(forecast.round(0).to_frame("forecast spend"))
# st.caption("Simple straight-line trend. It does not account for seasonal busy months.")

# with st.expander("Show raw data"):
#     st.dataframe(df)