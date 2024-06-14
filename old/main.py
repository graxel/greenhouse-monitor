
import os, sys
thispath = os.path.dirname(__file__)
if thispath not in sys.path: sys.path.append(thispath)
###############################
import fil
from datetime import datetime as dt

started_at = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
company_id = 6
website_url = 'earl'
website_type = 'fake'
finished_at = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')

data = (started_at, finished_at, company_id, website_url, website_type)

insert_query = """
        INSERT INTO company_page_scrapes (
            started_at, finished_at, company_id, website_url, website_type
        )
        VALUES (?, ?, ?, ?, ?)
        RETURNING company_page_scrape_id
        ;"""
result = fil.sql("""
    ALTER TABLE company_page_scrapes
    ADD new_column_name data_type;
    ;""")
company_page_scrape_id = result[0][0]
print(company_page_scrape_id)
