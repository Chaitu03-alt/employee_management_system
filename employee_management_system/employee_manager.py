"""CSV-backed employee collection management."""

from __future__ import annotations

import csv
import logging
from pathlib import Path

import pandas as pd

from employee import EMPLOYEE_FIELDS, Employee
from exceptions import DataStorageError, DataValidationError


LOGGER = logging.getLogger(__name__)


class EmployeeManager:
    """Load, query, and persist employees in a CSV file."""

    def __init__(self, csv_path: str | Path) -> None:
        self.csv_path = Path(csv_path)
        self._fieldnames: list[str] = EMPLOYEE_FIELDS.copy()
        self._employees: dict[int, Employee] = {}
        self.load()

    @property
    def employees(self) -> list[Employee]:
        """Return employees ordered by employee number."""
        return [self._employees[key] for key in sorted(self._employees)]

    @property
    def fieldnames(self) -> list[str]:
        """Return the CSV columns used by employee records."""
        return self._fieldnames.copy()

    def load(self) -> None:
        """Load all employees from the configured CSV file."""
        self._employees = {}
        if not self.csv_path.exists():
            self.save()
            return

        try:
            with self.csv_path.open("r", newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    employee = Employee.from_row(row)
                    if employee.employee_id in self._employees:
                        raise DataValidationError(f"Duplicate Employee ID found: {employee.employee_id}")
                    self._employees[employee.employee_id] = employee
        except (OSError, csv.Error) as error:
            raise DataStorageError(f"Could not load employee data: {error}") from error
        LOGGER.info("Loaded %s employees from %s", len(self._employees), self.csv_path)

    def get_by_id(self, employee_id: int) -> Employee | None:
        """Return an employee by ID, or None when it does not exist."""
        return self._employees.get(employee_id)

    def search(self, query: str) -> list[Employee]:
        """Find employees whose searchable fields contain the query."""
        query = query.strip().lower()
        return [
            employee
            for employee in self.employees
            if query in " ".join(
                [
                    str(employee.employee_id),
                    employee.name,
                    employee.department,
                    employee.city,
                ]
            ).lower()
        ]

    def advanced_search(
        self,
        *,
        employee_id: str | None = None,
        name: str | None = None,
        department: str | None = None,
        city: str | None = None,
        salary_min: float | None = None,
        salary_max: float | None = None,
        experience_min: float | None = None,
        experience_max: float | None = None,
    ) -> list[Employee]:
        """Filter CSV records with Pandas using the supplied search criteria.

        Text filters are case-insensitive partial matches. Numeric ranges are
        inclusive, so a salary of 500000 matches both a minimum and maximum
        value of 500000.
        """
        self._validate_range("Salary", salary_min, salary_max)
        self._validate_range("Experience", experience_min, experience_max)
        frame = self._read_search_frame()
        matches = pd.Series(True, index=frame.index)

        if employee_id:
            matches &= frame["Employee_ID"].eq(str(employee_id).strip())
        if name:
            matches &= frame["Name"].str.contains(name.strip(), case=False, regex=False, na=False)
        if department:
            matches &= frame["Department"].str.contains(
                department.strip(), case=False, regex=False, na=False
            )
        if city:
            matches &= frame["City"].str.contains(city.strip(), case=False, regex=False, na=False)

        salaries = pd.to_numeric(frame["Salary"], errors="coerce")
        experience = pd.to_numeric(frame["Experience"], errors="coerce")
        if salary_min is not None:
            matches &= salaries.ge(salary_min)
        if salary_max is not None:
            matches &= salaries.le(salary_max)
        if experience_min is not None:
            matches &= experience.ge(experience_min)
        if experience_max is not None:
            matches &= experience.le(experience_max)

        return [Employee.from_row(row) for row in frame.loc[matches].to_dict(orient="records")]

    def _read_search_frame(self) -> pd.DataFrame:
        """Load and normalize the CSV data for Pandas filtering."""
        frame = pd.read_csv(self.csv_path, dtype=str, keep_default_na=False)
        frame = frame.rename(
            columns={
                "Employee ID": "Employee_ID",
                "Joining Date": "Joining_Date",
                "Performance Rating": "Performance_Rating",
            }
        )
        missing_columns = set(EMPLOYEE_FIELDS) - set(frame.columns)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Employee CSV is missing required columns: {missing}")
        return frame

    @staticmethod
    def _validate_range(label: str, minimum: float | None, maximum: float | None) -> None:
        """Reject inverted numeric ranges before filtering."""
        if minimum is not None and maximum is not None and minimum > maximum:
            raise DataValidationError(f"{label} minimum cannot be greater than maximum")

    def add(self, employee: Employee) -> None:
        """Add an employee and persist the updated collection."""
        if employee.employee_id in self._employees:
            raise DataValidationError(f"Employee {employee.employee_id} already exists")
        self._employees[employee.employee_id] = employee
        self.save()
        LOGGER.info("Added employee %s", employee.employee_id)

    def update(self, employee: Employee) -> None:
        """Replace an existing employee and persist the change."""
        if employee.employee_id not in self._employees:
            raise DataValidationError(f"Employee {employee.employee_id} does not exist")
        self._employees[employee.employee_id] = employee
        self.save()
        LOGGER.info("Updated employee %s", employee.employee_id)

    def remove(self, employee_id: int) -> bool:
        """Remove an employee and return whether a record was deleted."""
        if employee_id not in self._employees:
            return False
        del self._employees[employee_id]
        self.save()
        LOGGER.info("Deleted employee %s", employee_id)
        return True

    def save(self) -> None:
        """Persist all employees using the canonical CSV columns."""
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self.csv_path.open("w", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self._fieldnames)
                writer.writeheader()
                writer.writerows(employee.to_row(self._fieldnames) for employee in self.employees)
        except (OSError, csv.Error) as error:
            raise DataStorageError(f"Could not save employee data: {error}") from error
