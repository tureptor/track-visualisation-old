import folium
from datetime import datetime
from folium import IFrame, plugins
from flask import Flask, render_template, request, flash

def create_map(markers, location=[0, 0], plot_marks=True, vary_size=False):
    tileLayers = [
        folium.TileLayer(name="ArcGIS",max_native_zoom=17, max_zoom=21,
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
),
        folium.TileLayer(name="Ocean",max_native_zoom=13, max_zoom=21,
tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}",
attr="Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri",
),
        folium.TileLayer(name="Nautical features", max_zoom=21,
tiles="https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",
attr='Map data: &copy; <a href="http://www.openseamap.org">OpenSeaMap</a> contributors',
overlay=True
),

        folium.TileLayer(name="Terrain", max_zoom=21,
tiles="https://stamen-tiles-{s}.a.ssl.fastly.net/toner-hybrid/{z}/{x}/{y}{r}.png",
attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
overlay=True
),

        folium.TileLayer(name="OpenTopoMap", max_zoom=21,
tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
)
    ]
    m = folium.Map(location=location, prefer_canvas=True, tiles=None,control_scale=True,max_zoom=21)
    for tilelayer in tileLayers:
        tilelayer.add_to(m)

    plugins.Fullscreen(
            position="topright",
            title="Enter fullscreen",
            title_canel="Exit fullscreen",
            force_separate_button=True
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    for i in range(1, len(markers)):
        createLine(m, markers[i-1], markers[i])

    if plot_marks:
        for i in range(len(markers)):
            is_endpoint = (i == 0 or i == len(markers)-1)
            createMarker(m, markers[i], is_endpoint, vary_size)

    
    return m._repr_html_()

def createMarker(m,data,is_endpoint,vary_size):
    text="Battery: "+str(data["battery"])+"%<br>Date: "+str(datetime.fromtimestamp(data["time"]))
    iframe=folium.IFrame(text, width=200,height=100)
    popup=folium.Popup(iframe)
    color = "#"+str(hex(round(data["battery"]*2.55)))[-2:] * 3
    if is_endpoint:
        folium.Marker(location=data["latlong"],popup=popup,color=color).add_to(m)
    elif vary_size: # make accuracy affect size
        folium.Circle(location=data["latlong"],popup=popup, radius=data["accuracy"][1],color=color,fill=True,fill_opacity=0.6).add_to(m)
    else:
        folium.CircleMarker(location=data["latlong"],popup=popup,color=color,fill=True,fill_opacity=0.6).add_to(m)
    
def createLine(m,start,end):
    path = [start["latlong"], end["latlong"]]
    color = "#" + str(hex(round(start["battery"]*2.55)))[-2:] * 3
    m.add_child(folium.PolyLine(path, color=color))
