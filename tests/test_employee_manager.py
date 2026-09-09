"""Regression tests for core employee CRUD and Pandas search behavior."""

import tempfile
import unittest
from pathlib import Path

from employee import Employee
from employee_manager import EmployeeManager


class EmployeeManagerTests(unittest.TestCase):
    """Validate persistence and advanced filtering in an isolated CSV file."""

    def test_crud_and_advanced_search(self) -> None:
        """Add, query, update, and delete an employee record."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "employees.csv"
            manager = EmployeeManager(csv_path)
            employee = Employee(1, "Asha Rao", "IT", "850000", "5", "Pune", "2022-01-10", "4")

            manager.add(employee)
            results = manager.advanced_search(department="it", salary_min=800000, salary_max=900000)
            self.assertEqual([item.employee_id for item in results], [1])

            manager.update(Employee(1, "Asha Rao", "IT", "900000", "6", "Pune", "2022-01-10", "5"))
            self.assertEqual(manager.get_by_id(1).salary, "900000")
            self.assertTrue(manager.remove(1))


if __name__ == "__main__":
    unittest.main()
