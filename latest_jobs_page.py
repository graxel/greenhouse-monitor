import streamlit as st
import pandas as pd

import fil

st.set_page_config(layout="wide")


the_latest_jobs = fil.sql("""
    select
        scraped_at,
        company_name,
        job_title,
        location,
        job_page_url
    from jobs
    order by job_id desc
    limit 100
    ;""")


df = pd.DataFrame(the_latest_jobs, columns=['Scraped at', 'Company Name', 'Job Title', 'Location', 'URL'])
df['Scraped at'] = pd.to_datetime(df['Scraped at'], format='%Y-%m-%d %H:%M:%S.%f').dt.round('s')

df['URL'] = df['URL'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

html_table = df.to_html(escape=False, index=False)



custom_css = """
<style>
    th {
        text-align: left !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


st.title('The Latest Jobs')
st.write(html_table, unsafe_allow_html=True)