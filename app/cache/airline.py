import os
import requests
from bs4 import BeautifulSoup
import json
import redis
from datetime import timedelta

url = "https://en.wikipedia.org/wiki/List_of_airline_codes"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Initialize Redis client with environment variable
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0, socket_connect_timeout=5)

def fetch_and_store_data(key, index):
    data = {}
    if not redis_client.exists(key):
        for table in soup.find_all("table", class_="wikitable"):
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) < 3:
                    continue
                code = cols[index].get_text(strip=True)
                airline = cols[2].get_text(strip=True)
                if not code or code.lower() == "n/a":
                    continue
                data[code] = airline

        redis_client.setex(key, timedelta(weeks=2), json.dumps(data, ensure_ascii=False, indent=2))
    return json.loads(redis_client.get(key))

def get_icao_mapping():
    return fetch_and_store_data('icao_mapping', 1)

def get_country_mapping():
    return fetch_and_store_data('country_mapping', 1)
