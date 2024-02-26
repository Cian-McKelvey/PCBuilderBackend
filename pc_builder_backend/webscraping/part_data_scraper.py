import requests
from bs4 import BeautifulSoup
from crawler import fetch_links_with_page_mentioned


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


def extract_gpu_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all('div', class_='card-horizontal')

    gpu_info = {}
    for product in products:
        name = product.find('div', class_='title').text.strip()
        price_elem = product.find('div', class_='price in-stock')
        if price_elem:
            price = price_elem.text.strip()
        else:
            price = 'Price not available'
        gpu_info[name] = price

    return gpu_info


def extract_ram_info(html_content):
    ...


def extract_ssd_info(html_content):
    ...


def extract_hdd_info(html_content):
    ...


def extract_motherboard_info(html_content):
    ...


def extract_power_supply_info(html_content):
    ...


def extract_case_info(html_content):
    ...


def fetch_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch HTML content from the URL.")
        return None


def main():
    cpu_url = "https://pcparts.uk/browse/cpus"
    gpu_url = "https://pcparts.uk/browse/graphics-cards"

    #url_list = []
    #url_list.append(url)
    #fetched_links = fetch_links_with_page_mentioned(url)
    # Append the second item onwards from fetched_links to url_list
    #url_list.extend(fetched_links[1:])

    # cpu_dict = {}
    # gpu_dict = {}

    cpu_content = fetch_html_content(cpu_url)
    gpu_content = fetch_html_content(gpu_url)

    cpu_dict = extract_cpu_info(html_content=cpu_content)
    gpu_dict = extract_gpu_info(html_content=gpu_content)

    # for url in url_list:
    #
    #     html_content = fetch_html_content(url)
    #
    #     if html_content:
    #         cpu_info = extract_cpu_info(html_content)
    #         if cpu_info:
    #
    #             cpu_dict.update(cpu_info)
    #
    #             for name, price in cpu_info.items():
    #                 print("Name:", name)
    #                 print("Price:", price)
    #                 print()
    #         else:
    #             print("No CPU information found on the page.")
    #     else:
    #         print("Unable to fetch data from the provided URL.")

    print(cpu_dict)
    print(gpu_dict)


if __name__ == "__main__":
    main()
