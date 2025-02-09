##useful commands on ubuntu during first time connection
#Change Authentication Method to mysql_native_password
'''
#Log into MySQL:
sudo mysql -u root -p
#Check the current authentication plugin:
SELECT user, host, plugin FROM mysql.user WHERE user = 'root';
#Update the authentication method:
ALTER USER 'your_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
#Restart MySQL:
sudo systemctl restart mysql
'''
import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger=setup_logger("db_helper")

@contextmanager
def get_db_curser(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="expense_manager",
        auth_plugin='mysql_native_password'

    )

    if connection.is_connected():
        print("Connection Successful")
    else:
        print("Failed in connecting to database")

    curser =connection.cursor(dictionary=True)
    yield curser
    if commit:
        connection.commit()
    curser.close()
    connection.close()


def fetch_all_records():
    with get_db_curser() as curser:
        curser.execute("SELECT * FROM expenses")
        expenses=curser.fetchall()
        for expense in expenses:
            print(expense)


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_curser() as curser:
        curser.execute("SELECT * FROM expenses WHERE expense_date=%s",(expense_date,))
        expenses=curser.fetchall()
        for expense in expenses:
            print(expense)
        return expenses

def insert_expense(expense_date,amount,category,notes):
    logger.info(f"insert_expense called with date: {expense_date},amount:{amount},category:{category},notes:{notes}")
    with get_db_curser(commit=True) as curser:
        curser.execute(
            "INSERT INTO expenses (expense_date,amount,category,notes) VALUES (%s,%s,%s,%s)",
            (expense_date,amount,category,notes)
        )
    
def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_curser(commit=True) as curser:
        curser.execute("DELETE FROM expenses WHERE expense_date=%s",(expense_date,))

def fetch_expense_summary(start_date,end_date):
    logger.info(f"fetch_expense_summary called with start:{start_date},end:{end_date}")
    with get_db_curser() as curser:
        curser.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date 
               BETWEEN %s and %s
               GROUP BY category;
            ''',(start_date,end_date)
            )
        expenses=curser.fetchall()
        return expenses
        
def fetch_expenses_by_month(year):
    logger.info(f"fetch_expenses_by_month called with year:{year}")
    with get_db_curser() as curser:
        curser.execute(
            '''SELECT 
                DATE_FORMAT(expense_date, '%Y-%m') AS month,
                SUM(amount) AS total_expense
                FROM expenses
                WHERE YEAR(expense_date) = %s
                GROUP BY month
                ORDER BY month;''', 
                (year,)
        )
        expenses=curser.fetchall()
        return expenses

if __name__=="__main__":
    #fetch_all_records()
    # fetch_expenses_for_date("2024-08-01")
    # insert_expense("2024-08-20",300,"Food","Panipuri")
    # print("***fetch expenses for 8/20***")
    # fetch_expenses_for_date("2024-08-20")
    # print("***delete expenses for 8/20***")
    # delete_expenses_for_date("2024-08-20")
    # print("***again fetch expenses for 8/20***")
    # fetch_expenses_for_date("2024-08-20")
    # summary=fetch_expense_summary("2024-08-01","2024-08-05")
    # for record in summary:
    #     print(record)
    expenses=fetch_expenses_by_month(2024)
    print(expenses)