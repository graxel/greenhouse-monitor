import os
import s3fs

def set_up_fs():
    fs = s3fs.S3FileSystem(
        key=os.getenv('AWS_ACCESS_KEY_ID'),
        secret=os.getenv('AWS_SECRET_ACCESS_KEY'))
    return fs

def make_s3_path(bucket_name, folder_name=None, file_name=None):
    s3_path = f"{bucket_name.strip('/')}/"
    if folder_name: s3_path += f"{folder_name.strip('/')}/"
    if file_name: s3_path += file_name.strip('/')
    return s3_path

def save_to_s3(content, bucket_name, folder_name=None, file_name=None):
    fs = set_up_fs()
    s3_path = make_s3_path(bucket_name, folder_name, file_name)
    with fs.open(s3_path, 'wb') as file:
        file.write(content.encode('utf-8'))

def check_if_file_exists_in_s3(bucket_name, folder_name=None, file_name=None):
    fs = set_up_fs()
    s3_path = make_s3_path(bucket_name, folder_name, file_name)
    file_exists = fs.exists(s3_path)
    return file_exists

def load_file_from_s3(bucket_name, folder_name=None, file_name=None):
    fs = set_up_fs()
    s3_path = make_s3_path(bucket_name, folder_name, file_name)
    with fs.open(s3_path, 'rb') as s3_file:
        content = s3_file.read()
    return content



if __name__ == "__main__":

    bucket_name = 'thelatestjobs'
    folder_name = 'job_scrapes'
    file_name = '93b844e35ce48dfc'

    # save_to_s3(content, bucket_name, folder_name=None, file_name)


    # file_exists = check_if_file_exists_in_s3(bucket_name, folder_name, file_name)
    # print(file_exists)

    file_content = load_file_from_s3(bucket_name, folder_name, file_name)
    print(file_content.decode('utf-8'))
