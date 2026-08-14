"""
=========================================================
TRAIN MACHINE LEARNING MODELS V2
AI-Powered Job Posting Analyzer
=========================================================
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)
from sklearn.model_selection import (
    StratifiedKFold,
    GridSearchCV
)
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

import joblib
from pathlib import Path
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


# --------------------------------------------------------
# Train Models V2
# --------------------------------------------------------

class TrainModelsV2:

    def __init__(self):

        print("=" * 60)
        print("TRAIN MACHINE LEARNING MODELS V2")
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

        # ---------------------------------------------
        # Drop non-feature columns
        # ---------------------------------------------

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

        # ---------------------------------------------
        # Target
        # ---------------------------------------------

        y = self.df[target_column]

        # ---------------------------------------------
        # Remaining object columns
        # ---------------------------------------------

        print()
        print("Remaining Object Columns")
        print("-" * 60)

        object_columns = X.select_dtypes(
            include=["object"]
        ).columns.tolist()

        print(object_columns)

               # ---------------------------------------------
        # Encode object columns
        # ---------------------------------------------

        self.feature_encoders = {}

        for column in object_columns:

            encoder = LabelEncoder()

            X[column] = encoder.fit_transform(
                X[column].fillna("").astype(str)
            )

            self.feature_encoders[column] = encoder

        # ---------------------------------------------
        # Remove Near-Zero Variance Features
        # ---------------------------------------------

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

        print(f"Original Features : {original_feature_count}")
        print(f"Selected Features : {len(selected_columns)}")
        print(f"Removed Features  : {original_feature_count - len(selected_columns)}")

        # ---------------------------------------------
        # Encode target
        # ---------------------------------------------

        self.label_encoder = LabelEncoder()

        y = self.label_encoder.fit_transform(y)

        # ---------------------------------------------
        # Save feature names
        # ---------------------------------------------

        self.feature_names = X.columns.tolist()

        # ---------------------------------------------
        # Train Test Split
        # ---------------------------------------------

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

        # ---------------------------------------------
        # Scale
        # ---------------------------------------------

        self.scaler = StandardScaler()

        self.X_train_scaled = self.scaler.fit_transform(
            self.X_train
        )

        self.X_test_scaled = self.scaler.transform(
            self.X_test
        )

        print()
        print(f"Training Rows : {len(self.X_train)}")
        print(f"Testing Rows  : {len(self.X_test)}")
        print(f"Features      : {len(self.feature_names)}")
        print(f"Classes       : {len(self.label_encoder.classes_)}")
            # --------------------------------------------------------
    # Define Machine Learning Models
    # --------------------------------------------------------

    def define_models(self):

        print()
        print("=" * 60)
        print("DEFINING MACHINE LEARNING MODELS")
        print("=" * 60)

        self.models = {

            "Logistic Regression": LogisticRegression(
                max_iter=1000,
                random_state=42
            ),

            "Linear SVM": LinearSVC(
    C=1.0,
    random_state=42,
    dual=False,
    max_iter=5000
),

            "Decision Tree": DecisionTreeClassifier(
                random_state=42
            ),

            "Random Forest": RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                n_jobs=-1
            ),

            "Gradient Boosting": GradientBoostingClassifier(
                random_state=42
            )

        }

        print(f"Models Defined : {len(self.models)}")
        print()

        for model_name in self.models.keys():
            print(f"✓ {model_name}")
                # --------------------------------------------------------
    # Train Models
    # --------------------------------------------------------

    def train_models(self):

        print()
        print("=" * 60)
        print("TRAINING MACHINE LEARNING MODELS")
        print("=" * 60)

        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score
        )

        self.results = []

        for name, model in self.models.items():

            print(f"\nTraining {name}...")

            # Logistic Regression benefits from scaling
            if name in ["Logistic Regression", "Linear SVM"]:

                model.fit(
                    self.X_train_scaled,
                    self.y_train
                )

                predictions = model.predict(
                    self.X_test_scaled
                )

            else:

                model.fit(
                    self.X_train,
                    self.y_train
                )

                predictions = model.predict(
                    self.X_test
                )

            accuracy = accuracy_score(
                self.y_test,
                predictions
            )

            precision = precision_score(
                self.y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            recall = recall_score(
                self.y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            f1 = f1_score(
                self.y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            self.results.append({

                "Model": name,
                "Accuracy": accuracy,
                "Precision": precision,
                "Recall": recall,
                "F1": f1,
                "ModelObject": model

            })

            print(f"Accuracy  : {accuracy:.4f}")
            print(f"Precision : {precision:.4f}")
            print(f"Recall    : {recall:.4f}")
            print(f"F1 Score  : {f1:.4f}")

        print()
        print("=" * 60)
        print("TRAINING COMPLETED")
        print("=" * 60)

        # --------------------------------------------------------
# Hyperparameter Tuning
# --------------------------------------------------------

def tune_models(self):

    print()
    print("=" * 60)
    print("HYPERPARAMETER TUNING")
    print("=" * 60)

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    tuned_models = {}

    # ----------------------------------------------------
    # Logistic Regression
    # ----------------------------------------------------

    print("\nTuning Logistic Regression...")

    lr_grid = {

        "C": [0.01, 0.1, 1, 5, 10, 20]

    }

    lr_search = GridSearchCV(

        LogisticRegression(
            max_iter=1000,
            random_state=42
        ),

        param_grid=lr_grid,

        scoring="f1_weighted",

        cv=cv,

        n_jobs=-1

    )

    lr_search.fit(

        self.X_train_scaled,

        self.y_train

    )

    print("Best Parameters :", lr_search.best_params_)

    print("Best CV Score   :", round(lr_search.best_score_, 4))

    tuned_models["Logistic Regression"] = lr_search.best_estimator_

    # ----------------------------------------------------
    # Linear SVM
    # ----------------------------------------------------

    print("\nTuning Linear SVM...")

    svm_grid = {

        "C": [0.01, 0.1, 1, 5, 10]

    }

    svm_search = GridSearchCV(

        LinearSVC(

            random_state=42,

            dual=False,

            max_iter=5000

        ),

        param_grid=svm_grid,

        scoring="f1_weighted",

        cv=cv,

        n_jobs=-1

    )

    svm_search.fit(

        self.X_train_scaled,

        self.y_train

    )

    print("Best Parameters :", svm_search.best_params_)

    print("Best CV Score   :", round(svm_search.best_score_, 4))

    tuned_models["Linear SVM"] = svm_search.best_estimator_

    # ----------------------------------------------------
    # Replace Existing Models
    # ----------------------------------------------------

    self.models["Logistic Regression"] = tuned_models["Logistic Regression"]

    self.models["Linear SVM"] = tuned_models["Linear SVM"]

    print()

    print("✓ Tuned Logistic Regression")

    print("✓ Tuned Linear SVM")
            # --------------------------------------------------------
    # Evaluate Models
    # --------------------------------------------------------

    def evaluate_models(self):

        print()
        print("=" * 60)
        print("MODEL EVALUATION")
        print("=" * 60)

        best_model = max(
            self.results,
            key=lambda x: x["F1"]
        )

        self.best_model = best_model

        print()
        print(f"Best Model : {best_model['Model']}")
        print(f"Accuracy   : {best_model['Accuracy']:.4f}")

        model = best_model["ModelObject"]

        if best_model["Model"] in ["Logistic Regression", "Linear SVM"]:

            predictions = model.predict(
                self.X_test_scaled
            )

        else:

            predictions = model.predict(
                self.X_test
            )

        print()
        print("=" * 60)
        print("CLASSIFICATION REPORT")
        print("=" * 60)

        print(
            classification_report(
                self.y_test,
                predictions,
                target_names=self.label_encoder.classes_,
                zero_division=0
            )
        )

        print()
        print("=" * 60)
        print("CONFUSION MATRIX")
        print("=" * 60)

        cm = confusion_matrix(
            self.y_test,
            predictions
        )

        print(cm)

        self.predictions = predictions
            # --------------------------------------------------------
    # Save Best Model
    # --------------------------------------------------------

    def save_best_model(self):

        print()
        print("=" * 60)
        print("SAVING MODEL")
        print("=" * 60)

        model_name = (
            self.best_model["Model"]
            .lower()
            .replace(" ", "_")
        )

        model_path = (
            MODEL_FOLDER
            / f"{model_name}.pkl"
        )

        joblib.dump(
            self.best_model["ModelObject"],
            model_path
        )

        scaler_path = (
            MODEL_FOLDER
            / "scaler.pkl"
        )

        joblib.dump(
            self.scaler,
            scaler_path
        )

        encoder_path = (
            MODEL_FOLDER
            / "label_encoder.pkl"
        )

        joblib.dump(
            self.label_encoder,
            encoder_path
        )

        features_path = (
            MODEL_FOLDER
            / "feature_columns.pkl"
        )

        joblib.dump(
            self.feature_names,
            features_path
        )

        print()

        print("Saved Files")
        print("-" * 60)

        print(model_path.name)
        print(scaler_path.name)
        print(encoder_path.name)
        print(features_path.name)


# --------------------------------------------------------
# Main
# --------------------------------------------------------

if __name__ == "__main__":

    trainer = TrainModelsV2()

    trainer.prepare_data()

    trainer.define_models()

    trainer.train_models()

    trainer.evaluate_models()

    trainer.tune_models()

    trainer.save_best_model()