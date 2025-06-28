import os
import joblib
import streamlit as st
import plotly.graph_objects as go
from data_processing import load_and_clean_data
from feature_engineering import add_features
from forecast import forecast_next_7_days

# Define your files
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

# Prefix all file paths with data folder
for location in files:
    files[location] = os.path.join("data", files[location])

# --- Streamlit App Starts ---
st.set_page_config(layout="wide")
st.title("🌫️ Mumbai AQI Forecast Dashboard (Next 7 Days)")
st.markdown("View AQI forecasts per location using pre-trained models.")

# Allow user to select multiple locations or view all
selected_locations = st.multiselect("Select locations to view forecast", options=list(files.keys()), default=list(files.keys()))

# Loop through selected locations
for location in selected_locations:
    filepath = files[location]

    if not os.path.exists(filepath):
        st.warning(f"File not found: {filepath}")
        continue

    # Load and preprocess data
    df = load_and_clean_data(filepath)
    df = add_features(df)

    # Load model
    model_path = os.path.join("data", f"aqi_model_{location}.joblib")
    if not os.path.exists(model_path):
        st.warning(f"Model not found: {model_path}")
        continue

    model = joblib.load(model_path)
    forecast = forecast_next_7_days(df, model)

    # Plot forecast
    dates = [d for d, _ in forecast]
    values = [v for _, v in forecast]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', name='Forecasted AQI'))
    fig.update_layout(title=f"{location} - AQI Forecast",
                      xaxis_title="Date", yaxis_title="AQI",
                      template="plotly_white")

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)
