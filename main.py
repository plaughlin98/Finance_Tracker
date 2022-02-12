import sqlite3
from transactions import Transaction

# INSERT'finances.db' AFTER TESTING
conn = sqlite3.connect(':memory:')

c = conn.cursor()


# CREATE TABLES
# EXPENSES
c.execute(""" CREATE TABLE expenses (
            date text,
            amount integer,
            desc text,
            trans_id text
            )""")

# INCOME
c.execute(""" CREATE TABLE income (
            date text,
            amount integer,
            desc text,
            trans_id text
            )""")

def insert_trans(trans, table):
    with conn:
        c.execute("INSERT INTO :table VALUES (:date, :amount, :desc)", {'date': trans.date, 'amount': trans.amount, 'desc': trans.desc})

## TO-DO: REFACTOR CODE INTO LESS FUNCTIONS
def update_amount(trans, amount, table):
    with conn:
        c.execute("""UPDATE :table SET amount = :amount
                    WHERE trans_id = :trans_id""",
                    {'table': table, 'trans_id': trans.trans_id, 'amount': amount})

def update_date(trans, date, table):
    with conn:
        c.connect("""UPDATE :table SET date = :date
                    WHERE trans_id = :trans_id""",
                    {'table': table, 'date': date, 'trans_id': trans.trans_id})

def update_desc(trans, desc, table):
    with conn:
        c.connect(""" UPDATE :table SET desc = :desc
                    WHERE trans_id = :trans_id""",
                    {'table': table, 'desc': desc, 'trans_id': trans.trans_id})

def remove_trans(trans, table):
    with conn:
        c.connect(""" DELETE from :table WHERE trans_id = :trans_id""",
                    {'table': table, 'trans_id': trans.trans_id})

def get_trans_by_date(date, table):
    c.connect("SELECT * FROM :table WHERE date = :date", {'table': table, 'date': date})
    return c.fetchall()

def get_trans_overunder_amount(amount,over_under ,table):
    over_under = over_under.lower()
    if over_under == "over":
        over_under = ">"
    else:
        over_under = "<"
    c.connect("SELECT * FROM :table WHERE amount :over_under :amount",
            {'table': table, 'over_under': over_under, 'amount': amount})
    return c.fetchall()

def get_trans_by_id(trans_id, table):
    c.connect("SELECT * FROM :table WHERE trans_id = :trans_id", {'table': table, 'trans_id': trans_id})
    return c.fetchall()

def get_trans_by_table(table):
    c.connect("SELECT * FROM :table WHERE table = :table", {'table': table})