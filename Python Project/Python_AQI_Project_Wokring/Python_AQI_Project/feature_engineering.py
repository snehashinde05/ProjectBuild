# === Feature Engineering ===
def add_features(df):
    for col in ["pm25", "pm10", "no2", "o3"]:
        df[f"{col}_roll3"] = df[col].rolling(3).mean()
        df[f"{col}_roll7"] = df[col].rolling(7).mean()
        df[f"{col}_std3"] = df[col].rolling(3).std()
    df["dayofweek"] = df.index.dayofweek
    df["month"] = df.index.month
    df["day"] = df.index.day
    return df.dropna()