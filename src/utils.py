import datetime
import os
import sys
import time

"""
Adapted from https://github.com/gabrielgz92/location_history_data/blob/master/key_value_parsing.py
"""

def parse_time(time_str):
    formats = ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"]
    for f in formats:
        try:
            return int(time.mktime(datetime.datetime.strptime(time_str, f).timetuple()))
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
    trip_id = parse_time(trip_id)
    time_stamp = timeStampToExcelDate(trip_id)
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
def timeStampToExcelDate(unix_timestamp):
    return (unix_timestamp / 86400) + 25569 + 1



def getJSONFiles():
    current_dir = sys.argv[1]
    json_file_names = []
    json_file_names += [each for each in os.listdir(current_dir)
                       if (each.lower().endswith(".json"))]

    return json_file_names, current_dir

def printJSONList(file_names: str = []):
    # Generates a formatted list in the console
    out = ""
    for i in range(len(file_names)):
        out += '(' + str(i+1) + ') ' + file_names[i] + "   "  # 3 spaces
        if((i + 1) % 3 == 0):
            out += "\n"
    out += "\n(a) Select all\n"
    print(out)
    
def input_json_files(files: list):
    files_length = len(files)
    index_arr = []
    valid = False
    while not valid:
        index_seq = input("Sequence of files for xlsx creation\n").split()
        valid = True
        if len(index_seq) == 0:
            valid = False

        if 'a' in index_seq: # Option to merge all files in ascending order
            index_seq = range(1, files_length+1)

        for i in index_seq:
            try:
                file_num = int(i)
                if file_num > files_length or file_num < 1:
                    raise Exception()
                index_arr.append(file_num-1)
            except Exception:
                print("Invalid input: " + str(i))
                print("""     - Make sure to enter a valid number sequence separated by spaces
        - The numbers must match the file indices
                """)
                printJSONList(files)
                valid = False
                index_seq = ""
                index_arr = []
    return index_arr