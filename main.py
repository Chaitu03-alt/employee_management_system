"""Console entry point for the Employee Management System."""

import logging

from analytics import EmployeeAnalytics
from config import DATA_FILE, DISPLAY_LIMIT, REPORTS_DIRECTORY
from employee import Employee
from employee_manager import EmployeeManager
from excel_reports import ExcelReportGenerator
from exceptions import EmployeeManagementError
from logging_config import configure_logging
from salary_predictor import SalaryPredictor
from utils import (
    print_menu,
    prompt_advanced_search_filters,
    prompt_employee_fields,
    prompt_int,
    prompt_text,
)

LOGGER = logging.getLogger(__name__)


def add_employee(manager: EmployeeManager) -> None:
    """Collect and add a new employee."""
    employee_id = prompt_int("Employee ID: ")
    data = {"Employee_ID": str(employee_id), **prompt_employee_fields()}
    manager.add(Employee.from_row(data))
    LOGGER.info("Employee added: id=%s", employee_id)
    print("Employee added.")


def update_employee(manager: EmployeeManager) -> None:
    """Update an existing employee using blank input to retain values."""
    employee_id = prompt_int("Employee ID: ")
    employee = manager.get_by_id(employee_id)
    if employee is None:
        print("Employee not found.")
        return
    current = employee.to_row(manager.fieldnames)
    updated = {"Employee_ID": str(employee_id), **prompt_employee_fields(current)}
    manager.update(Employee.from_row(updated))
    LOGGER.info("Employee updated: id=%s", employee_id)
    print("Employee updated.")


def advanced_search(manager: EmployeeManager) -> None:
    """Collect advanced filters and display matching employee records."""
    filters = prompt_advanced_search_filters()
    if not any(value is not None and value != "" for value in filters.values()):
        print("Enter at least one search filter.")
        return

    results = manager.advanced_search(**filters)
    if not results:
        print("No employees found.")
        return

    display_employees(results, "advanced search")


def display_employees(employees: list[Employee], source: str) -> None:
    """Display a concise employee-result preview without flooding the console."""
    print(f"Found {len(employees):,} employee(s) from {source}.")
    for employee in employees[:DISPLAY_LIMIT]:
        print(employee.summary())
    if len(employees) > DISPLAY_LIMIT:
        print(f"Showing the first {DISPLAY_LIMIT} results. Refine your search to narrow the list.")


def generate_excel_reports(manager: EmployeeManager) -> None:
    """Generate the employee Excel reporting workbook."""
    report_path = ExcelReportGenerator(manager.employees, REPORTS_DIRECTORY).generate()
    LOGGER.info("Excel reports generated: %s", report_path)
    print(f"Excel reports saved to: {report_path}")


def run_salary_prediction() -> None:
    """Train the salary model and show its test-set evaluation."""
    predictor = SalaryPredictor(DATA_FILE, REPORTS_DIRECTORY)
    result = predictor.train()
    graph_paths = predictor.generate_graphs()
    LOGGER.info("Salary model trained with R2=%.4f", result.r2)
    print("\nSalary Prediction Model Results")
    print(f"Accuracy (R2 score): {result.r2:.2%}")
    print(f"Mean absolute error: INR {result.mean_absolute_error:,.2f}")
    print(f"Root mean squared error: INR {result.root_mean_squared_error:,.2f}")
    print("\nSample predictions:")
    print(result.predictions.head(10).round(2).to_string(index=False))
    print("\nGraphs saved to:")
    for graph_path in graph_paths:
        print(f"- {graph_path}")


def run() -> None:
    """Run the interactive application loop."""
    configure_logging()
    try:
        manager = EmployeeManager(DATA_FILE)
    except EmployeeManagementError as error:
        LOGGER.exception("Application startup failed")
        print(f"Unable to start application: {error}")
        return

    while True:
        try:
            print_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                add_employee(manager)
            elif choice == "2":
                update_employee(manager)
            elif choice == "3":
                employee_id = prompt_int("Employee ID: ")
                print("Employee deleted." if manager.remove(employee_id) else "Employee not found.")
            elif choice == "4":
                query = prompt_text("Search by ID, name, department, or city: ")
                if not query:
                    print("Enter a search term.")
                else:
                    results = manager.search(query)
                    if results:
                        display_employees(results, "basic search")
                    else:
                        print("No employees found.")
            elif choice == "5":
                display_employees(manager.employees, "all employees")
            elif choice == "6":
                chart_paths = EmployeeAnalytics(manager.employees, REPORTS_DIRECTORY).generate_all_charts()
                print("Charts saved to:")
                for chart_path in chart_paths:
                    print(f"- {chart_path}")
            elif choice == "7":
                advanced_search(manager)
            elif choice == "8":
                generate_excel_reports(manager)
            elif choice == "9":
                run_salary_prediction()
            elif choice == "0":
                LOGGER.info("Application closed by user")
                print("Goodbye.")
                break
            else:
                print("Invalid option.")
        except EmployeeManagementError as error:
            LOGGER.warning("Application operation failed: %s", error)
            print(f"Operation failed: {error}")
        except (ValueError, TypeError) as error:
            LOGGER.warning("Invalid user input: %s", error)
            print(f"Invalid input: {error}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")


if __name__ == "__main__":
    run()
