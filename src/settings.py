import os
from dotenv import load_dotenv

dotenv_path = "../.env" # Path to .env file, change as needed
load_dotenv(dotenv_path)
GEOCODIO_API_KEY = os.environ.get("GEOCODIO_API_KEY")
print(GEOCODIO_API_KEY)