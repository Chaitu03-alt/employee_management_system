"""Generate a realistic Faker-based employee dataset."""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

from employee import EMPLOYEE_FIELDS


DEPARTMENTS = ("IT", "HR", "Sales", "Finance", "Marketing", "Operations")
CITIES = (
    "Bengaluru",
    "Chennai",
    "Delhi",
    "Hyderabad",
    "Kolkata",
    "Mumbai",
    "Pune",
)
DEPARTMENT_SALARY_BASES = {
    "IT": 550_000,
    "HR": 400_000,
    "Sales": 420_000,
    "Finance": 500_000,
    "Marketing": 450_000,
    "Operations": 380_000,
}


def create_employee_record(employee_id: int, faker: Faker, randomizer: random.Random) -> dict[str, str | int]:
    """Create one realistic employee record."""
    department = randomizer.choice(DEPARTMENTS)
    joining_date = _random_joining_date(randomizer)
    maximum_experience = min(25, max(0, (date.today() - joining_date).days // 365))
    experience = randomizer.randint(0, maximum_experience)
    salary = _calculate_salary(department, experience, randomizer)

    return {
        "Employee_ID": employee_id,
        "Name": faker.name(),
        "Department": department,
        "Salary": salary,
        "Experience": experience,
        "City": randomizer.choice(CITIES),
        "Joining_Date": joining_date.isoformat(),
        "Performance_Rating": randomizer.choices((1, 2, 3, 4, 5), weights=(5, 15, 40, 30, 10), k=1)[0],
    }


def generate_employee_dataset(output_path: str | Path, record_count: int = 25_000, seed: int = 42) -> Path:
    """Write ``record_count`` employee records to a CSV file and return its path."""
    if record_count <= 0:
        raise ValueError("record_count must be greater than zero")

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    faker = Faker("en_IN")
    faker.seed_instance(seed)
    randomizer = random.Random(seed)

    with destination.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=EMPLOYEE_FIELDS)
        writer.writeheader()
        for employee_id in range(1, record_count + 1):
            writer.writerow(create_employee_record(employee_id, faker, randomizer))

    return destination


def _random_joining_date(randomizer: random.Random) -> date:
    """Return a joining date from the last 25 years through today."""
    earliest_date = date.today() - timedelta(days=25 * 365)
    span = (date.today() - earliest_date).days
    return earliest_date + timedelta(days=randomizer.randint(0, span))


def _calculate_salary(department: str, experience: int, randomizer: random.Random) -> int:
    """Calculate an annual INR salary using department and experience."""
    base_salary = DEPARTMENT_SALARY_BASES[department]
    experience_component = experience * randomizer.randint(45_000, 70_000)
    variation = randomizer.randint(-50_000, 150_000)
    return max(250_000, base_salary + experience_component + variation)


def parse_arguments() -> argparse.Namespace:
    """Read optional command-line generation settings."""
    parser = argparse.ArgumentParser(description="Generate a realistic employee CSV dataset.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent / "data" / "employee_data.csv",
        help="CSV destination (default: data/employee_data.csv)",
    )
    parser.add_argument("--count", type=int, default=25_000, help="Number of records (default: 25000)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for repeatable data")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    generated_file = generate_employee_dataset(arguments.output, arguments.count, arguments.seed)
    print(f"Generated {arguments.count:,} employee records in {generated_file}")
