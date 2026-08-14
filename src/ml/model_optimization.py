"""
=========================================================
MODEL OPTIMIZATION
AI-Powered Job Posting Analyzer
=========================================================
"""
import joblib
from pathlib import Path
import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    GridSearchCV
)

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler
)

from sklearn.feature_selection import VarianceThreshold

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

from src.normalization.config import PROJECT_ROOT


# --------------------------------------------------------
# File Paths
# --------------------------------------------------------

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "final_ml_dataset_v2.csv"
)
MODEL_FOLDER = (
    PROJECT_ROOT
    / "models"
)

MODEL_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


class ModelOptimization:

    # --------------------------------------------------------
    # Initialize
    # --------------------------------------------------------

    def __init__(self):

        print("=" * 60)
        print("MODEL OPTIMIZATION")
        print("=" * 60)

        self.df = pd.read_csv(INPUT_FILE)

        print(f"Rows Loaded : {len(self.df):,}")

    # --------------------------------------------------------
    # Prepare Dataset
    # --------------------------------------------------------

    def prepare_data(self):

        print()
        print("=" * 60)
        print("PREPARING DATA")
        print("=" * 60)

        target_column = "standard_title"

        drop_columns = [

            "job_id",
            "company_name",
            "title",
            "location",
            "experience",
            "education",
            "work_type",

            target_column

        ]

        X = self.df.drop(
            columns=drop_columns,
            errors="ignore"
        )

        y = self.df[target_column]

        object_columns = X.select_dtypes(
            include=["object"]
        ).columns.tolist()

        for column in object_columns:

            encoder = LabelEncoder()

            X[column] = encoder.fit_transform(
                X[column].fillna("").astype(str)
            )

        # --------------------------------------------------------
        # Feature Selection (keeps this in sync with train_models_v2.py)
        # --------------------------------------------------------

        print()
        print("=" * 60)
        print("FEATURE SELECTION")
        print("=" * 60)

        original_feature_count = X.shape[1]

        selector = VarianceThreshold(
            threshold=0.02
        )

        X_selected = selector.fit_transform(X)

        selected_columns = X.columns[
            selector.get_support()
        ]

        X = pd.DataFrame(
            X_selected,
            columns=selected_columns
        )

        self.feature_columns = list(selected_columns)

        print(f"Original Features : {original_feature_count}")
        print(f"Selected Features : {len(selected_columns)}")
        print(
            f"Removed Features  : "
            f"{original_feature_count - len(selected_columns)}"
        )

        self.label_encoder = LabelEncoder()

        y = self.label_encoder.fit_transform(y)

        (
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test

        ) = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=42,

            stratify=y

        )

        self.scaler = StandardScaler()

        self.X_train = self.scaler.fit_transform(
            self.X_train
        )

        self.X_test = self.scaler.transform(
            self.X_test
        )

        print(f"Training Rows : {len(self.X_train)}")
        print(f"Testing Rows  : {len(self.X_test)}")
        print(f"Features      : {X.shape[1]}")
        print(f"Classes       : {len(self.label_encoder.classes_)}")

    # --------------------------------------------------------
    # Random Forest Baseline
    # --------------------------------------------------------

    def baseline_random_forest(self):

        print()
        print("=" * 60)
        print("RANDOM FOREST BASELINE")
        print("=" * 60)

        model = RandomForestClassifier(

            random_state=42,

            n_estimators=300,

            n_jobs=-1

        )

        scores = cross_val_score(

            model,

            self.X_train,

            self.y_train,

            cv=5,

            scoring="accuracy"

        )

        print()
        print("Fold Accuracies")

        for i, score in enumerate(scores, start=1):

            print(f"Fold {i}: {score:.4f}")

        print()

        print(f"Average Accuracy : {np.mean(scores):.4f}")
        print(f"Std Deviation    : {np.std(scores):.4f}")

        self.baseline_accuracy = np.mean(scores)

    # --------------------------------------------------------
    # Optimize Random Forest
    # --------------------------------------------------------

    def optimize_random_forest(self):

        print()
        print("=" * 60)
        print("GRID SEARCH - RANDOM FOREST")
        print("=" * 60)

        param_grid = {

            "n_estimators": [200, 300, 500],

            "max_depth": [None, 10, 20],

            "min_samples_split": [2, 5],

            "min_samples_leaf": [1, 2],

            "class_weight": [None, "balanced"]

        }

        rf = RandomForestClassifier(
            random_state=42,
            n_jobs=-1
        )

        grid = GridSearchCV(

            estimator=rf,

            param_grid=param_grid,

            cv=5,

            scoring="accuracy",

            n_jobs=-1,

            verbose=1

        )

        grid.fit(
            self.X_train,
            self.y_train
        )

        print()
        print("Best Parameters")
        print("-" * 60)

        for key, value in grid.best_params_.items():
            print(f"{key}: {value}")

        print()
        print(f"Best CV Accuracy : {grid.best_score_:.4f}")

        self.best_rf = grid.best_estimator_
        self.best_rf_accuracy = grid.best_score_

    # --------------------------------------------------------
    # Save Optimized Model
    # --------------------------------------------------------

    def save_optimized_model(self):

        print()
        print("=" * 60)
        print("SAVING OPTIMIZED MODEL")
        print("=" * 60)

        joblib.dump(
            self.best_rf,
            MODEL_FOLDER / "random_forest_optimized.pkl"
        )

        joblib.dump(
            self.feature_columns,
            MODEL_FOLDER / "feature_columns.pkl"
        )

        print()

        print("Saved")

        print("random_forest_optimized.pkl")
        print("feature_columns.pkl")


# --------------------------------------------------------
# Main
# --------------------------------------------------------

if __name__ == "__main__":

    optimizer = ModelOptimization()

    optimizer.prepare_data()

    optimizer.baseline_random_forest()

    optimizer.optimize_random_forest()

    optimizer.save_optimized_model()