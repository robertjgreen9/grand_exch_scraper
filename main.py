import os
from dotenv import dotenv_values
from pathlib import Path
from mysql.connector import Error
import mysql.connector
import requests
from ids import ids 

url = "https://api.weirdgloop.org/exchange/history/rs/latest?id="

# Finds the config file in the project folder
dotenv_path = Path('009 MySQL\.env')
config = dotenv_values(dotenv_path)

# Opens the connection to the server in the config .env
connection = mysql.connector.connect(
    host = config["HOST"],
    database = config["DATABASE"],
    user = config["USERNAME"],
    password = config["PASSWORD"],
    ssl_ca = os.getenv("SSL_CERT")
)

# Creates the cursor object, which is the method for interacting with the database
try:
    if connection.is_connected():
        cursor = connection.cursor()
    cursor.execute("select @@version ")
    version = cursor.fetchone()
    if version:
        print('Running version: ', version)
    else:
        print('Not connected.')
except Error as e:
    print("Error while connecting to MySQL", e)


# Load the GE API's JSON for each ID
def load_json(url, id):
    r = requests.get(f"{url}{id}")
    return r.json()

# Read the JSON and return the ID, Price and Scraping timestamp
def parse_json(json, id):
    keys = json[f"{id}"]
    id, price, timestamp = keys['id'], keys['price'], keys['timestamp']
    return id, price, timestamp

# Testing the write and commit
def write_to_table(cursor, id, price, timestamp):
    sql = "INSERT INTO grand_exchange_data (id, price, timestamp) VALUES (%s, %s, %s)"
    val = id, price, timestamp
    cursor.execute(sql, val)
    connection.commit()

for i in range(0, len(ids)):
    json = load_json(url, ids[i])
    id, price, timestamp = parse_json(json, ids[i])
    write_to_table(cursor, id, price, timestamp)

connection.close()