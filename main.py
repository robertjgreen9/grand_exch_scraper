import os
from dotenv import dotenv_values, load_dotenv
load_dotenv()
from pathlib import Path
import requests
from ids import ids
import ssl
import pymysql.cursors
import time
import json


url = "https://api.weirdgloop.org/exchange/history/rs/latest?id="

# Finds the config file in the project folder
current_directory = os.path.dirname(os.path.realpath(__file__))
dotenv_path = f"{current_directory}/.env"
config = dotenv_values(dotenv_path)

connection = pymysql.connect(
  host= os.getenv("HOST"),
  user=os.getenv("USERNAME"),
  passwd= os.getenv("PASSWORD"),
  db= os.getenv("DATABASE"),
  ssl_ca = "/etc/ssl/certs/ca-certificates.crt",
  cursorclass = pymysql.cursors.DictCursor
)

# Creates the cursor object, which is the method for interacting with the database
cursor = connection.cursor()


# Load the GE API's JSON for each ID
def load_json(url, id):
    r = requests.get(f"{url}{id}")
    return r.json()

# Read the JSON and return the ID, Price and Scraping timestamp
def parse_json(json, id):
    keys = json[f"{id}"]
    id, price, timestamp = keys['id'], keys['price'], keys['timestamp']
    return id, price, timestamp

def load_timestamp_json():
    with open("/home/pi/grand_exch_scraper/last_time_stamp.json", "r") as jsonFile:
        timestamp_json = json.load(jsonFile)
    timestamp_record = timestamp_json
    return timestamp_record

def update_timestamp_json(new_timestamp):
    with open("/home/pi/grand_exch_scraper/last_time_stamp.json", "w") as jsonFile:
        json.dump(new_timestamp, jsonFile)

# Testing the write and commit
def write_to_table(cursor, id, price, timestamp):
    sql = "INSERT INTO grand_exchange_data (id, price, timestamp) VALUES (%s, %s, %s)"
    val = id, price, timestamp
    cursor.execute(sql, val)
    connection.commit()

def run_script():
    old_timestamp = str(load_timestamp_json())
    for i in range(0, len(ids)):
        json = load_json(url, ids[i])
        id, price, timestamp = parse_json(json, ids[i])
        if timestamp == old_timestamp:
            pass
        else:
            write_to_table(cursor, id, price, timestamp)
    update_timestamp_json(timestamp)
    
run_script()

connection.close()
