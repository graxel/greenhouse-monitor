import os
import sys
import psycopg2
from psycopg2 import OperationalError, Error


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
        SELECT table_schema, table_name, column_name
        FROM information_schema.columns
        WHERE table_schema in ('public', 'dev')
        ORDER BY table_schema, table_name
        ;""")
    if resp is not None:
        for line in resp:
            print(line)