import datetime
import uuid


class PCBuild:

    def __init__(self):
        """
        Initializes a Build object with default values and a unique build ID.
        """
        # Initialise None as parts defaults bar the build_id
        self.cpu = None
        self.gpu = None
        self.ram = None
        self.storage = None
        self.motherboard = None
        self.power_supply = None
        self.case = None
        self.build_id = str(uuid.uuid4())

        # Initialise prices as 0
        self.overall_price: float = 0
        self.cpu_price = 0
        self.gpu_price = 0
        self.ram_price = 0
        self.storage_price = 0
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

    def set_storage(self, storage, price) -> None:
        self.storage = storage
        self.storage_price = price
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
            self.storage_price,
            self.motherboard_price,
            self.power_supply_price,
            self.case_price
        ])

    def __repr__(self):
        """
        Returns a string representation of the PC Build information.

        :return: String representation of the PC Build.
        """
        representation = (
            f"PC Build Information : {self.build_id}\n"
            f"CPU: {self.cpu} - Price: £{self.cpu_price}\n"
            f"GPU: {self.gpu} - Price: £{self.gpu_price}\n"
            f"RAM: {self.ram} - Price: £{self.ram_price}\n"
            f"Storage: {self.storage} - Price: £{self.storage_price}\n"
            f"Motherboard: {self.motherboard} - Price: £{self.motherboard_price}\n"
            f"Power Supply: {self.power_supply} - Price: £{self.power_supply_price}\n"
            f"Case: {self.case} - Price: £{self.case_price}\n"
            "-----------------------------------------------------------------\n"
            f"Overall Price: £{self.overall_price:.2f}\n"  # Rounds to 2 decimal places
        )

        return representation

    def display_info(self) -> None:
        """
        Displays PC Build information.

        :return: None
        """
        print(f"PC Build Information : {self.build_id}")
        print(f"CPU: {self.cpu} - Price: £{self.cpu_price}")
        print(f"GPU: {self.gpu} - Price: £{self.gpu_price}")
        print(f"RAM: {self.ram} - Price: £{self.ram_price}")
        print(f"Storage: {self.storage} - Price: £{self.storage_price}")
        print(f"Motherboard: {self.motherboard} - Price: £{self.motherboard_price}")
        print(f"Power Supply: {self.power_supply} - Price: £{self.power_supply_price}")
        print(f"Case: {self.case} - Price: £{self.case_price}\n")
        f"Overall Price: £{self.overall_price:.2f}\n"  # Rounds to 2 decimal places

    def is_valid(self):
        """
        Checks if the PC Build is valid (all components are present and prices are positive).

        :return: True if the PC Build is valid, False otherwise.
        """
        attributes = ['cpu', 'gpu', 'ram', 'storage', 'motherboard', 'power_supply', 'case']
        prices = ['cpu_price', 'gpu_price', 'ram_price', 'storage_price', 'motherboard_price', 'power_supply_price', 'case_price']

        for attr, price_attr in zip(attributes, prices):
            if getattr(self, attr) is None:
                return False
            if getattr(self, price_attr) <= 0:
                return False

        return True

    def to_dict(self, user_id: str) -> dict:
        """
        Converts the PC Build object to a dictionary.

        :param user_id: ID of the user associated with the build.
        :return: Dictionary representation of the PC Build object.
        """
        return {
            "CPU": {"value": self.cpu, "price": self.cpu_price},
            "GPU": {"value": self.gpu, "price": self.gpu_price},
            "RAM": {"value": self.ram, "price": self.ram_price},
            "Storage": {"value": self.storage, "price": self.storage_price},
            "Motherboard": {"value": self.motherboard, "price": self.motherboard_price},
            "PowerSupply": {"value": self.power_supply, "price": self.power_supply_price},
            "Case": {"value": self.case, "price": self.case_price},
            "OverallPrice": self.overall_price,
            "build_id": self.build_id,
            "user_id": user_id,
            "created_at": datetime.datetime.now()
        }
