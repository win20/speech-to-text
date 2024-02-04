import os
import pymysql.cursors
from pymysql import converters


converions = converters.conversions
converions[pymysql.FIELD_TYPE.BIT] = lambda x: False if x == b'\x00' else True


def init_connection():
    conn = pymysql.connect(host=os.getenv('DB_HOST'),
                           port=3306,
                           user=os.environ.get('DB_USER'),
                           password=os.environ.get('DB_PASSWORD'),
                           database=os.environ.get('DB_DATABASE'),
                           cursorclass=pymysql.cursors.DictCursor,
                           conv=converions,
                           )
    return conn


def query_get(sql, param):
    connection = init_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, param)
            return cursor.fetchall()


def query_put(sql, param):
    connection = init_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, param)
            connection.commit()
            return cursor.lastrowid


def query_update(sql, param):
    connection = init_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, param)
            connection.commit()
            return True
