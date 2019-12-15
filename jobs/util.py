import sqlite3, os
from flask import g

PATH = os.getenv("DB_PATH", "db/jobs.sqlite")
ALLOWED_EXTENSIONS = {"txt", "pdf", "doc", "docx"}


def open_connection():
    connection = getattr(g, "_connection", None)

    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row

    return connection


def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)

    if commit:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
