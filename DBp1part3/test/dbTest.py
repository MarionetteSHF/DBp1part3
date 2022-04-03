import os

from DBp1part3 import sql


rows =sql.fetchall('Photos')
print(rows)
print(os.getcwd())


a = "12345"
print(a[2::-1])