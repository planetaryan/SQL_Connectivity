import oracledb
import getpass
import time
#enter in command prompt to see changes made in python on terminal
# sqlplus System/harsh123@localhost/xepdb1

con = oracledb.connect(user="SYSTEM", password="harsh123", dsn="localhost/xepdb1")
cur = con.cursor()

def update_prod_status():
    vehicle_id = input("Enter vehicle ID: ")
    new_prod_status = input("Enter updated production status: ")

    sql = "UPDATE vehicle SET production_status = :status WHERE vehicle_id = :vehicle_id"
    val = {"status": new_prod_status, "vehicle_id": vehicle_id}

    cur.execute(sql, val)
    con.commit() 

   
    cur.execute("SELECT * FROM vehicle WHERE vehicle_id = :vehicle_id", {"vehicle_id": vehicle_id})
    res = cur.fetchone()
    print(res)


def update_emp_salary():
    emp_id = input("Enter Employee ID: ")
    new_salary = input("Enter updated salary: ")

    sql = "UPDATE employee SET salary = :new_salary WHERE e_id= :emp_id"
    val={"emp_id": emp_id,"new_salary":new_salary}
    cur.execute(sql, val)
    con.commit() 

   
    cur.execute("SELECT * FROM employee WHERE e_id = :emp_id", {"emp_id": emp_id})
    res = cur.fetchone()
    print(res)


def view_notifications():
    cur.execute("BEGIN DBMS_OUTPUT.ENABLE(); END;")
    cur.callproc("check_due_date_warning")
    lines = []
    status_var = cur.var(int)
    line_var = cur.var(str)
    while True:
      cur.callproc("DBMS_OUTPUT.GET_LINE", (line_var, status_var))
      if status_var.getvalue() != 0:
        break
      lines.append(line_var.getvalue())

    # Print the output
    for line in lines:
     print(line)
    con.commit() 


def total_vehicles_produced():
    line_id = input("Enter line ID: ")

    sql = """
    SELECT 
        a.line_id,
        a.line_name,
        SUM((ei.hours_worked * a.production_rate)) AS vehicles_produced
    FROM 
        assembly a
    JOIN 
        employee_info ei ON a.line_id = ei.assembly_line_id
    WHERE 
        a.line_id = :line_id
    GROUP BY 
        a.line_id, a.line_name
    """

    val = {"line_id": line_id}
    cur.execute(sql, val)
    con.commit()

    # Fetch and print the results
    for row in cur:
        print(row)

def update_supplier_status():
    sup_id = input("Enter Supplier ID: ")
    up_status = input("Enter updated status: ")
    
    sql = """
    UPDATE supplier
    SET status = :new_status
    WHERE supplier_id = :supplier_id
    """

    val = {"new_status": up_status, "supplier_id": sup_id}
    cur.execute(sql, val)
    con.commit()

    # Fetch and print the updated row
    cur.execute("SELECT * FROM supplier WHERE supplier_id = :supplier_id", {"supplier_id": sup_id})
    updated_row = cur.fetchone()
    print("Updated Row:")
    print(updated_row)

def generate_monthly_expense_report():
    try:
        cur.execute("""
                  BEGIN
                   DBMS_OUTPUT.ENABLE();
                END;
                      """)
        # Get input from the user for year and month
        year = int(input("Enter the year (e.g., 2024): "))
        month = int(input("Enter the month (1-12): "))

        # Execute the PL/SQL procedure with the specified year and month
        cur.callproc("generate_monthly_expense_report", [year, month])
        
        con.commit()
        print("Monthly expense report generated successfully!")
        time.sleep(5)
        # Fetch and print the report


        lines = []
        line_var = cur.var(str)
        status_var = cur.var(int)
        while True:
            cur.callproc("DBMS_OUTPUT.GET_LINE", (line_var, status_var))
            print(line_var.getvalue())
            if status_var.getvalue() != 0:
                break
            lines.append(line_var.getvalue())



    except oracledb.DatabaseError as e:
        print("Error:", e)



def machines_per_assembly_line():
    try:
        # Get input from the user for assembly ID
        assembly_id = int(input("Enter the assembly ID: "))

        # Execute the SQL query to count machines per assembly line
        sql = """
        SELECT a.line_id, COUNT(m.machine_id) AS num_machines
        FROM assembly a
        LEFT JOIN machine_inventory m ON a.line_id = m.assembly_id
        WHERE a.line_id = :assembly_id
        GROUP BY a.line_id
        """
        cur.execute(sql, {"assembly_id": assembly_id})
        result = cur.fetchone()

        # Print the result
        if result:
            print(f"Assembly ID: {result[0]}, Number of Machines: {result[1]}")
        else:
            print("No machines found for the specified assembly ID.")
    except oracledb.DatabaseError as e:
        print("Error:", e)

def view_production_status():
    try:
        # Execute the PL/SQL function to update production status
        result = cur.callfunc("update_production_status", oracledb.NUMBER)
        print("Function executed successfully with result:", result)
        con.commit()
        # Fetch all records from the vehicle table
        cur.execute("SELECT * FROM vehicle")
        records = cur.fetchall()

        # Print all records
        print("Updated Vehicle Records:")
        for record in records:
            print(record)
    except oracledb.DatabaseError as e:
        print("Error:", e)

def increase_salary_if_above_avg():
    try:
        # Execute SQL query to calculate the average number of hours worked by all employees
        cur.execute("SELECT AVG(hours_worked) FROM employee_info")
        avg_hours_worked = cur.fetchone()[0]

        # Execute SQL query to update salary for employees who have worked more than the average
        sql = """
        UPDATE employee
        SET salary = salary * 1.05
        WHERE e_id IN (
            SELECT e_id
            FROM employee_info
            WHERE hours_worked > :avg_hours_worked
        )
        """
        cur.execute(sql, {"avg_hours_worked": avg_hours_worked})
        con.commit()

        print("Salary increased by 5% for employees who worked more than the average hours.")
    
    except oracledb.DatabaseError as e:
        print("Error:", e)

def view_supplier_limit():
    try:


        # Enable DBMS_OUTPUT
        cur.callproc("DBMS_OUTPUT.ENABLE")

        # PL/SQL block to check expense amount against supplier limit
        plsql_block = """
        DECLARE
            v_expense_amount NUMBER;
            v_supplier_max_cost NUMBER;
        BEGIN
            -- Get the total amount from the expenses table
            SELECT SUM(amount) INTO v_expense_amount FROM expense;

            -- Get the maximum cost from the supplier table
            SELECT MAX(total_cost) INTO v_supplier_max_cost FROM supplier;

            -- Check if the total expense amount exceeds the maximum supplier cost
            IF v_expense_amount > v_supplier_max_cost THEN
                -- Raise an exception
                RAISE_APPLICATION_ERROR(-20001, 'Total expense amount exceeds maximum supplier cost');
            ELSE
                -- Display a success message
                DBMS_OUTPUT.PUT_LINE('Expense amount is within supplier limits.');
            END IF;
            -- Print the values for debugging
            DBMS_OUTPUT.PUT_LINE('Total expense amount: ' || v_expense_amount);
            DBMS_OUTPUT.PUT_LINE('Maximum supplier cost: ' || v_supplier_max_cost);
        EXCEPTION
            WHEN OTHERS THEN
                -- Handle exceptions
                DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
        END;
        """

        # Execute the PL/SQL block
        cur.execute(plsql_block)

        # Fetch and print the output
        while True:
            line = cur.var(str)
            status = cur.var(int)
            cur.callproc("DBMS_OUTPUT.GET_LINE", (line, status))
            if status.getvalue() != 0:
                break
            print(line.getvalue())

    except oracledb.DatabaseError as e:
        # Print any database errors
        print("Error:", e)


users = ("Aryan","Harsh")
pw=123

user = input("enter username: ")
if user in users:
    print("Authorised user")
else:
    print("Unauthorised User")
    exit(1)

password = getpass.getpass("Enter password: ")
if password==str(pw):
    print("Successful log in!")
else:
    print("Incorrect password")
    exit(1)

print("Welcome to AH Automobile Assembly Plant Database Interface")

while True:
    print("User controls:\n")
    print("1.Update production status")
    print("2.Update Employee Salary")
    print("3.View expense notifications")
    print("4.View total vehicles produced on an assembly line")
    print("5.Update supply status")
    print("6.Generate expense report")
    print("7.Number of machines per assembly line")
    print("8.View vehicle production status")
    print("9.Activate bonuses for employees")
    print("10.Check supplier expense limit")
    print("11.EXIT")

    ch=int(input("Enter choice "))
    if ch==1:
        update_prod_status()

    elif ch==2:
        update_emp_salary()

    elif ch==3:
        view_notifications()

    elif ch==4:
        total_vehicles_produced()

    elif ch==5:
        update_supplier_status()
    
    elif ch==6:
        generate_monthly_expense_report()

    elif ch==7:
        machines_per_assembly_line()
    
    elif ch==8:
        view_production_status()

    elif ch==9:
        increase_salary_if_above_avg()

    elif ch==10:
        view_supplier_limit()

    elif ch==11:
        print("Exiting.....")
        break





    ans= input("Would you like to continue? ")
    if ans in "yY":
        print()
    else:
        break


    
