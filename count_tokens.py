from datetime import datetime as dt
import fil
from transformers import DistilBertTokenizer

start = dt.now()

# Load pre-trained tokenizer
model_name = 'distilbert-base-uncased'
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model_loaded = dt.now()
print('model loaded in', (model_loaded - start).total_seconds(), 'seconds.')

rows = fil.sql(
    """
    SELECT job_id, job_title, job_description
    FROM jobs
    WHERE tokens is NULL
    LIMIT 1000
    ;"""
)
print('rows retrieved:', len(rows))
query_executed = dt.now()
print('query executed in', (query_executed - model_loaded).total_seconds(), 'seconds.')

rows_processed = 0

for row in rows:
    
    if rows_processed % 100 == 0:
        print('   ', end=' ', flush=True)
    if rows_processed % 200 == 0:
        print('\n', end='', flush=True)
    if rows_processed % 20 == 0:
        print(f"{rows_processed:03}", end=' ', flush=True)

    job_id, job_title, job_description = row
    text = job_title + ':\n' + job_description
    tokens_length = len(tokenizer.encode(text, add_special_tokens=False))
    
    fil.sql(
        'UPDATE jobs SET tokens = ? WHERE job_id = ?',
        data=(tokens_length, job_id)
    )

    rows_processed += 1

rows_updated = dt.now()
print('rows updated in', (rows_updated - query_executed).total_seconds(), 'seconds.')
print('(', (rows_updated - query_executed).total_seconds() / rows_processed, ' seconds per row)', sep='')