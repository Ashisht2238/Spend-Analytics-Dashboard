import numpy as np
import pandas as pd


def forecast_next_month(df): 
    monthly = df.pivot_table(
        index="month", columns="category", values="total_amount", aggfunc="sum"
    ).fillna(0) 
    all_months = pd.date_range(monthly.index.min(), monthly.index.max(), freq="MS")
    monthly = monthly.reindex(all_months, fill_value=0)
    x = np.arange(len(monthly))
    results = {}
    for category in monthly.columns:
        slope, intercept = np.polyfit(x, monthly[category].values, 1)
        results[category] = max(slope * len(monthly) + intercept, 0)
    next_month = monthly.index[-1] + pd.offsets.MonthBegin(1)
    return pd.Series(results, name="forecast"), next_month
















 