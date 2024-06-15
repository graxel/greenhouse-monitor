-- DROP TABLE users;

-- DROP TABLE companies;

-- DROP TABLE user_interest;

-- DROP TABLE company_page_scrapes;

-- DROP TABLE listing_parses;

-- DROP TABLE jobs;

-- DROP TABLE job_scrapes;

-- DROP TABLE company_page_scraper_status;

-- DROP TABLE job_scraper_status;

CREATE TABLE company_name_list (
  company_name_id INTEGER PRIMARY KEY AUTOINCREMENT,
  company_name TEXT UNIQUE NOT NULL
);

CREATE TABLE job_site_list (
  job_site_id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_site_name TEXT UNIQUE NOT NULL,
  job_site_url TEXT UNIQUE NOT NULL
);

CREATE TABLE company_searches (
  search_id INTEGER PRIMARY KEY AUTOINCREMENT,
  search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  company_name_id INTEGER,
  job_site_id INTEGER,
  search_terms TEXT,
  result_title TEXT,
  result_url TEXT,
  FOREIGN KEY (company_name_id) REFERENCES company_name_list(company_name_id),
  FOREIGN KEY (job_site_id) REFERENCES job_site_list(job_site_id)
);

CREATE TABLE redirects (
  redirect_id INTEGER PRIMARY KEY AUTOINCREMENT,
  last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  test_url TEXT UNIQUE NOT NULL,
  end_url TEXT NOT NULL,
  does_redirect BOOLEAN NOT NULL
);

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT
);

CREATE TABLE companies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  company_name TEXT,
  website_url TEXT UNIQUE,
  website_type TEXT,
  blacklisted BOOLEAN DEFAULT FALSE
);

CREATE TABLE user_interest (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  company_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE company_page_scrapes (
  company_page_scrape_id INTEGER PRIMARY KEY AUTOINCREMENT,
  started_at TIMESTAMP,
  finished_at TIMESTAMP,
  company_id INTEGER,
  company_name TEXT,
  processed BOOLEAN DEFAULT FALSE,
  website_type TEXT,
  website_url TEXT,
  page_hash TEXT,
  page_content TEXT,
  FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE company_page_scraper_status (
  status_id INTEGER PRIMARY KEY AUTOINCREMENT,
  company_page_scrape_id INTEGER,
  event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status TEXT,
  FOREIGN KEY (company_page_scrape_id) REFERENCES company_page_scrapes(company_page_scrape_id)
);

CREATE TABLE listing_parses (
  listing_parse_id INTEGER PRIMARY KEY AUTOINCREMENT,
  company_page_scrape_id INTEGER,
  scraped_at TIMESTAMP,
  company_id INTEGER,
  job_page_url TEXT,
  website_type TEXT,
  page_hash TEXT,
  FOREIGN KEY (company_page_scrape_id) REFERENCES company_page_scrapes(company_page_scrape_id)
);

CREATE TABLE jobs (
  job_id INTEGER PRIMARY KEY AUTOINCREMENT,
  scraped_at TIMESTAMP,
  is_active TEXT,
  company_id INTEGER,
  company_name TEXT,
  department TEXT,
  location TEXT,
  job_title TEXT,
  job_page_url TEXT UNIQUE,
  job_description TEXT,
  website_type TEXT,
  page_hash TEXT,
  FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE job_scrapes (
  job_scrape_id INTEGER PRIMARY KEY AUTOINCREMENT,
  started_at TIMESTAMP,
  finished_at TIMESTAMP,
  company_id INTEGER,
  company_name TEXT,
  job_page_url TEXT,
  website_type TEXT,
  page_hash TEXT
);

CREATE TABLE job_scraper_status (
  status_id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_scrape_id INTEGER,
  event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status TEXT,
  FOREIGN KEY (job_scrape_id) REFERENCES job_scrapes(job_scrape_id)
);
