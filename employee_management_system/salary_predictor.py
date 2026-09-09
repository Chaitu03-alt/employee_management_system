"""Scikit-learn Linear Regression model for employee salary prediction."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from config import MODEL_RANDOM_STATE, MODEL_TEST_SIZE
from exceptions import ModelTrainingError

matplotlib.use("Agg")
import matplotlib.pyplot as plt


FEATURE_COLUMNS = ["Experience", "Department", "Performance_Rating"]
TARGET_COLUMN = "Salary"
LOGGER = logging.getLogger(__name__)


@dataclass
class SalaryPredictionResult:
    """Store model evaluation metrics and test-set predictions."""

    r2: float
    mean_absolute_error: float
    root_mean_squared_error: float
    predictions: pd.DataFrame


class SalaryPredictor:
    """Train, evaluate, and visualize a salary prediction model."""

    def __init__(self, csv_path: str | Path, reports_directory: str | Path) -> None:
        self.csv_path = Path(csv_path)
        self.reports_directory = Path(reports_directory)
        self.model: Pipeline | None = None
        self.result: SalaryPredictionResult | None = None

    def train(self) -> SalaryPredictionResult:
        """Train Linear Regression and evaluate it with a held-out test set."""
        data = pd.read_csv(self.csv_path)
        self._validate_columns(data)
        data = data[FEATURE_COLUMNS + [TARGET_COLUMN]].copy()
        data["Experience"] = pd.to_numeric(data["Experience"], errors="coerce")
        data["Performance_Rating"] = pd.to_numeric(data["Performance_Rating"], errors="coerce")
        data[TARGET_COLUMN] = pd.to_numeric(data[TARGET_COLUMN], errors="coerce")
        data["Department"] = data["Department"].fillna("Unknown").astype(str)
        data = data.dropna(subset=["Experience", "Performance_Rating", TARGET_COLUMN])
        if len(data) < 10:
            raise ModelTrainingError("At least 10 valid employee records are required to train the model")

        features = data[FEATURE_COLUMNS]
        target = data[TARGET_COLUMN]
        features_train, features_test, target_train, target_test = train_test_split(
            features, target, test_size=MODEL_TEST_SIZE, random_state=MODEL_RANDOM_STATE
        )
        self.model = Pipeline(
            steps=[
                (
                    "preprocessor",
                    ColumnTransformer(
                        transformers=[
                            ("department", OneHotEncoder(handle_unknown="ignore"), ["Department"]),
                            ("numeric", "passthrough", ["Experience", "Performance_Rating"]),
                        ]
                    ),
                ),
                ("regressor", LinearRegression()),
            ]
        )
        self.model.fit(features_train, target_train)
        predicted_salary = np.asarray(self.model.predict(features_test))

        predictions = features_test.reset_index(drop=True).copy()
        predictions["Actual Salary"] = target_test.reset_index(drop=True)
        predictions["Predicted Salary"] = predicted_salary
        self.result = SalaryPredictionResult(
            r2=r2_score(target_test, predicted_salary),
            mean_absolute_error=mean_absolute_error(target_test, predicted_salary),
            root_mean_squared_error=root_mean_squared_error(target_test, predicted_salary),
            predictions=predictions,
        )
        LOGGER.info("Salary model trained with %s valid records; R2=%.4f", len(data), self.result.r2)
        return self.result

    def predict_salary(self, experience: float, department: str, performance_rating: float) -> float:
        """Predict one employee's salary after calling :meth:`train`."""
        if self.model is None:
            raise RuntimeError("Train the salary model before requesting a prediction")
        record = pd.DataFrame(
            [
                {
                    "Experience": experience,
                    "Department": department,
                    "Performance_Rating": performance_rating,
                }
            ]
        )
        return float(self.model.predict(record)[0])

    def generate_graphs(self) -> list[Path]:
        """Save actual-vs-predicted and residual-distribution charts."""
        if self.result is None:
            raise RuntimeError("Train the salary model before generating graphs")

        self.reports_directory.mkdir(parents=True, exist_ok=True)
        predictions = self.result.predictions
        actual = predictions["Actual Salary"]
        predicted = predictions["Predicted Salary"]
        residuals = np.subtract(actual.to_numpy(), predicted.to_numpy())

        scatter_path = self.reports_directory / "salary_actual_vs_predicted.png"
        figure, axis = plt.subplots(figsize=(8, 6))
        axis.scatter(actual, predicted, alpha=0.45, color="#4C78A8", edgecolors="none")
        lower_bound = min(actual.min(), predicted.min())
        upper_bound = max(actual.max(), predicted.max())
        axis.plot([lower_bound, upper_bound], [lower_bound, upper_bound], "r--", label="Perfect prediction")
        axis.set_title("Actual vs Predicted Salary")
        axis.set_xlabel("Actual Salary")
        axis.set_ylabel("Predicted Salary")
        axis.legend()
        figure.tight_layout()
        figure.savefig(scatter_path, dpi=150)
        plt.close(figure)

        residual_path = self.reports_directory / "salary_prediction_residuals.png"
        figure, axis = plt.subplots(figsize=(8, 6))
        axis.hist(residuals, bins=30, color="#59A14F", edgecolor="white")
        axis.axvline(0, color="red", linestyle="--", label="Zero error")
        axis.set_title("Salary Prediction Residual Distribution")
        axis.set_xlabel("Actual Salary - Predicted Salary")
        axis.set_ylabel("Employee Count")
        axis.legend()
        figure.tight_layout()
        figure.savefig(residual_path, dpi=150)
        plt.close(figure)

        return [scatter_path, residual_path]

    @staticmethod
    def _validate_columns(data: pd.DataFrame) -> None:
        """Ensure the source dataset contains the required model columns."""
        required_columns = set(FEATURE_COLUMNS + [TARGET_COLUMN])
        missing_columns = required_columns - set(data.columns)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ModelTrainingError(f"Employee CSV is missing required model columns: {missing}")
