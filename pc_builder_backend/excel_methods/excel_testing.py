from excel_helper_methods import read_excel_data, fetch_valid_parts
import os
import pandas as pd

from pc_builder_backend.pc_build import PCBuild

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
# Adds 20% to use as the higher range, subtracts 20% to use as the lower range
target_price = 70
target_plus = target_price + (target_price * 20 / 100)
target_minus = target_price - (target_price * 20 / 100)

# Filter the DataFrame to only include SSD parts with prices between target_minus and target_plus
ssd_dataframe = complete_parts_df.query('(Type == "SSD") & (@target_minus <= Price <= @target_plus)')
print(ssd_dataframe)


print("-------------------")

print("Helper method below")
method_ssd_dataframe = fetch_valid_parts(part_name="SSD", parts_dataframe=complete_parts_df, target_price=70)
print(method_ssd_dataframe)


"""
        print(f"SSD: {self.ssd} - Price: £{self.ssd_price}")
        print(f"HDD: {self.hdd} - Price: £{self.hdd_price}")
        print(f"Motherboard: {self.motherboard} - Price: £{self.motherboard_price}")
        print(f"Power Supply: {self.power_supply} - Price: £{self.power_supply_price}")
        print(f"Case: {self.case} - Price: £{self.case_price}\n")
"""


# HERE ON

print("\n\n#######################################################\n")

# CPU DataFrame
cpu_dataframe = complete_parts_df.query('Type == "CPU" and 200 <= Price <= 300')
sample_cpu = cpu_dataframe.sample(n=1)
sample_cpu_name = sample_cpu.loc[sample_cpu.index[0], 'Name']
sample_cpu_price = sample_cpu.loc[sample_cpu.index[0], 'Price']

# GPU DataFrame
gpu_dataframe = complete_parts_df.query('Type == "GPU" and 250 <= Price <= 400')
sample_gpu = gpu_dataframe.sample(n=1)
sample_gpu_name = sample_gpu.loc[sample_gpu.index[0], 'Name']
sample_gpu_price = sample_gpu.loc[sample_gpu.index[0], 'Price']

# RAM DataFrame
ram_dataframe = complete_parts_df.query('Type == "RAM" and 75 <= Price <= 125')
sample_ram = ram_dataframe.sample(n=1)
sample_ram_name = sample_ram.loc[sample_ram.index[0], 'Name']
sample_ram_price = sample_ram.loc[sample_ram.index[0], 'Price']

# HDD DataFrame
hdd_dataframe = complete_parts_df.query('Type == "HDD" and 75 <= Price <= 150')
sample_hdd = hdd_dataframe.sample(n=1)
sample_hdd_name = sample_hdd.loc[sample_hdd.index[0], 'Name']
sample_hdd_price = sample_hdd.loc[sample_hdd.index[0], 'Price']

# SSD DataFrame
ssd_dataframe = complete_parts_df.query('Type == "SSD" and 100 <= Price <= 150')
sample_ssd = ssd_dataframe.sample(n=1)
sample_ssd_name = sample_ssd.loc[sample_ssd.index[0], 'Name']
sample_ssd_price = sample_ssd.loc[sample_ssd.index[0], 'Price']

# Motherboard DataFrame
motherboard_dataframe = complete_parts_df.query('Type == "Motherboard" and 75 <= Price <= 125')
sample_motherboard = motherboard_dataframe.sample(n=1)
sample_motherboard_name = sample_motherboard.loc[sample_motherboard.index[0], 'Name']
sample_motherboard_price = sample_motherboard.loc[sample_motherboard.index[0], 'Price']

# Power Supply DataFrame
ps_dataframe = complete_parts_df.query('Type == "Power Supply" and 75 <= Price <= 125')
sample_ps = ps_dataframe.sample(n=1)
sample_ps_name = sample_ps.loc[sample_ps.index[0], 'Name']
sample_ps_price = sample_ps.loc[sample_ps.index[0], 'Price']

# Case DataFrame where parts are filtered by price
case_dataframe = complete_parts_df.query('Type == "Case" and 50 <= Price <= 70')
sample_case = case_dataframe.sample(n=1)
sample_case_name = sample_case.iloc[0]['Name']
sample_case_price = sample_case.iloc[0]['Price']

new_build = PCBuild()
new_build.set_cpu(sample_cpu_name, sample_cpu_price)
new_build.set_gpu(sample_gpu_name, sample_gpu_price)
new_build.set_ram(sample_ram_name, sample_ram_price)
new_build.set_hdd(sample_hdd_name, sample_hdd_price)
new_build.set_ssd(sample_ssd_name, sample_ssd_price)
new_build.set_motherboard(sample_motherboard_name, sample_motherboard_price)
new_build.set_power_supply(sample_ps_name, sample_ps_price)
new_build.set_case(sample_case_name, sample_case_price)

print(new_build)

