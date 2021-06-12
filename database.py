import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv()
import os

def init():
    database = mysql.connect(
        host="DB_HOST",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
    )
    database.autocommit = True
    cursor = database.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS " + os.getenv("DB_NAME"))
    cursor.execute("USE " + os.getenv("DB_NAME"))
    cursor.execute("")
