import requests
from bs4 import BeautifulSoup
from pc_builder_backend.excel_methods.excel_helper_methods import create_data_frame, combine_dataframes, write_excel_data
import pandas as pd
import os


def scrape_part_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all('div', class_='card-horizontal')

    part_info = {}
    for product in products:
        name = product.find('div', class_='title').text.strip()
        price_elem = product.find('div', class_='price in-stock')
        if price_elem:
            price = price_elem.text.strip()
        else:
            price = 'Price not available'
        part_info[name] = price

    return part_info


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
    ram_url = "https://pcparts.uk/browse/memory"
    ssd_url = "https://pcparts.uk/browse/solid-state-drives"
    hdd_url = "https://pcparts.uk/browse/hard-drives"
    motherboard_url = "https://pcparts.uk/browse/motherboards"
    power_supply_url = "https://pcparts.uk/browse/power-supplies"
    case_url = "https://pcparts.uk/browse/cases"

    # Fetch all the urls for the parts
    cpu_storage_dict = {}
    cpu_url_list = [cpu_url]
    # fetched_cpu_urls = fetch_links_with_page_mentioned_old(cpu_url)
    # cpu_url_list.append(fetched_cpu_urls[1:])

    gpu_storage_dict = {}
    gpu_url_list = [gpu_url]
    # fetched_gpu_urls = fetch_links_with_page_mentioned(gpu_url)
    # gpu_url_list.append(fetched_gpu_urls[2:])

    ram_storage_dict = {}
    ram_url_list = [ram_url]
    # fetched_ram_urls = fetch_links_with_page_mentioned(ram_url)
    # ram_url_list.append(fetched_ram_urls[2:])

    ssd_storage_dict = {}
    ssd_url_list = [ssd_url]
    # fetched_ssd_urls = fetch_links_with_page_mentioned(ssd_url)
    # ssd_url_list.append(fetched_ssd_urls[2:])

    hdd_storage_dict = {}
    hdd_url_list = [hdd_url]
    # fetched_hdd_urls = fetch_links_with_page_mentioned(hdd_url)
    # hdd_url_list.append(fetched_hdd_urls[2:])

    motherboard_storage_dict = {}
    motherboard_url_list = [motherboard_url]
    # fetched_motherboard_urls = fetch_links_with_page_mentioned(motherboard_url)
    # motherboard_url_list.append(fetched_motherboard_urls[2:])

    power_supply_storage_dict = {}
    power_supply_url_list = [power_supply_url]
    # fetched_power_supply_urls = fetch_links_with_page_mentioned(power_supply_url)
    # power_supply_url_list.append(fetched_power_supply_urls[2:])

    case_storage_dict = {}
    case_url_list = [case_url]
    # fetched_case_urls = fetch_links_with_page_mentioned(case_url)
    # case_url_list.append(fetched_case_urls[2:])

    for url in cpu_url_list:
        html_data = fetch_html_content(url)

        if html_data:
            cpu_data = scrape_part_data(html_content=html_data)

            if cpu_data:
                cpu_storage_dict.update(cpu_data)
            else:
                print("NO CPU DATA FOUND")
        else:
            print("URL ISN'T VALID + ", url)

    for url in gpu_url_list:
        html_data = fetch_html_content(url)

        if html_data:
            gpu_data = scrape_part_data(html_content=html_data)

            if gpu_data:
                gpu_storage_dict.update(gpu_data)
            else:
                print("NO CPU DATA FOUND")
        else:
            print("URL ISN'T VALID + ", url)


    for url in ram_url_list:
        html_data = fetch_html_content(url)

        if html_data:
            ram_data = scrape_part_data(html_content=html_data)

            if ram_data:
                ram_storage_dict.update(ram_data)
            else:
                print("NO CPU DATA FOUND")
        else:
            print("URL ISN'T VALID + ", url)

    # Loop for scraping data from HDD URLs
    for url in hdd_url_list:
        html_data = fetch_html_content(url)

        if html_data:
            hdd_data = scrape_part_data(html_content=html_data)

            if hdd_data:
                hdd_storage_dict.update(hdd_data)
            else:
                print("NO HDD DATA FOUND")
        else:
            print("URL ISN'T VALID: ", url)

    # Loop for scraping data from SSD URLs
    for url in ssd_url_list:
        html_data = fetch_html_content(url)

        if html_data:
            ssd_data = scrape_part_data(html_content=html_data)

            if ssd_data:
                ssd_storage_dict.update(ssd_data)
            else:
                print("NO SSD DATA FOUND")
        else:
            print("URL ISN'T VALID: ", url)

    # Loop for scraping data from Motherboard URLs
    for url in motherboard_url_list:
        html_data = fetch_html_content(url)

        if html_data:
            motherboard_data = scrape_part_data(html_content=html_data)

            if motherboard_data:
                motherboard_storage_dict.update(motherboard_data)
            else:
                print("NO MOTHERBOARD DATA FOUND")
        else:
            print("URL ISN'T VALID: ", url)

    # Loop for scraping data from Power Supply URLs
    for url in power_supply_url_list:
        html_data = fetch_html_content(url)

        if html_data:
            power_supply_data = scrape_part_data(html_content=html_data)

            if power_supply_data:
                power_supply_storage_dict.update(power_supply_data)
            else:
                print("NO POWER SUPPLY DATA FOUND")
        else:
            print("URL ISN'T VALID: ", url)

    # Loop for scraping data from Case URLs
    for url in case_url_list:
        html_data = fetch_html_content(url)

        if html_data:
            case_data = scrape_part_data(html_content=html_data)

            if case_data:
                case_storage_dict.update(case_data)
            else:
                print("NO CASE DATA FOUND")
        else:
            print("URL ISN'T VALID: ", url)

    # Printing to test
    print(len(cpu_storage_dict))
    print(cpu_storage_dict)
    print("\n")

    print(len(gpu_storage_dict))
    print(gpu_storage_dict)
    print("\n")

    print(len(ram_storage_dict))
    print(ram_storage_dict)
    print("\n")

    print("HDD Data:")
    print(len(hdd_storage_dict))
    print(hdd_storage_dict)
    print("\n")

    print("SSD Data:")
    print(len(ssd_storage_dict))
    print(ssd_storage_dict)
    print("\n")

    print("Motherboard Data:")
    print(len(motherboard_storage_dict))
    print(motherboard_storage_dict)
    print("\n")

    print("Power Supply Data:")
    print(len(power_supply_storage_dict))
    print(power_supply_storage_dict)
    print("\n")

    print("Case Data:")
    print(len(case_storage_dict))
    print(case_storage_dict)
    print("\n")

    cpu_df = create_data_frame(part_type="CPU", part_dict=cpu_storage_dict)

    gpu_df = create_data_frame(part_type="GPU", part_dict=gpu_storage_dict)

    ram_df = create_data_frame(part_type="RAM", part_dict=ram_storage_dict)

    hdd_df = create_data_frame(part_type="HDD", part_dict=hdd_storage_dict)

    ssd_df = create_data_frame(part_type="SSD", part_dict=ssd_storage_dict)

    motherboard_df = create_data_frame(part_type="Motherboard", part_dict=motherboard_storage_dict)

    psu_df = create_data_frame(part_type="Power Supply", part_dict=power_supply_storage_dict)

    case_df = create_data_frame(part_type="Case", part_dict=case_storage_dict)

    complete_df = combine_dataframes(cpu_df, gpu_df, ram_df, hdd_df, ssd_df, motherboard_df, psu_df, case_df)
    print(complete_df)

    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the Excel file relative to the project root
    excel_file = os.path.abspath(os.path.join(current_dir, '../../parts/components.xlsx'))

    write_excel_data(filepath=excel_file, dataframe=complete_df)


if __name__ == "__main__":
    main()
