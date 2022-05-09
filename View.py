import folium
from datetime import datetime
from folium import IFrame
from flask import Flask, render_template, request, flash

def create_map(markers, location=[0, 0], plot_marks=True):
    tiles= folium.TileLayer(max_zoom=21, max_native_zoom=17,
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community')
    m = folium.Map(location=location, prefer_canvas=True, tiles=None,control_scale=True)
    tiles.add_to(m)

    for i in range(1, len(markers)):
        createLine(m, markers[i-1], markers[i])

    if plot_marks:
        for i in range(len(markers)):
            is_endpoint = (i == 0 or i == len(markers)-1)
            createMarker(m, markers[i], is_endpoint)

    
    return m._repr_html_()

def createMarker(m,data,is_endpoint):
    text="Battery: "+str(data["battery"])+"%<br>Date: "+str(datetime.fromtimestamp(data["time"]))
    iframe=folium.IFrame(text, width=200,height=100)
    popup=folium.Popup(iframe)
    color = "#"+str(hex(round(data["battery"]*2.55)))[-2:] * 3
    if is_endpoint:
        folium.Marker(location=data["latlong"],popup=popup,color=color).add_to(m)
    elif True: # make accuracy affect size
        folium.Circle(location=data["latlong"],popup=popup, radius=data["accuracy"][1],color=color,fill=True,fill_opacity=0.6).add_to(m)
    else:
        folium.CircleMarker(location=data["latlong"],popup=popup,color=color,fill=True,fill_opacity=0.6).add_to(m)
    
def createLine(m,start,end):
    path = [start["latlong"], end["latlong"]]
    color = "#" + str(hex(round(start["battery"]*2.55)))[-2:] * 3
    m.add_child(folium.PolyLine(path, color=color))
