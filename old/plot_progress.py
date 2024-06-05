import pandas as pd
import pytz
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import add_root
import fil


scrape_history = fil.sql("""
    SELECT job_scrape_id, started_at, finished_at
    FROM job_scrapes
    ORDER BY job_scrape_id DESC
    ;""")

target = fil.sql("""
    SELECT
    (SELECT MAX(job_scrape_id) FROM job_scrapes) + 
    (SELECT COUNT(DISTINCT lp.job_page_url)
    FROM listing_parses lp
    LEFT JOIN job_scrapes js
        ON lp.job_page_url = js.job_page_url
    LEFT JOIN companies co
        ON lp.company_id = co.id
    WHERE js.job_page_url IS NULL
        AND lp.job_page_url != 'NaN'
        AND co.blacklisted != true)
    ;""")[0][0]

df = pd.DataFrame(scrape_history, columns=['job_scrape_id', 'started_at', 'finished_at'])

# Fit a linear regression model
model = LinearRegression()
# sample = df[df['job_scrape_id']>11450]
sample = df.head(1000)

timestamp = pd.to_datetime(sample['finished_at'], utc=False)
utc_timestamp = timestamp.dt.tz_localize('EST').dt.tz_convert('UTC')
y = (utc_timestamp.astype(int) / 1e9).values.reshape(-1, 1)
X = sample['job_scrape_id'].values.reshape(-1, 1)
model.fit(X, y)

predicted_time = model.predict([[target]])[0][0]
print(f"Current job scrape target: {target}")
print(f"Current max job scrape id: {df['job_scrape_id'].max()}")
print(f"Projected time to finish scraping jobs: {datetime.fromtimestamp(predicted_time)}", flush=True)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df['finished_at'], df['job_scrape_id'], marker='.', linestyle='-', label='Scrape Progress')
# plt.plot(sample['finished_at'], sample['job_scrape_id'], marker='.', linestyle='-', label='Scrape Progress')
# Plot the linear regression line
linear_range = np.linspace(0, target, 100).reshape(-1, 1)
predicted_array = model.predict(linear_range)
predicted_timestamps = [datetime.fromtimestamp(preds[0]) for preds in predicted_array]
plt.plot(predicted_timestamps, linear_range, color='red', linestyle='--', label='Linear Regression')


plt.title('Scrape Progression Over Time')
plt.xlabel('finished_at')
plt.ylabel('job_scrape_id')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
