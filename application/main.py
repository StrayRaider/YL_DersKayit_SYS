import psycopg2

conn = psycopg2.connect(database="DersKayitSys",
                        host="localhost",
                        user="emre",
                        password="123",
                        port="5432")


command = """
    CREATE TABLE emre (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
)"""

cursor = conn.cursor()
cursor.execute(command)

ınsertNew = """ INSERT INTO emre VALUES ('1', 'emre');  """
cursor.execute(ınsertNew)

cursor.execute("SELECT * FROM emre WHERE id = 1")

print(cursor.fetchone())

