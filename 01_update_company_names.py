import fil
import pandas as pd

company_name_list = pd.read_csv('seed_data/company_name_list.csv').drop_duplicates()

def prep_for_insert(data):
    data_s = data.apply(lambda r: '(' + ', '.join(['%s']*len(r)) + ')', axis=1)
    data_placeholders = ', '.join(data_s)
    flattened_data = data.values.flatten().tolist()
    return flattened_data, data_placeholders


flattened_data, data_placeholders = prep_for_insert(company_name_list)
insert_query = f"""
    INSERT INTO company_name_list (company_name)
    VALUES {data_placeholders}
    ON CONFLICT (company_name) DO NOTHING
    ;"""
fil.sql(insert_query, flattened_data)

company_names_in_db = fil.sql("""
    SELECT * FROM company_name_list
    ;""")
for row in company_names_in_db:
    print(row)