import unittest
from unittest.mock import patch

import pandas as pd
from pc_builder_backend.excel_methods.excel_helper_methods import allocate_budget, fetch_valid_parts, read_excel_data, \
    get_component_info


class TestExcelHelperMethods(unittest.TestCase):

    def test_read_excel_data(self):
        """
        Test the read_excel_data function to ensure it correctly reads data from an Excel file.
        """
        # Prepare test data
        test_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        # Mock the pandas.read_excel function using patch
        with patch('pandas.read_excel') as mock_read_excel:
            # Set the return value of the mocked function to the test data
            mock_read_excel.return_value = test_data
            # Call the read_excel_data function with a dummy file path
            result = read_excel_data('test_file.xlsx')
            # Assert that the result is equal to the expected test data
            self.assertTrue(result.equals(test_data))

    def test_fetch_valid_parts_valid_input(self):
        """
        Test the fetch_valid_parts function with valid input parameters.
        """
        test_data = pd.DataFrame({'Type': ['CPU', 'GPU', 'RAM'], 'Name': ['Intel i5', 'NVIDIA GTX 1080', 'Corsair 16GB'], 'Price': [200, 400, 100]})
        result = fetch_valid_parts('CPU', test_data, 200)
        expected = pd.DataFrame({'Type': ['CPU'], 'Name': ['Intel i5'], 'Price': [200]})
        # Assert that the result matches the expected DataFrame
        self.assertTrue(result.equals(expected))

    def test_fetch_valid_parts_invalid_input(self):
        """
        Test the fetch_valid_parts function with invalid input parameters to ensure it raises the correct exceptions.
        """
        test_data = pd.DataFrame({'Type': ['CPU', 'GPU', 'RAM'], 'Name': ['Intel i5', 'NVIDIA GTX 1080', 'Corsair 16GB'], 'Price': [200, 400, 100]})
        # Assert that a ValueError is raised when part_name is not a string
        with self.assertRaises(ValueError):
            fetch_valid_parts(123, test_data, 200)
        # Assert that a ValueError is raised when parts_dataframe is not a pandas DataFrame
        with self.assertRaises(ValueError):
            fetch_valid_parts('CPU', 'not a dataframe', 200)
        # Assert that a ValueError is raised when target_price is not a numeric value
        with self.assertRaises(ValueError):
            fetch_valid_parts('CPU', test_data, 'not a number')

    def test_allocate_budget_valid_input(self):
        """
        Test the allocate_budget function with a valid input budget.
        """
        result = allocate_budget(750)
        expected = {'CPU': 0.15, 'GPU': 0.30, 'RAM': 0.20, 'Storage': 0.15, 'Motherboard': 0.10, 'Power Supply': 0.05, 'Case': 0.05}
        # Assert that the result matches the expected dictionary of part ratios
        self.assertEqual(result, expected)

    def test_allocate_budget_invalid_input(self):
        """
        Test the allocate_budget function with an invalid input budget to ensure it raises the correct exception.
        """
        # Assert that a ValueError is raised when the budget is out of range
        with self.assertRaises(ValueError):
            allocate_budget(2500)

    def test_get_component_info(self):
        """
        Test the get_component_info function to ensure it correctly retrieves the name and price of a component from a DataFrame.
        """
        test_data = pd.DataFrame({'Name': ['Intel i5', 'NVIDIA GTX 1080', 'Corsair 16GB'], 'Price': [200, 400, 100]})
        # Mock the pandas.DataFrame.sample method using patch
        with patch('pandas.DataFrame.sample') as mock_sample:
            # Set the return value of the mocked method to the first row of the test data
            mock_sample.return_value = test_data.iloc[[0]]
            name, price = get_component_info(test_data)
            # Assert that the retrieved name and price match the expected values
            self.assertEqual(name, 'Intel i5')
            self.assertEqual(price, 200)


if __name__ == '__main__':
    unittest.main()
