import add_root
import pandas as pd
import fil


scrapes = fil.sql("""
    SELECT 
      company_page_scrape_id,
      started_at,
      finished_at,
      company_id,
      company_name,
      processed,
      website_type,
      website_url,
      page_content
    FROM company_page_scrapes
    WHERE processed = FALSE
    ORDER BY finished_at ASC NULLS LAST
    LIMIT 10 OFFSET 9600
    ;""")

# scrapes = fil.sql("""
#     SELECT 
#       company_page_scrape_id,
#       started_at,
#       finished_at,
#       company_id,
#       company_name,
#       processed,
#       website_type,
#       website_url,
#       page_content
#     FROM company_page_scrapes
#     WHERE website_url like '%embed_%' --processed = FALSE
#     AND page_content is not null
#     ORDER BY finished_at ASC NULLS LAST
#     LIMIT 10
#     ;""")

pd.DataFrame(scrapes, columns=[
    'company_page_scrape_id',
    'started_at',
    'finished_at',
    'company_id',
    'company_name',
    'processed',
    'website_type',
    'website_url',
    'page_content'
]).to_csv('bandaid_output.csv', index=False)