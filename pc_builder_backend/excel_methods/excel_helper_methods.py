from typing import Union
import pandas as pd

from pc_builder_backend.constants import PART_COST_RANGE
from pc_builder_backend.pc_build import PCBuild


def read_excel_data(filepath: str) -> pd.DataFrame:
    """
    Reads data from the Excel doc into a pandas dataframe

    :param filepath: The filepath of the Excel doc
    :return: Dataframe containing the contents of the Excel doc
    """
    dataframe = pd.read_excel(filepath)
    return dataframe


def fetch_valid_parts(part_name: str, parts_dataframe: pd.DataFrame, target_price: Union[int, float]) -> pd.DataFrame:
    """
    Fetches valid parts from a DataFrame based on the specified part name and target price range.

    :param part_name: Name of the part to be fetched.
    :param parts_dataframe: DataFrame containing information about available parts.
    :param target_price: Target price for the part.
    :return: DataFrame containing valid parts within the target price range.
    :raises ValueError: If the input parameters are not of the expected types.
    """
    # Validate input parameters
    if not isinstance(part_name, str):
        raise ValueError("part_name must be a string.")
    if not isinstance(parts_dataframe, pd.DataFrame):
        raise ValueError("parts_dataframe must be a pandas DataFrame.")
    if not isinstance(target_price, (int, float)):
        raise ValueError("target_price must be a numeric value.")

    part_type = part_name
    target_plus = target_price + (target_price * PART_COST_RANGE / 100)
    target_minus = target_price - (target_price * PART_COST_RANGE / 100)
    query_string = '(Type == @part_type) & (@target_minus <= Price <= @target_plus)'
    trimmed_dataframe = parts_dataframe.query(query_string)
    if len(trimmed_dataframe) == 0:
        print("No items found")
    return trimmed_dataframe


def allocate_budget(build_budget: Union[int, float]) -> dict:
    """
    Allocates budget for different PC components based on the given build budget.

    :param build_budget: The budget allocated for the PC build.
    :return: A dictionary containing the price ratios for different PC components.
    :raises ValueError: If the budget is out of range.
    """

    if build_budget <= 500:
        part_ratios = {
            "CPU": 0.20,
            "GPU": 0.25,
            "RAM": 0.10,
            "Storage": 0.15,  # Combined SSD and HDD
            "Motherboard": 0.10,
            "Power Supply": 0.10,
            "Case": 0.10
        }
        return part_ratios
    elif 500 < build_budget <= 1000:
        part_ratios = {
            "CPU": 0.20,
            "GPU": 0.30,
            "RAM": 0.15,
            "Storage": 0.15,  # Combined SSD and HDD
            "Motherboard": 0.10,
            "Power Supply": 0.10,
            "Case": 0.10
        }
        return part_ratios

    elif 1000 < build_budget <= 1500:
        part_ratios = {
            "CPU": 0.25,
            "GPU": 0.40,
            "RAM": 0.10,
            "Storage": 0.10,  # Combined SSD and HDD
            "Motherboard": 0.10,
            "Power Supply": 0.05,
            "Case": 0.05
        }
        return part_ratios

    elif 1500 < build_budget <= 2000:
        part_ratios = {
            "CPU": 0.25,
            "GPU": 0.40,
            "RAM": 0.10,
            "Storage": 0.10,  # Combined SSD and HDD
            "Motherboard": 0.10,
            "Power Supply": 0.05,
            "Case": 0.05
        }
        return part_ratios

    else:
        raise ValueError("Budget out of range")


def generate_build_from_excel(build_price: Union[int, float], complete_parts_df: pd.DataFrame) -> PCBuild:
    """
    Generates a PC build based on a given budget and available parts information.

    :param build_price: The budget allocated for the PC build.
    :param complete_parts_df: DataFrame containing information about available parts.
    :return: An instance of the PCBuild class representing the generated PC build.
    """
    new_build = PCBuild()

    price_ratios = allocate_budget(build_budget=build_price)

    cpu_price = build_price * price_ratios["CPU"]
    gpu_price = build_price * price_ratios["GPU"]
    ram_price = build_price * price_ratios["RAM"]
    storage_price = build_price * price_ratios["Storage"]
    motherboard_price = build_price * price_ratios["Motherboard"]
    psu_price = build_price * price_ratios["Power Supply"]
    case_price = build_price * price_ratios["Case"]

    valid_cpu_df = fetch_valid_parts(part_name="CPU", parts_dataframe=complete_parts_df, target_price=cpu_price)
    valid_gpu_df = fetch_valid_parts(part_name="GPU", parts_dataframe=complete_parts_df, target_price=gpu_price)
    valid_ram_df = fetch_valid_parts(part_name="RAM", parts_dataframe=complete_parts_df, target_price=ram_price)

    # Below will fetch both hdd and ssd to the same dataframe
    valid_storage_df = fetch_valid_parts(part_name="HDD", parts_dataframe=complete_parts_df, target_price=storage_price)
    valid_storage_df = pd.concat([valid_storage_df, fetch_valid_parts(part_name="SSD",
                                                                      parts_dataframe=complete_parts_df,
                                                                      target_price=storage_price)], ignore_index=True)

    valid_motherboard_df = fetch_valid_parts(part_name="Motherboard", parts_dataframe=complete_parts_df,
                                             target_price=motherboard_price)

    valid_psu_df = fetch_valid_parts(part_name="Power Supply", parts_dataframe=complete_parts_df,
                                     target_price=psu_price)

    valid_case_df = fetch_valid_parts(part_name="Case", parts_dataframe=complete_parts_df, target_price=case_price)

    cpu = valid_cpu_df.sample(n=1)
    cpu_name = cpu.iloc[0]['Name']
    cpu_price = cpu.iloc[0]['Price']

    gpu = valid_gpu_df.sample(n=1)
    gpu_name = gpu.iloc[0]['Name']
    gpu_price = gpu.iloc[0]['Price']

    ram = valid_ram_df.sample(n=1)
    ram_name = ram.iloc[0]['Name']
    ram_price = ram.iloc[0]['Price']

    storage = valid_storage_df.sample(n=1)
    storage_name = storage.iloc[0]['Name']
    storage_price = storage.iloc[0]['Price']

    motherboard = valid_motherboard_df.sample(n=1)
    motherboard_name = motherboard.iloc[0]['Name']
    motherboard_price = motherboard.iloc[0]['Price']

    psu = valid_psu_df.sample(n=1)
    psu_name = psu.iloc[0]['Name']
    psu_price = psu.iloc[0]['Price']

    case = valid_case_df.sample(n=1)
    case_name = case.iloc[0]['Name']
    case_price = case.iloc[0]['Price']

    new_build.set_cpu(cpu_name, cpu_price)
    new_build.set_gpu(gpu_name, gpu_price)
    new_build.set_ram(ram_name, ram_price)
    new_build.set_storage(storage_name, storage_price)
    new_build.set_motherboard(motherboard_name, motherboard_price)
    new_build.set_power_supply(psu_name, psu_price)
    new_build.set_case(case_name, case_price)

    return new_build
