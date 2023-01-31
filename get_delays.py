import psycopg2
import pandas as pd
from config import params_dic



conn = psycopg2.connect(**params_dic)

cursor = conn.cursor()
cursor.execute("SELECT * FROM real_flight WHERE '0' = cancelled and '0' = diverted" )
rows = cursor.fetchall()


cursor.close()

df = pd.DataFrame(rows, columns=[desc.name for desc in cursor.description])
print(df.head())

missing_rows = df[df["arr_del15"].isna()]
print(len(missing_rows))
missing_rows = df[df["dep_del15"].isna()]
print(len(missing_rows))


df["delayed"] = np.where((df["arr_del15"] == '1') | (df["dep_del15"] == "1"), 1, 0)

airline_delays = df.groupby("op_unique_carrier")["delayed"].mean()
airline_delays.sort_values(inplace=True, ascending=False)
print(airline_delays)

airline_delays.plot.bar()

airport_delays = df.groupby("origin")["delayed"].mean()
airport_delays.sort_values(inplace=True, ascending=False)
airport_delays.to_csv("airport_delays_jan.csv")
print(airport_delays)

airport_delays.plot.bar()
