import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_links(url) -> list:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    link_tags = soup.find_all('a', href=True)
    absolute_links = [urljoin(url, link['href']) for link in link_tags]
    return absolute_links


def fetch_links_with_page_mentioned(url) -> list:
    links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a', href=True):
        if 'page' in link['href']:
            links.append(link['href'])
    return links


url = 'https://pcparts.uk/browse/cpus'
links = fetch_links_with_page_mentioned(url)
for link in links:
    print(link)
