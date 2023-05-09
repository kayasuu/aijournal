import psycopg2
import os

def sql_read(query, parameters):
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("JUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    results = cursor.fetchall()
    connection.close()
    return results

def sql_write(query, parameters):
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("JUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    connection.close()

#    connection = psycopg2.connect(dbname="journal_db", port=5433, password="3113")
