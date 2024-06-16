import os
import fil
import sys
import pandas as pd

if len(sys.argv) < 2:
    print("Usage: python db_query.py <query or .sql file>")
else:
    # Join all the arguments except the script name
    query_or_file = ' '.join(sys.argv[1:])
    if os.path.exists(query_or_file):
        with open(query_or_file) as f:
            query = f.read()
    else:
        query = query_or_file
    res = fil.sql(query)
    print(pd.DataFrame(res))