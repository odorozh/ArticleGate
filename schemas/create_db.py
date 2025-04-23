#! /usr/bin/python3

import sqlite3

def create_article_gate_db(db_filename, sql_cmd):
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    cursor.executescript(sql_cmd)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    db_filename = 'article_gate.sqlite3'
    create_sql_filename = 'create_db.sql'

    create_sql_cmd = None
    with open(create_sql_filename, 'r') as cmdf:
        create_sql_cmd = cmdf.read()

    create_article_gate_db(db_filename, create_sql_cmd)
