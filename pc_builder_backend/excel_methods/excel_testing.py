from excel_helper_methods import read_excel_data
import os
import pandas as pd

# Get the current directory of the script
current_dir = os.path.dirname(os.path.realpath(__file__))
# Construct the path to the Excel file relative to the project root
excel_file = os.path.abspath(os.path.join(current_dir, '../../parts/components.xlsx'))

complete_parts_df = read_excel_data(excel_file)
print(complete_parts_df)

print("\n\n\n\n")

# Filter the DataFrame to only include CPU parts
cpu_dataframe = complete_parts_df.query('Type == "CPU"')
print(cpu_dataframe)

print("\n\n\n\n")

# Filter the DataFrame to only include CPU parts
ssd_dataframe = complete_parts_df.query('Type == "SSD"')
print(ssd_dataframe)
