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


all_lat_long = getAllLatLong(parsed_data)
locations = geocodio_client.reverse(all_lat_long)

print(locations)