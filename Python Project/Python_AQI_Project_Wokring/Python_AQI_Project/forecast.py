# === Forecast Next 7 Days ===
from datetime import timedelta

import joblib
import pandas as pd


def forecast_next_7_days(df, model):
    last_date = df.index[-1]
    forecast_data = df.copy()
    predictions = []

    for i in range(1, 8):
        next_day = last_date + timedelta(days=i)
        row = {
            "pm25": forecast_data["pm25"].iloc[-1],
            "pm10": forecast_data["pm10"].iloc[-1],
            "no2": forecast_data["no2"].iloc[-1],
            "o3": forecast_data["o3"].iloc[-1],
            "pm25_roll3": forecast_data["pm25"].rolling(3).mean().iloc[-1],
            "pm25_roll7": forecast_data["pm25"].rolling(7).mean().iloc[-1],
            "pm25_std3": forecast_data["pm25"].rolling(3).std().iloc[-1],
            "pm10_roll3": forecast_data["pm10"].rolling(3).mean().iloc[-1],
            "pm10_roll7": forecast_data["pm10"].rolling(7).mean().iloc[-1],
            "pm10_std3": forecast_data["pm10"].rolling(3).std().iloc[-1],
            "no2_roll3": forecast_data["no2"].rolling(3).mean().iloc[-1],
            "no2_roll7": forecast_data["no2"].rolling(7).mean().iloc[-1],
            "no2_std3": forecast_data["no2"].rolling(3).std().iloc[-1],
            "o3_roll3": forecast_data["o3"].rolling(3).mean().iloc[-1],
            "o3_roll7": forecast_data["o3"].rolling(7).mean().iloc[-1],
            "o3_std3": forecast_data["o3"].rolling(3).std().iloc[-1],
            "dayofweek": next_day.dayofweek,
            "month": next_day.month,
            "day": next_day.day
        }
        
       #model = joblib.load("aqi_model_xgb.joblib")
       # pred = model.predict(pd.DataFrame([row], index=[next_day]))[0]
        pred = model.predict(pd.DataFrame([row], index=[next_day]))[0]
        predictions.append((next_day.strftime('%Y-%m-%d'), round(pred, 2)))

        new_data = pd.Series({
            "pm25": row["pm25"], "pm10": row["pm10"],
            "no2": row["no2"], "o3": row["o3"],
            "calculated_aqi": pred
        })
        forecast_data = pd.concat([forecast_data, pd.DataFrame([new_data], index=[next_day])])

    return predictions
