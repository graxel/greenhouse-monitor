import os

def save_file(content, *args):
    path = os.path.join('data/', *args)
    with open(path, 'wb') as file:
        file.write(content.encode('utf-8'))

def check_if_file_exists(*args):
    path = os.path.join('data/', *args)
    file_exists = os.path.exists(path)
    return file_exists

def load_file(*args):
    path = os.path.join('data/', *args)
    with open(path, 'rb') as file:
        content = file.read()
    return content
