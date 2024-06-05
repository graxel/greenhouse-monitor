import fil
import pandas as pd

# get all the companies that have been hoovered so far
found_companies = fil.sql("""
    WITH searches AS (
        SELECT
            REGEXP_REPLACE((REGEXP_MATCHES(company_searches.result_title, ' at (.*?)( - .*$|$)'))[1], ',', '', 'g') as found_company_name,
            (REGEXP_MATCHES(company_searches.result_url, CONCAT_WS('|',
                '(https://boards.greenhouse.io/embed.+',
                'https://boards.greenhouse.io/[^/|\?]+',
                'https://careers.smartrecruiters.com/[^/|\?]+)'
            )))[1] as found_company_url,
            job_site_list.job_site_name
        FROM company_searches
        LEFT JOIN job_site_list
            ON company_searches.job_site_id = job_site_list.job_site_id
    )
    , labelled_searches AS (
        SELECT found_company_name, found_company_url, job_site_name,
            ROW_NUMBER() OVER w AS rn
        FROM searches
        WINDOW w AS (PARTITION BY found_company_url ORDER BY found_company_name DESC NULLS LAST)
        ORDER BY found_company_url ASC, rn ASC
    )
    SELECT found_company_name, found_company_url, job_site_name
    FROM labelled_searches
    WHERE rn = 1
    ORDER BY CASE 
        WHEN found_company_name IS NULL THEN 0
        WHEN found_company_name LIKE '%...%' THEN 1
        ELSE 2
    END, found_company_name ASC
    ;""")

# companies to review
fc = pd.DataFrame(found_companies, columns=['found_company_name', 'found_company_url', 'job_site_name'])

for test_url in fc['found_company_url']:
    fil.check_url(test_url)

redirs = fil.sql("""
    SELECT test_url, end_url, does_redirect
    FROM redirects
    ;""")

rd = pd.DataFrame(redirs, columns=['test_url', 'end_url', 'does_redirect'])

df = fc.merge(rd, left_on='found_company_url', right_on='test_url')

df = df.rename(columns={
        'found_company_name': 'company_name',
        'end_url': 'website_url',
        'job_site_name': 'website_type'
    })
df = df.drop(columns=['found_company_url', 'test_url', 'does_redirect'])
df = df[['company_name', 'website_url', 'website_type']]
df.to_csv('companies_to_review.csv', index=False)
