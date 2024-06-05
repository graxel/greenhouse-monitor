import time
import requests
from bs4 import BeautifulSoup

def load_page(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    response = requests.get(url, headers={'User-Agent': user_agent})
    return response

def parse_greenhouse_page(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        c_name = soup.find('h1').text
    except:
        c_name = 'error'
    return c_name

with open('c_urls.txt') as f:
    c_urls = f.read().splitlines()

for c_url in c_urls[764:]:
    response = load_page(c_url)
    c_name = parse_greenhouse_page(response)
    print(f"{c_url},{c_name}", flush=True)
    time.sleep(0.2)


