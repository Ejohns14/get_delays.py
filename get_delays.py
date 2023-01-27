import psycopg2
import pandas as pd

params_dic = {
    "host"      : "localhost",
    "dbname"    : "flights",
    "user"      : "postgres",
    "password"  : "ebony",
    "port" : "5432"     
}

conn = psycopg2.connect(**params_dic)

cursor = conn.cursor()
cursor.execute("SELECT * FROM real_flight WHERE '0' = cancelled and '0' = diverted" )
rows = cursor.fetchall()


cursor.close()

df = pd.DataFrame(rows, columns=[desc.name for desc in cursor.description])
print(df.head())

