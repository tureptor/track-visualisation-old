from email.policy import default
from flask import Flask, render_template, request, flash
import folium
import View
import Model

app = Flask(__name__)
app.secret_key = "sEcrEt.kEy" # Necessary for flash to work (ideally should be encrypted)
app.debug = True

default_map = folium.Map(location=[48, -102], zoom_start=3)._repr_html_()

@app.route("/")
@app.route("/home")
def index():
    return render_template("map.html", folium_map=default_map, showMarkers=True, varyMarkerSize=False, 
                                         minHorizontalAcc=100, minVerticalAcc=100, maxTimeGap=1)
    
@app.route("/", methods=["GET", "POST"])
def show_map():
    file = request.files['file']
    flash(file.filename)

    showMarkers = request.form.get("showMarkers")
    varyMarkerSize = request.form.get("varyMarkerSize")
    minHorizontalAcc = int(request.form["minHorizontalAcc"])
    minVerticalAcc = int(request.form["minVerticalAcc"])
    maxTimeGap = int(request.form["maxTimeGap"])

    if "file" not in request.files:
        flash('No file part')
        return redirect(request.url)

    else:
        try:
            points = Model.file_to_points(file)
            bunches = Model.group_adjacent_points(points, maxTimeGap)
            filtered_points = Model.filter_bunches_by_accuracy(bunches, minHorizontalAcc, minVerticalAcc)
            folium_map = View.create_map(filtered_points,
                                         Model.avg_latlong(filtered_points), showMarkers, varyMarkerSize)
            return render_template("map.html", folium_map=folium_map, showMarkers=showMarkers, varyMarkerSize = varyMarkerSize,
                                                 minHorizontalAcc=minHorizontalAcc, minVerticalAcc=minVerticalAcc, maxTimeGap=maxTimeGap) # Display the map
        except Exception as error:
            flash("Error in decoding stage:" + repr(error))

    return render_template("map.html", folium_map=default_map, showMarkers=True,
                                        varyMarkerSize = False, minHorizontalAcc=100, minVerticalAcc=100, maxTimeGap=1) # If an error occured, simply load the original page

if __name__ == "__main__":
    app.run()
