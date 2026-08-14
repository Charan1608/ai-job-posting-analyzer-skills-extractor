from pathlib import Path
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]

DATASET = ROOT / "data" / "processed" / "final_ml_dataset_v2.csv"
MODEL_FILE = ROOT / "models" / "best_model.pkl"
SELECTOR_FILE = ROOT / "models" / "variance_selector.pkl"
SCALER_FILE = ROOT / "models" / "scaler.pkl"
FEATURE_COLUMNS_FILE = ROOT / "models" / "feature_columns.pkl"
LABEL_ENCODER_FILE = ROOT / "models" / "label_encoder.pkl"

OUTPUT_FILE = ROOT / "reports" / "misclassification_examples.csv"

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

print("=" * 70)
print("REAL ROLE MISCLASSIFICATION AUDIT")
print("=" * 70)

df = pd.read_csv(DATASET)

print(f"\nRows Loaded       : {len(df)}")
print(f"Columns Loaded    : {len(df.columns)}")

label_encoder = joblib.load(LABEL_ENCODER_FILE)

y_raw = df["standard_title"].astype(str)
y = label_encoder.transform(y_raw)

X = df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns])

print(f"Feature Columns   : {X.shape[1]}")

# Same preprocessing used by train_model_v3
object_columns = X.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

print(f"Object Columns Encoded : {len(object_columns)}")

# Load feature encoders only if required
feature_encoders = joblib.load(
    ROOT / "models" / "feature_encoders.pkl"
)

for col in object_columns:
    encoder = feature_encoders[col]
    X[col] = encoder.transform(
        X[col].astype(str).fillna("missing")
    )

X = X.fillna(0)
X = X.apply(pd.to_numeric, errors="coerce")
X = X.fillna(0)

# EXACT project split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print(f"Train Rows        : {len(X_train)}")
print(f"Test Rows         : {len(X_test)}")

# Load CURRENT artifacts
feature_columns = joblib.load(FEATURE_COLUMNS_FILE)
selector = joblib.load(SELECTOR_FILE)
scaler = joblib.load(SCALER_FILE)
model = joblib.load(MODEL_FILE)

print("\nCURRENT ARTIFACTS")
print("-" * 70)
print(f"Model             : {MODEL_FILE}")
print(f"Model Type        : {type(model).__name__}")
print(f"Model Features    : {model.n_features_in_}")
print(f"Selector Features : {selector.get_support().sum()}")
print(f"Saved Raw Features: {len(feature_columns)}")

# Recreate exact raw feature order
X_train = X_train.reindex(
    columns=feature_columns,
    fill_value=0
)

X_test = X_test.reindex(
    columns=feature_columns,
    fill_value=0
)

# Same selector
X_train_selected = selector.transform(X_train)
X_test_selected = selector.transform(X_test)

print(f"Selected Features : {X_test_selected.shape[1]}")

# Same scaler
X_train_scaled = scaler.transform(X_train_selected)
X_test_scaled = scaler.transform(X_test_selected)

# CRITICAL CHECK
if model.n_features_in_ != X_test_scaled.shape[1]:
    raise ValueError(
        f"FEATURE MISMATCH: model expects "
        f"{model.n_features_in_}, but test data has "
        f"{X_test_scaled.shape[1]}"
    )

print("Feature compatibility : OK")

# Prediction
y_pred = model.predict(X_test_scaled)

actual = label_encoder.inverse_transform(y_test)
predicted = label_encoder.inverse_transform(y_pred)

# Preserve original rows
result = df.loc[
    X_test.index,
    ["job_id", "title", "standard_title"]
].copy()
result["actual_role"] = actual
result["predicted_role"] = predicted

result["correct"] = (
    result["actual_role"] == result["predicted_role"]
)

errors = result[result["correct"] == False].copy()

print("\n" + "=" * 70)
print("RESULT")
print("=" * 70)

print(f"Test Records          : {len(result)}")
print(f"Correct Predictions   : {result['correct'].sum()}")
print(f"Misclassified Records : {len(errors)}")

print("\nTOP 5 REAL MISCLASSIFICATIONS")
print("-" * 70)

for _, row in errors.head(5).iterrows():

    print(f"\nJob ID       : {row['job_id']}")
    print(f"Job Title    : {row['title']}")
    print(f"Actual Role  : {row['actual_role']}")
    print(f"Predicted    : {row['predicted_role']}")

    description = str(row["description"]).replace("\n", " ")

    print(
        "Description : "
        + description[:500]
    )

    print("-" * 70)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

errors.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"\nSaved misclassification file:")
print(OUTPUT_FILE)

print("\nAUDIT COMPLETE")
