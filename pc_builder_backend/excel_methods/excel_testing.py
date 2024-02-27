from excel_helper_methods import read_excel_data, fetch_valid_parts, generate_build_from_excel
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
new_build.set_storage(sample_hdd_name, sample_hdd_price)
new_build.set_motherboard(sample_motherboard_name, sample_motherboard_price)
new_build.set_power_supply(sample_ps_name, sample_ps_price)
new_build.set_case(sample_case_name, sample_case_price)

print(new_build)

print('_' * 25)
print('\n\n\n')
print('_' * 25)

build_500 = PCBuild()
build_budget = 500

cpu_price = build_budget * 0.20
gpu_price = build_budget * 0.25
ram_price = build_budget * 0.10
storage_price = build_budget * 0.15
motherboard_price = build_budget * 0.10
psu_price = build_budget * 0.10
case_price = build_budget * 0.10

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
valid_psu_df = fetch_valid_parts(part_name="Power Supply", parts_dataframe=complete_parts_df, target_price=psu_price)
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

build_500.set_cpu(cpu_name, cpu_price)
build_500.set_gpu(gpu_name, gpu_price)
build_500.set_ram(ram_name, ram_price)
build_500.set_storage(storage_name, storage_price)
build_500.set_motherboard(motherboard_name, motherboard_price)
build_500.set_power_supply(psu_name, psu_price)
build_500.set_case(case_name, case_price)

print(build_500)


print('\n\n\n')
print('|' * 25)
print('\n\n\n')
print('|' * 25)
print('\n\n\n')

method_build = generate_build_from_excel(build_price=1000, complete_parts_df=complete_parts_df)
print(method_build)
