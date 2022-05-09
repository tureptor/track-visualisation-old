from email.policy import default
from flask import Flask, render_template, request, flash
import folium
import View
import tempfile
import json

app = Flask(__name__)
app.secret_key = "sEcrEt.kEy" # Necessary for flash to work (ideally should be encrypted)
app.debug = True

default_map = folium.Map(location=[48, -102], zoom_start=3)._repr_html_()

@app.route("/")
@app.route("/home")
def index():
  return render_template("map.html", folium_map=default_map)
  
@app.route("/", methods=["GET", "POST"])
def show_map():
  file = request.files['file']
  flash(file.filename)
  if "file" not in request.files:
      flash('No file part')
      return redirect(request.url)
  else:
    f = tempfile.TemporaryFile()
    file.save(f)
    f.seek(0)
    ny = json.load(f)
    f.close()
    print(ny.keys())
    try:
      folium_map = View.create_map([{"latlong": [10.02, 9.98], "timestamp": 123, "batterylevel": 0.8}],
                                   location=[0, 0])
      return render_template("map.html", folium_map=folium_map) # Display the map
    except Exception as error:
      flash("The following error occured: " + repr(error)) # Display an error message
    
  return render_template("map.html", folium_map=default_map) # If an error occured, simply load the original page

  

if __name__ == "__main__":
  app.run()
