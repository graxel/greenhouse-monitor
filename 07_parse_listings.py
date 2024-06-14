
import fil

import time
import pandas as pd
from bs4 import BeautifulSoup

def find_job_links(row):
    html_content = row['page_content']
    if html_content is None:
        return []
    website_url = row['website_url']
    url_base = website_url.strip('/').split('/')[-1] + '/'
    soup = BeautifulSoup(html_content, 'html.parser')
    a_elements = soup.find_all(
        'a',
        href=lambda href: href
        and (url_base in href or 'gh_jid' in href)
        and ('oneclick-ui' not in href)
    )
    job_links = [
        'https://boards.greenhouse.io'+a['href']
        if a['href'].lstrip('/').startswith(url_base)
        else a['href']
        for a in a_elements
    ]
    return list(set(job_links))
    
def count_job_links(row):
    job_links = row['job_links']
    link_count = len(job_links)
    return link_count

oldest_scrape_query = """
    SELECT 
      company_page_scrape_id,
      started_at,
      finished_at,
      company_id,
      company_name,
      processed,
      website_type,
      website_url,
      page_hash
      -- page_content
    FROM company_page_scrapes
    WHERE processed = FALSE
    ORDER BY finished_at ASC NULLS LAST
    LIMIT 1
    ;"""

# oldest_scrape_query = """
    # SELECT 
    #     cs.company_page_scrape_id,
    #     cs.started_at,
    #     cs.finished_at,
    #     cs.company_id,
    #     cs.company_name,
    #     cs.processed,
    #     cs.website_type,
    #     cs.website_url,
    #     cs.page_hash
    # FROM company_page_scrapes cs
    # LEFT JOIN listing_parses lp
    # ON cs.company_page_scrape_id = lp.company_page_scrape_id
    # WHERE cs.page_hash IS NOT NULL
    # AND lp.company_page_scrape_id IS NULL
    # ORDER BY cs.finished_at ASC NULLS LAST
    # LIMIT 1
#     ;"""

while True:
    scrape_resp = fil.sql(oldest_scrape_query)
    if len(scrape_resp) == 0:
        print('waiting for more scrapes')
        time.sleep(30)
    else:
        scrape = pd.DataFrame(scrape_resp, columns=[
            'company_page_scrape_id',
            'started_at',
            'finished_at',
            'company_id',
            'company_name',
            'processed',
            'website_type',
            'website_url',
            'page_hash'
        ])
        website_url = scrape['website_url'].iloc[0]
        company_page_scrape_id = int(scrape['company_page_scrape_id'].iloc[0])
        print(f'got scrape record of {website_url}', flush=True)

        file_exists = fil.check_if_file_exists_in_s3(
            bucket_name = 'thelatestjobs',
            folder_name = 'company_scrapes',
            file_name = scrape['page_hash'].iloc[0]
        )
        if not file_exists:
            print(f"page content not found!\n\tbucket_name={bucket_name}\n\tfolder_name={folder_name}\n\tfile_name={file_name}")
        else:
            file_content = fil.load_file_from_s3(
                bucket_name = 'thelatestjobs',
                folder_name = 'company_scrapes',
                file_name = scrape['page_hash'].iloc[0]
            )
            scrape['page_content'] = file_content.decode('utf-8')

            if scrape['page_content'].iloc[0] is None:
                print('\tno page to process', flush=True)
            else:
                print('\tprocessing scraped page', flush=True)
                # print(scrape, flush=True)
                scrape['job_links'] = scrape.apply(find_job_links, axis=1)
                # scrapes['link_count'] = scrapes.apply(count_job_links, axis=1)

                df = scrape.explode('job_links')[[
                   'company_page_scrape_id',
                   'company_id',
                   # 'started_at',
                   'finished_at',
                   'website_type',
                   'job_links'
                ]]

                # print(df, flush=True)
                flattened_data = df.values.flatten().tolist()

                data_s = ['(' + ', '.join(['?'] * len(row)) + ')' for row in df.values]
                data_placeholders = ', '.join(data_s)

                # print(data_placeholders, flush=True)
                # print(flattened_data, flush=True)
                # break
                fil.sql(f"""
                    INSERT INTO listing_parses
                    (company_page_scrape_id, company_id, scraped_at, website_type, job_page_url)
                    VALUES {data_placeholders}
                ;""", flattened_data)

        print('\tupdating scrapes table', flush=True)
        fil.sql("""
            UPDATE company_page_scrapes
            SET processed = true
            WHERE company_page_scrape_id = ?
        ;""", (company_page_scrape_id,))
        print('\tdone\n', flush=True)
