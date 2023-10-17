import psycopg2

def connect():
    conn = psycopg2.connect(database="DersKayitSys",
                        host="localhost",
                        user="emre",
                        password="123",
                        port="5432")
    return conn;
