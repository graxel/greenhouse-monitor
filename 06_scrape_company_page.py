import time
import random
import requests
from selenium import webdriver
from datetime import datetime as dt
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

import hashlib


import fil


options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

def get_company_to_scrape():
    company_data = fil.sql("""
        WITH latest_scrapes AS (
            SELECT finished_at, company_id
            FROM (
                SELECT company_id, started_at, finished_at,
                    ROW_NUMBER() OVER (PARTITION BY company_id ORDER BY finished_at DESC NULLS LAST) AS rn
                FROM company_page_scrapes
            ) labelled_scrapes
            WHERE rn = 1
        )
        SELECT companies.id, companies.company_name, companies.website_url, companies.website_type
        FROM latest_scrapes
        FULL OUTER JOIN companies ON latest_scrapes.company_id = companies.id
        WHERE companies.blacklisted=false
        ORDER BY latest_scrapes.finished_at ASC NULLS FIRST
        LIMIT 1
        ;""")
    company_id, company_name, website_url, website_type = company_data[0]
    return company_id, company_name, website_url, website_type


def sel_scroll(driver):
    # scroll to the bottom of the page
    prev_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        print('\tscrolling down', flush=True)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == prev_height: break
        prev_height = new_height
    # print('done scrolling', flush=True)

def sel_show_more_jobs(driver):
    # click every "Show more jobs" link
    while True:
        try: 
            more_links = driver.find_elements(By.XPATH, "//a[text()='Show more jobs']")
            if more_links:
                print('\tclicking "Show more jobs"', flush=True)
                driver.execute_script("arguments[0].scrollIntoView(true);", more_links[-1])
                time.sleep(0.1)
                driver.execute_script("arguments[0].click();", more_links[-1])
            else:
                break
        except StaleElementReferenceException:
            pass

def sel_expand(driver):
    # expand all accordion buttons
    try: 
        joblist = driver.find_element(by=By.ID, value="all-open-roles-1")
        butts = joblist.find_elements(By.TAG_NAME, "button")
        for butt in butts:
            print('\tclicking accordion button', flush=True)
            butt.click()
    except NoSuchElementException:
        pass

def scrape_with_selenium(driver, website_url):
    print('\tscraping with selenium', flush=True)
    driver.get(website_url)

    driver.implicitly_wait(2)

    sel_scroll(driver)

    sel_show_more_jobs(driver)

    sel_expand(driver)

    return driver.page_source

def scrape_with_requests(website_url):
    print('\tscraping with requests', flush=True)
    user_agent = 'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    response = requests.get(website_url, headers={'User-Agent': user_agent})
    return response.text


def calculate_hash(content, hash_length=16):
    encoded_content = content.encode('utf-8')
    hashed_content = hashlib.sha256(encoded_content).hexdigest()
    return hashed_content[:hash_length]


error_number = 1001
try:
    while True:
        wait_time = random.uniform(4, 10)
        time.sleep(wait_time)
        try:
            # Note time at start of scrape process
            started_at = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            # Get company to scrape
            company_id, company_name, website_url, website_type = get_company_to_scrape()
            print(f"\ngot {website_url}", flush=True)

            # Decide which method to use to scrape page
            if website_url.startswith('https://boards.greenhouse.io'):
                page_content = scrape_with_requests(website_url)
            else:
                page_content = scrape_with_selenium(driver, website_url)

            # Note time at end of scrape process
            finished_at = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            # Calculate page hash.
            page_hash = calculate_hash(page_content)

            # If hash doesn't exist in s3, save to s3, otherwise do nothing
            file_exists = fil.check_if_file_exists_in_s3(
                bucket_name='thelatestjobs',
                folder_name='company_scrapes',
                file_name=page_hash
            )
            if file_exists == False:
                fil.save_to_s3(page_content,
                    bucket_name='thelatestjobs',
                    folder_name='company_scrapes',
                    file_name=page_hash
                )

            # Store parsed data to db
            data = (started_at, finished_at, company_id, company_name, website_url, website_type, page_hash)
            insert_query = f"""
                INSERT INTO company_page_scrapes
                    (started_at, finished_at, company_id, company_name, website_url, website_type, page_hash)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            fil.sql(insert_query, data)

            # loop breaker
            if website_url == 'https://careers.smartrecruiters.com/itw':
                break

        except Exception as e:
            print(e)
            print()
            with open(f"error_page_{error_number}.html", 'w') as ef:
                ef.write(driver.page_source)
            time.sleep(5)

except KeyboardInterrupt:
    # If you want to handle a keyboard interrupt to stop the script gracefully
    print("Script interrupted by the user.")

finally:
    # Close the browser after all iterations or when the loop ends
    driver.quit()


