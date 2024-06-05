
import sqlite3
import os

if not os.path.exists('fil.db'):
    with open('database_setup_sqlite.sql') as f:
        db_setup_spec_raw = f.read()

    db_setup_spec = [db_cmd_raw.strip() + ';' for db_cmd_raw in db_setup_spec_raw.split(';')]

    con = sqlite3.connect('fil.db')
    cur = con.cursor()
    for db_cmd in db_setup_spec:
        cur.execute(db_cmd)
    con.close()

new_con = sqlite3.connect('fil.db')
new_cur = new_con.cursor()

tables = new_cur.execute('''
    SELECT name FROM sqlite_master  
    WHERE type='table'
    ;''')

table_list = tables.fetchall()
for table in table_list:
    table = table[0]
    columns = new_cur.execute(f'''SELECT '{table}', * FROM PRAGMA_TABLE_INFO('{table}');''')
    column_list = columns.fetchall()
    for column in column_list:
        print(column)
new_con.close()