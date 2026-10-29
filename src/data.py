import pandas as pd


def load_data(path="data/purchase_orders.csv"):
    df = pd.read_csv(path, parse_dates=["po_date"])
    # Turn each date into the first day of its month, e.g. 2025-03-17 -> 2025-03-01
    df["month"] = df["po_date"].dt.to_period("M").dt.to_timestamp()
    return df