from typing import Union


"""
    Note that due to the nature of not knowing compatibility, we will not be showing any fans, or other misc elements
    These will be up to the users discretion
"""


# cpu_plus = cpu_price + (cpu_price * 20 / 100)
# cpu_minus = cpu_price - (cpu_price * 20 / 100)


# Generates a budget percentage for each component
def build_cost_calculation(pc_budget: Union[int, float]) -> dict:
    if pc_budget >= 500:
        """ For a PC budget of 500 or less
        CPU (Central Processing Unit): 20%
        GPU (Graphics Processing Unit): 25%
        RAM (Random Access Memory): 10%
        Storage (SSD or HDD): 15%
        Motherboard: 10%
        Power Supply Unit (PSU): 10%
        Case: 10%
        """

        budget_dict = {
            'CPU_PRICE': pc_budget * 20 / 100,
            'GPU_PRICE': pc_budget * 25 / 100,
            'RAM_PRICE': pc_budget * 10 / 100,
            'STORAGE_PRICE': pc_budget * 15 / 100,
            'MOTHERBOARD_PRICE': pc_budget * 15 / 100,
            'PSU_PRICE': pc_budget * 10 / 100,
            'Case_PRICE': pc_budget * 10 / 100
        }
        return budget_dict

    if 500 < pc_budget <= 1000:
        budget_dict = {
            'CPU_PRICE': pc_budget * 20 / 100,
            'GPU_PRICE': pc_budget * 25 / 100,
            'RAM_PRICE': pc_budget * 10 / 100,
            'STORAGE_PRICE': pc_budget * 15 / 100,
            'MOTHERBOARD_PRICE': pc_budget * 15 / 100,
            'PSU_PRICE': pc_budget * 10 / 100,
            'Case_PRICE': pc_budget * 10 / 100
        }
        return budget_dict

    if 1000 < pc_budget <= 1500:
        budget_dict = {
            'CPU_PRICE': pc_budget * 20 / 100,
            'GPU_PRICE': pc_budget * 25 / 100,
            'RAM_PRICE': pc_budget * 10 / 100,
            'STORAGE_PRICE': pc_budget * 15 / 100,
            'MOTHERBOARD_PRICE': pc_budget * 15 / 100,
            'PSU_PRICE': pc_budget * 10 / 100,
            'Case_PRICE': pc_budget * 10 / 100
        }
        return budget_dict

    if 1500 < pc_budget <= 2000:
        budget_dict = {
            'CPU_PRICE': pc_budget * 20 / 100,
            'GPU_PRICE': pc_budget * 25 / 100,
            'RAM_PRICE': pc_budget * 10 / 100,
            'STORAGE_PRICE': pc_budget * 15 / 100,
            'MOTHERBOARD_PRICE': pc_budget * 15 / 100,
            'PSU_PRICE': pc_budget * 10 / 100,
            'Case_PRICE': pc_budget * 10 / 100
        }
        return budget_dict

    if pc_budget > 2000:
        budget_dict = {
            'CPU_PRICE': pc_budget * 20 / 100,
            'GPU_PRICE': pc_budget * 25 / 100,
            'RAM_PRICE': pc_budget * 10 / 100,
            'STORAGE_PRICE': pc_budget * 15 / 100,
            'MOTHERBOARD_PRICE': pc_budget * 15 / 100,
            'PSU_PRICE': pc_budget * 10 / 100,
            'Case_PRICE': pc_budget * 10 / 100
        }
        return budget_dict
