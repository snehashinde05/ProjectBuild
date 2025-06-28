import os
import joblib
import streamlit as st
import plotly.graph_objects as go
from data_processing import load_and_clean_data
from feature_engineering import add_features
from forecast import forecast_next_7_days
from route_recommendation_bkp import suggest_cleanest_nearby_location  # <-- Your map logic
from config import LOCATION_COORDINATES

# --- File paths ---
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

for location in files:
    files[location] = os.path.join("data", files[location])

# --- Streamlit Layout ---
st.set_page_config(layout="wide")
st.title("🌫️ Mumbai AQI Forecast Dashboard (Next 7 Days)")
st.markdown("View AQI forecasts per location using pre-trained models.")

# --- Location Selection ---
selected_location = st.selectbox(
    "Select a location to view AQI forecast (Next 7 Days)",
    options=list(files.keys())
)

trained_models = {}
original_dfs = {}

# --- Forecast Display ---
location = selected_location
filepath = files[location]

if not os.path.exists(filepath):
    st.warning(f"File not found: {filepath}")
else:
    df = load_and_clean_data(filepath)
    df = add_features(df)

    model_path = os.path.join("data", f"aqi_model_{location}.joblib")
    if not os.path.exists(model_path):
        st.warning(f"Model not found: {model_path}")
    else:
        model = joblib.load(model_path)
        forecast = forecast_next_7_days(df, model)

        # Save for routing
        trained_models[location] = model
        original_dfs[location] = df

        # Plotting
        dates = [d for d, _ in forecast]
        values = [v for _, v in forecast]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', name='Forecasted AQI'))
        fig.update_layout(
            title=f"{location} - AQI Forecast (Next 7 Days)",
            xaxis_title="Date",
            yaxis_title="AQI",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

# --- Route Map Section ---
st.markdown("---")
st.header("🚴 Route Suggestion to Cleanest Nearby AQI Location")

with st.form("route_form"):
    user_lat = st.number_input("Enter your latitude", format="%.6f")
    user_lon = st.number_input("Enter your longitude", format="%.6f")
    submitted = st.form_submit_button("Suggest Route")

if submitted:
    with st.spinner("Processing recommendation and drawing route map..."):
        output_path = "maps/recommended_all_routes_map.html"
        suggest_cleanest_nearby_location(user_lat, user_lon, trained_models, original_dfs, output_path)

        # Display the saved HTML map
        if os.path.exists(output_path):
            st.components.v1.html(open(output_path, 'r', encoding='utf-8').read(), height=600)
        else:
            st.error("Map could not be displayed. Something went wrong.")
