import json
from utils import parse_data

# test
fileName = "2021_OCTOBER.json"
with open(f"data/{fileName}") as f:
    data = json.load(f)

parse_data(data)