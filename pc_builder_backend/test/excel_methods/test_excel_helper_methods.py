import unittest
from pc_builder_backend.excel_methods.excel_helper_methods import allocate_budget


class TestExcelHelperMethods(unittest.TestCase):

    def test_part_price_allocation_500(self):
        pc_price = 500
        budget_dict = allocate_budget(pc_price)
        cpu_price = pc_price * budget_dict['CPU']
        self.assertEqual(int(cpu_price), 75)

    def test_part_price_allocation_1000(self):
        pc_price = 1000
        budget_dict = allocate_budget(pc_price)
        cpu_price = pc_price * budget_dict['CPU']
        self.assertEqual(int(cpu_price), 150)


if __name__ == '__main__':
    unittest.main()