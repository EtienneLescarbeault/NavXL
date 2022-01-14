import json
from utils import parse_data

# test
fileName = "../data/2021_OCTOBER.json"
with open(fileName, 'r', encoding="cp866") as f:
    data = json.load(f)

a = parse_data(data)
print(a)