import os
import time
import requests
import json
from datetime import datetime as dt
from bs4 import BeautifulSoup


from fil.jobsdb_sql import sql

def load_page(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ' + \
        '(KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    response = requests.get(url, headers={'User-Agent': user_agent})
    return response

def parse_greenhouse_page(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []
    for div in soup.find_all('div', {'class':'opening'}):
        job_title = div.find('a').text
        job_url = 'https://boards.greenhouse.io' + div.find('a')['href']
        job_loc = div.find('span').text
        element = div
        hierarchy = []
        while element and (element.name != 'section' or 'level-0' not in element.get('class', [])):
            element = element.parent
            hierarchy.append(element.find_all()[0].get_text(separator=' '))
        jobs.append({
            'job_title': job_title,
            'job_page_url': job_url,
            'location': job_loc,
            'department': hierarchy
        })
    return jobs

def save_to_db(company_page_scrape_id, scraped_at, company_id, company_name, jobs, website_type):

    if jobs is None or len(jobs) == 0:
        return None
    data = []
    placeholder_list = []
    for job in jobs:
        job_title = job['job_title']
        location = job['location']
        department = str(job['department'])
        job_page_url = job['job_page_url']

        row = (company_page_scrape_id, scraped_at, company_id, company_name, job_title, department, location, job_page_url, website_type)

        row_placeholders = ', '.join(['%s']*len(row))
        data.extend(row)
        placeholder_list.append('(' + row_placeholders + ')')

    column_names = 'company_page_scrape_id, scraped_at, company_id, company_name, job_title, department, location, job_page_url, website_type'
    data_placeholders = ', '.join(placeholder_list)
    insert_query = f"""
        INSERT INTO listing_parses ({column_names})
        VALUES {data_placeholders}
        ;"""
    sql(insert_query, data)

def test_save(test_data):
    data = []
    placeholder_list = []
    for firstname, lastname in test_data:
        row = (firstname, lastname)
        row_placeholders = ', '.join(['%s']*len(row))
        data.extend(row)
        placeholder_list.append('(' + row_placeholders + ')')

    column_names = 'firstname, lastname'
    data_placeholders = ', '.join(placeholder_list)
    insert_query = f"""
        INSERT INTO test ({column_names})
        VALUES {data_placeholders}
        ;"""

    sql(insert_query, data)

def update_company_scraper_status(scraper_status_info):
    insert_query = f"""
        INSERT INTO company_page_scraper_status (company_page_scrape_id, status)
        VALUES (%s, %s)
        ;"""
    sql(insert_query, scraper_status_info)

def scrape_company_page(company_data):
    company_id, company_name, website_url, website_type = company_data
    started_at = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    # record scrape attempt, get scrape_id
    scrape_data = (started_at, company_id, company_name, website_url, website_type)
    result = sql(f"""
        INSERT INTO company_page_scrapes
            (started_at, company_id, company_name, website_url, website_type)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING company_page_scrape_id
        ;""", scrape_data)
    company_page_scrape_id = result[0][0]

    # try:
    print('scraping page', flush=True)
    scraper_status_info = (company_page_scrape_id, 'Scraping page')
    update_company_scraper_status(scraper_status_info)
    scraped_at = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    response = load_page(website_url)

    print('parsing page', flush=True)
    scraper_status_info = (company_page_scrape_id, 'Parsing page')
    update_company_scraper_status(scraper_status_info)
    if website_type=='Greenhouse':
        jobs = parse_greenhouse_page(response)
    else:
        jobs = None

    print('Storing jobs in DB', flush=True)
    scraper_status_info = (company_page_scrape_id, 'Storing jobs in DB')
    update_company_scraper_status(scraper_status_info)
    save_to_db(company_page_scrape_id, scraped_at, company_id, company_name, jobs, website_type)

    print('Finished', flush=True)
    scraper_status_info = (company_page_scrape_id, 'Finished')
    update_company_scraper_status(scraper_status_info)

    finished_at = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    sql(f"""
        UPDATE company_page_scrapes
        SET finished_at = %s
        WHERE company_page_scrape_id = %s
        ;""", (finished_at, company_page_scrape_id))

    # except:
    #     print('scrape error', flush=True)


if __name__ == "__main__":
    print('test')
    # scrape_dict = {
    #     # 'Faire': 'https://boards.greenhouse.io/faire',
    #     # 'Point72': 'https://boards.greenhouse.io/point72',
    #     # 'Twitch': 'https://boards.greenhouse.io/twitch',
    #     'Ogilvy Health USA': 'https://boards.greenhouse.io/ogilvyhealthusa',
    #     'Ogilvy UK': 'https://boards.greenhouse.io/ogilvyuk'
    # }

    # for company_name, company_page_url in scrape_dict.items():
    #     scrape_company_page(company_name, company_page_url)

