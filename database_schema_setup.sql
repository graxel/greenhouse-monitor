-- DROP TABLE dev.users;

-- DROP TABLE dev.company;

-- DROP TABLE dev.user_interest;

-- DROP TABLE dev.company_page_scrapes;

-- DROP TABLE dev.listing_parses;

-- DROP TABLE dev.jobs;

-- DROP TABLE dev.job_scrapes;

-- DROP TABLE dev.company_page_scraper_status;

-- DROP TABLE dev.job_scraper_status;

CREATE TABLE dev.company_name_list (
  company_name_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  company_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE dev.job_site_list (
  job_site_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  job_site_name VARCHAR(255) UNIQUE NOT NULL,
  job_site_url VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE dev.company_searches (
  search_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  company_name_id BIGINT,
  job_site_id BIGINT,
  search_terms VARCHAR(255),
  result_title VARCHAR(255),
  result_url VARCHAR(255)
);

CREATE TABLE dev.redirects (
  redirect_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  test_url VARCHAR(255) UNIQUE NOT NULL,
  end_url VARCHAR(255) NOT NULL,
  does_redirect BOOLEAN NOT NULL
);

CREATE TABLE dev.users (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  username VARCHAR(255)
);

CREATE TABLE dev.companies (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  company_name VARCHAR(255),
  website_url VARCHAR(255),
  website_type VARCHAR(255),
  blacklisted BOOLEAN DEFAULT FALSE
);

CREATE TABLE dev.user_interest (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT REFERENCES dev.users(id),
  company_id BIGINT REFERENCES dev.companies(id)
);

CREATE TABLE dev.company_page_scrapes (
  company_page_scrape_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  started_at TIMESTAMP,
  finished_at TIMESTAMP,
  company_id BIGINT REFERENCES dev.companies(id),
  company_name VARCHAR(255),
  processed BOOLEAN DEFAULT FALSE,
  website_type VARCHAR(255),
  website_url VARCHAR(255),
  page_hash VARCHAR(16),
  page_content TEXT -- delete
);

CREATE TABLE dev.company_page_scraper_status (
  status_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  company_page_scrape_id BIGINT REFERENCES dev.company_page_scrapes(company_page_scrape_id),
  event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(255)
);

CREATE TABLE dev.listing_parses (
  listing_parse_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  company_page_scrape_id BIGINT REFERENCES dev.company_page_scrapes(company_page_scrape_id),
  scraped_at TIMESTAMP,
  company_id BIGINT,
  job_page_url VARCHAR(255),
  website_type VARCHAR(255),
  page_hash VARCHAR(16)
);

CREATE TABLE dev.jobs (
  job_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  first_scraped_at TIMESTAMP,
  last_scraped_at TIMESTAMP,
  is_active VARCHAR(255),
  company_id BIGINT REFERENCES dev.companies(id),
  company_name VARCHAR(255),
  department VARCHAR(255),
  location VARCHAR(255),
  job_title VARCHAR(255),
  job_page_url VARCHAR(255) UNIQUE,
  job_description TEXT,
  website_type VARCHAR(255),
  page_hash VARCHAR(16)
);

CREATE TABLE dev.job_scrapes (
  job_scrape_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  started_at TIMESTAMP,
  finished_at TIMESTAMP,
  company_id BIGINT,
  company_name VARCHAR(255),
  job_page_url VARCHAR(255),
  website_type VARCHAR(255),
  page_hash VARCHAR(16)
);

CREATE TABLE dev.job_scraper_status (
  status_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  job_scrape_id BIGINT REFERENCES dev.job_scrapes(job_scrape_id),
  event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(255)
);
