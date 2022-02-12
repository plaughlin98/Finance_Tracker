import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import sqlite3
from transactions import Transaction
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')

### TEMP DATA
exp1 = Transaction("2022-04-12", 54300, "Books", "Trans1", "expenses")
exp2 = Transaction("2022-10-12", 621, "Books", "Trans1", "expenses")

inc1 = Transaction("2022-08-12", 44, "Books", "Trans1", "incomes")
inc2 = Transaction("2022-02-12", 88796, "Books", "Trans1", "incomes")

# INSERT'finances.db' AFTER TESTING
# INSERT ':memory:' for testing

conn = sqlite3.connect(':memory:')

c = conn.cursor()
# CREATE TABLES
# EXPENSES
c.execute(""" CREATE TABLE IF NOT EXISTS expenses (
            date text,
            amount integer,
            category text,
            trans_id text,
            trans_type text
            )""")

# INCOME
c.execute(""" CREATE TABLE IF NOT EXISTS incomes (
            date text,
            amount integer,
            category text,
            trans_id text,
            trans_type text
            )""")

def insert_trans(trans, table):
    """trans -> Transaction Class Instance
    """
    with conn:
        c.execute("INSERT INTO expenses VALUES (:date, :amount, :category, :trans_id, :trans_type)",
        {'date': trans.date, 'amount': trans.amount, 'category': trans.category, 'trans_id': trans.trans_id, 'trans_type': trans.trans_type})
        
        conn.commit()

## TO-DO: REFACTOR CODE INTO LESS FUNCTIONS

# def update_trans(trans, item, value)
#   pass

def get_range():
    pass
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

def get_trans_overunder_value(value, over_under ,table):
    over_under = over_under.lower()
    if over_under == "over":
        over_under = ">"
    else:
        over_under = "<"
    c.execute("SELECT * FROM :table WHERE amount :over_under :amount",
            {'table': table, 'over_under': over_under, 'amount': value})
    return c.fetchall()

def get_trans_by_id(trans_id, table):
    c.execute("SELECT * FROM :table WHERE trans_id = :trans_id", {'table': table, 'trans_id': trans_id})
    return c.fetchall()

def get_trans_by_table(table):
    c.execute("SELECT * FROM :table WHERE table = :table", {'table': table})
    return c.fetchall()

def graph_data(table):
    c.execute('SELECT date, amount FROM {}'.format(table))
    data = c.fetchall()
    for row in data:
        print(row)

    dates = []
    amounts = []

    for row in data:
        dates.append(parser.parse(row[0]))
        amounts.append(row[1])

    plt.plot_date(dates,amounts,'-')
    plt.show()


def main_loop():
    pass

insert_trans(exp1, "expenses")
insert_trans(exp1, "expenses")
insert_trans(inc1, "income")
insert_trans(inc2, "income")

graph_data("expenses")

#Commits Transaction 
conn.commit()
conn.close()


