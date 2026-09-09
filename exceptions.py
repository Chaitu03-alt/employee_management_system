"""Domain-specific exceptions for the Employee Management System."""


class EmployeeManagementError(Exception):
    """Base class for user-facing application errors."""


class DataValidationError(EmployeeManagementError):
    """Raised when employee data or search criteria is invalid."""


class DataStorageError(EmployeeManagementError):
    """Raised when CSV data cannot be read or persisted."""


class ReportGenerationError(EmployeeManagementError):
    """Raised when a report or chart cannot be generated."""


class ModelTrainingError(EmployeeManagementError):
    """Raised when the salary prediction model cannot be trained."""
