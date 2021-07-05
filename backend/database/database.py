from datetime import date, datetime
import mysql.connector as mysql
from dotenv import load_dotenv
from json import loads as from_JSON, dumps as to_JSON

load_dotenv()
import os

def init():
    DB_HOST = os.getenv("DB_HOST")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_TABLE_NAME = os.getenv("TABLE_NAME")

    database = mysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
    )
    database.autocommit = True
    cursor = database.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS " + DB_NAME)
    cursor.execute("USE " + DB_NAME)
    cursor.execute("CREATE TABLE IF NOT EXISTS " + DB_TABLE_NAME + " (ID INT AUTO_INCREMENT PRIMARY KEY, SENDER VARCHAR(30) NOT NULL, SENT_ON DATE DEFAULT CURDATE(), LOCATIONS JSON NOT NULL, START VARCHAR(30) NOT NULL, RESULT JSON NOT NULL, SPEED REAL DEFAULT 40.0)")

def push(sender: str, locations: list, start: str, result: list, speed: float, sent_on: date = datetime.now().date()):
    DB_HOST = os.getenv("DB_HOST")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_TABLE_NAME = os.getenv("TABLE_NAME")

    database = mysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    database.autocommit = True
    cursor = database.cursor()

    query: str = "INSERT INTO " + DB_TABLE_NAME + " (SENDER, SENT_ON, LOCATIONS, START, RESULT, SPEED) VALUES (%s, %s, %s, %s, %s, %s)"
    sender = sender
    sent_on = str(sent_on)
    locations = to_JSON(locations)
    start = start
    result = to_JSON(result)

    cursor.execute(query, (sender, sent_on, locations, start, result, speed))
    print("Successfully inserted a data into database.")

def get_latest():
    DB_HOST = os.getenv("DB_HOST")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_TABLE_NAME = os.getenv("TABLE_NAME")

    database = mysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    database.autocommit = True
    cursor = database.cursor()

    cursor.execute("SELECT * FROM " + DB_TABLE_NAME + " ORDER BY ID DESC LIMIT 1")
    all_attributes = cursor.fetchone()

    return all_attributes

def get_by_name_and_date(sender: str, sent_on: date=datetime.now().date):
    DB_HOST = os.getenv("DB_HOST")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_TABLE_NAME = os.getenv("TABLE_NAME")

    database = mysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    database.autocommit = True
    cursor = database.cursor()

    sender = "'".__add__(sender).__add__("'")
    sent_on = "'".__add__(str(sent_on)).__add__("'")
    
    cursor.execute("SELECT * FROM " + DB_TABLE_NAME + " WHERE SENDER=" + sender + " AND SENT_ON=" + sent_on + " ORDER BY ID DESC LIMIT 1")
    all_attributes = cursor.fetchone()

    return all_attributes

'''
def delete():
    DB_HOST = os.getenv("DB_HOST")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_TABLE_NAME = os.getenv("TABLE_NAME")

    database = mysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    database.autocommit = True
    cursor = database.cursor()

    cursor.execute("DELETE FROM " + DB_TABLE_NAME)
'''