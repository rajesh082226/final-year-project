import webbrowser

def open_arcgis_map(lat, lon):
    # Drop webmap= so the marker actually appears
    url = (
        f"https://www.arcgis.com/apps/mapviewer/index.html?"
        f"marker={lon};{lat};;Fire%20Detected;;Fire%20Location"
        f"&level=12"
    )
    print(f"Opening ArcGIS map at: {lat}, {lon}")
    webbrowser.open(url)