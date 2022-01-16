import datetime

"""
Adapted from https://github.com/gabrielgz92/location_history_data/blob/master/key_value_parsing.py
"""

#Returns a list of all the waypoints of a activity.
def activitySegment(activitySegment_dict):
    start_point = activityStartPoint(activitySegment_dict)
    end_point = activityEndPoint(activitySegment_dict)
    return {"start_point": start_point, "end_point": end_point}

#Set start point of activity as a list.
def activityStartPoint(activitySegment_dict):
    trip_id = activitySegment_dict["duration"]["startTimestampMs"]
    lat = activitySegment_dict["startLocation"]["latitudeE7"]
    lon = activitySegment_dict["startLocation"]["longitudeE7"]
    time_stamp = timeStampToExcelDate(int(trip_id))
    distance = activitySegment_dict.get("distance", 0)

    #Formatting variables
    lat = int(lat)/1e7
    lon = int(lon)/1e7
    start_point = {"trip_id": trip_id, "lat": lat, "lon": lon, "time_stamp": time_stamp, "distance": distance}
    return start_point

#Set end point of activity as a list.
def activityEndPoint(activitySegment_dict):
    trip_id = activitySegment_dict["duration"]["startTimestampMs"]
    lat = activitySegment_dict["endLocation"]["latitudeE7"]
    lon = activitySegment_dict["endLocation"]["longitudeE7"]
    time_stamp = activitySegment_dict["duration"]["endTimestampMs"]
    distance = activitySegment_dict.get("distance", 0)
    #Formatting variables
    lat = int(lat)/1e7
    lon = int(lon)/1e7
    time_stamp = timeStampToExcelDate(int(time_stamp))
    end_point = {"trip_id": trip_id, "lat": lat, "lon": lon, "time_stamp": time_stamp, "distance": distance}
    return end_point

#Convert milliseconds timestamp into a readable date.
def timeStampToExcelDate(milliseconds):
    temp = datetime.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = datetime.datetime.fromtimestamp(milliseconds/1000) - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

#Method to run all the scripts.
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