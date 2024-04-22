import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import oracledb
import getpass
import time

con = oracledb.connect(user="SYSTEM", password="harsh123", dsn="localhost/xepdb1")
cur = con.cursor()

class DatabaseInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("AH Automobile Assembly Plant Database Interface")
        self.root.geometry("900x400")

        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Check username and password
        if username == "Aryan" and password == "123":
            messagebox.showinfo("Login", "Successful login!")
            self.show_menu()
        elif username=="Harsh" and password=="123":
            messagebox.showinfo("Login", "Successful login!")
            self.show_menu()
        else:
            messagebox.showerror("Login Error", "Incorrect username or password")

    def show_menu(self):
        self.username_label.destroy()
        self.username_entry.destroy()
        self.password_label.destroy()
        self.password_entry.destroy()
        self.login_button.destroy()

        self.menu_label = tk.Label(self.root, text="Choose an option:")
        self.menu_label.pack()

        self.menu_options = [
            "Update production status",
            "Update Employee Salary",
            "View expense notifications",
            "View total vehicles produced on an assembly line",
            "Update supply status",
            "Generate expense report",
            "Number of machines per assembly line",
            "View vehicle production status",
            "Activate bonuses for employees",
            "Check supplier expense limit",
            "EXIT"
        ]

        for i, option in enumerate(self.menu_options, start=1):
            tk.Button(self.root, text=option, command=lambda opt=option: self.handle_option(opt)).pack()

    def handle_option(self, option):
        if option == "EXIT":
            self.root.destroy()
        elif option == "Update production status":
            self.update_prod_status()
        elif option == "Update Employee Salary":
            self.update_emp_salary()
        elif option == "View expense notifications":
            self.view_notifications()
        elif option == "View total vehicles produced on an assembly line":
            self.total_vehicles_produced()
        elif option == "Update supply status":
            self.update_supplier_status()
        elif option == "Generate expense report":
            self.generate_monthly_expense_report()
        elif option == "Number of machines per assembly line":
            self.machines_per_assembly_line()
        elif option == "View vehicle production status":
            self.view_production_status()
        elif option == "Activate bonuses for employees":
            self.increase_salary_if_above_avg()
        elif option == "Check supplier expense limit":
            self.view_supplier_limit()

    # Implement your functions here
    def update_prod_status(self):
        vehicle_id = simpledialog.askstring("Input", "Enter vehicle ID:")
        if vehicle_id is None:
            return
        new_prod_status = simpledialog.askstring("Input", "Enter updated production status:")

        sql = "UPDATE vehicle SET production_status = :status WHERE vehicle_id = :vehicle_id"
        val = {"status": new_prod_status, "vehicle_id": vehicle_id}

        cur.execute(sql, val)
        con.commit() 

        cur.execute("SELECT * FROM vehicle WHERE vehicle_id = :vehicle_id", {"vehicle_id": vehicle_id})
        res = cur.fetchone()
        messagebox.showinfo("Production Status Updated", str(res))

    def update_emp_salary(self):
        emp_id = simpledialog.askstring("Input", "Enter Employee ID:")
        if emp_id is None:
            return
        new_salary = simpledialog.askstring("Input", "Enter updated salary:")
        if new_salary is None:
            return

        sql = "UPDATE employee SET salary = :new_salary WHERE e_id= :emp_id"
        val={"emp_id": emp_id,"new_salary":new_salary}
        cur.execute(sql, val)
        con.commit() 

        cur.execute("SELECT * FROM employee WHERE e_id = :emp_id", {"emp_id": emp_id})
        res = cur.fetchone()
        messagebox.showinfo("Employee Salary Updated", str(res))

    def view_notifications(self):
        try:
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
        
            if lines:
                notification_message = "\n".join(lines)
                messagebox.showinfo("Notifications", notification_message)
            else:
                messagebox.showinfo("Notifications", "No notifications found.")
        
        except oracledb.DatabaseError as e:
            messagebox.showerror("Error", str(e))


    def total_vehicles_produced(self):
        try:
            line_id = simpledialog.askstring("Input", "Enter line ID:")
            if line_id is None:
                return

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

        # Fetch the results
            results = cur.fetchall()

        # Prepare the message to display
            message = ""
            for row in results:
                message += f"Line ID: {row[0]}, Line Name: {row[1]}, Vehicles Produced: {row[2]}\n"

            if message:
                messagebox.showinfo("Total Vehicles Produced", message)
            else:
                messagebox.showinfo("Total Vehicles Produced", "No data found for the specified line ID.")

        except oracledb.DatabaseError as e:
            messagebox.showerror("Error", str(e))


    def update_supplier_status(self):
        try:
            sup_id = simpledialog.askstring("Input", "Enter Supplier ID:")
        
        # Check if the user clicked Cancel
            if sup_id is None:
                return
        
            up_status = simpledialog.askstring("Input", "Enter updated status:")
        
        # Check if the user clicked Cancel
            if up_status is None:
                return
    
            sql = """
            UPDATE supplier
            SET status = :new_status
            WHERE supplier_id = :supplier_id
            """

            val = {"new_status": up_status, "supplier_id": sup_id}
            cur.execute(sql, val)
            con.commit()

        # Fetch the updated row
            cur.execute("SELECT * FROM supplier WHERE supplier_id = :supplier_id", {"supplier_id": sup_id})
            updated_row = cur.fetchone()

            if updated_row:
                messagebox.showinfo("Updated Row", str(updated_row))
            else:
                messagebox.showinfo("Updated Row", "No row found with the specified Supplier ID.")
    
        except oracledb.DatabaseError as e:
            messagebox.showerror("Error", str(e))

    def generate_monthly_expense_report(self):
        try:
            cur.execute("BEGIN DBMS_OUTPUT.ENABLE(); END;")
            year = simpledialog.askinteger("Input", "Enter the year (e.g., 2024):")
            if year is None:
                return
            month = simpledialog.askinteger("Input", "Enter the month (1-12):")
            if month is None:
                return
            cur.callproc("generate_monthly_expense_report", [year, month])
        
            con.commit()
            time.sleep(5)

            lines = []
            line_var = cur.var(str)
            status_var = cur.var(int)
            while True:
                cur.callproc("DBMS_OUTPUT.GET_LINE", (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                lines.append(line_var.getvalue())

            report = '\n'.join(lines)
            messagebox.showinfo("Monthly Expense Report", report)

        except oracledb.DatabaseError as e:
            print("Error:", e)

    def machines_per_assembly_line(self):
        try:
        # Get input from the user for assembly ID
            assembly_id = simpledialog.askinteger("Input", "Enter the assembly ID:")

        # Check if the user clicked Cancel
            if assembly_id is None:
                return

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

        # Prepare the message to display
            if result:
                message = f"Assembly ID: {result[0]}, Number of Machines: {result[1]}"
            else:
                message = "No machines found for the specified assembly ID."

        # Show the result in a message box
            messagebox.showinfo("Machines Per Assembly Line", message)

        except oracledb.DatabaseError as e:
            messagebox.showerror("Error", str(e))


    def view_production_status(self):
        try:
        # Execute the PL/SQL function to update production status
            result = cur.callfunc("update_production_status", oracledb.NUMBER)
            messagebox.showinfo("Function Execution", f"Function executed successfully with result: {result}")
            con.commit()

        # Fetch all records from the vehicle table
            cur.execute("SELECT * FROM vehicle")
            records = cur.fetchall()

        # Prepare the message to display
            message = "Updated Vehicle Records:\n"
            for record in records:
                message += str(record) + "\n"

        # Show the records in a message box
            messagebox.showinfo("Updated Vehicle Records", message)
        
        except oracledb.DatabaseError as e:
            messagebox.showerror("Error", str(e))


    def increase_salary_if_above_avg(self):
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

            messagebox.showinfo("Salary Update", "Salary increased by 5% for employees who worked more than the average hours.")
    
        except oracledb.DatabaseError as e:
            messagebox.showerror("Error", str(e))


    def view_supplier_limit(self):
        try:
        # Enable DBMS_OUTPUT
            cur.callproc("DBMS_OUTPUT.ENABLE")

        # Execute the PL/SQL block to check expense amount against supplier limit
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

        # Fetch the output from DBMS_OUTPUT
            output = []
            line_var = cur.var(str)
            status_var = cur.var(int)
            while True:
                cur.callproc("DBMS_OUTPUT.GET_LINE", (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                output.append(line_var.getvalue())

        # Prepare the message to display
            message = "\n".join(output)

        # Show the output in a message box
            messagebox.showinfo("Supplier Limit Check", message)

        except oracledb.DatabaseError as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = DatabaseInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
