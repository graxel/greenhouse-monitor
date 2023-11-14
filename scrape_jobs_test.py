import os
import time
import requests
import json
from bs4 import BeautifulSoup


def load_page(url):
    time.sleep(1)
    scraped_at = time.time()
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ' + \
        '(KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    response = requests.get(url, headers={'User-Agent': user_agent})
    return response, scraped_at

def parse_greenhouse_page(response):
    time.sleep(1)
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

def fwprint(*things, w=14, **kwargs):
    trunc_things = [str(thing)[:w] for thing in things]
    fw_things = [thing+(' '*(w-len(thing))) for thing in trunc_things]
    print(*fw_things, **kwargs)
    
def save_to_db(company_name, jobs, scraped_at):
    # print()
    # fwprint('Title', 'Company', 'Location', 'Department', 'Scraped_at', 'URL', sep=' | ')
    # fwprint(*['-'*12]*6, sep=' | ')
    # for job in jobs:
    #     time.sleep(200)
    #     title = job['Title']
    #     location = job['Location']
    #     department = job['Hierarchy']
    #     url = job['URL']
        
    #     fwprint(title, company_name, location, department, scraped_at, url, sep=' | ')
    # print()

    with open('jobs_table.csv', 'a') as jfile:
        for job in jobs:
            time.sleep(0.2)
            title = job['Title']
            location = job['Location']
            department = job['Hierarchy']
            url = job['URL']

            print(scraped_at, title, company_name, location, department, url, sep='|', file=jfile)


def update_status(timestamp, worker_id, task, scraper_type, company, site, url):

    # fwprint(timestamp, '01', task, scraper_type, company, site, url, sep=' | ')

    with open('worker_status_table.csv', 'a') as sfile:
        print(timestamp, worker_id, task, scraper_type, company, site, url, sep='|', file=sfile)


def scrape_company_page(company_name, company_page_url, jobs_site='Greenhouse'):
    # fwprint('timestamp', 'id', 'task', 'scraper_type', 'company', 'site', 'url', sep=' | ')
    # fwprint(*['-'*12]*7, sep=' | ')

    scraped_at = time.time()
    update_status(
        timestamp=scraped_at,
        worker_id='01',
        task='Scraping page',
        scraper_type='company',
        company=company_name,
        site=jobs_site,
        url=company_page_url
    ) # initial task

    response = load_page(company_page_url)

    parsed_at = time.time()
    update_status(
        timestamp=parsed_at,
        worker_id='01',
        task='Parsing page',
        scraper_type='company',
        company=company_name,
        site=jobs_site,
        url=company_page_url
    ) # parsing

    if jobs_site=='Greenhouse':
        jobs = parse_greenhouse_page(response)

    stored_at = time.time()
    update_status(
        timestamp=stored_at,
        worker_id='01',
        task='Storing jobs in DB',
        scraper_type='company',
        company=company_name,
        site=jobs_site,
        url=company_page_url
    ) # saving to db

    save_to_db(company_name, jobs, scraped_at)

    finished_at = time.time()
    update_status(
        timestamp=finished_at,
        worker_id='01',
        task='Done',
        scraper_type='company',
        company=company_name,
        site=jobs_site,
        url=company_page_url
    ) # done


if __name__ == "__main__":

    from sql import sql
    query = """
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ;"""

    resp = sql(query)
    print(resp)


#     scrape_dict = {
#         'Faire': 'https://boards.greenhouse.io/faire',
#         'Point72': 'https://boards.greenhouse.io/point72',
#         'Twitch': 'https://boards.greenhouse.io/twitch',
#         'Ogilvy Health USA': 'https://boards.greenhouse.io/ogilvyhealthusa',
#         'Ogilvy UK': 'https://boards.greenhouse.io/ogilvyuk'
#     }

#     for company_name, company_page_url in scrape_dict.items():
#         scrape_company_page(company_name, company_page_url)

