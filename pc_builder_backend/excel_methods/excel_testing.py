from excel_helper_methods import read_excel_data, fetch_valid_parts
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

# Target price and adjustment values, gets the aimed price of the part in this case its hardcoded.
# Adds 15% to use as the higher range, subtracts 15% to use as the lower range
target_price = 70
target_plus = target_price + (target_price * 15 / 100)
target_minus = target_price - (target_price * 15 / 100)

# Filter the DataFrame to only include SSD parts with prices between target_minus and target_plus
ssd_dataframe = complete_parts_df.query('(Type == "SSD") & (@target_minus <= Price <= @target_plus)')
print(ssd_dataframe)


print("-------------------")


method_ssd_dataframe = fetch_valid_parts(part_name="SSD", parts_dataframe=complete_parts_df, target_price=70)
print(method_ssd_dataframe)
