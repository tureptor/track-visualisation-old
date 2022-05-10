import folium
from folium import IFrame
from flask import Flask, render_template, request, flash

def create_map(markers, location=[0, 0], plot_marks=True):
    m = folium.Map(location=location, prefer_canvas=True, max_zoom=17,
                   tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                   attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community')
    if plot_marks:
        for mark in markers:
            createMarker(m, mark)

    for i in range(1, len(markers)):
        createLine(m, [markers[i-1]["latlong"], markers[i]["latlong"]])
    
    return m._repr_html_()

def createMarker(m,data):
    text="battery level: "#+str(data["batterylevel"])+"\n"+"timestamp:"+str(data["timestamp"])
    iframe=folium.IFrame(text, width=200,height=50)
    popup=folium.Popup(iframe)
    Text=folium.Marker(location=data["latlong"],popup=popup, tooltip="Click for more information.",icon=folium.Icon(color="gray"))
    m.add_child(Text)
    #print("added", (data["GPSPosition"]["latitude"],data["GPSPosition"]["longitude"]), data["Timestamp"]["timestamp"])
    
def createLine(m,path):
    m.add_child(folium.PolyLine(path))
