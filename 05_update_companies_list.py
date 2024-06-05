"""
Company list updater -- SCRIPT
    1. Manually started
    2. Loads companies_list.csv
    3. Upserts rows into DB
"""
import pandas as pd
import add_root
import fil

def insert_company(row):
    insert_query = """
        INSERT INTO companies (company_name, website_url, website_type)
        VALUES (%s, %s, %s)
        ON CONFLICT (website_url) 
        DO UPDATE SET company_name = EXCLUDED.company_name, website_type = EXCLUDED.website_type
        ;"""
    fil.sql(
        insert_query,
        (row['company_name'], row['website_url'], row['website_type'])
    )

pd.read_csv('companies_to_add.csv').drop_duplicates().apply(insert_company, axis=1)

companies_in_db = fil.sql("""
    SELECT * FROM companies
    ;""")
for row in companies_in_db:
    print(row)