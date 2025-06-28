import pandas as pd

from data_processing import load_and_clean_data
from feature_engineering import add_features
import plotly.graph_objects as go
import numpy as np
from datetime import timedelta
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import os
import matplotlib.pyplot as plt
from aqi_utils import calculate_cpcb_aqi
#import folium
from folium.plugins import HeatMap
from forecast import forecast_next_7_days

from config import LOCATION_COORDINATES   # <-- add this
from data_files import files                  # <-- add this

from aqi_utils import calculate_cpcb_aqi
from interactive_plots_vis import avg_plots
from model import train_and_save_model
from route_recommendation_bkp import run_route_recommendation
from visualization import forcasting_each_location  
#from route_recommendation import suggest_cleanest_nearby_location

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
    if flag!=1:
      print("\n📈 AQI Model Accuracy:")
      print(f"  MAE : {mean_absolute_error(y_test, preds):.2f}")
      print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, preds)):.2f}")
      print(f"  R²  : {r2_score(y_test, preds):.2f}")
    return model, y_test, preds

if __name__ == "__main__":
    #plot_average_pollutants(files)

    for location, path in files.items():
        if not os.path.exists(path):
            print(f"⚠️ File not found: {path}")
            continue

        print(f"\n=== Processing {location} ===")
        df = load_and_clean_data(path)
        df = add_features(df)

        model, y_test, preds = train_aqi_model(df, flag=0) '''

'''sneha
os.makedirs("saved_models", exist_ok=True)

files = {
    "BKC": "data/BandraKurlaComplexMumbaiIITM.csv",
    "BandraMPCB": "data/BandraMumbaiMPCB.csv",
    "BoriValiEastIITM": "data/BorivaliEastMumbaiIITM.csv",
    "BoriValiEastMPCB": "data/BorivaliEastMumbaiMPCB.csv",
    "AndheriEast": "data/ChakalaAndheriEastMumbaiIITM.csv",
    "VileParleWestMumbai": "data/VileParleWestMumbaiMPCB.csv",
    "VasaiWestMumbai": "data/VasaiWestMumbaiMPCB.csv",
    "SionMumbai": "data/SionMumbaiMPCB.csv",
    "SiddharthNagarWorli": "data/SiddharthNagarWorliMumbaiIITM.csv",
    "PowaiMumbai": "data/PowaiMumbaiMPCB.csv",
    "NavyNagarColaba": "data//NavyNagarColabaMumbaiIITM.csv",
    "MulundWestMumbai": "data/MulundWestMumbaiMPCB.csv",
    "MazgaonMumbai": "data/MazgaonMumbaiIITM.csv",
    "MaladWestMumbai": "data/MaladWestMumbaiIITM.csv",
    "KurlaMumbai": "data/KurlaMumbaiMPCB.csv",
    "KhindipadaBhandupWestMumbai": "data/KhindipadaBhandupWestMumbaiIITM.csv",
    "KandivaliEastMumbai": "data/KandivaliEastMumbaiMPCB.csv",
    "DeonarMumbai": "data/DeonarMumbaiIITM.csv",
    "ColabaMumbai": "data/ColabaMumbaiMPCB.csv",
    "ChhatrapatiShivajiIntlAirport": "data/ChhatrapatiShivajiIntlAirportT2MumbaiMPCB.csv",
    "ChakalaAndheri": "data/ChakalaAndheriEastMumbaiIITM.csv",
    "Worli": "data/WorliMumbaiMPCB.csv"
}

for location, path in files.items():
    if not os.path.exists(path):
        print(f"⚠️ File not found: {path}")
        continue

    df = load_and_clean_data(path)
    df = add_features(df)
    train_and_save_model(df, location) '''


def main():
    while True:
        print("\n=== AQI Prediction and Route Recommendation ===")
        print("1. Train and Save Models")
        print("2. Get Clean Route Recommendation")
        print("3. Forecast AQI ")
        print("4. Plots")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            train_and_save_model()

        elif choice == '2':
            run_route_recommendation()

        elif choice =='3':
            forcasting_each_location()

        elif choice == '4':
            avg_plots()
        
        elif choice == '5':
            break
        
        else:
            print("Invalid choice.")
    '''
    print("=== AQI Prediction and Route Recommendation ===")
    print("1. Train and Save Models")
    print("2. Get Clean Route Recommendation")
    print("3. Forecast AQI ")
    choice = input("Enter your choice: ")

    if choice == '1':
        train_and_save_model()

    elif choice == '2':
        run_route_recommendation()
    elif choice =='3':
        forcasting_each_location()
        
    else:
        print("Invalid choice.")
    '''

    
if __name__ == "__main__":
    main()
