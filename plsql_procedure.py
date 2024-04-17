import oracledb

# Establish a connection to the Oracle database
connection = oracledb.connect(user="System", password="harsh123", dsn="localhost/xepdb1")

# Create a cursor object
cursor = connection.cursor()

try:
    # Bind variables for input and output parameters
    v1 =int(input("enter number "))
    v2 = cursor.var(oracledb.NUMBER)

    # Execute the PL/SQL procedure
    cursor.callproc("myproc", [v1, v2])

    # Fetch the value of the output parameter
    result = v2.getvalue()
    print("Result:", result)

except oracledb.DatabaseError as e:
    print("Oracle error:", e)

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
