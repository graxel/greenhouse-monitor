import fil
from transformers import DistilBertTokenizer

# Load pre-trained tokenizer
model_name = 'distilbert-base-uncased'
tokenizer = DistilBertTokenizer.from_pretrained(model_name)

rows = fil.sql(
    """
    SELECT job_id, job_title, job_description
    FROM jobs
    WHERE tokens is NULL
    LIMIT 1000
    ;"""
)
print('rows retrieved:', len(rows))
rows_processed = 0

for row in rows:
    rows_processed += 1
    if rows_processed % 200 == 0:
        print('\n', end='', flush=True)
    if rows_processed % 100 == 0:
        print('   ', end=' ', flush=True)
    if rows_processed % 20 == 0:
        print(f"{rows_processed:03}", end=' ', flush=True)

    job_id, job_title, job_description = row
    text = job_title + ':\n' + job_description
    tokens_length = len(tokenizer.encode(text, add_special_tokens=False))
    
    fil.sql(
        'UPDATE jobs SET tokens = ? WHERE job_id = ?',
        data=(tokens_length, job_id)
    )

