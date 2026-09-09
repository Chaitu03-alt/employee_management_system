# Employee Management System

A production-minded, console-based Employee Management System built with Python, Pandas, NumPy, Matplotlib, OpenPyXL, and Scikit-learn.

## Folder structure

```text
employee_management_system/
|-- main.py                 # Console menu and application flow
|-- employee.py             # Employee domain model
|-- employee_manager.py     # CSV loading, CRUD, search, and save operations
|-- config.py               # Central paths, model, logging, and UI settings
|-- exceptions.py           # Domain-specific exception hierarchy
|-- logging_config.py       # Rotating UTF-8 application logger
|-- analytics.py            # Matplotlib employee dashboard chart generator
|-- excel_reports.py        # OpenPyXL Excel report generator
|-- salary_predictor.py     # Scikit-learn salary prediction module
|-- data_generator.py       # Faker-based 25,000-record CSV generator
|-- utils.py                # Input validation and menu display helpers
|-- requirements.txt        # Python dependencies
|-- tests/                  # Standard-library regression tests
|-- data/
    |-- employee_data.csv   # Application CSV storage, created automatically
    |-- employees.csv       # Optional sample CSV data
|-- Reports/                # Generated charts and Excel report workbook
|-- logs/                   # Rotating runtime logs, created automatically
```

## Run

From the `employee_management_system` directory:

```text
python main.py
```

Install all dependencies:

```text
pip install -r requirements.txt
```

## Employee fields

Each CSV record contains:

- Employee ID
- Name
- Department
- Salary
- Experience
- City
- Joining Date
- Performance Rating

## Operations

The console menu supports adding, updating, deleting, searching, and viewing all employees. Updates keep the current value when a field is left blank.

The application uses Python's built-in `csv` module to load and save `data/employee_data.csv`. If the file does not exist, it is created automatically.

## Portfolio features

- CRUD operations with CSV persistence and validation
- Basic and advanced Pandas filtering with salary and experience ranges
- Matplotlib analytics dashboard charts
- OpenPyXL Excel reporting workbook
- Scikit-learn Linear Regression salary prediction
- NumPy-based numeric processing for analytics and modeling
- Centralized configuration, rotating logs, custom exceptions, and regression tests

## Dashboard charts

Choose option `6` in the console menu to create the following PNG files in `Reports/`:

- Salary Distribution
- Department Employee Count
- City Distribution
- Performance Rating Analysis
- Experience Distribution

## Advanced search

Choose option `7` to filter employees with Pandas. Combine any of these optional filters: employee ID, name, department, city, inclusive salary range, and inclusive experience range. Text matching is case-insensitive and supports partial values.

## Excel reports

Choose option `8` to create `Reports/employee_reports.xlsx` with these worksheets:

- Employee Report
- Department Report
- Salary Report
- Performance Report

## Salary prediction

Choose option `9` to train a Linear Regression model using `Experience`, `Department`, and `Performance_Rating` to predict `Salary`. The console displays the R² accuracy score, MAE, RMSE, and ten test-set predictions. It also saves `salary_actual_vs_predicted.png` and `salary_prediction_residuals.png` in `Reports/`.

## Generate the large dataset

Generate the default 25,000 employee records with Faker:

```text
python data_generator.py
```

The generated `data/employee_data.csv` uses these columns: `Employee_ID`, `Name`, `Department`, `Salary`, `Experience`, `City`, `Joining_Date`, and `Performance_Rating`.

## Quality checks

Run the regression test suite from the project directory:

```text
python -m unittest discover -s tests
```

Runtime events and unexpected application failures are written to `logs/employee_management.log`.
