import fil

def sql(query):
    rows = fil.sql(query)
    if rows is not None:
        for row in rows:
            print(row)

with open('database_schema_setup.sql') as f:
    setup_sql = f.read()

# sql(setup_sql)


print('dev\n=======================')

rows = fil.sql(f"""
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = 'dev'
    ORDER BY table_name
    ;""")
for row in rows:
    print(row)