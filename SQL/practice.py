import sqlite3

conn = sqlite3.connect("Presidents.db")
cursor = conn.cursor()

data = dict(Presidency=2, President="John Adams", Wikipedia Entry=)
cursor.execute("""
        insert into departments (department_id, department_name)
        values (:dept_id, :dept_name)""", data)