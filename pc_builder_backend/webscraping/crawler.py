import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

"""
These methods aren't used at the moment to keep the scraper functioning correctly and legally, 
in the event they are needed they are here
"""


def fetch_links(url) -> list:
    """
    Fetches all links from the given URL and returns absolute URLs.

    :param url: URL to fetch links from.
    :return: List of absolute URLs.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    link_tags = soup.find_all('a', href=True)
    absolute_links = [urljoin(url, link['href']) for link in link_tags]
    return absolute_links


def fetch_links_with_page_mentioned_old(url) -> list:
    """
    Fetches links from the given URL that mention a page number in their href attribute.

    :param url: URL to fetch links from.
    :return: List of links mentioning a page number.
    """
    links = set()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a', href=True):
        if 'page' in link['href']:  # Fetches only the links with mentions of a page number
            links.add(link['href'])
    return list(links)


def fetch_links_with_page_mentioned(url) -> list:
    """
    Fetches links from the given URL that mention a page number in their href attribute.

    :param url: URL to fetch links from.
    :return: List of links mentioning a page number.
    """
    links = set()  # Use a set to automatically remove duplicates
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
        soup = BeautifulSoup(response.content, 'html.parser')
        base_url = response.url  # Get the base URL in case the links are relative
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(base_url, link['href'])  # Convert relative URL to absolute URL
            if 'page' in absolute_url:  # Check if the absolute URL contains 'page'
                links.add(absolute_url)  # Add the absolute URL to the set
    except requests.exceptions.RequestException as e:
        print(f"Error fetching links from {url}: {e}")
    return list(links)  # Convert the set back to a list before returning it
