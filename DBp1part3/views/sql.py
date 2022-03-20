import psycopg2,functools
host_name = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"
user_name = "hs3239"
password = "7505"

def connectToDB():

    engine = psycopg2.connect(
        database="proj1part2",
        user=user_name,
        password=password,
        host=host_name,
        port='5432'
    )
    return engine.cursor()
# import psycopg2
# conn = psycopg2.connect(database='proj1part2',user='hs3239',password='7505',host="127.0.0.1", port="5000")

def fetchall(table_name):

    cur = connectToDB()
    # rows= cur.execute("SELECT * FROM Users").fetchone()
    cur.execute("SELECT * FROM "+ str(table_name))
    rows = cur.fetchall()
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM table1 LIMIT 10")
    # rows = cur.fetchall()

    return rows
rows = fetchall('Items_Posted')[0]
print(rows[0])
print(fetchall('Items_Posted')[0])
    # engine.commit()
    # cur.close()
    # engine.close()
print("Opened database successfully")