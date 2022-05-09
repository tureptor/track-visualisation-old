import tempfile
import json

def file_to_objects(file):
    f = tempfile.TemporaryFile()
    file.save(f)
    f.seek(0)
    raw = f.read().decode("utf-8").strip("\n")
    f.close()
    objects = []
    for obj in raw.split("\n"):
        objects.append(json.loads(obj))
    return objects

def file_to_points(file):
    unlinked_points = file_to_objects(file)
    entries = []
    newentry = {}
    for point in unlinked_points:
        newentry |= point
        if "GPSPosition" in point:
            newentry["latlong"] = (point["GPSPosition"]["latitude"],point["GPSPosition"]["longitude"])
            entries.append(newentry)
            newentry = {}
    return entries

def avg_latlong(entries):
    count = 0
    total_lat = 0
    total_long = 0
    for e in entries:
        lat,long = e["latlong"]
        total_lat += lat
        total_long += long
        count += 1
    return (total_lat/count, total_long/count)

def filter_points_by_accuracy(points, min_hori_accu, min_vert_accu):
    filtered_points = []
    for entry in points:
        if entry["GPSPosition"]["accuracyHorizontal"] <= min_hori_accu and entry["GPSPosition"]["accuracyVertical"] <= min_vert_accu:
            filtered_points.append(entry)
    filtered_points.sort(key=(lambda e: e["Timestamp"]["timestamp"]))
    return filtered_points

def group_by_time():
    return []
