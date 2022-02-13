from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import sqlite3
import PROMPT_STRINGS as prmpt
from datetime import date
from transactions import Transaction
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')

### TEMP DUMMY DATA
exp1 = Transaction("2022-04-12", 530, "Books", "Trans1", "expense")
exp2 = Transaction("2022-10-12", 621, "Books", "Trans1", "expense")

inc1 = Transaction("2022-08-12", 44, "Books", "Trans1", "income")
inc2 = Transaction("2022-02-12", 896, "Books", "Trans1", "income")

# INSERT'finances.db' AFTER TESTING
# INSERT ':memory:' for testing
conn = sqlite3.connect(':memory:')
c = conn.cursor()


#**************************************************************************************
#***************************** SETUP & CONFIG FUNCTIONS *******************************
#**************************************************************************************

# CREATE TABLES
#USERS
c.execute("""CREATE TABLE IF NOT EXISTS users (
        user text,
        table_name text
        )""")

# EXPENSES
def create_user_trans_tbl(user):
    c.execute(""" CREATE TABLE IF NOT EXISTS {}_transactions (
                trans_date text,
                amount integer,
                category text,
                trans_id text,
                trans_type text
                )""".format(user))

# GET ALL CURRENT USERS
def get_users():
    c.execute("SELECT * FROM users")
    return c.fetchone()

# GENERATE ID FOR TRANSACTION
def get_next_id(user):
    table = user + "_transactions"
    c.execute("""SELECT * FROM {}
                 WHERE trans_id = (SELECT MAX(trans_id)  FROM {})
                 """.format(table, table))
    if c.fetchone() == None:
        return "{:04d}".format(0)
    else:
        trans_id = c.fetchone
        trans_id = int(trans_id) + 1
        return "{:04d}".format(trans_id)

def get_new_trans_info(user):
    print("Please enter in your transaction")
    trans_type = input("Is it an expense or income? ")
    trans_date = date.today().strftime("%Y-%d-%m")
    amount = input("How much was the transaction")
    category = input("Please state the category")
    trans_id = get_next_id(user)

    return Transaction(trans_date, amount, category, trans_id, trans_type)


def display(trans_get, count):
    if trans_get is None:
        print("That is not a valid Query")
    if count > 1:
        for item in trans_get:
            print(item)
    else:
        print(trans_get)

#**************************************************************************************
#*************************** SETUP & GENERAL FUNCTIONS END ****************************
#**************************************************************************************


#**************************************************************************************
#***************************** UPDATE /REMOVE QUERIES *********************************
#**************************************************************************************

def insert_trans(trans, table):
    """trans -> Transaction Class Instance
    """
    with conn:
        c.execute("INSERT INTO {} VALUES (:trans_date, :amount, :category, :trans_id, :trans_type)".format(table),
        {'trans_date': trans.trans_date, 'amount': trans.amount, 'category': trans.category, 'trans_id': trans.trans_id, 'trans_type': trans.trans_type})
        
        conn.commit()

def update_trans(table, trans_id, item, value):
    with conn:
        c.execute(""" UPDATE {} SET {} = :value
                    WHERE trans_id = :trans_id""".format(table, item),
                    {'trans_id': trans_id, 'value': value})

        conn.commit()

def remove_trans(trans_id, table):
    with conn:
        c.execute(""" DELETE from {} WHERE trans_id = :trans_id""".format(table),
                    {'trans_id': trans_id})
        conn.commit()

#**************************************************************************************
#***************************** UPDATE /REMOVE QUERIES END *****************************
#**************************************************************************************

#**************************************************************************************
#***************************** SELECT QUERIES *****************************************
#**************************************************************************************

def get_account_balance(table):
    c.execute("SELECT amount FROM {} WHERE trans_type = expense".format(table))
    expenses = c.fetchall()
    total_expenses = 0

    for expense in expenses:
        total_expenses += expense

    c.execute("SELECT amount FROM {} WHERE trans_type = income".format(table))
    incomes = c.fetchall()

    total_incomes = 0
    for income in incomes:
        total_incomes += income

    print(total_incomes - total_expenses)

def get_spec_trans(item, value, table):
    c.execute("SELECT COUNT(*) FROM {}".format(table))
    for i in c.fetchone():
        count = i

    c.execute("SELECT * FROM {} WHERE {} = :value".format(table, item), { 'value': value})
    
    if count == 1:
        display_get = c.fetchone()
    else:
        display_get = c.fetchall()

    display(display_get, count)

def get_over_under_value(value, item, over_under,table):
    c.execute("SELECT COUNT(*) FROM {}".format(table))
    for i in c.fetchone():
        count = i

    over_under = over_under.lower()
    if over_under == "over":
        over_under = ">"
    else:
        over_under = "<"
    c.execute("SELECT * FROM {} WHERE :item :over_under :value".format(table),
            {'item': item, 'over_under': over_under, 'value': value})

    if count == 1:
        display_get = c.fetchone()
    else:
        display_get = c.fetchall()

    display(display_get, count)

def get_all_trans(table):
    c.execute("SELECT COUNT(*) FROM {}".format(table))
    for i in c.fetchone():
        count = i
        
    c.execute("SELECT * FROM {}".format(table))
    if count == 1:
        display_get = c.fetchone()
    else:
        display_get = c.fetchall()

    display(display_get, count)

#**************************************************************************************
#***************************** SELECT QUERIES END *************************************
#**************************************************************************************

#**************************************************************************************
#********************************** GRAPHING ******************************************
#**************************************************************************************

# TO-DO: FIX GRAPH FORMATTING AND ALLOW USER TO DYNAMICALLY CHOOSE WHAT TO GRAPH
def graph_data(table):
    c.execute('SELECT trans_date, amount FROM {} ORDER BY trans_date ASC'.format(table))
    data = c.fetchall()
    for row in data:
        print(row)

    dates = []
    amounts = []

    for row in data:
        dates.append(row[0])
        amounts.append(row[1])
    

    plt.plot(dates,amounts,'-')
    plt.xlabel("Date")
    plt.ylabel("Transaction Amount")
    plt.show()

#**************************************************************************************
#******************************* GRAPHING END *****************************************
#**************************************************************************************

# TO-DO: CREATE INPUT LOOP TO DYNAMICALLY GO THROUGH ALL FUNCTIONS BASED ON USER INPUT
def main_loop():
    #print("Hello, Welcome")
    user = input("Please Enter your username: ")
    user_table = user + "_transactions"
    user_list = get_users()

    if not user_list or user not in user_list:
        #Make Input Prompt later  
        print("Looks like you don't have an account, would you like to create one?")
        create_user_trans_tbl(user)
    print("Hello {}".format(user))

    insert_trans(exp1, user_table)
    get_all_trans(user_table)
    get_spec_trans('category', 'Books', user_table)

if __name__ == "__main__":
    main_loop()

conn.close()