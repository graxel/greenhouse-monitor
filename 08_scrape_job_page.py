import time
import random
import requests
from datetime import datetime as dt

import hashlib

import add_root
import fil


def get_jobs_to_scrape():
    print('querying db...', flush=True)
    jobs = fil.sql("""
        SELECT 
            lp.company_id,
            lp.job_page_url,
            lp.website_type
        FROM listing_parses lp
        LEFT JOIN job_scrapes js
            ON lp.job_page_url = js.job_page_url
        LEFT JOIN companies co
            ON lp.company_id = co.id
        WHERE js.job_page_url IS NULL
            AND lp.job_page_url != 'NaN'
            AND co.blacklisted != true
        ORDER BY lp.scraped_at ASC NULLS LAST
        LIMIT 10
        ;""")
    return jobs
    # company_id, job_page_url, website_type = job_data[0]
    # return company_id, job_page_url, website_type



def scrape_with_requests(website_url):
    print('\tscraping with requests', flush=True)
    user_agent = 'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    try:
        response = requests.get(website_url, headers={'User-Agent': user_agent})
        page_content = response.text
    except:
        print('\tproblem loading page')
        page_content = ''
    return page_content


def calculate_hash(content, hash_length=16):
    encoded_content = content.encode('utf-8')
    hashed_content = hashlib.sha256(encoded_content).hexdigest()
    return hashed_content[:hash_length]


try:
    while True:
        wait_time = 0#random.uniform(4, 10)
        time.sleep(wait_time)
        try:
            print()
            started_at = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # company_id, job_page_url, website_type = get_job_to_scrape()
            jobs = get_jobs_to_scrape()
            for job in jobs:
                company_id, job_page_url, website_type = job
                print(f"got {job_page_url}", flush=True)
                # if job_page_url.startswith('https://boards.greenhouse.io'):
                page_content = scrape_with_requests(job_page_url)
                # else:
                #     page_content = scrape_with_selenium(driver, job_page_url)
                finished_at = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                page_hash = calculate_hash(page_content)

                file_exists = fil.check_if_file_exists_in_s3(
                    bucket_name='thelatestjobs',
                    folder_name='job_scrapes',
                    file_name=page_hash
                )
                if file_exists == False:
                    fil.save_to_s3(page_content,
                        bucket_name='thelatestjobs',
                        folder_name='job_scrapes',
                        file_name=page_hash
                    )
                data = (started_at, finished_at, company_id, job_page_url, website_type, page_hash)
                insert_query = f"""
                    INSERT INTO job_scrapes
                        (started_at, finished_at, company_id, job_page_url, website_type, page_hash)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """
                fil.sql(insert_query, data)
            if 1 == 0: ####### break loop after certain point? (change the 1 == 0)
                break
        except Exception as e:
            print(e)
            print()
            time.sleep(5)

except KeyboardInterrupt:
    # If you want to handle a keyboard interrupt to stop the script gracefully
    print("Script interrupted by the user.")

