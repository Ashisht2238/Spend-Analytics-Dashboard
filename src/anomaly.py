import numpy as np
from sklearn.ensemble import IsolationForest


def flag_anomalies(df, contamination=0.015):
    """Mark unusual orders. Each category is checked separately,
    because a normal laptop order looks very different from a normal pen order."""
    df = df.copy()
    df["is_anomaly"] = False
    for category, group in df.groupby("category"):
        # log1p squashes big numbers so the model compares sizes fairly
        features = np.log1p(group[["quantity", "unit_price",]])
        model = IsolationForest(contamination=contamination, random_state=42)
        model.fit(features)
        df.loc[group.index, "is_anomaly"] = model.predict(features) == -1
    return df