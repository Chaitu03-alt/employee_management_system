"""Employee domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


EMPLOYEE_FIELDS = [
    "Employee_ID",
    "Name",
    "Department",
    "Salary",
    "Experience",
    "City",
    "Joining_Date",
    "Performance_Rating",
]


@dataclass
class Employee:
    """Represent one employee record."""

    employee_id: int
    name: str
    department: str
    salary: str
    experience: str
    city: str
    joining_date: str
    performance_rating: str

    @classmethod
    def from_row(cls, row: Mapping[str, str]) -> "Employee":
        """Create an employee from a CSV row."""
        employee_id = row.get("Employee_ID", row.get("Employee ID", row.get("EmployeeNumber", "")))
        if not str(employee_id).strip():
            raise ValueError("Employee ID is required")

        try:
            employee_number = int(employee_id)
        except (TypeError, ValueError) as error:
            raise ValueError("Employee ID must be a whole number") from error
        if employee_number <= 0:
            raise ValueError("Employee ID must be greater than zero")
        return cls(
            employee_id=employee_number,
            name=(row.get("Name") or f"Employee {employee_number}").strip(),
            department=(row.get("Department") or "Unknown").strip(),
            salary=(row.get("Salary") or row.get("MonthlyIncome") or "Unknown").strip(),
            experience=(row.get("Experience") or row.get("TotalWorkingYears") or "Unknown").strip(),
            city=(row.get("City") or "Unknown").strip(),
            joining_date=(row.get("Joining_Date") or row.get("Joining Date") or "Unknown").strip(),
            performance_rating=(
                row.get("Performance_Rating")
                or row.get("Performance Rating")
                or row.get("PerformanceRating")
                or "Unknown"
            ).strip(),
        )

    def to_row(self, fieldnames: list[str]) -> dict[str, str]:
        """Return this employee in the CSV column order."""
        values = {
            "Employee_ID": str(self.employee_id),
            "Name": self.name,
            "Department": self.department,
            "Salary": self.salary,
            "Experience": self.experience,
            "City": self.city,
            "Joining_Date": self.joining_date,
            "Performance_Rating": self.performance_rating,
        }
        return {field: values.get(field, "") for field in fieldnames}

    def summary(self) -> str:
        """Return a concise display string for console output."""
        return (
            f"#{self.employee_id} | {self.name} | {self.department} | "
            f"Salary: {self.salary} | Experience: {self.experience} | "
            f"City: {self.city} | Rating: {self.performance_rating}"
        )
