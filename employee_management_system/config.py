"""Central application configuration."""

from pathlib import Path


BASE_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = BASE_DIRECTORY / "data"
DATA_FILE = DATA_DIRECTORY / "employee_data.csv"
REPORTS_DIRECTORY = BASE_DIRECTORY / "Reports"
LOG_DIRECTORY = BASE_DIRECTORY / "logs"
LOG_FILE = LOG_DIRECTORY / "employee_management.log"

DISPLAY_LIMIT = 50
CSV_ENCODING = "utf-8"
MODEL_RANDOM_STATE = 42
MODEL_TEST_SIZE = 0.20
LOG_MAX_BYTES = 1_000_000
LOG_BACKUP_COUNT = 3
