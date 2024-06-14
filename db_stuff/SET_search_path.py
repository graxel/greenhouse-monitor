
import fil

rows = fil.sql("""
    --ALTER USER postgres SET search_path TO 'dev', 'public'
    --ALTER USER postgres RESET search_path
    SHOW search_path
    ;""")

if rows is not None:
    for row in rows:
        print(row)
