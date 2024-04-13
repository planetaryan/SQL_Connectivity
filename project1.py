import oracledb

#enter in command prompt to see changes made in python
# sqlplus System/harsh123@localhost/xepdb1

con = oracledb.connect(user="SYSTEM", password="harsh123", dsn="localhost/xepdb1")
cur = con.cursor()
cur.execute("drop table branch")
# Create the department1 table
cur.execute("""create table branch (
        id number(3),
        name varchar(20))""")

# Define rows to be inserted
rows = [
    (121, "civil"),
    (122, "mech" ),
    (123, "es" ),
    (124, "eee" ),
    (125, "cse" )
]

# Insert rows into the department1 table
cur.executemany("""insert into branch values(:1, :2)""", rows)

# Fetch all rows from the department1 table
cur.execute("select * from branch")
res = cur.fetchall()

for i,j in res:
    print(i,j,end="\n") 
print(res)
con.commit()
# Close cursor and connection
cur.close()
con.close()
