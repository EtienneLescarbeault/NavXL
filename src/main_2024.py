import json
import random
import time
import sys
from utils import getJSONFiles, printJSONList, input_json_files
import xlsxwriter
import os
import json

files, root = getJSONFiles()
files_length = len(files)
if len(files) <= 0:
    print("No JSON file found! Exiting...\n")
    time.sleep(3)
    sys.exit()

printJSONList(files)
chosen_files_ids = input_json_files(files)
sys.stdout.write("Preparing xlsx file...\n")

# open the file and read the content
with open('../data/location_history/semantic_location_history/2023/2023_APRIL.json', 'r') as f:
    data = json.load(f)
    timeline_objs = data['timelineObjects']
    print(len(timeline_objs))
    for i in range(0, len(timeline_objs)-1, 2):
        act = timeline_objs[i]['activitySegment']
        distance_m = 0
        if 'distance' in act:
            distance_m = act['distance']

        start_time = act['duration']['startTimestamp'].split('T')[0]
        start_lat = act['startLocation']['latitudeE7']
        start_long = act['startLocation']['longitudeE7']
        
        end_lat = act['endLocation']['latitudeE7']
        end_long = act['endLocation']['longitudeE7']  # should correspond to placeVisit
        
        adress = timeline_objs[i+1]['placeVisit']['location']['address']
        #print(i)
        
