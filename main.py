import sqlite3

conn = sqlite3.connect('finances.db')

c = conn.cursor()


# CREATE TABLES

c.execute(""" CREATE TABLE expenses (
            expense_date text,
            amount integer,
            desc text
            )""")

c.execute(""" CREATE TABLE income (
            expense_date text,
            amount integer,
            desc text
            )""")