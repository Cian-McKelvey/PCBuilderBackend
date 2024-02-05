import pandas as pd

# This definitely sucks too but there's nothing here so who cares


# Used for dict's, lists etc
def write_to_excel(filepath, data):
    df = pd.DataFrame(data)
    df.to_excel(filepath, sheet_name='Sheet1', index=False)


# Used for pre-made dataframes
def write_frame_to_excel(filepath, frame):
    frame.to_excel(filepath, sheet_name='Sheet1', index=False)


def read_excel_data(filepath: str) -> pd.DataFrame:
    dataframe = pd.read_excel(filepath)
    return dataframe
