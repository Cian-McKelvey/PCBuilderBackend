import requests
from bs4 import BeautifulSoup


def extract_cpu_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all('div', class_='card-horizontal')

    cpu_info = {}
    for product in products:
        name = product.find('div', class_='title').text.strip()
        price_elem = product.find('div', class_='price in-stock')
        if price_elem:
            price = price_elem.text.strip()
        else:
            price = 'Price not available'
        cpu_info[name] = price

    return cpu_info


def fetch_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch HTML content from the URL.")
        return None


def main():
    url = "https://pcparts.uk/browse/cpus"
    html_content = fetch_html_content(url)
    if html_content:
        cpu_info = extract_cpu_info(html_content)
        if cpu_info:
            for name, price in cpu_info.items():
                print("Name:", name)
                print("Price:", price)
                print()
        else:
            print("No CPU information found on the page.")
    else:
        print("Unable to fetch data from the provided URL.")


if __name__ == "__main__":
    main()
