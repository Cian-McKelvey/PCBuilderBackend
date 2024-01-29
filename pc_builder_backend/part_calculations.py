# Ripped from the existing GitHub repo, ignore this it probably sucks
# Collection of methods that allow the calculation of approximate part costs


def cpu_cost_calculator(budget):
    if budget <= 1000:
        return (budget / 100) * 30  # The 30 here is the percentage. This is not a final number
    if budget > 1000 & budget <= 1500:
        return 2
    if budget > 1500 & budget <= 2000:
        return 3
    if budget > 2000:
        return 4


def gpu_cost_calculator(budget):
    if budget <= 1000:
        return 1
    if budget > 1000 & budget <= 1500:
        return 2
    if budget > 1500 & budget <= 2000:
        return 3
    if budget > 2000:
        return 4


def motherboard_cost_calculator(budget):
    if budget <= 1000:
        return 1
    if budget > 1000 & budget <= 1500:
        return 2
    if budget > 1500 & budget <= 2000:
        return 3
    if budget > 2000:
        return 4


def storage_cost_calculator(budget):
    if budget <= 1000:
        return 1
    if budget > 1000 & budget <= 1500:
        return 2
    if budget > 1500 & budget <= 2000:
        return 3
    if budget > 2000:
        return 4


def power_supply_cost_calculator(budget):
    if budget <= 1000:
        return 1
    if budget > 1000 & budget <= 1500:
        return 2
    if budget > 1500 & budget <= 2000:
        return 3
    if budget > 2000:
        return 4


def ram_cost_calculator(budget):
    if budget <= 1000:
        return 1
    if budget > 1000 & budget <= 1500:
        return 2
    if budget > 1500 & budget <= 2000:
        return 3
    if budget > 2000:
        return 4

