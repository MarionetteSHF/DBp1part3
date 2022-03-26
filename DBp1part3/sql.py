import psycopg2,functools
from flask import current_app, g

from flask.cli import with_appcontext
# with app.app_context():


# def get_db():
#     if 'db' not in g:
#         g.db = psycopg2.connect(
#         current_app.config['DATABASE'],
#         database="proj1part2",
#         user=user_name,
#         password=password,
#         host=host_name,
#
#         port='5432'
#     )
#     return g.db
#
# def close_db(e=None):
#     db = g.pop('db', None)
#
#     if db is not None:
#         db.close()

host_name = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"
user_name = "hs3239"
password = "7505"

def get_db():

    engine = psycopg2.connect(
        database="proj1part2",
        user=user_name,
        password=password,
        host=host_name,
        port='5432'
    )

    return engine

def fetchall(table_name):

    engine = get_db()
    cur = engine.cursor()

    engine.commit()

    cur.execute("SELECT * FROM "+ str(table_name))
    rows = cur.fetchall()
    # rows = cur.fetchone()

    engine.close()
    return rows



#     # engine.commit()
#     # cur.close()
#     # engine.close()
# print("Opened database successfully")
