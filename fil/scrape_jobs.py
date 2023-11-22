import os
import time
import requests
import json
from datetime import datetime as dt
from bs4 import BeautifulSoup

from jobsdb_sql import sql


def load_page(url):
    scraped_at = time.time()
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ' + \
        '(KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    response = requests.get(url, headers={'User-Agent': user_agent})
    return response, scraped_at

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
            'Title': job_title,
            'URL': job_url,
            'Location': job_loc,
            'Hierarchy': hierarchy
        })
    return jobs

def save_to_db(company, jobs, scraped_at):
    if len(jobs) == 0:
        return None
    scraped_at = dt.fromtimestamp(scraped_at).strftime('%Y-%m-%d %H:%M:%S.%f')
    data = []
    placeholder_list = []
    for job in jobs:
        title = job['Title']
        location = job['Location']
        department = str(job['Hierarchy'])
        url = job['URL']

        row = (scraped_at, title, company, location, department, url)
        row_placeholders = ', '.join(['%s']*len(row))
        data.extend(row)
        placeholder_list.append('(' + row_placeholders + ')')

    column_names = 'scraped_at, title, company, location, department, url'
    data_placeholders = ', '.join(placeholder_list)
    insert_query = f"""
        INSERT INTO jobs ({column_names})
        VALUES {data_placeholders}
        ;"""
    print(insert_query)
    print(data)
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

def update_status(status_dict):
    column_names = ', '.join(status_dict.keys())
    data = tuple(status_dict.values())
    data_placeholders = ', '.join(['%s']*len(data))
    insert_query = f"""
        INSERT INTO scraper_status ({column_names})
        VALUES ({data_placeholders})
        ;"""
    sql(insert_query, data)

def scrape_company_page(company_name, company_page_url, jobs_site='Greenhouse'):

    scraper_info = {
        'scraper_id': 0,
        'scraper_type': 'company',
        'company_name': company_name,
        'jobs_site': jobs_site,
        'page_url': company_page_url
    }

    scraper_info['scraper_status'] = 'Scraping page'
    update_status(scraper_info)
    response, scraped_at = load_page(company_page_url)

    scraper_info['scraper_status'] = 'Parsing page'
    update_status(scraper_info)
    if jobs_site=='Greenhouse':
        jobs = parse_greenhouse_page(response)

    scraper_info['scraper_status'] = 'Storing jobs in DB'
    update_status(scraper_info)
    save_to_db(company_name, jobs, scraped_at)

    scraper_info['scraper_status'] = 'Finished'
    update_status(scraper_info)


if __name__ == "__main__":
    scrape_dict = {
        # 'Faire': 'https://boards.greenhouse.io/faire',
        # 'Point72': 'https://boards.greenhouse.io/point72',
        # 'Twitch': 'https://boards.greenhouse.io/twitch',
        'Ogilvy Health USA': 'https://boards.greenhouse.io/ogilvyhealthusa',
        'Ogilvy UK': 'https://boards.greenhouse.io/ogilvyuk'
    }

    for company_name, company_page_url in scrape_dict.items():
        scrape_company_page(company_name, company_page_url)

