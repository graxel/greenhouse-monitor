import fil

res = fil.sql("""
    SELECT DISTINCT
        lp.company_id,
        SUBSTR(lp.job_page_url, 1, 20) AS truncated_url,
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
for row in res:
    print(row)