import os
import psycopg2
from psycopg2 import OperationalError, Error
import pandas as pd

def sql(query, data=None):
    try:
        conn = psycopg2.connect(
            host=os.getenv('JOBSDB_HOST'),
            database=os.getenv('JOBSDB_DATABASE'),
            user=os.getenv('JOBSDB_USERNAME'),
            password=os.getenv('JOBSDB_PASSWORD'))
        cursor = conn.cursor()
        if data is None:
            cursor.execute(query)
        else:
            cursor.execute(query, data)
        conn.commit()
        if cursor.pgresult_ptr is not None:
            rows = cursor.fetchall()
            return rows
    except Error as e:
        print("Error: Unable to execute the query.")
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
res = sql("""SELECT company_name, website_url, website_type, blacklisted FROM companies;""")
res_list = list(res)

df = pd.DataFrame(data=res_list, columns=['company_name', 'website_url', 'website_type', 'blacklisted'])
df.to_csv('companies_to_add.csv', index=False)
