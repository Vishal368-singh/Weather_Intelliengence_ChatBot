from decimal import Decimal
from datetime import datetime, date, time
from Database.db import get_connection


def convert_value(value):

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date, time)):
        return value.isoformat()

    return value


def execute_sql(sql):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sql)

    columns = [desc[0] for desc in cur.description]

    rows = []

    for row in cur.fetchall():

        rows.append({
            columns[i]: convert_value(row[i])
            for i in range(len(columns))
        })

    cur.close()
    conn.close()

    return rows