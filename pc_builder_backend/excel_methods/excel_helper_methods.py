from typing import Union

import pandas as pd


def read_excel_data(filepath: str) -> pd.DataFrame:
    dataframe = pd.read_excel(filepath)
    return dataframe


def fetch_valid_parts(part_name: str, parts_dataframe: pd.DataFrame, target_price: Union[int, float]) -> pd.DataFrame:
    part_type = part_name
    target_plus = target_price + (target_price * 15 / 100)
    target_minus = target_price - (target_price * 15 / 100)
    query_string = '(Type == @part_type) & (@target_minus <= Price <= @target_plus)'
    trimmed_dataframe = parts_dataframe.query(query_string)
    return trimmed_dataframe


"""
target_price = 70
target_plus = target_price + (target_price * 15 / 100)
target_minus = target_price - (target_price * 15 / 100)

# Filter the DataFrame to only include SSD parts with prices between target_minus and target_plus
ssd_dataframe = complete_parts_df.query('(Type == "SSD") & (@target_minus <= Price <= @target_plus)')
print(ssd_dataframe)
"""