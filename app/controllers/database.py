from dotenv import load_dotenv
from os import getenv
import pymysql.cursors
from pymysql import converters

load_dotenv()


def db_connect():
    return pymysql.connect(host=getenv('DB_HOST'),
                           port=3306,
                           user=getenv('DB_USER'),
                           password=getenv('DB_PASSWORD'),
                           database=getenv('DB_DATABASE'))
