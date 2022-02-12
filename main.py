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

### TEMP DATA
exp1 = Transaction("2022-04-12", 54300, "Books", "Trans1", "expense")
exp2 = Transaction("2022-10-12", 621, "Books", "Trans1", "expense")

inc1 = Transaction("2022-08-12", 44, "Books", "Trans1", "income")
inc2 = Transaction("2022-02-12", 88796, "Books", "Trans1", "income")

# INSERT'finances.db' AFTER TESTING
# INSERT ':memory:' for testing

conn = sqlite3.connect(':memory:')
c = conn.cursor()
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

def get_users():
    c.execute("SELECT * FROM users")
    return c.fetchone()

def get_next_id(user):
    pass

def get_new_trans_info(user):
    print("Please enter in your transaction")
    trans_type = input("Is it an expense or income? ")
    trans_date = date.today().strftime("%Y-%d-%m")
    amount = input("How much was the transaction")
    category = input("Please state the category")
    trans_id = get_next_id(user)

    return Transaction(trans_date, amount, category, trans_id, trans_type)

def insert_trans(trans, table):
    """trans -> Transaction Class Instance
    """
    with conn:
        c.execute("INSERT INTO {} VALUES (:trans_date, :amount, :category, :trans_id, :trans_type)".format(table),
        {'trans_date': trans.trans_date, 'amount': trans.amount, 'category': trans.category, 'trans_id': trans.trans_id, 'trans_type': trans.trans_type})
        
        conn.commit()

## TO-DO: REFACTOR CODE INTO LESS FUNCTIONS

def update_trans(table, trans_id, item, value):
    with conn:
        c.execute(""" UPDATE {} SET :item = :value
                    WHERE trans_id = :trans_id""".format(table),
                    {'trans_id': trans_id, 'item': item, 'value': value})

# def update_amount(trans, amount, table):
#     with conn:
#         c.execute("""UPDATE :table SET amount = :amount
#                     WHERE trans_id = :trans_id""",
#                     {'table': table, 'trans_id': trans.trans_id, 'amount': amount})

# def update_date(trans, trans_date, table):
#     with conn:
#         c.execute("""UPDATE :table SET trans_date = :trans_date
#                     WHERE trans_id = :trans_id""",
#                     {'table': table, 'trans_date': trans_date, 'trans_id': trans.trans_id})

# def update_category(trans, category, table):
#     with conn:
#         c.execute(""" UPDATE :table SET category = :category
#                     WHERE trans_id = :trans_id""",
#                     {'table': table, 'category': category, 'trans_id': trans.trans_id})

def remove_trans(trans_id, table):
    with conn:
        c.execute(""" DELETE from {} WHERE trans_id = :trans_id""".format(table),
                    {'trans_id': trans_id})

def get_trans_by_date(trans_date, table):
    c.execute("SELECT * FROM {} WHERE trans_date = :trans_date".format(table), {'trans_date': trans_date})
    return c.fetchall()

def get_trans_overunder_value(value, over_under ,table):
    over_under = over_under.lower()
    if over_under == "over":
        over_under = ">"
    else:
        over_under = "<"
    c.execute("SELECT * FROM {} WHERE amount :over_under :amount".format(table),
            {'over_under': over_under, 'amount': value})
    return c.fetchall()

def get_trans_by_id(trans_id, table):
    c.execute("SELECT * FROM {} WHERE trans_id = :trans_id".format(table), {'trans_id': trans_id})
    return c.fetchall()


def get_trans_by_table(table):
    c.execute("SELECT * FROM {}".format(table))
    return c.fetchall()

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


def main_loop():
    print("Hello, Welcome")
    user = input("Please Enter your username: ")
    user_list = get_users()
    print(user_list)

    if not user_list or user not in user_list:
        #Make Input Prompt later  
        print("Looks like you don't have an account, would you like to create one?")
        create_user_trans_tbl(user)
    user_table = user + "_transactions"
    print("Hello {}".format(user))

    # DUMMY DATA // DELETE
    # insert_trans(get_new_trans_info(user), user_table)
    insert_trans(exp1, user_table)
    insert_trans(exp2, user_table)
    insert_trans(inc1, user_table)
    insert_trans(inc2, user_table)
    print(get_trans_by_table(user_table))
    graph_data(user_table)


# insert_trans(exp1, "expenses")
# insert_trans(exp1, "expenses")
# insert_trans(inc1, "income")
# insert_trans(inc2, "income")


main_loop()

conn.commit()
conn.close()


