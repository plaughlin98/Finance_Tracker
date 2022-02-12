import matplotlib as plt
import pandas as pd
import sqlite3
from transactions import Transaction

# INSERT'finances.db' AFTER TESTING
conn = sqlite3.connect('finances.db')

c = conn.cursor()


# CREATE TABLES
# EXPENSES
c.execute(""" CREATE TABLE IF NOT EXISTS expenses (
            date text,
            amount integer,
            category text,
            trans_id text
            )""")

# INCOME
c.execute(""" CREATE TABLE IF NOT EXISTS income (
            date text,
            amount integer,
            category text,
            trans_id text
            )""")

def insert_trans(trans, table):
    with conn:
        c.execute("INSERT INTO :table VALUES (:date, :amount, :category)", {'table': table, 'date': trans.date, 'amount': trans.amount, 'category': trans.category})

## TO-DO: REFACTOR CODE INTO LESS FUNCTIONS
def update_amount(trans, amount, table):
    with conn:
        c.execute("""UPDATE :table SET amount = :amount
                    WHERE trans_id = :trans_id""",
                    {'table': table, 'trans_id': trans.trans_id, 'amount': amount})

def update_date(trans, date, table):
    with conn:
        c.execute("""UPDATE :table SET date = :date
                    WHERE trans_id = :trans_id""",
                    {'table': table, 'date': date, 'trans_id': trans.trans_id})

def update_category(trans, category, table):
    with conn:
        c.execute(""" UPDATE :table SET category = :category
                    WHERE trans_id = :trans_id""",
                    {'table': table, 'category': category, 'trans_id': trans.trans_id})

def remove_trans(trans, table):
    with conn:
        c.execute(""" DELETE from :table WHERE trans_id = :trans_id""",
                    {'table': table, 'trans_id': trans.trans_id})

def get_trans_by_date(date, table):
    c.execute("SELECT * FROM :table WHERE date = :date", {'table': table, 'date': date})
    return c.fetchall()

def get_trans_overunder_amount(amount,over_under ,table):
    over_under = over_under.lower()
    if over_under == "over":
        over_under = ">"
    else:
        over_under = "<"
    c.execute("SELECT * FROM :table WHERE amount :over_under :amount",
            {'table': table, 'over_under': over_under, 'amount': amount})
    return c.fetchall()

def get_trans_by_id(trans_id, table):
    c.execute("SELECT * FROM :table WHERE trans_id = :trans_id", {'table': table, 'trans_id': trans_id})
    return c.fetchall()

def get_trans_by_table(table):
    c.execute("SELECT * FROM :table WHERE table = :table", {'table': table})
    return c.fetchall()