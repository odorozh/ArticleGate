#! /usr/bin/python3

import sqlite3

def article_gate_db_exec(db_filename, sql_cmd):
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    cursor.executescript(sql_cmd)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    db_filename = 'article_gate.sqlite3'
    create_sql_filename = 'create_db.sql'
    fill_data_sql_filename = 'fill_init_data.sql'

    create_sql_cmd = None
    with open(create_sql_filename, 'r') as cmdf:
        create_sql_cmd = cmdf.read()

    fill_sql_cmd = None
    with open(fill_data_sql_filename, 'r') as cmdf:
        fill_sql_cmd = cmdf.read()

    article_gate_db_exec(db_filename, create_sql_cmd)
    article_gate_db_exec(db_filename, fill_sql_cmd)
