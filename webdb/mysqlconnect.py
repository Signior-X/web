import mysql.connector
from dotenv import load_dotenv
import os

cwd = os.getcwd()
envindex = cwd.find("webdb")
if envindex == -1:
    load_dotenv(cwd+'/.env')
else:
    load_dotenv(cwd[:envindex]+'/.env')

mydb = mysql.connector.connect(
    host = os.environ.get("DB_HOST"),
    port = os.environ.get("DB_PORT"),
    user = os.environ.get("DB_USER"),
    password = os.environ.get("DB_PASSWORD"),
    db = os.environ.get("DB")
)

mycursor = mydb.cursor()
