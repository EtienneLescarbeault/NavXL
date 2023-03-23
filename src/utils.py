import datetime
import os
import sys

"""
Adapted from https://github.com/gabrielgz92/location_history_data/blob/master/key_value_parsing.py
"""

def parse_time(time_str):
    formats = ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"]
    for f in formats:
        try:
            return int(datetime.datetime.strptime(time_str, f).utcnow().timestamp())
        except ValueError:
            pass
    raise ValueError("No valid date format found.")

#Returns a list of all the waypoints of a activity.
def activitySegment(activitySegment_dict):
    start_point = activityStartPoint(activitySegment_dict)
    end_point = activityEndPoint(activitySegment_dict)
    return {"start_point": start_point, "end_point": end_point}

#Set start point of activity as a list.
def activityStartPoint(activitySegment_dict):
    trip_id = activitySegment_dict["duration"]["startTimestamp"]
    lat = activitySegment_dict["startLocation"]["latitudeE7"]
    lon = activitySegment_dict["startLocation"]["longitudeE7"]
    # matches 2022-10-01T13:31:22Z
    trip_id = int(parse_time(trip_id))
    time_stamp = timeStampToExcelDate(int(trip_id))
    distance = activitySegment_dict.get("distance", 0)

    #Formatting variables
    lat = int(lat)/1e7
    lon = int(lon)/1e7
    start_point = {"trip_id": trip_id, "lat": lat, "lon": lon, "time_stamp": time_stamp, "distance": distance}
    return start_point

#Set end point of activity as a list.
def activityEndPoint(activitySegment_dict):
    trip_id = activitySegment_dict["duration"]["startTimestamp"]
    lat = activitySegment_dict["endLocation"]["latitudeE7"]
    lon = activitySegment_dict["endLocation"]["longitudeE7"]
    time_stamp = activitySegment_dict["duration"]["endTimestamp"]
    distance = activitySegment_dict.get("distance", 0)
    #Formatting variables
    lat = int(lat)/1e7
    lon = int(lon)/1e7
    trip_id = parse_time(trip_id)
    time_stamp = timeStampToExcelDate(trip_id)
    end_point = {"trip_id": trip_id, "lat": lat, "lon": lon, "time_stamp": time_stamp, "distance": distance}
    return end_point

# Convert milliseconds timestamp into an excel compatible date.
def timeStampToExcelDate(milliseconds):
    temp = datetime.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = datetime.datetime.fromtimestamp(milliseconds/1000) - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

# Method to run all the scripts.
def parseData(data):
    activity_points = []
    for data_unit in data["timelineObjects"]:
        if "activitySegment" in data_unit.keys():
            activity_points.append(activitySegment(data_unit["activitySegment"]))
    return activity_points

def getAllLatLong(parsed_data):
    """
    Alternates between start and end points of each activity segment.
    """
    lat_lon = []
    for point in parsed_data:
        lat_lon.append((point["start_point"]["lat"], point["start_point"]["lon"]))
        lat_lon.append((point["end_point"]["lat"], point["end_point"]["lon"]))
    return lat_lon

def getJSONFiles():
    current_dir = sys.argv[1]
    json_file_names = []
    json_file_names += [each for each in os.listdir(current_dir)
                       if (each.lower().endswith(".json"))]

    return json_file_names

def printJSONList(file_names: str = []):
    # Generates a formatted list in the console
    out = ""
    for i in range(len(file_names)):
        out += '(' + str(i+1) + ') ' + file_names[i] + "   "  # 3 spaces
        if((i + 1) % 3 == 0):
            out += "\n"
    out += "\n(a) Select all\n"
    print(out)