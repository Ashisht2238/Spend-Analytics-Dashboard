import numpy as np
import pandas as pd


def forecast_next_month(df):
    """Draw a straight trend line through each category's monthly spend
    and read off where it lands next month."""
    monthly = df.pivot_table(
        index="month", columns="category", values="total_amount", aggfunc="sum"
    ).fillna(0)
    # Make sure every month between the first and last is present, so a month
    # with no orders counts as 0 instead of silently disappearing.
    all_months = pd.date_range(monthly.index.min(), monthly.index.max(), freq="MS")
    monthly = monthly.reindex(all_months, fill_value=0)
    x = np.arange(len(monthly))
    results = {}
    for category in monthly.columns:
        slope, intercept = np.polyfit(x, monthly[category].values, 1)
        results[category] = max(slope * len(monthly) + intercept, 0)
    next_month = monthly.index[-1] + pd.offsets.MonthBegin(1)
    return pd.Series(results, name="forecast"), next_month

















# import numpy as np
# import pandas as pd


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