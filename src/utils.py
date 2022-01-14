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
    order = 1
    lat = activitySegment_dict["startLocation"]["latitudeE7"]
    lon = activitySegment_dict["startLocation"]["longitudeE7"]
    time_stamp = timeStampToDate(int(trip_id))
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
    time_stamp = timeStampToDate(int(time_stamp))
    end_point = {"trip_id": trip_id, "lat": lat, "lon": lon, "time_stamp": time_stamp, "distance": distance}
    return end_point

#Convert milliseconds timestamp into a readable date.
def timeStampToDate(milliseconds):
    date = datetime.datetime.fromtimestamp(milliseconds/1000.0)
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    return date

#Method to run all the scripts.
def parse_data(data):
    activity_points = []
    visit_points = []
    for data_unit in data["timelineObjects"]:
        if "activitySegment" in data_unit.keys():
            activity_points.append(activitySegment(data_unit["activitySegment"]))
    return activity_points
