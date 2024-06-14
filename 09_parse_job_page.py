from bs4 import BeautifulSoup
import sys

import fil
import time

def scrape_greenhouse_page(soup):
    try:
        logo_section = soup.find(class_="logo-container")
        logo_element = logo_section.find('img')
        logo_url = logo_element['src']
    except:
        logo_url = ''

    try:
        # header = soup.find(id="header")
        title_element = soup.find(class_="app-title")
        title = title_element.text.strip()
    except:
        title = ''

    try:
        company_name_element = soup.find(class_="company-name")
        company_name = company_name_element.text.strip()
        if company_name.startswith('at '):
            company_name = company_name[3:]
    except:
        company_name = ''

    try:
        location_element = soup.find(class_="location")
        location = location_element.text.strip()
    except:
        location = ''

    try:
        content_element = soup.find(id="content")
        desc = join_nested_elements(content_element)
    except:
        desc = ''

    data = {
        'logo_url': logo_url,
        'job_title': title,
        'company_name': company_name,
        'location': location,
        'description': desc
    }
    return data

def scrape_smartrecruiters_page(soup):

    main = soup.find('main', class_='jobad-main job')

    try:
        logo_section = soup.find(class_="header-logo logo")
        logo_element = logo_section.find('img')
        logo_url = logo_element['src']
    except:
        logo_url = ''

    try:
        title_element = main.find(itemprop="title")
        title = title_element.text
    except:
        title = ''

    try:
        date_posted_element = main.find(itemprop="datePosted")
        date_posted = date_posted_element['content']
    except:
        date_posted = ''

    try:
        industry_element = main.find(itemprop="industry")
        industry = industry_element['content']
    except:
        industry = ''

    try:
        company_name_element = main.find(itemprop="hiringOrganization")
        company_name = company_name_element['content']
    except:
        company_name = ''

    try:
        location_element = main.find('spl-job-location')########
        location = location_element['formattedaddress']
    except:
        location = ''

    try:
        location_element = main.find('spl-job-location')########
        workplace_type = location_element['workplacetype']
    except:
        workplace_type = ''

    try:
        emp_type_element = main.find(itemprop="employmentType")
        emp_type = emp_type_element.text
    except:
        emp_type = ''

    try:
        c_desc_element = main.find(id="st-companyDescription")
        c_desc = join_nested_elements(c_desc_element)
    except:
        c_desc = ''

    try:
        j_desc_element = main.find(id="st-jobDescription")
        j_desc = join_nested_elements(j_desc_element)
    except:
        j_desc = ''

    try:
        quals_element = main.find(id="st-qualifications")
        quals = join_nested_elements(quals_element)
    except:
        quals = ''

    try:
        addl_info_element = main.find(id="st-additionalInformation")
        addl_info = join_nested_elements(addl_info_element)
    except:
        addl_info = ''

    desc = ' '.join([c_desc, j_desc, quals, addl_info])

    data = {
        'logo_url': logo_url,
        'job_title': title,
        'date_posted': date_posted,
        'industry': industry,
        'company_name': company_name,
        'location': location,
        'workplace_type': workplace_type,
        'emp_type': emp_type,
        'c_description': c_desc,
        'j_description': j_desc,
        'qualifications': quals,
        'addl_info': addl_info,
        'description': desc
    }
    return data

def join_nested_elements(big_element, sep=' '):
    pieces = [
        nested_element.strip()
        for nested_element in big_element.descendants
        if isinstance(nested_element, str)
    ]
    joined_text = ' '.join(pieces)
    return joined_text.strip()

def get_job_to_parse():
    print('querying db...', flush=True)
    scrape_data = fil.sql("""
        SELECT 
            js.finished_at,
            js.company_id,
            js.job_page_url,
            js.website_type,
            js.page_hash
        FROM job_scrapes js
        LEFT JOIN jobs j
            ON js.job_page_url = j.job_page_url
        WHERE j.job_page_url IS NULL
        ORDER BY js.finished_at ASC NULLS LAST
        LIMIT 1
        ;""")
    return scrape_data

def check_for_job(job_page_url):
    # print(f"checking jobs table for {job_page_url}", flush=True)
    jobs_that_already_exist = fil.sql("""
        select
            scraped_at,
            company_name,
            job_title,
            location,
            job_page_url
        from jobs
        where job_page_url = ?
        limit 100
        ;""", (job_page_url,))
    return jobs_that_already_exist

while True:
    try:
        print()
        scrape_data = get_job_to_parse()
        if len(scrape_data) < 1:
            print('waiting for more jobs to parse')
            time.sleep(5)
            continue
        scraped_at, company_id, job_page_url, website_type, page_hash = scrape_data[0]


 
        jobs_that_already_exist = check_for_job(job_page_url)
        if len(jobs_that_already_exist) > 0:
            print('hmm, that job_page_url is already in the jobs table')
            # break



        print(f"parsing scrape from {job_page_url}")

        bucket_name = 'thelatestjobs'
        folder_name = 'job_scrapes'
        file_name = page_hash

        file_exists = fil.check_if_file_exists_in_s3(bucket_name, folder_name, file_name)
        if not file_exists:
            print(f"s3://{bucket_name}/{folder_name}/{file_name} not found!")
            break
        else:
            file_content = fil.load_file_from_s3(bucket_name, folder_name, file_name)
            html_content = file_content.decode('utf-8')

            soup = BeautifulSoup(html_content, 'html.parser')

            if website_type == 'Greenhouse':
                data = scrape_greenhouse_page(soup)
            elif website_type == 'SmartRecruiters':
                data = scrape_smartrecruiters_page(soup)
            else:
                print('Unknown page format, defaulting to Greenhouse')
                data = scrape_greenhouse_page(soup)

            data['scraped_at'] = scraped_at
            data['company_id'] = company_id
            data['job_page_url'] = job_page_url
            data['website_type'] = website_type
            data['page_hash'] = page_hash

            column_names = ', '.join(data.keys())
            data_placeholders = ', '.join(['?']*len(data.keys()))

            
            insert_query = f"""
                INSERT INTO jobs
                    ({column_names})
                VALUES ({data_placeholders});
            """
            # print(insert_query)
            print(tuple(data.values())[-3])
            # break

            print('storing in db')
            fil.sql(insert_query, tuple(data.values()))

    except Exception as e:
        print(e)
        print()
        time.sleep(5)