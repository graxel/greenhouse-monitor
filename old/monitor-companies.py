"""
Company prioritizer -- PROCESS
    1. Activated every N seconds
    2. Get least recently scraped company
    3. Calls company page scraper to scrape company
"""
import add_root
import os, sys
thispath = os.path.dirname(__file__)
if thispath not in sys.path: sys.path.append(thispath)

import fil
import schedule
import time


def get_company_to_scrape():
    result = fil.sql(f"""
        SELECT companies.id, companies.company_name, companies.website_url, companies.website_type
        FROM (
            SELECT company_id, started_at, finished_at,
                ROW_NUMBER() OVER (PARTITION BY company_id ORDER BY finished_at DESC NULLS LAST) AS rn
            FROM company_page_scrapes
            ) lease_recently_scraped
        JOIN companies
            ON lease_recently_scraped.company_id=companies.id
        WHERE lease_recently_scraped.rn=1
            AND companies.blacklisted=false
        ORDER BY lease_recently_scraped.finished_at ASC NULLS FIRST
        LIMIT 1
        ;""")
    company_data = result[0]
    return company_data

def check_company():
    print('Getting company to scrape...', end=' ', flush=True)
    company_data = get_company_to_scrape()
    print(f"got {company_data[1]}.", flush=True)
    fil.scrape_company_page(company_data)
    print()

schedule.every(10).seconds.do(check_company)

while True:
    schedule.run_pending()
    time.sleep(1)