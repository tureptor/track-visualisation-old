import folium
from folium import IFrame
from IPython.display import display
from flask import Flask, render_template, request, flash

def create_map(markers, location=[0, 0]):
    m = folium.Map(location=location)

    for mark in markers:
        createMarker(m, mark)
    
    return m._repr_html_()

def createMarker(m,data):
    text="battery level: "+str(data["batterylevel"])+"\n"+"timestamp:"+str(data["timestamp"])
    print(text)
    iframe=folium.IFrame(text, width=200,height=50)
    popup=folium.Popup(iframe)
    Text=folium.Marker(location=data["latlong"],popup=popup, tooltip="Click for more information.",icon=folium.Icon(color="gray"))
    m.add_child(Text)
    

