print("=" * 78)
print("10.3 MODEL EVALUATION – CONSOLIDATED VALIDATION SUMMARY")
print("=" * 78)

print("\nEVALUATION FRAMEWORK")
print("-" * 78)
print("Training Records       : 160")
print("Independent Test Rows  : 40")
print("Target Classes         : 6")
print("Cross-Validation       : Stratified 5-Fold")
print("Primary Metrics        : Accuracy, Precision, Recall, F1-Score")

print("\nVALIDATION COMPONENTS")
print("-" * 78)
print("[1] Cross-Validation Performance")
print("[2] Held-Out Test Performance")
print("[3] Class-Level Precision / Recall / F1")
print("[4] Confusion Matrix")
print("[5] Misclassification Analysis")

print("\nMODEL VALIDATION FLOW")
print("-" * 78)

print("Final Feature Matrix")
print("        ↓")
print("Train / Test Separation")
print("        ↓")
print("Stratified 5-Fold Cross-Validation")
print("        ↓")
print("Held-Out Test Evaluation")
print("        ↓")
print("Classification Metrics")
print("        ↓")
print("Confusion Matrix")
print("        ↓")
print("Misclassification Analysis")

print("\nVALIDATION CONCLUSION")
print("-" * 78)

print(
    "The classification system was evaluated using multiple complementary "
    "validation measures rather than relying on a single performance metric. "
    "Cross-validation assessed model stability, the independent test set "
    "measured generalization performance, and the confusion matrix and "
    "misclassification analysis identified class-specific prediction errors."
)

print("\n" + "=" * 78)
print("10.3 CONSOLIDATED MODEL EVALUATION COMPLETE")
print("=" * 78)