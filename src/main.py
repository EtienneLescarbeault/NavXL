import json
import random
import time
import sys
from utils import getJSONFiles, parseData, getAllLatLong, printJSONList
from geocodio import GeocodioClient
from settings import GEOCODIO_API_KEY
import xlsxwriter

# init
#geocodio_client = GeocodioClient(GEOCODIO_API_KEY)

files = getJSONFiles()
files_length = len(files)
if files_length <= 0:
    print("No JSON file found! Exiting...\n")
    time.sleep(3)
    sys.exit()

printJSONList(files)

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

sys.stdout.write("Preparing xlsx file...\n")

data_arr = []
for i in index_arr:
    try:
        f = open(files[i], 'r', encoding="cp866")
        data = json.load(f)
    except:
        print("Error: Could not open " + files[i])
        print("It will be ignored in the process. \n")
        continue
    try:
        parsed_data = parseData(data)
        data_arr.extend(parsed_data)
    except Exception as e:
        print(e)
        print("Error: Could not parse " + files[i] + ". File is incompatible.\n")
        print("It will be ignored in the process. \n")
        continue

if len(data_arr) <= 0:
    print("No valid data found! Exiting...\n")
    time.sleep(3)   
    sys.exit()
print(data_arr[0])

"""all_lat_long = getAllLatLong(data_arr)
locations = geocodio_client.reverse(all_lat_long)
with open('response.json', 'w') as f:
    json.dump(locations, f)"""

with open('response.json', 'r') as f:
    locations = json.load(f)

formatted_addresses = []
for l in locations:
    formatted_address = l["results"][0]["formatted_address"]
    formatted_addresses.append(formatted_address)

j = 0
for i, formatted_address in enumerate(formatted_addresses):
    if i % 2 == 0: # start point
        parsed_data[j]["start_point"]["formatted_address"] = formatted_address
    else: # end point
        parsed_data[j]["end_point"]["formatted_address"] = formatted_address
        j += 1

sys.stdout.flush()
sys.stdout.write = "Done!"

output_name = input("Output name: \n")
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(output_name + '.xlsx')
date_format = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss'})
bold_format = workbook.add_format({'bold': True})
worksheet = workbook.add_worksheet()

col_names = ["ID", "Date", "Depart", "Arrivee", "Distance (Km)"]
for i, c in enumerate(col_names):
    worksheet.write(0, i, c, bold_format)

for j, line in enumerate(parsed_data):
    row = j + 1
    worksheet.write_number(row, 0, row)
    worksheet.write(row, 1, line["start_point"]["time_stamp"], date_format)
    worksheet.write_string(row, 2, line["start_point"]["formatted_address"])
    worksheet.write_string(row, 3, line["end_point"]["formatted_address"])
    worksheet.write_number(row, 4, line["end_point"]["distance"]/1000)

workbook.close()
sys.exit()