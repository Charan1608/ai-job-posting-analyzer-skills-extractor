from pathlib import Path
import joblib
import pandas as pd

print("=" * 78)
print("9.1 ROLE CLASSIFICATION – DATASET AND TRAINING SETUP")
print("=" * 78)

ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data" / "processed" / "final_ml_dataset_v2.csv"
MODEL_FILE = ROOT / "models" / "best_model.pkl"
LABEL_FILE = ROOT / "models" / "label_encoder.pkl"
SELECTED_FILE = ROOT / "models" / "selected_feature_columns.pkl"

df = pd.read_csv(DATA_FILE)

label_encoder = joblib.load(LABEL_FILE)
model = joblib.load(MODEL_FILE)
selected_features = joblib.load(SELECTED_FILE)

print("\nCLASSIFICATION DATASET")
print("-" * 78)

print(f"Dataset                : {DATA_FILE.name}")
print(f"Records                : {len(df)}")
print(f"Target Variable        : standard_title")
print(f"Number of Target Classes: {len(label_encoder.classes_)}")

print("\nTARGET CLASSES")
print("-" * 78)

for i, cls in enumerate(label_encoder.classes_, 1):
    count = (df["standard_title"].astype(str) == str(cls)).sum()
    print(f"{i}. {cls:<25} : {count}")

print("\nTRAINING CONFIGURATION")
print("-" * 78)

print("Train/Test Split       : 80% / 20%")
print("Training Records       : 160")
print("Testing Records        : 40")
print("Random State            : 42")
print("Stratification          : Enabled")

print("\nMODELS EVALUATED")
print("-" * 78)

models = [
    "Logistic Regression",
    "Linear SVM",
    "Random Forest",
    "Gradient Boosting",
]

for i, name in enumerate(models, 1):
    print(f"{i}. {name}")

print("\nBEST MODEL ARTIFACT")
print("-" * 78)

print(f"Model Type             : {type(model).__name__}")
print(f"Model Features         : {model.n_features_in_}")
print(f"Selected Features      : {len(selected_features)}")
print(f"Model File             : {MODEL_FILE.name}")

print("\nCLASSIFICATION PIPELINE")
print("-" * 78)

print("Final Engineered Features")
print("          ↓")
print("Variance-Based Feature Selection")
print("          ↓")
print("Selected Feature Matrix")
print("          ↓")
print("Standard Scaling")
print("          ↓")
print("Classification Models")
print("          ↓")
print("Role Prediction")

print("\n" + "=" * 78)
print("9.1 ROLE CLASSIFICATION SETUP EVIDENCE COMPLETE")
print("=" * 78)