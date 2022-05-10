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
            entries.append({
                "latlong":(point["GPSPosition"]["latitude"],point["GPSPosition"]["longitude"]),
                "time":newentry["Timestamp"]["timestamp"],
                "accuracy":(point["GPSPosition"]["accuracyVertical"],point["GPSPosition"]["accuracyHorizontal"])
            })
            if "BatteryCharge" in newentry:
                entries[-1]["battery"] = newentry["BatteryCharge"]["charge"]
            newentry = {}
    entries.sort(key=(lambda e: e["time"]))
    battery_level = 100
    for entry in entries:
        if "battery" in entry:
            battery_level = entry["battery"]
        else:
            entry["battery"] = battery_level
    return entries


def group_adjacent_points(entries, max_gap = 5):
    bunches = []
    current_time = -1
    entries.sort(key=(lambda e: e["time"]))
    bunch = []
    for entry in entries:
        if entry["time"] > current_time + max_gap:
            bunches.append(bunch)
            bunch = [entry]
        else:
            bunch.append(entry)
        current_time = entry["time"]
    return bunches

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

def filter_bunches_by_accuracy(bunches, min_hori_accu, min_vert_accu):
    filtered_points = []
    for bunch in bunches:
        bunch.sort(key=(lambda e: e["accuracy"][1]))
        for entry in bunch:
            vert_accu, hori_accu = entry["accuracy"]
            if hori_accu <= min_hori_accu and vert_accu <= min_vert_accu:
                filtered_points.append(entry)
                break
    filtered_points.sort(key=(lambda e: e["time"]))
    return filtered_points
