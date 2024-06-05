
import os
import hashlib
import boto3
from botocore.exceptions import NoCredentialsError


def calculate_hash(content, hash_length=16):
    encoded_content = content.encode('utf-8')
    hashed_content = hashlib.sha256(encoded_content).hexdigest()
    return hashed_content[:hash_length]

def upload_to_s3(filename, content):
    s3 = boto3.client('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    bucket_name = 'thelatestjobs'
    try:
        s3.put_object(Bucket=bucket_name, Key=filename, Body=content)
    except NoCredentialsError:
        print("AWS credentials not found")



page_content = 'here are a few emojis:😊 ❤️ 🌟 🎉 🌈 🍕'

hash_value = calculate_hash(page_content)
filepath = f"company_scrapes/{hash_value}"
upload_to_s3(filepath, page_content)

