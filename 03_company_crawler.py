import fil
from duckduckgo_search import DDGS
from googlesearch import search
import time

def get_next_search():
    query = """
        SELECT cnl.company_name_id, cnl.company_name, jsl.job_site_id, jsl.job_site_name, jsl.job_site_url
        FROM company_name_list cnl
        CROSS JOIN job_site_list jsl
        LEFT JOIN (
            SELECT *,
                ROW_NUMBER() OVER qux AS rn
            FROM company_searches
            WINDOW qux AS (PARTITION BY job_site_id, company_name_id ORDER BY search_time DESC)
        ) cs
        ON cnl.company_name_id = cs.company_name_id
            AND jsl.job_site_id = cs.job_site_id
        ORDER BY cs.search_time ASC NULLS FIRST
        LIMIT 1;
    """
    response = fil.sql(query)
    return response[0] if response else None

def perform_search(company_name_id, company_name, job_site_id, job_site_name, job_site_url):
    sleep_time = 3
    search_terms = f"site:{job_site_url} {company_name}"
    max_tries = 20
    response = []
    successfully_searched = False

    print(f"Searching \"{search_terms}\" on duckduckgo", end='', flush=True)


    # for _ in range(max_tries):
    #     try:
    #         search_results = list(search(search_terms, num_results=5, sleep_interval=5))
    #         print(' ✔', flush=True)
    #         successfully_searched = True
    #         break
    #     except:
    #         print(".", end='', flush=True)
    #         time.sleep(sleep_time)
    #     time.sleep(sleep_time)


    for _ in range(max_tries):
        try:
            with DDGS() as ddgs:
                response = list(ddgs.text(search_terms, max_results=5))
            print(' ✔')
            successfully_searched = True
            break
        except:
            print(".", end='', flush=True)
            time.sleep(sleep_time)
        time.sleep(sleep_time)



    if successfully_searched:
        results = [
            (company_name_id, job_site_id, search_terms, result['title'], result['href'])
            for result in response
        ]

        flattened_data = [item for result in results for item in result]
        data_s = ['(' + ', '.join(['%s'] * len(result)) + ')' for result in results]
        data_placeholders = ', '.join(data_s)

        # Insert data into the database
        insert_query = f"""
            INSERT INTO company_searches
                (company_name_id, job_site_id, search_terms, result_title, result_url)
            VALUES {data_placeholders};
        """
        fil.sql(insert_query, flattened_data)
    else:
        print()

while True:
    search_params = get_next_search()

    if search_params:
        company_name_id, company_name, job_site_id, job_site_name, job_site_url = search_params
        perform_search(company_name_id, company_name, job_site_id, job_site_name, job_site_url)
    else:
        print("Error retrieving search parameters.")
