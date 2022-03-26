from DBp1part3 import sql

import datetime
rows =sql.fetchall('Items_Posted')
print(rows)
print(datetime.datetime.now().strftime("%m/%d/%Y"))