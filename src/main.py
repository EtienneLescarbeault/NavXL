import json
from utils import parseData, getAllLatLong
from geocodio import GeocodioClient
from settings import GEOCODIO_API_KEY

# init
geocodio_client = GeocodioClient(GEOCODIO_API_KEY)


# test
fileName = "../data/2021_OCTOBER.json"
with open(fileName, 'r', encoding="cp866") as f:
    data = json.load(f)

parsed_data = parseData(data)


#all_lat_long = getAllLatLong(parsed_data)
#locations = geocodio_client.reverse(all_lat_long)
with open("../data/EMULATED_RESP.json", 'r') as f:
    locations = json.load(f)

res_arr = locations["results"]
for i, res_elem in enumerate(res_arr):
    address_elem = res_elem["response"]["results"][0] # Most likely address is the first in the list
    formatted_address = address_elem["formatted_address"]
    print(formatted_address)
