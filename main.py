import sqlite3

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

def update_amount(trans, amount, table):
    with conn:
        c.execute("""UPDATE :table SET amount = :amount
                    WHERE trans_id = :trans_id""",
                    {'table': table, 'trans_id': trans.trans_id, 'amount': amount})

def update_date(trans, date, table):
    with conn:
        c.connect()

def update_desc(trans, desc, table):
    pass

def remove_trans(emp, table):
    pass

def get_trans_by_date(date, table):
    pass