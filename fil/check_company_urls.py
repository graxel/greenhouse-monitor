import requests


from fil.jobsdb_sql import sql

def check_url(test_url):
    try:
        response = requests.head(test_url, allow_redirects=True)

        if response.history:
            end_url = response.url
            does_redirect = True
        else:
            end_url = test_url
            does_redirect = False

        print(f"{test_url}\t{end_url}\t{does_redirect}", flush=True)

        data = (test_url, end_url, does_redirect)
        insert_query = f"""
            INSERT INTO redirects (test_url, end_url, does_redirect)
            VALUES (%s, %s, %s)
            ON CONFLICT (test_url) 
            DO UPDATE SET end_url = EXCLUDED.end_url, does_redirect = EXCLUDED.does_redirect
            ;"""
        sql(insert_query, data)


    except requests.RequestException as e:
        print(f"URL: {test_url} could not be reached - Error: {e}")


# after the redirects have been tested, join the check list with the redirects and make the new "list for review"