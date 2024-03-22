import json
import random
import time
import sys
from utils import getJSONFiles, printJSONList, input_json_files
import xlsxwriter
import os
from geocodio import GeocodioClient
from settings import GEOCODIO_API_KEY

geocodio_client = GeocodioClient(GEOCODIO_API_KEY)

available_files, root = getJSONFiles()
if len(available_files) <= 0:
    print("No JSON file found! Exiting...\n")
    time.sleep(3)
    sys.exit()

printJSONList(available_files)

chosen_files_ids = input_json_files(available_files)

output_name = 'output.xlsx'
workbook = xlsxwriter.Workbook('output.xlsx')
date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
bold_format = workbook.add_format({'bold': True})
worsheet = workbook.add_worksheet()

col_names = ["Date", "start_lat", "start_long", "end_lat", "end_long", "address", "distance"]
for i, col_name in enumerate(col_names):
    worsheet.write(0, i, col_name, bold_format)
    
row = 1
for i in chosen_files_ids:
    file_path = os.path.join(root, available_files[i])
    with open(file_path, 'r') as f:
        data = json.load(f)
        timeline_objs = data['timelineObjects']
        for i in range(0, len(timeline_objs)-1, 2):
            act = timeline_objs[i]['activitySegment']
            distance_m = 0
            if 'distance' in act:
                distance_m = act['distance'] / 1000 # kms
            start_date = act['duration']['startTimestamp'].split('T')[0]
            start_lat = act['startLocation']['latitudeE7']
            start_long = act['startLocation']['longitudeE7']
            
            
            end_lat = act['endLocation']['latitudeE7']
            end_long = act['endLocation']['longitudeE7']  # should correspond to placeVisit
                        
            adress = timeline_objs[i+1]['placeVisit']['location']['address']
            
            #worsheet.write_number(row, 0, row)
            worsheet.write(row, 0, start_date, date_format)
            worsheet.write_number(row, 1, start_lat)
            worsheet.write_number(row, 2, start_long)
            worsheet.write_number(row, 3, end_lat)
            worsheet.write_number(row, 4, end_long)
            worsheet.write_string(row, 5, adress)
            worsheet.write_number(row, 6, distance_m)
            row += 1
workbook.close()
print("File created successfully!")
print("Exiting...")
