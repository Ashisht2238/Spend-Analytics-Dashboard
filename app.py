import streamlit as st
import matplotlib.pyplot as plt

from src.data import load_data
from src.anomaly import flag_anomalies
from src.forecast import forecast_next_month


# ---------- PAGE CONFIGURATION ----------
st.set_page_config(page_title="Spend Analytics Dashboard",layout="wide")

st.title("Spend Analytics Dashboard")


# ---------- LOAD DATA ----------
@st.cache_data
def get_data():
    return load_data()

df = get_data()
df = flag_anomalies(df, contamination=0.015)


# ---------- HEADLINE NUMBERS ----------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Spend", f"₹ {df['total_amount'].sum():,.0f}")
c2.metric("Orders", f"{len(df):,}")
c3.metric("Vendors", df["vendor"].nunique())
c4.metric("Flagged Orders", int(df["is_anomaly"].sum()))


# ---------- SPEND CHARTS ----------
st.header("1. Spend Analysis")

left, right = st.columns(2)


# ---------- VENDOR CHART ----------
with left:
    st.subheader("Spend by Vendor")

    vendor_spend = (df.groupby("vendor")["total_amount"].sum().sort_values(ascending=True))

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(vendor_spend.index , vendor_spend.values)

    ax.set_xlabel("Total Spend (₹)")
    ax.set_ylabel("Vendor") 

    ax.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# ---------- CATEGORY CHART ----------
with right:

    st.subheader("Spend by Category")

    category_spend = (df.groupby("category")["total_amount"].sum().sort_values(ascending=True))

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar( category_spend.index , category_spend.values)

    ax.set_xlabel("Total Spend (₹)")
    ax.set_ylabel("Category")

    ax.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# ---------- MONTHLY SPEND CHART ----------
st.subheader("Monthly Spending")

monthly_spend = (df.groupby("month")["total_amount"].sum().sort_index())

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(monthly_spend.index,monthly_spend.values,marker="o",linewidth=2)

ax.set_xlabel("Month")
ax.set_ylabel("Total Spend (₹)") 

ax.grid(True, linestyle="--", alpha=0.4)

fig.autofmt_xdate()
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)


# ---------- ANOMALY DETECTION ----------
st.header("2. Unusual Orders")

flagged = (
    df[df["is_anomaly"]]
    .sort_values("total_amount", ascending=False)
)

st.write(
    f"{len(flagged)} orders look unusual for their category."
)

st.dataframe(
    flagged[["po_number","po_date","vendor","category","item","quantity","unit_price","total_amount"]],
    width="stretch"
)


# ---------- FORECAST ----------
st.header("3. Forecast: Next Month's Spend")

forecast, next_month = forecast_next_month(df[~df["is_anomaly"]])

st.write(f"Predicted spend for **{next_month:%B %Y}**")

fig, ax = plt.subplots(figsize=(10, 5))

forecast = forecast.sort_values(ascending=True)

ax.barh(forecast.index , forecast.values)

ax.set_xlabel("Predicted Spend (₹)")
ax.set_ylabel("Category") 

ax.grid(axis="x", linestyle="--", alpha=0.4)

plt.tight_layout()

st.pyplot(fig)
plt.close(fig)
