import os

from DBp1part3 import sql


rows =sql.fetchall('Users')
# rows =sql.fetchall('Items_posted')
print(rows)
print(os.getcwd())


