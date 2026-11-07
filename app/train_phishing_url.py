"""
Module 3: Phishing URL Detector
Trains an XGBoost classifier on hand-crafted URL features. 100% offline.
Run this from the project root: python app/train_phishing_url.py
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from xgboost import XGBClassifier
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "datasets", "phishing_url_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
print(f"Total samples: {len(df)}")

FEATURE_COLS = [
    "url_length", "num_dots", "has_at_symbol", "has_https", "has_ip_address",
    "num_hyphens", "num_subdomains", "suspicious_word_count",
    "has_suspicious_tld", "url_depth", "has_query_params",
]

X = df[FEATURE_COLS]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training XGBoost model...")
model = XGBClassifier(
    n_estimators=200, max_depth=4, learning_rate=0.1,
    eval_metric="logloss", random_state=42
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\n--- Evaluation ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred, target_names=["legit", "phishing"]))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

print("\nFeature importances:")
for feat, imp in sorted(zip(FEATURE_COLS, model.feature_importances_), key=lambda x: -x[1]):
    print(f"  {feat}: {imp:.4f}")

joblib.dump(model, os.path.join(MODEL_DIR, "phishing_url_model.pkl"))
joblib.dump(FEATURE_COLS, os.path.join(MODEL_DIR, "phishing_url_features.pkl"))
print("\nSaved model -> models/phishing_url_model.pkl")
