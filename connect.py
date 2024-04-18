# !/usr/bin/env python

import mysql.connector # type: ignore
from mysql.connector.connection import MySQLConnection # type: ignore



users = ("nekunj", "arnav", "aryan")
user = input("enter username: ")
if user in users:
    print("authorised user")
else:
    print("Unauthorised User")
    exit(1)

def Comp_Inventory(con):
    with con.cursor() as cur:
        cur.execute(
            """
            create table if not exists Comp_Inventory(
                c_no int PRIMARY KEY, c_name varchar(30),
                no_inventory int,
                no_ordered int,
                factory_name varchar(20)
            )
            """
        )

    cur = con.cursor()

    def insertrec(conn: MySQLConnection):
        with conn.cursor() as cursor:
            a = int(input("enter component number "))
            b = input("enter component name ")
            c = int(input("enter no. in inventory "))
            d = int(input("enter no. ordered "))
            e = input("enter factory name ")

            val = (a, b, c, d, e)
            sql = "insert into Comp_Inventory values(%s,%s,%s,%s,%s)"
            cursor.execute(sql, val)

            con.commit()
            cursor.close()

    def deleterec(conn: MySQLConnection):
        with conn.cursor() as cursor:
            a = int(input("enter component number "))

            val = (a,)
            sql = "delete from Comp_Inventory where c_no=%s"
            cur.execute(sql, val)

            con.commit()
            cursor.close()

    def updaterec(conn: MySQLConnection):
        with conn.cursor() as cursor:
            sql = "update Comp_Inventory set c_name = %s,no_inventory  = %s, no_ordered = %s, factory_name = %s WHERE c_no = %s "
            a = int(input("enter component number "))
            b = input("enter component name ")
            c = int(input("enter no. in inventory "))
            d = int(input("enter no. ordered "))
            e = input("enter factory name ")

            val = (b, c, d, e, a)
            cursor.execute(sql, val)

            conn.commit()
            cursor.close()

    def viewrec(conn: MySQLConnection):
        with conn.cursor() as cursor:
            sql = "select * from Comp_Inventory"
            cursor.execute(sql)
            for i in cursor:
                print(i)

           
            cursor.close()

    while True:
        print("1. Insert Record")
        print("2. Delete Record")
        print("3. Update Record")
        print("4. View Records")
        ans = int(input("enter choice "))
        if ans == 1:
            insertrec(con)
        if ans == 2:
            deleterec(con)
        if ans == 3:
            updaterec(con)
        if ans == 4:
            viewrec(con)

        ans1 = input("Would you like to continue? ")
        if ans1 in "yY":
            print()
        else:
            break


def employee(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            create table if not exists employee(
                emp_id varchar(5) primary key not null,
                emp_name varchar(10) not null,
                machine_id varchar(30) not null,
                machinename tinytext not null,
                salary integer not null
            )
            """
        )

    while True:
        print("1. view all records")
        print("2. insert records")
        print("3. delete records")
        print("4. Update records")
        print("Any other integer to exit")
        k = int(input("select option: "))

        if k == 1:
            with conn.cursor() as cursor:
                
                sql = "select * from employee"
                cursor.execute(sql)
                for i in cursor:
                    print(i)

                cursor.close()

        elif k == 2:
            with conn.cursor() as cursor:
                l = input("enter emp_id: ")
                m = input("enter emp_name: ")
                n = input("enter machine_id: ")
                o = input("enter machinename: ")
                p = int(input("enter salary: "))
                sql = "insert into employee(emp_id, emp_name,machine_id, machinename, salary) values(%s,%s,%s,%s,%s)"
                z = (l, m, n, o, p)
                cursor.execute(sql, z)

                print("Values added.")
                conn.commit()
                cursor.close()

        elif k == 3:
            with conn.cursor() as cursor:
                l = input("enter no")
                val = (l,)
                sql = "delete from employee where emp_id = %s"
                cursor.execute(sql, val)

                conn.commit()
                cursor.close()

        elif k == 4:
            with conn.cursor() as cursor:
                sql = "update employee set emp_name  = %s, machine_id = %s, machinename = %s,salary=%s WHERE emp_id  = %s "
                a = input("enter employee name ")
                b = input("enter machine id ")
                c = input("enter machine name ")
                e = int(input("enter salary "))
                d = input("enter employee id to be changed ")

                val = (a,b,c,e,d)
                cursor.execute(sql, val)
                

                conn.commit()
                cursor.close()

        else:
            break


def MachineInventory(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS MachineInventory(
                MachineId          VARCHAR(5) PRIMARY KEY,
                MachineName        TINYTEXT NOT NULL,
                Manufacturer       TINYTEXT NOT NULL,
                MachineDescription TEXT NOT NULL,
                AmountAvailable    INTEGER NOT NULL
            )
            """
        )

    while True:
        print("Menu:")
        print("\t1. Add record to Machine Inventory.")
        print("\t2. Get record in Machine inventory by its MachineId.")
        print("\t3. Update record in Machine inventory by specifying MachineId")
        print("\t4. Remove record by MachineId in Machine Inventory.")
        print("\t5. Get all records in Machine inventory.")
        print("\tAny other integer to exit.")
        choice = int(input("Enter choice: "))

        if choice == 1:

            machine_id = input("Enter new Machine Id: ")
            name = input("Enter name of machine: ")
            manufacturer = input("Enter name of manufacturer: ")
            description = input("Enter description of machine: ")
            amount_available = int(input("Enter amount of machines available: "))
            data_tuple = (machine_id, name, manufacturer, description, amount_available)

            with conn.cursor() as cursor:
                sql = "INSERT INTO MachineInventory(MachineId, MachineName, Manufacturer, MachineDescription, AmountAvailable) VALUES(%s, %s, %s, %s, %s)"
                cursor.execute(sql, data_tuple)

                conn.commit()
                cursor.close()

            print("Record added.")

        elif choice == 2:
            machine_id = input("Enter MachineId: ")
            result = None
            with conn.cursor() as cursor:
                sql = "SELECT MachineId, MachineName, Manufacturer, MachineDescription, AmountAvailable FROM MachineInventory WHERE MachineId = %s"
                cursor.execute(sql, (machine_id,))

                result = cursor.fetchone()
                cursor.close()

            if result == None:
                print("Record with MachineId '{}' not found.".format(machine_id))
                continue

            print("Record found:")
            print("\tMachine Id:", machine_id)
            print("\tMachine Name:", result[1])
            print("\tManufacturer:", result[2])
            print("\tDescription:", result[3])
            print("\tAmount Available:", result[4])

        elif choice == 3:

            machine_id = input("Enter MachineId: ")
            name = input("Enter new name for machine: ")
            manufacturer = input("Enter new manufactuer: ")
            description = input("Enter description: ")
            amount_available = int(input("Enter number of machines available: "))

            data_tuple = (name, manufacturer, description, amount_available, machine_id)
            with conn.cursor() as cursor:
                sql = "UPDATE MachineInventory SET MachineName = %s, Manufacturer = %s, MachineDescription = %s, AmountAvailable = %s WHERE MachineId = %s"
                cursor.execute(sql, data_tuple)

                conn.commit()
                cursor.close()

            print("Record updated.")

        elif choice == 4:
            machine_id = input("Enter MachineId: ")

            with conn.cursor() as cursor:
                sql = "DELETE FROM MachineInventory WHERE MachineId = %s"
                cursor.execute(sql, (machine_id,))

                conn.commit()
                cursor.close()

            print("Records with MachineId '{}' deleted.".format(machine_id))

        elif choice == 5:
            with conn.cursor() as cursor:
                
                sql = "select * from MachineInventory "
                cursor.execute(sql)
                for i in cursor:
                    print(i)
                


        print()


credentials = {
    "host": "localhost",
    "user": "root",
    "passwd": "operation eagle",
    "db": "mysql",
}

with mysql.connector.connect(**credentials) as conn:
    conn.cursor().execute("CREATE DATABASE IF NOT EXISTS mydb")

with mysql.connector.connect(**credentials) as conn:
    while True:
        print("Comp_Inventory, employee , MachineInventory")
        table = input("enter name of table to be used from the above list: ")

        if table == "Comp_Inventory":
            Comp_Inventory(conn)
        elif table == "employee":
            employee(conn)
        elif table == "MachineInventory":
            MachineInventory(conn)
        else:
            print("[ERROR] Invalid table name '{}'. Try again.".format(table))
            continue

        ans = input("Would you like to use another table (y/n): ")
        if ans in "Yy":
            print()
        else:
            break