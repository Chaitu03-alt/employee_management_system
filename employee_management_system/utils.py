"""Small input and display helpers for the console application."""


def prompt_int(message: str) -> int:
    """Prompt repeatedly until the user enters an integer."""
    while True:
        try:
            return int(input(message).strip())
        except ValueError:
            print("Please enter a valid number.")


def prompt_text(message: str, default: str = "") -> str:
    """Read text input, optionally returning a default for blank input."""
    value = input(message).strip()
    return value or default


def prompt_optional_number(message: str) -> float | None:
    """Prompt for an optional numeric value; blank input returns ``None``."""
    while True:
        value = input(message).strip()
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number or leave it blank.")


def prompt_number_range(label: str) -> tuple[float | None, float | None]:
    """Prompt for optional inclusive minimum and maximum values."""
    minimum = prompt_optional_number(f"Minimum {label} [optional]: ")
    maximum = prompt_optional_number(f"Maximum {label} [optional]: ")
    return minimum, maximum


def prompt_advanced_search_filters() -> dict[str, str | float | None]:
    """Collect optional advanced-search filters from the console."""
    print("Leave a field blank to ignore that filter.")
    employee_id = prompt_text("Employee ID [optional]: ")
    name = prompt_text("Name [optional]: ")
    department = prompt_text("Department [optional]: ")
    city = prompt_text("City [optional]: ")
    salary_min, salary_max = prompt_number_range("salary")
    experience_min, experience_max = prompt_number_range("experience")
    return {
        "employee_id": employee_id,
        "name": name,
        "department": department,
        "city": city,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "experience_min": experience_min,
        "experience_max": experience_max,
    }


def prompt_employee_fields(existing: dict[str, str] | None = None) -> dict[str, str]:
    """Prompt for employee fields, using existing values for updates."""
    existing = existing or {}
    return {
        "Name": prompt_text(f"Name [{existing.get('Name', '')}]: ", existing.get("Name", "")),
        "Department": prompt_text(
            f"Department [{existing.get('Department', '')}]: ", existing.get("Department", "")
        ),
        "Salary": prompt_text(f"Salary [{existing.get('Salary', '')}]: ", existing.get("Salary", "")),
        "Experience": prompt_text(
            f"Experience [{existing.get('Experience', '')}]: ", existing.get("Experience", "")
        ),
        "City": prompt_text(f"City [{existing.get('City', '')}]: ", existing.get("City", "")),
        "Joining_Date": prompt_text(
            f"Joining date [{existing.get('Joining_Date', '')}]: ", existing.get("Joining_Date", "")
        ),
        "Performance_Rating": prompt_text(
            f"Performance rating [{existing.get('Performance_Rating', '')}]: ",
            existing.get("Performance_Rating", ""),
        ),
    }


def print_menu() -> None:
    """Display the available application actions."""
    print("\nEmployee Management System")
    print("1. Add employee")
    print("2. Update employee")
    print("3. Delete employee")
    print("4. Search employee")
    print("5. View all employees")
    print("6. Generate dashboard charts")
    print("7. Advanced search")
    print("8. Generate Excel reports")
    print("9. Train salary prediction model")
    print("0. Exit")
