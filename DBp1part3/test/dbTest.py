import os

from DBp1part3 import sql


rows =sql.fetchall('Photos')
rows =sql.fetchall('Items_posted')
print(rows)
print(os.getcwd())


a = "12345"
print(a[2::-1])