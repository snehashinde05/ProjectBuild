# === Load and preprocess data ===
import pandas as pd
from aqi_utils import calculate_cpcb_aqi

def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.rename(columns={"from_date": "timestamp", "ozone": "o3", "pm2.5": "pm25"})
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df = df[["timestamp", "pm25", "pm10", "no2", "o3"]].dropna()
    df = df.set_index("timestamp").resample("h").mean().dropna()

    def rowwise_aqi(row):
        return max(filter(None, [
            calculate_cpcb_aqi("pm25", row["pm25"]),
            calculate_cpcb_aqi("pm10", row["pm10"]),
            calculate_cpcb_aqi("no2", row["no2"]),
            calculate_cpcb_aqi("o3", row["o3"]),
        ]), default=None)

    df["calculated_aqi"] = df.apply(rowwise_aqi, axis=1)
    return df