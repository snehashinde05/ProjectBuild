
import os
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
import joblib

# Save the model to a file



'''def train_aqi_model(df, flag):
    features = [col for col in df.columns if col != "calculated_aqi"]
    X = df[features]
    y = df["calculated_aqi"]
    split = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = XGBRegressor(objective='reg:squarederror', n_estimators=200, max_depth=4, learning_rate=0.1)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    joblib.dump(model, "data/aqi_model_xgb.joblib")

    #### New code 
      # ✅ Save model
    os.makedirs("data/models", exist_ok=True)
    joblib.dump(model, f"data/models/abc_model.joblib")

    # ✅ Save predictions
    results = pd.DataFrame({"Actual_AQI": y_test.values, "Predicted_AQI": preds})
    results.to_csv(f"data/models/abc_predictions.csv", index=False)
    if flag!=1:
      print("\n📈 AQI Model Accuracy:")
      print(f"  MAE : {mean_absolute_error(y_test, preds):.2f}")
      print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, preds)):.2f}")
      print(f"  R²  : {r2_score(y_test, preds):.2f}")
    return model, y_test, preds '''

import os
import joblib
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from data_processing import load_and_clean_data
from feature_engineering import add_features

files = {
        "BKC": "data\BandraKurlaComplexMumbaiIITM.csv",
        "BandraMPCB": "data\BandraMumbaiMPCB.csv",
        "BoriValiEastIITM": "data\BorivaliEastMumbaiIITM.csv",
        "BoriValiEastMPCB": "data\BorivaliEastMumbaiMPCB.csv",
        "AndheriEast": "data\ChakalaAndheriEastMumbaiIITM.csv",
        "VileParleWestMumbai": "data\VileParleWestMumbaiMPCB.csv",
        "VasaiWestMumbai": "data\VasaiWestMumbaiMPCB.csv",
        "SionMumbai": "data\SionMumbaiMPCB.csv",
        "SiddharthNagarWorli": "data\SiddharthNagarWorliMumbaiIITM.csv",
        "PowaiMumbai": "data\PowaiMumbaiMPCB.csv",
        "NavyNagarColaba": "data/NavyNagarColabaMumbaiIITM.csv",
        "MulundWestMumbai": "data\MulundWestMumbaiMPCB.csv",
        "MazgaonMumbai": "data\MazgaonMumbaiIITM.csv",
        "MaladWestMumbai": "data\MaladWestMumbaiIITM.csv",
        "KurlaMumbai": "data\KurlaMumbaiMPCB.csv",
        "KhindipadaBhandupWestMumbai": "data\KhindipadaBhandupWestMumbaiIITM.csv",
        "KandivaliEastMumbai": "data\KandivaliEastMumbaiMPCB.csv",
        "DeonarMumbai": "data\DeonarMumbaiIITM.csv",
        "ColabaMumbai": "data\ColabaMumbaiMPCB.csv",
        "ChhatrapatiShivajiIntlAirport": "data\ChhatrapatiShivajiIntlAirportT2MumbaiMPCB.csv",
        "ChakalaAndheri": "data\ChakalaAndheriEastMumbaiIITM.csv",
        "Worli": "data\WorliMumbaiMPCB.csv"
    }

def train_aqi_model(df, flag):
    features = [col for col in df.columns if col != "calculated_aqi"]
    X = df[features]
    y = df["calculated_aqi"]
    split = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = XGBRegressor(objective='reg:squarederror', n_estimators=200, max_depth=4, learning_rate=0.1)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    if flag != 1:
        print("\n📈 AQI Model Accuracy:")
        print(f"  MAE : {mean_absolute_error(y_test, preds):.2f}")
        print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, preds)):.2f}")
        print(f"  R²  : {r2_score(y_test, preds):.2f}")
    return model, y_test, preds

def train_and_save_model():
    print("🔁 Starting model training and saving...")
    for location, path in files.items():
        if not os.path.exists(path):
            print(f"⚠️ File not found: {path}")
            continue

        print(f"\n=== Processing {location} ===")
        df = load_and_clean_data(path)
        df = add_features(df)

        try:
            model, _, _ = train_aqi_model(df, flag=0)
            model_path = f"data/aqi_model_{location}.joblib"
            joblib.dump(model, model_path)
            print(f"✅ Saved model: {model_path}")
        except Exception as e:
            print(f"❌ Failed to train model for {location}: {e}")
    print("🔁 Model training and saving completed.")