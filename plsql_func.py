import oracledb


con = oracledb.connect(user="System", password="harsh123", dsn="localhost/xepdb1")
cur = con.cursor()

res = cur.callfunc('myfunc', int, ('abc', 2))
print(res)