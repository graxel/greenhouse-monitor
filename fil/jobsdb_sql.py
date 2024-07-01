from datetime import datetime as dt
import sqlite3
import traceback

def sql(query, data=None, col_names=False):
    try:
        conn = sqlite3.connect('fil.db')
        cursor = conn.cursor()
        if data is None:
            cursor.execute(query)
        else:
            cursor.execute(query, data)
        conn.commit()
        if cursor.description:  # Check if the query returns any result
            rows = cursor.fetchall()
            if col_names == True:
                column_names = [description[0] for description in cursor.description]
                return rows, column_names
            else:
                return rows
    except:
        print(dt.now())
        print(f"Error: Unable to execute the query. Query:\n{query}\n")
        print(traceback.format_exc())
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_scraper_status_table():
    sql("""
        CREATE TABLE public.scraper_status (
            event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            scraper_id integer,
            scraper_status varchar(255),
            scraper_type varchar(255),
            company_name varchar(255),
            jobs_site varchar(255),
            page_url varchar(255)
        )
        ;""")

def create_companies_table():
    sql("""
        CREATE TABLE public.scraper_status (
            company_name varchar(255),
            jobs_site varchar(255),
            page_url varchar(255)
        )
        ;""")

def create_jobs_table():
    sql("""
        CREATE TABLE public.jobs (
            scraped_at TIMESTAMP,
            title varchar(255),
            company varchar(255),
            location varchar(255),
            department varchar(255),
            url varchar(255)
        )
        ;""")

def create_test_table():
    sql("""
        CREATE TABLE public.test (
            firstname varchar(255),
            lastname varchar(255)
        )
        ;""")


if __name__ == "__main__":
    resp = sql("""
        SELECT name FROM sqlite_master  
        WHERE type='table'
        ;""")
    print(resp)
    print()
    if resp is not None:
        for line in resp:
            print(line)
        for table in resp:
            table = table[0]
            columns = sql(f'''
                SELECT '{table}', *
                FROM PRAGMA_TABLE_INFO('{table}')
                ;''')
            for column in columns:
                print(column)