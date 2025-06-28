# import os
# import folium
# import joblib
# from matplotlib import pyplot as plt
# from config import LOCATION_COORDINATES
# from data_processing import load_and_clean_data
# from feature_engineering import add_features
# from forecast import forecast_next_7_days
# from model import train_aqi_model
# from folium.plugins import HeatMap
# import plotly.graph_objects as go

# def avg_plots(trained_models,original_dfs):
#     files = {
#         "BKC": "data\BandraKurlaComplexMumbaiIITM.csv",
#         "BandraMPCB": "data\BandraMumbaiMPCB.csv",
#         "BoriValiEastIITM": "data\BorivaliEastMumbaiIITM.csv",
#         "BoriValiEastMPCB": "data\BorivaliEastMumbaiMPCB.csv",
#         "AndheriEast": "data\ChakalaAndheriEastMumbaiIITM.csv",
#         "VileParleWestMumbai": "data\VileParleWestMumbaiMPCB.csv",
#         "VasaiWestMumbai": "data\VasaiWestMumbaiMPCB.csv",
#         "SionMumbai": "data\SionMumbaiMPCB.csv",
#         "SiddharthNagarWorli": "data\SiddharthNagarWorliMumbaiIITM.csv",
#         "PowaiMumbai": "data\PowaiMumbaiMPCB.csv",
#         "NavyNagarColaba": "data\\NavyNagarColabaMumbaiIITM.csv",
#         "MulundWestMumbai": "data\MulundWestMumbaiMPCB.csv",
#         "MazgaonMumbai": "data\MazgaonMumbaiIITM.csv",
#         "MaladWestMumbai": "data\MaladWestMumbaiIITM.csv",
#         "KurlaMumbai": "data\KurlaMumbaiMPCB.csv",
#         "KhindipadaBhandupWestMumbai": "data\KhindipadaBhandupWestMumbaiIITM.csv",
#         "KandivaliEastMumbai": "data\KandivaliEastMumbaiMPCB.csv",
#         "DeonarMumbai": "data\DeonarMumbaiIITM.csv",
#         "ColabaMumbai": "data\ColabaMumbaiMPCB.csv",
#         "ChhatrapatiShivajiIntlAirport": "data\ChhatrapatiShivajiIntlAirportT2MumbaiMPCB.csv",
#         "ChakalaAndheri": "data\ChakalaAndheriEastMumbaiIITM.csv",
#         "Worli": "data\WorliMumbaiMPCB.csv"
#     }
#     # Ensure the folder exists
#     output_dir = "interactive_plots_show"
#     os.makedirs(output_dir, exist_ok=True)
#     predictions_by_location = {}
#     avg_aqi_by_location = {}
#     for location, path in files.items():
#         if not os.path.exists(path):
#             print(f"⚠️ File not found: {path}")
#             continue

#         print(f"\n=== Processing {location} ===")
#         df = load_and_clean_data(path)
#         df = add_features(df)

#        # model, y_test, preds = train_aqi_model(df,0)
#         model_path = os.path.join("data", f"aqi_model_{location}.joblib")
#         if not os.path.exists(model_path):
#             print(f"❌ Model not found: {model_path}")
#             continue
#         model = joblib.load(model_path)
        
#        # predictions_by_location[location] = (model.reset_index(drop=True), model.predict(df))
#         df = df.reset_index(drop=True)  # Reset index on the input dataframe

#         df = df.reset_index(drop=True)

#         # Drop target column before prediction
#         if "calculated_aqi" in df.columns:
#             df_features = df.drop(columns=["calculated_aqi"])
#         else:
#             df_features = df  # fallback in case it's already removed

#         predictions = model.predict(df_features)

#         predictions_by_location[location] = (df["calculated_aqi"], predictions)

#        # predictions = model.predict(df)  # Make predictions

#        # predictions_by_location[location] = (df, predictions)


#         avg_aqi = df["calculated_aqi"].mean()
#         avg_aqi_by_location[location] = avg_aqi

    

 

#     # === Heatmap ===
#     print("\n🗺️ Generating AQI Heatmap...")
#     mumbai_map = folium.Map(location=[19.0760, 72.8777], zoom_start=11)
#     heat_data = []

#     for location, aqi in avg_aqi_by_location.items():
#         coords = LOCATION_COORDINATES.get(location)
#         if coords:
#             heat_data.append((*coords, aqi))
#             folium.CircleMarker(
#                 location=coords,
#                 radius=7,
#                 popup=f"{location}: AQI {aqi:.1f}",
#                 fill=True,
#                 fill_color="red" if aqi > 200 else "orange" if aqi > 100 else "green",
#                 color=None,
#                 fill_opacity=0.6
#             ).add_to(mumbai_map)

#     HeatMap(heat_data, radius=20, blur=15, max_zoom=13).add_to(mumbai_map)

#     for location, aqi in avg_aqi_by_location.items():
#         coords = LOCATION_COORDINATES.get(location)
#         if coords:
#             color = "green" if aqi <= 100 else "orange" if aqi <= 200 else "red"
#             folium.Marker(
#                 location=coords,
#                 icon=folium.DivIcon(html=f"""
#                     <div style="
#                         font-size: 10pt;
#                         font-weight: bold;
#                         color: black;
#                         background-color: rgba(255, 255, 255, 0.7);
#                         padding: 3px;
#                         border-radius: 5px;
#                         text-align: center;
#                         border: 1px solid #999;
#                         ">
#                         {location}<br>AQI: {int(aqi)}
#                     </div>""")
#             ).add_to(mumbai_map)

#     mumbai_map.save("mumbai_aqi_heatmap.html")
#     print("✅ Heatmap saved as 'mumbai_aqi_heatmap.html'")

#     # === Bar Graph ===
    
    
#     print("📊 Generating AQI Bar Graph...")
#     plt.figure(figsize=(12, 6))
#     locations = list(avg_aqi_by_location.keys())
#     aqi_values = list(avg_aqi_by_location.values())

#     plt.barh(locations, aqi_values, color='skyblue')
#     plt.xlabel("Average AQI")
#     plt.title("Average AQI at Each Location")
#     plt.grid(axis='x', linestyle='--', alpha=0.5)
#     plt.tight_layout()
#     plt.savefig("average_aqi_bargraph.png")
#     plt.show()
#     print("✅ Bar graph saved as 'average_aqi_bargraph.png'")
    
    

#     # === Interactive Plotly Graphs ===
#     print("\n📈 Generating interactive graphs for predictions...")
#     for location, (y_test, preds) in predictions_by_location.items():
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             y=y_test,
#             mode='lines+markers',
#             name='Actual AQI',
#             line=dict(color='blue')
#         ))
#         fig.add_trace(go.Scatter(
#             y=preds,
#             mode='lines+markers',
#             name='Predicted AQI',
#             line=dict(color='orange')
#         ))
#         fig.update_layout(
#             title=f'Predicted vs Actual AQI - {location}',
#             xaxis_title='Time Index',
#             yaxis_title='AQI',
#             legend=dict(x=0, y=1),
#             template='plotly_white'
#         )
#         filename = f"interactive_aqi_plot_{location}.html".replace(" ", "_")
#        # filename = f"interactive_aqi_plot_{location}.html".replace(" ", "_")
#         filepath = os.path.join(output_dir, filename)
#         #fig.write_html(filename)
#         fig.write_html(filepath)
#         print(f"✅ Saved interactive plot: {filename}") 

'''
import os
import folium
import joblib
from matplotlib import pyplot as plt
from config import LOCATION_COORDINATES
from data_processing import load_and_clean_data
from feature_engineering import add_features
from folium.plugins import HeatMap
import plotly.graph_objects as go

def avg_plots():
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
        "NavyNagarColaba": "data/NavyNagarColabaMumbaiIITM.csv",
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

    output_dir = "interactive_plots_show"
    os.makedirs(output_dir, exist_ok=True)

    processed_locations = set()
    predictions_by_location = {}
    avg_aqi_by_location = {}

    for location, path in files.items():
        if location in processed_locations:
            print(f"⚠️ Skipping already processed location: {location}")
            continue

        if not os.path.exists(path):
            print(f"❌ File not found: {path}")
            continue

        print(f"\n📍 Processing {location}...")
        df = load_and_clean_data(path)
        df = add_features(df)

        model_path = os.path.join("data", f"aqi_model_{location}.joblib")
        if not os.path.exists(model_path):
            print(f"❌ Model not found: {model_path}")
            continue

        model = joblib.load(model_path)
        df = df.reset_index(drop=True)

        if "calculated_aqi" in df.columns:
            df_features = df.drop(columns=["calculated_aqi"])
        else:
            df_features = df

        predictions = model.predict(df_features)
        predictions_by_location[location] = (df["calculated_aqi"], predictions)
        avg_aqi_by_location[location] = df["calculated_aqi"].mean()

        processed_locations.add(location)

    # === AQI Heatmap ===
    print("\n🗺️ Generating AQI Heatmap...")
    mumbai_map = folium.Map(location=[19.0760, 72.8777], zoom_start=11)
    heat_data = []

    for location, aqi in avg_aqi_by_location.items():
        coords = LOCATION_COORDINATES.get(location)
        if coords:
            heat_data.append((*coords, aqi))
            folium.CircleMarker(
                location=coords,
                radius=7,
                popup=f"{location}: AQI {aqi:.1f}",
                fill=True,
                fill_color="red" if aqi > 200 else "orange" if aqi > 100 else "green",
                color=None,
                fill_opacity=0.6
            ).add_to(mumbai_map)

    HeatMap(heat_data, radius=20, blur=15, max_zoom=13).add_to(mumbai_map)

    for location, aqi in avg_aqi_by_location.items():
        coords = LOCATION_COORDINATES.get(location)
        if coords:
            folium.Marker(
                location=coords,
                icon=folium.DivIcon(html=f"""
                    <div style="
                        font-size: 10pt;
                        font-weight: bold;
                        color: black;
                        background-color: rgba(255, 255, 255, 0.7);
                        padding: 3px;
                        border-radius: 5px;
                        border: 1px solid #999;
                        text-align: center;
                        ">
                        {location}<br>AQI: {int(aqi)}
                    </div>""")
            ).add_to(mumbai_map)

    mumbai_map.save("mumbai_aqi_heatmap.html")
    print("✅ Heatmap saved as 'mumbai_aqi_heatmap.html'")

    # === Bar Graph ===
    print("📊 Generating AQI Bar Graph...")
    plt.figure(figsize=(12, 6))
    locations = list(avg_aqi_by_location.keys())
    aqi_values = list(avg_aqi_by_location.values())

    plt.barh(locations, aqi_values, color='skyblue')
    plt.xlabel("Average AQI")
    plt.title("Average AQI at Each Location")
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("average_aqi_bargraph.png")
    plt.show()
    print("✅ Bar graph saved as 'average_aqi_bargraph.png'")

    # === Interactive Plotly Graphs ===
    print("\n📈 Generating interactive graphs for predictions...")
    for location, (y_test, preds) in predictions_by_location.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=y_test,
            mode='lines+markers',
            name='Actual AQI',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            y=preds,
            mode='lines+markers',
            name='Predicted AQI',
            line=dict(color='orange')
        ))
        fig.update_layout(
            title=f'Predicted vs Actual AQI - {location}',
            xaxis_title='Time Index',
            yaxis_title='AQI',
            legend=dict(x=0, y=1),
            template='plotly_white'
        )
        filename = f"interactive_aqi_plot_{location}.html".replace(" ", "_")
        filepath = os.path.join(output_dir, filename)
        fig.write_html(filepath)
        print(f"✅ Saved interactive plot: {filename}")

        '''

import os

import folium
import joblib
from matplotlib import pyplot as plt
from config import LOCATION_COORDINATES
from data_processing import load_and_clean_data
from feature_engineering import add_features
from forecast import forecast_next_7_days
from model import train_aqi_model
import plotly.graph_objects as go
from folium.plugins import HeatMap


def avg_plots():
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

    predictions_by_location = {}
    avg_aqi_by_location = {}

    for location, path in files.items():
        if not os.path.exists(path):
            print(f"⚠️ File not found: {path}")
            continue

        print(f"\n=== Processing {location} ===")
        df = load_and_clean_data(path)
        df = add_features(df)

        model_path = os.path.join("data", f"aqi_model_{location}.joblib")

        if not os.path.exists(model_path):
            print(f"❌ Pre-trained model not found for {location}: {model_path}")
            continue

        model = joblib.load(model_path)

        # Prepare your X and y (assuming your `add_features()` gives you the same structure as used in training)
        X = df.drop(columns=["calculated_aqi"])
        y = df["calculated_aqi"]

        # Make predictions (ensure data columns match training-time features)
        preds = model.predict(X)
        predictions_by_location[location] = (y.reset_index(drop=True), preds)

        #model, y_test, preds = train_aqi_model(df,0)
        #predictions_by_location[location] = (y_test.reset_index(drop=True), preds)



        avg_aqi = df["calculated_aqi"].mean()
        avg_aqi_by_location[location] = avg_aqi
        '''

        print("\n🔮 Forecast for Next 7 Days:")
        forecast = forecast_next_7_days(df, model)
        for date, pred in forecast:
            print(f"{date} → AQI: {pred}")
        '''

    # === Heatmap ===
    print("\n🗺️ Generating AQI Heatmap...")
    mumbai_map = folium.Map(location=[19.0760, 72.8777], zoom_start=11)
    heat_data = []

    for location, aqi in avg_aqi_by_location.items():
        coords = LOCATION_COORDINATES.get(location)
        if coords:
            heat_data.append((*coords, aqi))
            folium.CircleMarker(
                location=coords,
                radius=7,
                popup=f"{location}: AQI {aqi:.1f}",
                fill=True,
                fill_color="red" if aqi > 200 else "orange" if aqi > 100 else "green",
                color=None,
                fill_opacity=0.6
            ).add_to(mumbai_map)

    HeatMap(heat_data, radius=20, blur=15, max_zoom=13).add_to(mumbai_map)

    for location, aqi in avg_aqi_by_location.items():
        coords = LOCATION_COORDINATES.get(location)
        if coords:
            color = "green" if aqi <= 100 else "orange" if aqi <= 200 else "red"
            folium.Marker(
                location=coords,
                icon=folium.DivIcon(html=f"""
                    <div style="
                        font-size: 10pt;
                        font-weight: bold;
                        color: black;
                        background-color: rgba(255, 255, 255, 0.7);
                        padding: 3px;
                        border-radius: 5px;
                        text-align: center;
                        border: 1px solid #999;
                        ">
                        {location}<br>AQI: {int(aqi)}
                    </div>""")
            ).add_to(mumbai_map)

    mumbai_map.save("mumbai_aqi_heatmap.html")
    print("✅ Heatmap saved as 'mumbai_aqi_heatmap.html'")

    # === Bar Graph ===
    print("📊 Generating AQI Bar Graph...")
    plt.figure(figsize=(12, 6))
    locations = list(avg_aqi_by_location.keys())
    aqi_values = list(avg_aqi_by_location.values())

    plt.barh(locations, aqi_values, color='skyblue')
    plt.xlabel("Average AQI")
    plt.title("Average AQI at Each Location")
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("average_aqi_bargraph.png")
    plt.show()
    print("✅ Bar graph saved as 'average_aqi_bargraph.png'")

    # === Interactive Plotly Graphs ===
    print("\n📈 Generating interactive graphs for predictions...")

    # Create the folder if it doesn't exist
    output_dir = "interactive_graphs"
    os.makedirs(output_dir, exist_ok=True)

    for location, (y_test, preds) in predictions_by_location.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=y_test,
            mode='lines+markers',
            name='Actual AQI',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            y=preds,
            mode='lines+markers',
            name='Predicted AQI',
            line=dict(color='orange')
        ))
        fig.update_layout(
            title=f'Predicted vs Actual AQI - {location}',
            xaxis_title='Time Index',
            yaxis_title='AQI',
            legend=dict(x=0, y=1),
            template='plotly_white'
        )
        filename = os.path.join(output_dir, f"interactive_aqi_plot_{location}.html".replace(" ", "_"))
        fig.write_html(filename)
        print(f"✅ Saved interactive plot: {filename}")

    #avg_plots()