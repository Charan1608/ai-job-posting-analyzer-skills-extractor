"""
=========================================================
FEATURE IMPORTANCE
AI-Powered Job Posting Analyzer
=========================================================
"""

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from src.normalization.config import PROJECT_ROOT


MODEL_FOLDER = (
    PROJECT_ROOT
    / "models"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "outputs"
)

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


class FeatureImportance:

    def __init__(self):

        print("=" * 60)
        print("FEATURE IMPORTANCE")
        print("=" * 60)

        self.model = joblib.load(
            MODEL_FOLDER / "random_forest_optimized.pkl"
        )

        self.features = joblib.load(
            MODEL_FOLDER / "feature_columns.pkl"
        )

        print()

        print(f"Features Loaded : {len(self.features)}")

        print(
            f"Model Features  : "
            f"{self.model.n_features_in_}"
        )

    def calculate_importance(self):

        print()
        print("=" * 60)
        print("CALCULATING FEATURE IMPORTANCE")
        print("=" * 60)

        importance = self.model.feature_importances_

        self.importance_df = pd.DataFrame({
            "Feature": self.features,
            "Importance": importance
        })

        self.importance_df = self.importance_df.sort_values(
            by="Importance",
            ascending=False
        )

        print()
        print(self.importance_df.head(20))

        self.importance_df.to_csv(
            OUTPUT_FOLDER / "feature_importance.csv",
            index=False
        )

        print()
        print("Saved :", OUTPUT_FOLDER / "feature_importance.csv")

    def plot_importance(self, top_n=20):

        print()
        print("=" * 60)
        print("SAVING FEATURE IMPORTANCE PLOT")
        print("=" * 60)

        top_features = self.importance_df.head(top_n)

        plt.figure(figsize=(10, 8))
        plt.barh(top_features["Feature"], top_features["Importance"])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance")
        plt.title(f"Top {top_n} Feature Importances - Random Forest")
        plt.tight_layout()

        output_path = OUTPUT_FOLDER / "feature_importance.png"
        plt.savefig(output_path)
        plt.close()

        print()
        print(f"Saved : {output_path}")


if __name__ == "__main__":

    importance = FeatureImportance()
    importance.calculate_importance()
    importance.plot_importance()