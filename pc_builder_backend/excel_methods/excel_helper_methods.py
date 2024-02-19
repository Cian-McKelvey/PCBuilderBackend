from typing import Union
import pandas as pd

from pc_builder_backend.constants import PART_COST_RANGE


def read_excel_data(filepath: str) -> pd.DataFrame:
    dataframe = pd.read_excel(filepath)
    return dataframe


def fetch_valid_parts(part_name: str, parts_dataframe: pd.DataFrame, target_price: Union[int, float]) -> pd.DataFrame:
    """
    Fetch valid parts based on the specified part name and target price range.

    Args:
    - part_name (str): The type of part to search for.
    - parts_dataframe (pd.DataFrame): DataFrame containing parts data.
    - target_price (Union[int, float]): The target price for the part.

    Returns:
    - pd.DataFrame: DataFrame containing valid parts within the specified price range and part type.
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
    return trimmed_dataframe
