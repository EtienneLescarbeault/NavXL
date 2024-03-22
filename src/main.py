import json
import random
import time
import sys
from utils import getJSONFiles, printJSONList, input_json_files
import xlsxwriter
import os
from geocodio import GeocodioClient
from settings import GEOCODIO_API_KEY
from tqdm import tqdm, trange

geocodio_client = GeocodioClient(GEOCODIO_API_KEY)

available_files, root = getJSONFiles()
if len(available_files) <= 0:
    print("No JSON file found! Exiting...\n")
    time.sleep(3)
    sys.exit()

printJSONList(available_files)

chosen_files_ids = input_json_files(available_files)

output_name = input("Enter the name of the output file (no extension): ")
workbook = xlsxwriter.Workbook(output_name + '.xlsx')
date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
bold_format = workbook.add_format({'bold': True})
worsheet = workbook.add_worksheet()

col_names = ["date", "start_address", "end_address", "distance_km"]
for i, col_name in enumerate(col_names):
    worsheet.write(0, i, col_name, bold_format)

# December has a missing activitySegment key
row = 1
for i in chosen_files_ids:
    file_path = os.path.join(root, available_files[i])
    with open(file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        timeline_objs = data['timelineObjects']
        for i in trange(0, len(timeline_objs), postfix=f"{available_files[i]}"):
            if 'activitySegment' not in timeline_objs[i]:
                continue
            act = timeline_objs[i]['activitySegment']
            distance_m = 0.0
            if 'distance' in act:
                distance_m = act['distance']
            distance_m = distance_m / 1000
            start_date = act['duration']['startTimestamp'].split('T')[0]
            
            start_lat = act['startLocation']['latitudeE7'] / 1e7
            start_long = act['startLocation']['longitudeE7'] / 1e7
            
            
            end_lat = act['endLocation']['latitudeE7'] / 1e7
            end_long = act['endLocation']['longitudeE7'] / 1e7  # should correspond to placeVisit
            
            locations = geocodio_client.reverse([
                (start_lat, start_long),
                (end_lat, end_long)
            ])      
            start_address = locations.formatted_addresses[0]
            end_address = locations.formatted_addresses[1] 
            
            #worsheet.write_number(row, 0, row)
            worsheet.write(row, 0, start_date, date_format)
            worsheet.write_string(row, 1, start_address)
            worsheet.write_string(row, 2, end_address)
            worsheet.write_number(row, 3, distance_m)
            row += 1
workbook.close()
print("File created successfully!")
print("Exiting...")
