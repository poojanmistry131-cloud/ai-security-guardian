"""
Module 1: Prompt Injection / Jailbreak Detector
Trains a TF-IDF + Logistic Regression classifier. 100% offline.
Run this from the project root: python app/train_prompt_injection.py
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "datasets", "prompt_injection_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
print(f"Total samples: {len(df)}")

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

print("Vectorizing text (TF-IDF)...")
vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print("\n--- Evaluation ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred, target_names=["benign", "malicious"]))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

joblib.dump(model, os.path.join(MODEL_DIR, "prompt_injection_model.pkl"))
joblib.dump(vectorizer, os.path.join(MODEL_DIR, "prompt_injection_vectorizer.pkl"))
print("\nSaved model -> models/prompt_injection_model.pkl")
print("Saved vectorizer -> models/prompt_injection_vectorizer.pkl")
