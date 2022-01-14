import json
from utils import parse_data
from geocodio import GeocodioClient
from settings import GEOCODIO_API_KEY

# init
geocodio_client = GeocodioClient(GEOCODIO_API_KEY)


# test
fileName = "../data/2021_OCTOBER.json"
with open(fileName, 'r', encoding="cp866") as f:
    data = json.load(f)

parsed_data = parse_data(data)

a = geocodio_client.geocode("42370 Bob Hope Drive, Rancho Mirage CA")
print(a)