CREATE TABLE dev.users (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  username VARCHAR(255)
);

CREATE TABLE dev.company (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(255),
  website_url VARCHAR(255),
  website_type VARCHAR(255)
);

CREATE TABLE dev.user_interest (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  userid BIGINT REFERENCES dev.users(id),
  company_id BIGINT REFERENCES dev.company(id)
);

CREATE TABLE dev.company_page_scrapes (
  company_page_scrape_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  scraped_at TIMESTAMP,
  company_id BIGINT REFERENCES dev.company(id),
  website_url VARCHAR(255),
  website_type VARCHAR(255)
);

CREATE TABLE dev.listing_parses (
  listing_parse_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  company_page_scrape_id BIGINT REFERENCES dev.company_page_scrapes(company_page_scrape_id),
  scraped_at TIMESTAMP,
  company_id BIGINT REFERENCES dev.company(id),
  job_title VARCHAR(255),
  department VARCHAR(255),
  location VARCHAR(255),
  job_page_url VARCHAR(255),
  website_type VARCHAR(255)
);

CREATE TABLE dev.jobs (
  job_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  first_scraped_at TIMESTAMP,
  last_scraped_at TIMESTAMP,
  is_active VARCHAR(255),
  company_id BIGINT REFERENCES dev.company(id),
  department VARCHAR(255),
  location VARCHAR(255),
  job_title VARCHAR(255),
  job_page_url VARCHAR(255),
  job_description TEXT,
  website_type VARCHAR(255)
);

CREATE TABLE dev.job_scrapes (
  job_scrape_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  scraped_at TIMESTAMP,
  job_id BIGINT REFERENCES dev.jobs(job_id),
  company_id BIGINT REFERENCES dev.company(id),
  department VARCHAR(255),
  location VARCHAR(255),
  job_title VARCHAR(255),
  job_page_url VARCHAR(255),
  job_description TEXT,
  website_type VARCHAR(255)
);

CREATE TABLE dev.company_page_scraper_status (
  status_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  status VARCHAR(255),
  company_page_scrape_id BIGINT REFERENCES dev.company_page_scrapes(company_page_scrape_id),
  company_id BIGINT REFERENCES dev.company(id),
  worker_id BIGINT,
  event_time TIMESTAMP,
  website_type VARCHAR(255)
);

CREATE TABLE dev.job_scraper_status (
  status_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  status VARCHAR(255),
  job_scrape_id BIGINT REFERENCES dev.job_scrapes(job_scrape_id),
  worker_id BIGINT,
  event_time TIMESTAMP,
  website_type VARCHAR(255)
);
