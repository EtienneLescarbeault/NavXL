import json
import random
from utils import parseData, getAllLatLong
from geocodio import GeocodioClient
from settings import GEOCODIO_API_KEY
import xlsxwriter

# init
geocodio_client = GeocodioClient(GEOCODIO_API_KEY)


# test
fileName = "../data/2021_OCTOBER.json"
with open(fileName, 'r', encoding="cp866") as f:
    data = json.load(f)

parsed_data = parseData(data)
parsed_data = random.sample(parsed_data, 5)

all_lat_long = getAllLatLong(parsed_data)
locations = geocodio_client.reverse(all_lat_long)

j = 0
for i, formatted_address in enumerate(locations.formatted_addresses):
    if i % 2 == 0: # start point
        parsed_data[j]["start_point"]["formatted_address"] = formatted_address
    else: # end point
        parsed_data[j]["end_point"]["formatted_address"] = formatted_address
        j += 1


# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('test.xlsx')
date_format = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss'})
bold_format = workbook.add_format({'bold': True})
worksheet = workbook.add_worksheet()

col_names = ["ID", "Date", "Depart", "Arrivee", "Distance (Km)"]
for i, c in enumerate(col_names):
    worksheet.write(0, i, c, bold_format)

print(parsed_data)
for j, line in enumerate(parsed_data):
    row = j + 1
    worksheet.write_number(row, 0, row)
    worksheet.write(row, 1, line["start_point"]["time_stamp"], date_format)
    worksheet.write_string(row, 2, line["start_point"]["formatted_address"])
    worksheet.write_string(row, 3, line["end_point"]["formatted_address"])
    worksheet.write_number(row, 4, line["end_point"]["distance"]/1000)

workbook.close()