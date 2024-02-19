import datetime
import uuid


class PCBuild:

    def __init__(self):
        # Initialise None as parts defaults bar the build_id
        self.cpu = None
        self.gpu = None
        self.ram = None
        self.ssd = None
        self.hdd = None
        self.motherboard = None
        self.power_supply = None
        self.case = None
        self.build_id = str(uuid.uuid4())

        # Initialise prices as 0
        self.overall_price = 0
        self.cpu_price = 0
        self.gpu_price = 0
        self.ram_price = 0
        self.ssd_price = 0
        self.hdd_price = 0
        self.motherboard_price = 0
        self.power_supply_price = 0
        self.case_price = 0

    def set_cpu(self, cpu, price) -> None:
        self.cpu = cpu
        self.cpu_price = price
        # Recalculate overall price
        self.calculate_overall_price()

    def set_gpu(self, gpu, price) -> None:
        self.gpu = gpu
        self.gpu_price = price
        # Recalculate overall price
        self.calculate_overall_price()

    def set_ram(self, ram, price) -> None:
        self.ram = ram
        self.ram_price = price
        # Recalculate overall price
        self.calculate_overall_price()

    def set_ssd(self, ssd, price) -> None:
        self.ssd = ssd
        self.ssd_price = price
        # Recalculate overall price
        self.calculate_overall_price()

    def set_hdd(self, hdd, price) -> None:
        self.hdd = hdd
        self.hdd_price = price
        # Recalculate overall price
        self.calculate_overall_price()

    def set_motherboard(self, motherboard, price) -> None:
        self.motherboard = motherboard
        self.motherboard_price = price
        # Recalculate overall price
        self.calculate_overall_price()

    def set_power_supply(self, power_supply, price) -> None:
        self.power_supply = power_supply
        self.power_supply_price = price
        # Recalculate overall price
        self.calculate_overall_price()

    def set_case(self, case, price) -> None:
        self.case = case
        self.case_price = price
        # Recalculate overall price
        self.calculate_overall_price()

    def calculate_overall_price(self) -> None:
        self.overall_price = sum([
            self.cpu_price,
            self.gpu_price,
            self.ram_price,
            self.ssd_price,
            self.hdd_price,
            self.motherboard_price,
            self.power_supply_price,
            self.case_price
        ])

    def __repr__(self):
        representation = (
            f"PC Build Information : {self.build_id}\n"
            f"CPU: {self.cpu} - Price: £{self.cpu_price}\n"
            f"GPU: {self.gpu} - Price: £{self.gpu_price}\n"
            f"RAM: {self.ram} - Price: £{self.ram_price}\n"
        )

        # Since SSD and HDD are not required and may be one or another the print value will only show if not None
        if self.hdd is not None:
            representation += f"HDD: {self.hdd} - Price: £{self.hdd_price}\n"

        if self.ssd is not None:
            representation += f"SSD: {self.ssd} - Price: £{self.ssd_price}\n"

        representation += (
            f"Motherboard: {self.motherboard} - Price: £{self.motherboard_price}\n"
            f"Power Supply: {self.power_supply} - Price: £{self.power_supply_price}\n"
            f"Case: {self.case} - Price: £{self.case_price}\n"
            "-----------------------------------------------------------------\n"
            f"Overall Price: £{self.overall_price}"
        )

        return representation

    def display_info(self) -> None:
        print(f"PC Build Information : {self.build_id}")
        print(f"CPU: {self.cpu} - Price: £{self.cpu_price}")
        print(f"GPU: {self.gpu} - Price: £{self.gpu_price}")
        print(f"RAM: {self.ram} - Price: £{self.ram_price}")
        print(f"SSD: {self.ssd} - Price: £{self.ssd_price}")
        print(f"HDD: {self.hdd} - Price: £{self.hdd_price}")
        print(f"Motherboard: {self.motherboard} - Price: £{self.motherboard_price}")
        print(f"Power Supply: {self.power_supply} - Price: £{self.power_supply_price}")
        print(f"Case: {self.case} - Price: £{self.case_price}\n")
        print(f"Overall Price: £{self.overall_price}")

    """ 
    Allows the creation of a JSON object of the complete build
    Stores each component of the pc as a dictionary containing the part and its price
    Stores the overall price as its own singular non-dict value
    """
    @staticmethod
    def to_dict(pc_build, user_id: str) -> dict:
        return {
            "CPU": {"value": pc_build.cpu, "price": pc_build.cpu_price},
            "GPU": {"value": pc_build.gpu, "price": pc_build.gpu_price},
            "RAM": {"value": pc_build.ram, "price": pc_build.ram_price},
            "SSD": {"value": pc_build.ssd, "price": pc_build.ssd_price},
            "HDD": {"value": pc_build.hdd, "price": pc_build.hdd_price},
            "Motherboard": {"value": pc_build.motherboard, "price": pc_build.motherboard_price},
            "PowerSupply": {"value": pc_build.power_supply, "price": pc_build.power_supply_price},
            "Case": {"value": pc_build.case, "price": pc_build.case_price},
            "OverallPrice": pc_build.overall_price,
            "build_id": pc_build.build_id,
            "user_id": user_id,
            "created_at": datetime.datetime.now()
        }
