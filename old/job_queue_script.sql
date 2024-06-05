
INSERT INTO jobs (company_id, company_name, job_page_url, website_type)
SELECT 
    labeled_listings.company_id,
    labeled_listings.company_name,
    labeled_listings.job_page_url,
    labeled_listings.website_type
FROM (
    SELECT *, 
        ROW_NUMBER() OVER (PARTITION BY job_page_url ORDER BY scraped_at DESC) rn
    FROM listing_parses
) labeled_listings
WHERE labeled_listings.rn=1
ON CONFLICT (job_page_url) DO NOTHING;