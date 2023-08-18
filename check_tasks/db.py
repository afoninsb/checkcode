from typing import Any
import psycopg2
from config import config


def connect():
    try:
        return psycopg2.connect(config.DB_URI)
    except Exception:
        print('Can`t establish connection to database')


def save_result(data: dict[str, Any]):
    conn = connect()
    sql = (
        'INSERT INTO files_checkcode (code_id, result, status, sent_email) '
        'VALUES (%s, %s, %s, %s), '
        f'({data["code_id"]}, {data["result"]}, {data["status"]}, False)'
    )
    with conn.cursor() as curs:
        curs.execute(sql)
        return curs.fetchone()[0]


def update_result(check_id: int):
    conn = connect()
    sql = (
        'UPDATE files_checkcode SET sent_email = %s WHERE id = %s'
        f', (True, {check_id})'
    )
    with conn.cursor() as curs:
        curs.execute(sql)
