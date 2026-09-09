"""Matplotlib chart generation for employee data."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from pathlib import Path

import matplotlib
import numpy as np

# Allows reports to be generated on computers without a graphical display.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from employee import Employee


class EmployeeAnalytics:
    """Generate employee dashboard charts as PNG files."""

    def __init__(self, employees: Iterable[Employee], reports_directory: str | Path) -> None:
        self.employees = list(employees)
        self.reports_directory = Path(reports_directory)

    def generate_all_charts(self) -> list[Path]:
        """Create every dashboard chart and return the generated file paths."""
        self.reports_directory.mkdir(parents=True, exist_ok=True)
        return [
            self.salary_distribution_chart(),
            self.department_employee_count_chart(),
            self.city_distribution_chart(),
            self.performance_rating_analysis_chart(),
            self.experience_distribution_chart(),
        ]

    def salary_distribution_chart(self) -> Path:
        """Create a histogram of employee salaries."""
        salaries = np.asarray(self._numeric_values(employee.salary for employee in self.employees))
        figure, axis = plt.subplots(figsize=(9, 5))
        if salaries.size:
            axis.hist(salaries, bins=min(10, max(1, len(salaries))), color="#4C78A8", edgecolor="white")
            axis.set_xlabel("Salary")
            axis.set_ylabel("Employees")
        else:
            self._display_no_data(axis)
        axis.set_title("Salary Distribution")
        return self._save(figure, "salary_distribution.png")

    def department_employee_count_chart(self) -> Path:
        """Create a bar chart of employee counts by department."""
        counts = Counter(employee.department or "Unknown" for employee in self.employees)
        return self._categorical_bar_chart(
            counts, "Department Employee Count", "Department", "Employees", "department_employee_count.png"
        )

    def city_distribution_chart(self) -> Path:
        """Create a bar chart of employee counts by city."""
        counts = Counter(employee.city or "Unknown" for employee in self.employees)
        return self._categorical_bar_chart(
            counts, "City Distribution", "City", "Employees", "city_distribution.png"
        )

    def performance_rating_analysis_chart(self) -> Path:
        """Create a bar chart of employee counts by performance rating."""
        counts = Counter(employee.performance_rating or "Unknown" for employee in self.employees)
        return self._categorical_bar_chart(
            counts,
            "Performance Rating Analysis",
            "Performance Rating",
            "Employees",
            "performance_rating_analysis.png",
            numeric_labels=True,
        )

    def experience_distribution_chart(self) -> Path:
        """Create a histogram of employees' years of experience."""
        experience = np.asarray(self._numeric_values(employee.experience for employee in self.employees))
        figure, axis = plt.subplots(figsize=(9, 5))
        if experience.size:
            axis.hist(experience, bins=min(10, max(1, len(experience))), color="#59A14F", edgecolor="white")
            axis.set_xlabel("Years of Experience")
            axis.set_ylabel("Employees")
        else:
            self._display_no_data(axis)
        axis.set_title("Experience Distribution")
        return self._save(figure, "experience_distribution.png")

    def _categorical_bar_chart(
        self,
        counts: Counter[str],
        title: str,
        x_label: str,
        y_label: str,
        filename: str,
        *,
        numeric_labels: bool = False,
    ) -> Path:
        """Create and save a consistently styled categorical bar chart."""
        figure, axis = plt.subplots(figsize=(9, 5))
        if counts:
            labels = sorted(counts, key=self._label_sort_key if numeric_labels else str.casefold)
            values = [counts[label] for label in labels]
            axis.bar(labels, values, color="#F28E2B")
            axis.set_xlabel(x_label)
            axis.set_ylabel(y_label)
            axis.tick_params(axis="x", rotation=30)
        else:
            self._display_no_data(axis)
        axis.set_title(title)
        return self._save(figure, filename)

    def _save(self, figure: plt.Figure, filename: str) -> Path:
        """Save and close a Matplotlib figure."""
        output_path = self.reports_directory / filename
        figure.tight_layout()
        figure.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(figure)
        return output_path

    @staticmethod
    def _numeric_values(values: Iterable[str]) -> list[float]:
        """Return values that can be interpreted as numbers."""
        numbers: list[float] = []
        for value in values:
            try:
                numbers.append(float(str(value).replace(",", "").replace("INR", "").strip()))
            except (TypeError, ValueError):
                continue
        return numbers

    @staticmethod
    def _label_sort_key(label: str) -> tuple[int, float | str]:
        """Sort numeric rating labels before non-numeric labels."""
        try:
            return (0, float(label))
        except ValueError:
            return (1, label.casefold())

    @staticmethod
    def _display_no_data(axis: plt.Axes) -> None:
        """Display an informative chart when a metric contains no usable data."""
        axis.text(0.5, 0.5, "No data available", ha="center", va="center", transform=axis.transAxes)
        axis.set_xticks([])
        axis.set_yticks([])
