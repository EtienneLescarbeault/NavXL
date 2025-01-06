import json
import time
import sys
from utils import getJSONFiles, printJSONList, input_json_files
import xlsxwriter
import os
from geocodio import GeocodioClient
from settings import GEOCODIO_API_KEY
from tqdm import trange


def latlng_to_float(coord_string: str) -> tuple[float, float]:
    lat_str, lon_str = coord_string .replace('°', '').split(', ')
    return (float(lat_str), float(lon_str))
    

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

row = 1
for i in chosen_files_ids:
    file_path = os.path.join(root, available_files[i])
    with open(file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        semantic_segments = data['semanticSegments']
        for i in trange(0, len(semantic_segments), postfix=f"{available_files[i]}"):
            seg = semantic_segments[i]

            if 'activity' not in seg:
                continue
            act = seg['activity']
            
            if act['topCandidate']['type'] != 'IN_PASSENGER_VEHICLE':
                continue
    
            distance_km = 0.0
            if 'distanceMeters' in act:
                distance_km = act['distanceMeters'] / 1000
            start_date = seg['startTime'].split('T')[0]
            
            start_lat, start_long = latlng_to_float(act['start']['latLng'])            
            end_lat, end_long = latlng_to_float(act['end']['latLng'])
            
            locations = geocodio_client.reverse([
                (start_lat, start_long),
                (end_lat, end_long)
            ])      

            start_address = locations.formatted_addresses[0]
            end_address = locations.formatted_addresses[1] 
            
            worsheet.write(row, 0, start_date, date_format)
            worsheet.write_string(row, 1, start_address)
            worsheet.write_string(row, 2, end_address)
            worsheet.write_number(row, 3, distance_km)
            row += 1
workbook.close()
print("File created successfully!")
print("Exiting...")
