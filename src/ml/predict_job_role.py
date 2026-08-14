"""
=========================================================
PREDICT JOB ROLE
AI-Powered Job Posting Analyzer
=========================================================
"""

import joblib
import pandas as pd

from src.normalization.config import PROJECT_ROOT
from src.features.feature_engineering_v2 import FeatureEngineeringV2

# --------------------------------------------------------
# Paths
# --------------------------------------------------------

MODEL_FOLDER = PROJECT_ROOT / "models"

MODEL_FILE = MODEL_FOLDER / "best_model.pkl"

SCALER_FILE = MODEL_FOLDER / "scaler.pkl"

LABEL_ENCODER_FILE = MODEL_FOLDER / "label_encoder.pkl"

# Original, pre-selection raw feature list (96 columns) in the exact
# order the VarianceThreshold selector was fit on. Used to reindex the
# freshly engineered raw feature vector before calling
# variance_selector.transform() -- NOT the post-selection list.
FEATURE_COLUMNS_FILE = MODEL_FOLDER / "feature_columns.pkl"

SELECTED_FEATURE_COLUMNS_FILE = MODEL_FOLDER / "selected_feature_columns.pkl"

VARIANCE_SELECTOR_FILE = MODEL_FOLDER / "variance_selector.pkl"

TECHNOLOGY_VOCAB_FILE = MODEL_FOLDER / "technology_vocabulary.pkl"


# ========================================================
# Predictor
# ========================================================

class JobRolePredictor:

    def __init__(self):

        print("=" * 60)
        print("JOB ROLE PREDICTION ENGINE")
        print("=" * 60)

        self.load_artifacts()

    # ----------------------------------------------------
    # Load Model Artifacts
    # ----------------------------------------------------

    def load_artifacts(self):

        print("\nLoading Saved Models...\n")

        self.model = joblib.load(
            MODEL_FILE
        )

        self.scaler = joblib.load(
            SCALER_FILE
        )

        self.label_encoder = joblib.load(
            LABEL_ENCODER_FILE
        )

        self.feature_columns = joblib.load(
            FEATURE_COLUMNS_FILE
        )

        self.selected_feature_columns = joblib.load(
            SELECTED_FEATURE_COLUMNS_FILE
        )

        self.variance_selector = joblib.load(
            VARIANCE_SELECTOR_FILE
        )

        technology_vocabulary = joblib.load(
            TECHNOLOGY_VOCAB_FILE
        )

        # Reuse the exact same feature engineering implementation that
        # produced the training data, instead of manually recreating
        # features here. `load_data=False` skips reading the training
        # CSV, since inference only needs build_single_feature_vector().
        self.feature_engineer = FeatureEngineeringV2(load_data=False)
        self.feature_engineer.technologies = technology_vocabulary

        print(f"Model                : {MODEL_FILE.name}")
        print(f"Raw Feature Columns  : {len(self.feature_columns)}")
        print(f"Selected Features    : {len(self.selected_feature_columns)}")
        print(f"Technology Vocabulary: {len(technology_vocabulary)}")
        print(f"Classes              : {len(self.label_encoder.classes_)}")

    # ----------------------------------------------------
    # Build Model-Ready Input
    # ----------------------------------------------------

    def _build_model_input(self, normalized_skills):
        """
        Turn one job's normalized skills into the exact input the model
        expects, following the same pipeline used at training time:

            1. Build the raw 96-feature vector (FeatureEngineeringV2,
               same implementation as training).
            2. Reindex against feature_columns.pkl (raw, pre-selection
               order the selector was fit on).
            3. Reduce with the fitted VarianceThreshold selector.
            4. Scale only for models that were trained on scaled data.
        """

        X_raw = self.feature_engineer.build_single_feature_vector(
            normalized_skills
        )

        X_raw = X_raw.reindex(
            columns=self.feature_columns,
            fill_value=0
        )

        X_selected = self.variance_selector.transform(X_raw)

        # Convert back to DataFrame so feature names are preserved
        X_selected = pd.DataFrame(
            X_selected,
            columns=self.selected_feature_columns
        )

        if self.model.__class__.__name__ in [
            "LogisticRegression",
            "LinearSVC"
        ]:

            # Keep feature names attached, matching X_train_scaled at
            # training time (also a named DataFrame, not a bare array).
            X_input = pd.DataFrame(
                self.scaler.transform(X_selected),
                columns=self.selected_feature_columns
            )

        else:

            X_input = X_selected

        return X_input

    # ----------------------------------------------------
    # Predict
    # ----------------------------------------------------

    def predict(self, normalized_skills):

        X_input = self._build_model_input(normalized_skills)

        prediction = self.model.predict(
            X_input
        )[0]

        role = self.label_encoder.inverse_transform(
            [prediction]
        )[0]

        confidence = None

        if hasattr(self.model, "predict_proba"):

            probability = self.model.predict_proba(
                X_input
            )[0]

            confidence = probability.max()

        return {

            "predicted_role": role,

            "confidence": confidence

        }

    # ----------------------------------------------------
    # Top N Predictions
    # ----------------------------------------------------

    def predict_top_n(self, normalized_skills, top_n=5):

        X_input = self._build_model_input(normalized_skills)

        if not hasattr(self.model, "predict_proba"):

            return None

        probabilities = self.model.predict_proba(
            X_input
        )[0]

        df = pd.DataFrame({

            "Role": self.label_encoder.classes_,

            "Probability": probabilities

        })

        df = df.sort_values(

            "Probability",

            ascending=False

        )

        return df.head(top_n)

    # ----------------------------------------------------
    # Test
    # ----------------------------------------------------

    def test_feature_builder(self):

        sample = [

            {
                "normalized": "Python",
                "skill_type": "Programming Language"
            },

            {
                "normalized": "SQL",
                "skill_type": "Database Language"
            },

            {
                "normalized": "Power BI",
                "skill_type": "BI Tool"
            },

            {
                "normalized": "Tableau",
                "skill_type": "BI Tool"
            },

            {
                "normalized": "Excel",
                "skill_type": "Spreadsheet"
            }

        ]

        print("\n" + "=" * 60)
        print("RAW FEATURE VECTOR")
        print("=" * 60)

        raw_features = self.feature_engineer.build_single_feature_vector(sample)

        print(raw_features.T)

        result = self.predict(sample)

        print("\n" + "=" * 60)
        print("PREDICTION")
        print("=" * 60)

        print(f"Predicted Role : {result['predicted_role']}")

        if result["confidence"] is not None:
            print(f"Confidence     : {result['confidence']:.2%}")

        print("\nTOP PREDICTIONS")

        print(self.predict_top_n(sample))


# ========================================================
# Main
# ========================================================

if __name__ == "__main__":

    predictor = JobRolePredictor()

    predictor.test_feature_builder()