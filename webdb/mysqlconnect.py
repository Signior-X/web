import mysql.connector
from dotenv import load_dotenv
import os
from mysql.connector import Error as sqlerror

load_dotenv()

mydb = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    db = os.getenv("DB")
)

mycursor = mydb.cursor()

def create_insert_statement(data):   #pass the data in the JSON Format
    
    clst=""+data["tablename"]+"("
    vlst="("
    data.pop("tablename")
    for key in data:
        clst+=key+","
        vlst+="'"+data[key]+"',"

    if clst[-1]==',':
        clst=clst[:-1]
    if vlst[-1]==',':
        vlst=vlst[:-1]
    clst+=")"
    vlst+=')'

    stmt = "INSERT INTO "+clst+" VALUES"+vlst+";"
    return stmt
