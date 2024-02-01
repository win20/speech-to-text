from dotenv import load_dotenv, find_dotenv
from os import getenv
import pymysql.cursors

load_dotenv()


def db_connect():
    conn = pymysql.connect(host=getenv('DB_HOST'),
                           port=3306,
                           user=getenv('DB_USER'),
                           password=getenv('DB_PASSWORD'),
                           database=getenv('DB_DATABASE'),
                           cursorclass=pymysql.cursors.DictCursor,
                           )

    return conn
