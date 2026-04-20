import folium
import pandas as pd
import webbrowser
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

DATA_PATH = os.path.join(PROJECT_DIR, "raw_data", "nasa_firms.csv")

def show_fire_map(lat, lon):

    fire_map = folium.Map(location=[22,78], zoom_start=5)

    # Load dataset safely
    data = pd.read_csv(DATA_PATH)

    for _, row in data.iterrows():

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=2,
            color="orange",
            fill=True,
            fill_opacity=0.6
        ).add_to(fire_map)

    folium.Marker(
        [lat, lon],
        popup=f"🔥 Fire Detected\nLat:{lat}\nLon:{lon}",
        icon=folium.Icon(color="red")
    ).add_to(fire_map)

    fire_map.save("fire_map.html")

    webbrowser.open("fire_map.html")