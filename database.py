import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv()
import os

def init():
    DB_HOST = os.getenv("DB_HOST")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    database = mysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
    )
    database.autocommit = True
    cursor = database.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS " + DB_NAME)
    cursor.execute("USE " + DB_NAME)
    cursor.execute("")
