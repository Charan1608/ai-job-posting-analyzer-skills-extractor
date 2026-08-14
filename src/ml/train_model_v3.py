"""
src/ml/train_model_v3.py

AI-Powered Job Posting Analyzer
--------------------------------
Production training pipeline (v3) for the standard_title classification task.

Run with:
    python -m src.ml.train_model_v3
"""

import time
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.feature_selection import VarianceThreshold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_validate,
    train_test_split,
)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import LinearSVC

from src.normalization.config import PROJECT_ROOT

warnings.filterwarnings("ignore")


class TrainModelsV3:
    """
    End-to-end training pipeline for the AI-Powered Job Posting Analyzer.

    Loads the processed ML dataset, prepares features/target, tunes and
    trains four classification models, cross-validates them, evaluates them
    individually, exports comparison/interpretability reports, and persists
    the best-performing model along with every preprocessing artifact
    required to reproduce inference end to end.
    """

    DROP_COLUMNS = [
        "job_id",
        "company_name",
        "title",
        "location",
        "experience",
        "education",
        "work_type",
        "standard_title",
    ]

    TARGET_COLUMN = "standard_title"

    # Short, filesystem-safe keys used for per-model export filenames.
    MODEL_KEYS = {
        "Logistic Regression": "logistic",
        "Linear SVM": "svm",
        "Random Forest": "rf",
        "Gradient Boosting": "gb",
    }

    SCALED_MODELS = {"Logistic Regression", "Linear SVM"}
    PROBA_MODELS = {"Logistic Regression", "Random Forest"}

    def __init__(self):
        self.project_root = Path(PROJECT_ROOT)
        self.dataset_path = self.project_root / "data" / "processed" / "final_ml_dataset_v2.csv"
        self.models_dir = self.project_root / "models"
        self.reports_dir = self.project_root / "reports"

        self.df = None
        self.X = None
        self.y = None

        self.feature_columns = None
        self.selected_feature_columns = None

        self.label_encoders = {}
        self.target_encoder = None
        self.scaler = None
        self.variance_selector = None

        self.X_train = None
        self.X_test = None
        self.X_train_scaled = None
        self.X_test_scaled = None
        self.y_train = None
        self.y_test = None

        self.models = {}
        self.tuned_params = {}
        self.cv_results_frames = {}
        self.cross_val_summary = {}
        self.results = {}
        self.predictions = {}
        self.probabilities = {}

        self.best_model_name = None
        self.best_model = None

    # ------------------------------------------------------------------
    # Console helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _print_header(title):
        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)

    @staticmethod
    def _print_section(title):
        print("\n" + "-" * 60)
        print(title)
        print("-" * 60)

    def _model_data(self, name, split="train"):
        """Return the correct (scaled vs raw) feature matrix for a model/split."""
        use_scaled = name in self.SCALED_MODELS
        if split == "train":
            return self.X_train_scaled if use_scaled else self.X_train
        return self.X_test_scaled if use_scaled else self.X_test

    # ------------------------------------------------------------------
    # Data preparation
    # ------------------------------------------------------------------
    def prepare_data(self):
        self._print_section("PREPARING DATA")

        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found at: {self.dataset_path}")

        self.df = pd.read_csv(self.dataset_path)
        print(f"Rows Loaded       : {self.df.shape[0]}")
        print(f"Columns Loaded    : {self.df.shape[1]}")

        if self.TARGET_COLUMN not in self.df.columns:
            raise ValueError(f"Target column '{self.TARGET_COLUMN}' not found in dataset.")

        y_raw = self.df[self.TARGET_COLUMN].astype(str)

        drop_cols_present = [c for c in self.DROP_COLUMNS if c in self.df.columns]
        X = self.df.drop(columns=drop_cols_present)

        print(f"Columns Dropped   : {drop_cols_present}")
        print(f"Feature Columns   : {X.shape[1]}")

        object_columns = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
        print(f"Object Columns Encoded : {len(object_columns)}")

        for col in object_columns:
            encoder = LabelEncoder()
            X[col] = X[col].astype(str).fillna("missing")
            X[col] = encoder.fit_transform(X[col])
            self.label_encoders[col] = encoder

        X = X.fillna(0)
        X = X.apply(pd.to_numeric, errors="coerce")
        X = X.fillna(0)

        self.feature_columns = X.columns.tolist()

        self.target_encoder = LabelEncoder()
        self.y = self.target_encoder.fit_transform(y_raw)
        print(f"Target Classes            : {len(self.target_encoder.classes_)}")

        # Split BEFORE feature selection. VarianceThreshold is unsupervised,
        # but fitting it (or the scaler) on the full dataset still leaks
        # information about the test rows' distribution into training. The
        # stricter, leakage-free order is: split -> fit selector on train
        # only -> transform train and test with that fitted selector.
        X_train_raw, X_test_raw, self.y_train, self.y_test = train_test_split(
            X,
            self.y,
            test_size=0.20,
            random_state=42,
            stratify=self.y,
        )

        print(f"Train Rows                : {X_train_raw.shape[0]}")
        print(f"Test Rows                 : {X_test_raw.shape[0]}")

        self._print_section("FEATURE SELECTION")
        self.variance_selector = VarianceThreshold(threshold=0.02)
        X_train_selected = self.variance_selector.fit_transform(X_train_raw)
        X_test_selected = self.variance_selector.transform(X_test_raw)

        selected_mask = self.variance_selector.get_support()
        self.selected_feature_columns = [
            col for col, keep in zip(self.feature_columns, selected_mask) if keep
        ]

        print(f"Features Before Selection : {X_train_raw.shape[1]}")
        print(f"Features After Selection  : {len(self.selected_feature_columns)}")
        print("Selector Fitted On        : Training set only (no test-set leakage)")

        self.X_train = pd.DataFrame(
            X_train_selected, columns=self.selected_feature_columns, index=X_train_raw.index
        )
        self.X_test = pd.DataFrame(
            X_test_selected, columns=self.selected_feature_columns, index=X_test_raw.index
        )
        self.X = pd.concat([self.X_train, self.X_test]).sort_index()

        self.scaler = StandardScaler()
        self.X_train_scaled = pd.DataFrame(
            self.scaler.fit_transform(self.X_train),
            columns=self.selected_feature_columns,
            index=self.X_train.index,
        )
        self.X_test_scaled = pd.DataFrame(
            self.scaler.transform(self.X_test),
            columns=self.selected_feature_columns,
            index=self.X_test.index,
        )

        print("Scaling Applied           : StandardScaler, fit on train only (Logistic Regression / Linear SVM)")

    # ------------------------------------------------------------------
    # Model definition
    # ------------------------------------------------------------------
    def define_models(self):
        self._print_section("MODEL DEFINITION")

        self.models = {
            "Logistic Regression": LogisticRegression(
                max_iter=1000,
                random_state=42,
            ),
            "Linear SVM": LinearSVC(
                dual=False,
                max_iter=5000,
                random_state=42,
            ),
            "Random Forest": RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                n_jobs=-1,
            ),
            "Gradient Boosting": GradientBoostingClassifier(
                random_state=42,
            ),
        }

        for name in self.models:
            print(f"Model Defined : {name}")

    # ------------------------------------------------------------------
    # Hyperparameter tuning
    # ------------------------------------------------------------------
    def tune_models(self):
        self._print_section("HYPERPARAMETER TUNING")

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        # Only the linear models are grid-searched. With just 200 training
        # samples, exhaustively tuning Random Forest / Gradient Boosting as
        # well would multiply fit counts into the hundreds for little real
        # benefit and risks overfitting the validation folds themselves.
        # Random Forest and Gradient Boosting are trained below with the
        # fixed, sensible defaults set in define_models().
        param_grids = {
            "Logistic Regression": {"C": [0.001, 0.01, 0.1, 1, 5, 10, 20]},
            "Linear SVM": {"C": [0.01, 0.1, 1, 5, 10]},
        }

        for name, grid in param_grids.items():
            print(f"\nTuning {name} ...")
            base_model = self.models[name]
            X_fit = self._model_data(name, split="train")

            search = GridSearchCV(
                estimator=base_model,
                param_grid=grid,
                scoring="f1_weighted",
                cv=cv,
                n_jobs=-1,
                refit=True,
            )

            search.fit(X_fit, self.y_train)

            self.models[name] = search.best_estimator_
            self.tuned_params[name] = search.best_params_

            print(f"Best Params ({name}) : {search.best_params_}")
            print(f"Best CV F1 Weighted  : {search.best_score_:.4f}")

            self.cv_results_frames[name] = pd.DataFrame(search.cv_results_)

        for name in self.models:
            if name not in param_grids:
                print(f"\n{name} : using fixed parameters (not grid-searched)")

    # ------------------------------------------------------------------
    # Cross-validation summary (mean / std across folds for tuned models)
    # ------------------------------------------------------------------
    def cross_validate_models(self):
        self._print_section("CROSS-VALIDATION SUMMARY")

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scoring = ["accuracy", "f1_weighted"]

        for name, model in self.models.items():
            X_fit = self._model_data(name, split="train")
            estimator = clone(model)

            cv_output = cross_validate(
                estimator,
                X_fit,
                self.y_train,
                cv=cv,
                scoring=scoring,
                n_jobs=-1,
                return_train_score=False,
            )

            accuracy_mean = float(np.mean(cv_output["test_accuracy"]))
            accuracy_std = float(np.std(cv_output["test_accuracy"]))
            f1_mean = float(np.mean(cv_output["test_f1_weighted"]))
            f1_std = float(np.std(cv_output["test_f1_weighted"]))

            self.cross_val_summary[name] = {
                "CV_Accuracy_Mean": accuracy_mean,
                "CV_Accuracy_Std": accuracy_std,
                "CV_F1_Weighted_Mean": f1_mean,
                "CV_F1_Weighted_Std": f1_std,
            }

            print(f"\nModel : {name}")
            print(f"  Accuracy     : {accuracy_mean:.4f} (+/- {accuracy_std:.4f})")
            print(f"  F1 Weighted  : {f1_mean:.4f} (+/- {f1_std:.4f})")

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------
    def train_models(self):
        self._print_section("TRAINING MODELS")

        for name, model in self.models.items():
            print(f"Training {name} ...")
            X_fit = self._model_data(name, split="train")

            start = time.perf_counter()
            model.fit(X_fit, self.y_train)
            train_time = time.perf_counter() - start

            self.models[name] = model
            self.results.setdefault(name, {})["Train_Time_Seconds"] = train_time

            print(f"Finished Training : {name} ({train_time:.4f}s)")

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------
    def evaluate_models(self):
        self._print_section("EVALUATION")

        for name, model in self.models.items():
            X_eval_test = self._model_data(name, split="test")

            start = time.perf_counter()
            y_pred = model.predict(X_eval_test)
            predict_time = time.perf_counter() - start

            self.predictions[name] = y_pred

            if name in self.PROBA_MODELS and hasattr(model, "predict_proba"):
                self.probabilities[name] = model.predict_proba(X_eval_test)

            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred, average="weighted", zero_division=0)
            recall = recall_score(self.y_test, y_pred, average="weighted", zero_division=0)
            f1 = f1_score(self.y_test, y_pred, average="weighted", zero_division=0)

            self.results.setdefault(name, {}).update(
                {
                    "Accuracy": accuracy,
                    "Precision": precision,
                    "Recall": recall,
                    "F1_Weighted": f1,
                    "Predict_Time_Seconds": predict_time,
                }
            )

            print(f"\nModel : {name}")
            print(f"  Accuracy         : {accuracy:.4f}")
            print(f"  Precision (wtd)  : {precision:.4f}")
            print(f"  Recall (wtd)     : {recall:.4f}")
            print(f"  F1 Score (wtd)   : {f1:.4f}")
            print(f"  Train Time (s)   : {self.results[name]['Train_Time_Seconds']:.4f}")
            print(f"  Predict Time (s) : {predict_time:.4f}")

        self.best_model_name = max(
            self.results, key=lambda name: self.results[name]["F1_Weighted"]
        )
        self.best_model = self.models[self.best_model_name]

        print(f"\nBest Model Selected (by Weighted F1) : {self.best_model_name}")

        best_pred = self.predictions[self.best_model_name]
        target_names = [str(c) for c in self.target_encoder.classes_]

        self._print_section(f"CLASSIFICATION REPORT - {self.best_model_name}")
        report_text = classification_report(
            self.y_test,
            best_pred,
            labels=list(range(len(target_names))),
            target_names=target_names,
            zero_division=0,
        )
        print(report_text)

        self._print_section(f"CONFUSION MATRIX - {self.best_model_name}")
        cm = confusion_matrix(self.y_test, best_pred, labels=list(range(len(target_names))))
        cm_df = pd.DataFrame(cm, index=target_names, columns=target_names)
        print(cm_df)

    # ------------------------------------------------------------------
    # Save best model + full preprocessing artifact set
    # ------------------------------------------------------------------
    def save_best_model(self):
        self._print_section("SAVING MODEL")

        self.models_dir.mkdir(parents=True, exist_ok=True)

        best_model_path = self.models_dir / "best_model.pkl"
        scaler_path = self.models_dir / "scaler.pkl"
        label_encoder_path = self.models_dir / "label_encoder.pkl"
        feature_columns_path = self.models_dir / "feature_columns.pkl"
        selected_feature_columns_path = self.models_dir / "selected_feature_columns.pkl"
        variance_selector_path = self.models_dir / "variance_selector.pkl"
        feature_encoders_path = self.models_dir / "feature_encoders.pkl"

        joblib.dump(self.best_model, best_model_path)
        joblib.dump(self.scaler, scaler_path)
        joblib.dump(self.target_encoder, label_encoder_path)

        # CRITICAL: feature_columns.pkl must hold the ORIGINAL, pre-selection
        # feature list (in the exact order the VarianceThreshold selector
        # was fitted on). This is what any downstream inference code needs
        # to reindex a freshly engineered raw feature vector against before
        # calling variance_selector.transform(). Saving the post-selection
        # list here (as a previous version of this file did) causes
        # "feature names should match those passed during fit" errors at
        # inference time, because the selector was fit on the full raw
        # column set, not the reduced one.
        joblib.dump(self.feature_columns, feature_columns_path)

        # Kept separately for transparency / debugging / reporting. This is
        # the reduced set the selector actually outputs, and what the
        # scaler and model were trained on. Inference code should NOT use
        # this to build its raw feature vector -- it should use
        # feature_columns.pkl, then let variance_selector.transform()
        # perform the reduction itself.
        joblib.dump(self.selected_feature_columns, selected_feature_columns_path)

        joblib.dump(self.variance_selector, variance_selector_path)
        joblib.dump(self.label_encoders, feature_encoders_path)

        print(f"Saved Best Model              : {best_model_path}")
        print(f"Saved Scaler                  : {scaler_path}")
        print(f"Saved Label Encoder           : {label_encoder_path}")
        print(f"Saved Feature Columns (raw)   : {feature_columns_path}")
        print(f"Saved Feature Columns (post-selection, reference only) : {selected_feature_columns_path}")
        print(f"Saved Variance Selector       : {variance_selector_path}")
        print(f"Saved Feature Encoders        : {feature_encoders_path}")

    # ------------------------------------------------------------------
    # Export results
    # ------------------------------------------------------------------
    def export_results(self):
        self._print_section("EXPORTING RESULTS")

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        target_names = [str(c) for c in self.target_encoder.classes_]

        # -- model_comparison.csv (merged with cross-validation summary) --
        comparison_df = pd.DataFrame(self.results).T
        if self.cross_val_summary:
            cv_summary_df = pd.DataFrame(self.cross_val_summary).T
            comparison_df = comparison_df.join(cv_summary_df)
        comparison_df.index.name = "Model"

        # Sort by cross-validated F1 (weighted) when available, since that
        # is the more robust, fold-averaged estimate of generalization
        # performance; fall back to the single held-out test F1 otherwise.
        sort_column = "CV_F1_Weighted_Mean" if "CV_F1_Weighted_Mean" in comparison_df.columns else "F1_Weighted"
        comparison_df = comparison_df.sort_values(by=sort_column, ascending=False)
        comparison_path = self.reports_dir / "model_comparison.csv"
        comparison_df.to_csv(comparison_path)
        print(f"Saved Model Comparison       : {comparison_path} (sorted by {sort_column})")

        # -- classification_report.txt (best model, kept for backward compatibility) --
        best_pred = self.predictions[self.best_model_name]
        report_text = classification_report(
            self.y_test,
            best_pred,
            labels=list(range(len(target_names))),
            target_names=target_names,
            zero_division=0,
        )
        report_path = self.reports_dir / "classification_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"Best Model: {self.best_model_name}\n\n")
            f.write(report_text)
        print(f"Saved Classification Report : {report_path}")

        # -- confusion_matrix.csv (best model) --
        cm = confusion_matrix(self.y_test, best_pred, labels=list(range(len(target_names))))
        cm_df = pd.DataFrame(cm, index=target_names, columns=target_names)
        cm_path = self.reports_dir / "confusion_matrix.csv"
        cm_df.to_csv(cm_path)
        print(f"Saved Confusion Matrix       : {cm_path}")

        # -- per-model classification reports --
        for name, y_pred in self.predictions.items():
            key = self.MODEL_KEYS.get(name, name.lower().replace(" ", "_"))
            per_model_text = classification_report(
                self.y_test,
                y_pred,
                labels=list(range(len(target_names))),
                target_names=target_names,
                zero_division=0,
            )
            per_model_path = self.reports_dir / f"classification_{key}.txt"
            with open(per_model_path, "w", encoding="utf-8") as f:
                f.write(f"Model: {name}\n\n")
                f.write(per_model_text)
            print(f"Saved Per-Model Report       : {per_model_path}")

        # -- per-model confusion matrices --
        for name, y_pred in self.predictions.items():
            key = self.MODEL_KEYS.get(name, name.lower().replace(" ", "_"))
            per_model_cm = confusion_matrix(
                self.y_test, y_pred, labels=list(range(len(target_names)))
            )
            per_model_cm_df = pd.DataFrame(per_model_cm, index=target_names, columns=target_names)
            per_model_cm_path = self.reports_dir / f"confusion_{key}.csv"
            per_model_cm_df.to_csv(per_model_cm_path)
            print(f"Saved Per-Model Confusion Matrix : {per_model_cm_path}")

        # -- cv_results.csv per tuned model (GridSearchCV grid results) --
        for name, cv_df in self.cv_results_frames.items():
            key = self.MODEL_KEYS.get(name, name.lower().replace(" ", "_"))
            cv_results_path = self.reports_dir / f"cv_results_{key}.csv"
            cv_df.to_csv(cv_results_path, index=False)
            print(f"Saved Grid Search CV Results : {cv_results_path}")

        # -- cross_validation_summary.csv --
        if self.cross_val_summary:
            cv_summary_df = pd.DataFrame(self.cross_val_summary).T
            cv_summary_df.index.name = "Model"
            cv_summary_path = self.reports_dir / "cross_validation_summary.csv"
            cv_summary_df.to_csv(cv_summary_path)
            print(f"Saved Cross-Validation Summary : {cv_summary_path}")

        # -- feature_importance.csv (Random Forest) --
        rf_model = self.models.get("Random Forest")
        if rf_model is not None and hasattr(rf_model, "feature_importances_"):
            importance_df = pd.DataFrame(
                {
                    "Feature": self.selected_feature_columns,
                    "Importance": rf_model.feature_importances_,
                }
            ).sort_values(by="Importance", ascending=False).reset_index(drop=True)

            importance_path = self.reports_dir / "feature_importance.csv"
            importance_df.to_csv(importance_path, index=False)
            print(f"Saved Feature Importance     : {importance_path}")

            top20_df = importance_df.head(20)
            top20_path = self.reports_dir / "top20_feature_importance.csv"
            top20_df.to_csv(top20_path, index=False)
            print(f"Saved Top 20 Feature Importance : {top20_path}")

            self._print_section("TOP 20 FEATURES - RANDOM FOREST")
            print(top20_df.to_string(index=False))

        # -- predict_proba exports (Logistic Regression, Random Forest) --
        for name, proba in self.probabilities.items():
            key = self.MODEL_KEYS.get(name, name.lower().replace(" ", "_"))
            proba_df = pd.DataFrame(proba, columns=target_names, index=self.X_test.index)
            proba_path = self.reports_dir / f"predict_proba_{key}.csv"
            proba_df.to_csv(proba_path)
            print(f"Saved Prediction Probabilities : {proba_path}")

    # ------------------------------------------------------------------
    # Orchestration
    # ------------------------------------------------------------------
    def run(self):
        start_time = time.time()

        self._print_header("TRAIN MACHINE LEARNING MODELS V3")

        self.prepare_data()
        self.define_models()
        self.tune_models()
        self.cross_validate_models()
        self.train_models()
        self.evaluate_models()
        self.save_best_model()
        self.export_results()

        elapsed = time.time() - start_time

        self._print_header("FINISHED")
        print(f"Best Model     : {self.best_model_name}")
        print(f"Best F1 (wtd)  : {self.results[self.best_model_name]['F1_Weighted']:.4f}")
        print(f"Total Runtime  : {elapsed:.2f} seconds")
        print("=" * 60 + "\n")


def main():
    trainer = TrainModelsV3()
    trainer.run()


if __name__ == "__main__":
    main()