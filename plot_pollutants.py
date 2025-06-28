import os
import matplotlib.pyplot as plt
import pandas as pd
from data_processing import load_and_clean_data


# Step 3: Initialize Pollutant Data Storage
pollutant_data = {
    "Location": [],
    "PM2.5": [],
    "PM10": [],
    "NO2": [],
    "O3": []
}



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


for location, filepath in files.items():
    if os.path.exists(filepath):
        # Load your file here
        df = load_and_clean_data(filepath)
    else:
        print(f"File  found: {filepath}")



for location, filename in files.items():
    full_path = os.path.join("data", filename)
    files[location] = full_path



# Step 4: Process Each File and Extract Averages
for location, filename in files.items():
    try:
        df = pd.read_csv(filename)
        df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")

        pollutant_data["Location"].append(location)
        pollutant_data["PM2.5"].append(pd.to_numeric(df.get("PM2.5", pd.Series([None])), errors='coerce').mean())
        pollutant_data["PM10"].append(pd.to_numeric(df.get("PM10", pd.Series([None])), errors='coerce').mean())
        pollutant_data["NO2"].append(pd.to_numeric(df.get("NO2", pd.Series([None])), errors='coerce').mean())
        pollutant_data["O3"].append(pd.to_numeric(df.get("OZONE", pd.Series([None])), errors='coerce').mean())

    except Exception as e:
        print(f"⚠️ Error processing {filename}: {e}")

# Step 5: Convert to DataFrame
pollutants_df = pd.DataFrame(pollutant_data)

# Step 6: Plot the Graphs
fig, axs = plt.subplots(2, 2, figsize=(22, 12))
fig.suptitle("Average Pollutant Levels Across 21 Mumbai Locations", fontsize=20)

axs[0, 0].bar(pollutants_df["Location"], pollutants_df["PM2.5"], color='orange')
axs[0, 0].set_title("PM2.5 Levels")
axs[0, 0].tick_params(axis='x', rotation=90)

axs[0, 1].bar(pollutants_df["Location"], pollutants_df["PM10"], color='blue')
axs[0, 1].set_title("PM10 Levels")
axs[0, 1].tick_params(axis='x', rotation=90)

axs[1, 0].bar(pollutants_df["Location"], pollutants_df["NO2"], color='green')
axs[1, 0].set_title("NO₂ Levels")
axs[1, 0].tick_params(axis='x', rotation=90)

axs[1, 1].bar(pollutants_df["Location"], pollutants_df["O3"], color='purple')
axs[1, 1].set_title("O₃ Levels")
axs[1, 1].tick_params(axis='x', rotation=90)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
