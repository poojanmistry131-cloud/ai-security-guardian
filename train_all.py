"""
Runs all dataset generation + training steps in one go.
Fully offline. Run this once before starting the app.

Usage:
    python train_all.py
"""
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

steps = [
    ("Generating dataset: Prompt Injection", ["datasets/make_prompt_injection_dataset.py"], "datasets"),
    ("Generating dataset: AI-Generated Text", ["datasets/make_ai_text_dataset.py"], "datasets"),
    ("Generating dataset: Phishing URLs", ["datasets/make_phishing_url_dataset.py"], "datasets"),
    ("Training Module 1: Prompt Injection Detector", ["app/train_prompt_injection.py"], BASE_DIR),
    ("Training Module 2: AI-Generated Text Detector", ["app/train_ai_text.py"], BASE_DIR),
    ("Training Module 3: Phishing URL Detector", ["app/train_phishing_url.py"], BASE_DIR),
]

for title, script, cwd in steps:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    script_path = script[0]
    if cwd == "datasets":
        run_cwd = os.path.join(BASE_DIR, "datasets")
        script_name = os.path.basename(script_path)
        result = subprocess.run([sys.executable, script_name], cwd=run_cwd)
    else:
        result = subprocess.run([sys.executable, script_path], cwd=BASE_DIR)
    if result.returncode != 0:
        print(f"\nStep failed: {title}")
        sys.exit(1)

print("\n" + "=" * 60)
print("All 3 modules trained successfully!")
print("Run the app now with: python app/app.py")
print("=" * 60)
