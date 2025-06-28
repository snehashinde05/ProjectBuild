import os
import folium
import openrouteservice
from openrouteservice import convert
from geopy.distance import geodesic

from aqi_main import train_aqi_model
from config import LOCATION_COORDINATES
from data_processing import load_and_clean_data
from feature_engineering import add_features
from forecast import forecast_next_7_days

# 🔑 Replace with your real OpenRouteService API key
ORS_API_KEY = "5b3ce3597851110001cf6248c7de9e65bb2c4c15941aa7198568b6ec"
ors_client = openrouteservice.Client(key=ORS_API_KEY)

def suggest_cleanest_nearby_location(user_lat, user_lon, trained_models, original_dfs):
    # Step 1: Calculate distances to all monitoring stations
    distances = []
    for loc, coords in LOCATION_COORDINATES.items():
        dist = geodesic((user_lat, user_lon), coords).km
        distances.append((loc, coords, dist))

    # Step 2: Find 3 nearest stations
    nearest_three = sorted(distances, key=lambda x: x[2])[:3]
    print("\n📍 Nearest 3 AQI Monitoring Locations:")
    for loc, coords, dist in nearest_three:
        print(f"  {loc}: {dist:.2f} km")

    # Step 3: Predict next day's AQI for each
    next_day_preds = []
    for loc, coords, _ in nearest_three:
        model = trained_models.get(loc)
        df = original_dfs.get(loc)
        if model and df is not None:
            forecast = forecast_next_7_days(df, model)
            if forecast:
                next_day_preds.append((loc, coords, forecast[0][1]))  # Use day 1 forecast

    # Step 4: Recommend location with lowest AQI
    if not next_day_preds:
        print("❌ No predictions available.")
        return

    recommended = min(next_day_preds, key=lambda x: x[2])
    rec_loc, rec_coords, rec_aqi = recommended
    print(f"\n✅ Recommended Location: {rec_loc} with AQI {rec_aqi}")

    # Step 5: Plot all 3 routes
    print("🗺️ Drawing All Routes on Map...")
    route_map = folium.Map(location=[user_lat, user_lon], zoom_start=12)

    # User Marker
    folium.Marker(
        [user_lat, user_lon],
        tooltip="You",
        icon=folium.Icon(color='blue')
    ).add_to(route_map)

    for loc, coords, aqi in next_day_preds:
        color = 'blue' if loc == rec_loc else 'black'
        coords_ors = ((user_lon, user_lat), (coords[1], coords[0]))  # ORS: (lon, lat)
        try:
            route = ors_client.directions(coords_ors)
            geometry = route['routes'][0]['geometry']
            decoded = convert.decode_polyline(geometry)

            # Route line
            folium.PolyLine(
                locations=[(pt[1], pt[0]) for pt in decoded['coordinates']],
                color=color,
                weight=5,
                opacity=0.8,
                tooltip=f"{loc} (AQI: {aqi})"
            ).add_to(route_map)

            # Destination marker
            folium.Marker(
                [coords[0], coords[1]],
                tooltip=f"{loc} (AQI: {aqi})",
                icon=folium.Icon(color='green' if loc == rec_loc else 'orange')
            ).add_to(route_map)

        except Exception as e:
            print(f"❌ Failed to draw route to {loc}: {e}")

    route_map.save("recommended_all_routes_map.html")
    print("✅ Route map saved as 'recommended_all_routes_map.html'")


trained_models = {}
original_dfs = {}

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

for location, path in files.items():
    flag = 1
    if not os.path.exists(path):
        continue
    df = load_and_clean_data(path)
    df = add_features(df)
    model, _, _ = train_aqi_model(df, flag)
    trained_models[location] = model
    original_dfs[location] = df

user_lat = float(input("📍 Enter your current Latitude: "))
user_lon = float(input("📍 Enter your current Longitude: "))
suggest_cleanest_nearby_location(user_lat, user_lon, trained_models, original_dfs)