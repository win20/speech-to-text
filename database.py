from dotenv import load_dotenv
from os import getenv
import MySQLdb

load_dotenv()


def db_connect():
    db_config = {
        'host': getenv('DB_HOST'),
        'user': getenv('DB_USER'),
        'passwd': getenv('DB_PASSWORD'),
        'db': getenv('DB_DATABASE'),
    }

    return MySQLdb.connect(**db_config)
