# Employee Management System

Console-based employee management system with CSV persistence, Pandas-driven analytics, and a scikit-learn salary prediction model.

## Problem Statement

A CSV file is a common, low-friction way small teams store employee records — and a common source of bugs when read/write logic, validation, and reporting all live inline in one script. 

This project treats the CSV as a real data store: CRUD operations go through a dedicated manager layer with validation and typed errors. On top of that base, it provides Pandas-based advanced search, Matplotlib analytics dashboards, multi-sheet Excel workbooks, and a trained salary prediction model.

## Architecture

```text
main.py (console menu)
   │
   ├─► employee_manager.py ──► employee.py (Employee dataclass)
   │        │                       │
   │        │                       └─ validation on construction (from_row)
   │        │
   │        └─► data/employee_data.csv   (persistence layer)
   │
   ├─► analytics.py ──────────► Reports/*.png   (Matplotlib dashboards)
   │
   ├─► excel_reports.py ──────► Reports/employee_reports.xlsx (OpenPyXL, 4 sheets)
   │
   └─► salary_predictor.py ───► sklearn Pipeline: ColumnTransformer(OneHotEncoder)
                                  → LinearRegression → R² / MAE / RMSE + residual plots

Cross-cutting:
   exceptions.py     — typed error hierarchy (DataValidationError, DataStorageError, etc.)
   logging_config.py — rotating file logger, all modules log through it
   config.py         — single source of truth for paths, model settings, display limits