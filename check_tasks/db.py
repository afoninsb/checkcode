from datetime import datetime
from typing import Any

import psycopg2
from config import config


def connect():
    try:
        return psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
    except Exception as e:
        print('Can`t establish connection to database', e)


def save_result(data: dict[str, Any]):
    """Сохраняем результат анализа в базу данных."""
    conn = connect()
    cursor = conn.cursor()
    sql = (
        'INSERT INTO files_checkcode '
        '(code_id, time, result, status, sent_email) '
        'VALUES (%s, %s, %s, %s, %s)'
    )
    values = (
        data['code_id'], datetime.now(), data['result'], data['status'], False
    )
    cursor.execute(sql, values)
    conn.commit()
    sql = (
        f'SELECT * FROM files_checkcode WHERE code_id={data["code_id"]} '
        'ORDER BY time DESC'
    )
    cursor.execute(sql)
    conn.commit()
    check_id = cursor.fetchone()[0]
    sql = 'UPDATE files_codefile SET status = %s WHERE id = %s'
    cursor.execute(sql, (data['status'], data['code_id']))
    conn.commit()
    cursor.close()
    conn.close()
    return check_id


def update_result(check_id: int):
    """Обновляем результат анализа после отправки письма."""
    conn = connect()
    cursor = conn.cursor()
    sql = 'UPDATE files_checkcode SET sent_email = %s WHERE id = %s'
    cursor.execute(sql, (True, check_id))
    conn.commit()
    cursor.close()
    conn.close()
