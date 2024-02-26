import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_links(url) -> list:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    link_tags = soup.find_all('a', href=True)
    absolute_links = [urljoin(url, link['href']) for link in link_tags]
    return absolute_links


url = 'https://pcparts.uk/browse/cpus'
links = fetch_links(url)
for link in links:
    print(link)
