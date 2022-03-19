import psycopg2
host_name = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"
user_name = "hs3239"
password = "7505"


engine = psycopg2.connect(
    database="proj1part2",
    user=user_name,
    password=password,
    host=host_name,
    port='5432'
)
# import psycopg2
# conn = psycopg2.connect(database='proj1part2',user='hs3239',password='7505',host="127.0.0.1", port="5000")
cur = engine.cursor()
cur.execute("SELECT * FROM Users")

# cur = conn.cursor()
# cur.execute("SELECT * FROM table1 LIMIT 10")
rows = cur.fetchall()
print(rows)
# conn.commit()
# cur.close()
# conn.close()
# print("Opened database successfully")