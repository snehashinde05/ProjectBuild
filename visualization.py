
# import os

# from aqi_main import train_aqi_model
# from data_processing import load_and_clean_data
# from feature_engineering import add_features
# import plotly.graph_objects as go
# from forecast import forecast_next_7_days
# from data_files import files

# # files ={
# #     {
# #     "BKC": "BandraKurlaComplexMumbaiIITM.csv",
# #     "BandraMPCB": "BandraMumbaiMPCB.csv",
# #     "BoriValiEastIITM": "BorivaliEastMumbaiIITM.csv"
# # }
# # }

# for location, filepath in files.items():
#     if os.path.exists(filepath):
#         # Load your file here
#         df = load_and_clean_data(filepath)
#     else:
#         print(f"File not found: {filepath}")



# for location, filename in files.items():
#     full_path = os.path.join("data", filename)
#     files[location] = full_path




# def plot_forecast_interactive(forecast, location):
#     dates = [d for d, _ in forecast]
#     values = [v for _, v in forecast]
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', name='Forecasted AQI'))
#     fig.update_layout(title=f"7-Day AQI Forecast - {location}",
#                       xaxis_title="Date", yaxis_title="AQI",
#                       template="plotly_white")
#     fig.write_html(f"forecast_plot_{location}.html")
#     print(f"✅ Forecast plot saved: forecast_plot_{location}.html")

#     for location, file in files.items():
#         if not os.path.exists(file):
#             print(f"❌ Missing: {file}")
#             continue
#         df = load_and_clean_data(file)
#         df = add_features(df)
#         model, y_test, preds = train_aqi_model(df,0)
#         forecast = forecast_next_7_days(df, model)
#         print(f"\n🔮 {location} Forecast:")
#         for date, aqi in forecast:
#             print(f"{date}: AQI {aqi}")
#         plot_forecast_interactive(forecast, location)



import os
import joblib
import plotly.graph_objects as go
from interactive_plots_vis import avg_plots
from model import train_aqi_model
from data_processing import load_and_clean_data
from feature_engineering import add_features
from forecast import forecast_next_7_days

files = {
        "BKC": "BandraKurlaComplexMumbaiIITM.csv",
        "BandraMPCB": "BandraMumbaiMPCB.csv",
        "BoriValiEastIITM": "BorivaliEastMumbaiIITM.csv",
        "BoriValiEastMPCB": "BorivaliEastMumbaiMPCB.csv",
        "AndheriEast": "ChakalaAndheriEastMumbaiIITM.csv",
        "VileParleWestMumbai": "VileParleWestMumbaiMPCB.csv",
        "VasaiWestMumbai": "VasaiWestMumbaiMPCB.csv",
        "SionMumbai": "SionMumbaiMPCB.csv",
        "SiddharthNagarWorli": "SiddharthNagarWorliMumbaiIITM.csv",
        "PowaiMumbai": "PowaiMumbaiMPCB.csv",
        "NavyNagarColaba": "NavyNagarColabaMumbaiIITM.csv",
        "MulundWestMumbai": "MulundWestMumbaiMPCB.csv",
        "MazgaonMumbai": "MazgaonMumbaiIITM.csv",
        "MaladWestMumbai": "MaladWestMumbaiIITM.csv",
        "KurlaMumbai": "KurlaMumbaiMPCB.csv",
        "KhindipadaBhandupWestMumbai": "KhindipadaBhandupWestMumbaiIITM.csv",
        "KandivaliEastMumbai": "KandivaliEastMumbaiMPCB.csv",
        "DeonarMumbai": "DeonarMumbaiIITM.csv",
        "ColabaMumbai": "ColabaMumbaiMPCB.csv",
        "ChhatrapatiShivajiIntlAirport": "ChhatrapatiShivajiIntlAirportT2MumbaiMPCB.csv",
        "ChakalaAndheri": "ChakalaAndheriEastMumbaiIITM.csv",
        "Worli": "WorliMumbaiMPCB.csv"
    }


# Ensure all file paths are within the "data" folder
for location, filename in files.items():
    files[location] = os.path.join("data", filename)

# Ensure the "plots" directory exists
if not os.path.exists("plots"):
    os.makedirs("plots")

# Forecast plot function
def plot_forecast_interactive(forecast, location):
    dates = [d for d, _ in forecast]
    values = [v for _, v in forecast]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', name='Forecasted AQI'))
    fig.update_layout(title=f"7-Day AQI Forecast - {location}",
                      xaxis_title="Date", yaxis_title="AQI",
                      template="plotly_white")
    
    output_path = os.path.join("plots", f"forecast_plot_{location}.html")
    fig.write_html(output_path)
    print(f"✅ Forecast plot saved: {output_path}")

# Main processing loop
def forcasting_each_location():
    print("=== AQI Forecasting ===")
    for location, filepath in files.items():
        if not os.path.exists(filepath):
            print(f"❌ Missing: {filepath}")
            continue
        df = load_and_clean_data(filepath)
        df = add_features(df)
        #model, y_test, preds = train_aqi_model(df, flag=0)
        #model_path = joblib.load("data/aqi_model_xgb.joblib")
        
        model_path = os.path.join("data", f"aqi_model_{location}.joblib")
        if not os.path.exists(model_path):
            print(f"❌ Model not found: {model_path}")
            continue
        model = joblib.load(model_path)

        forecast = forecast_next_7_days(df, model)
        
        print(f"\n🔮 {location} Forecast:")
        for date, aqi in forecast:
            print(f"{date}: AQI {aqi}")
        
        plot_forecast_interactive(forecast, location)
        # Commenting out for now 
        
        

