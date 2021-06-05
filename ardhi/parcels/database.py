import psycopg2


def get_cursor():
    conn = psycopg2.connect(dbname="LandIs", user="postgres", password="kevoh", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    return cursor
