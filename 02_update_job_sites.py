import fil
import pandas as pd

job_site_list = pd.read_csv('seed_data/job_site_list.csv').drop_duplicates()

def prep_for_insert(data):
    data_s = data.apply(lambda r: '(' + ', '.join(['?']*len(r)) + ')', axis=1)
    data_placeholders = ', '.join(data_s)
    flattened_data = data.values.flatten().tolist()
    return flattened_data, data_placeholders


flattened_data, data_placeholders = prep_for_insert(job_site_list)
insert_query = f"""
    INSERT INTO job_site_list (job_site_name,job_site_url)
    VALUES {data_placeholders}
    ON CONFLICT (job_site_url) DO NOTHING
    ;"""
fil.sql(insert_query, flattened_data)

job_sites_in_db = fil.sql("""
    SELECT * FROM job_site_list
    ;""")
for row in job_sites_in_db:
    print(row)