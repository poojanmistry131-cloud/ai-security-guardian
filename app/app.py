"""
AI Security Guardian - Flask App
Integrates 3 offline-trained ML modules:
  1. Prompt Injection / Jailbreak Detector
  2. AI-Generated Text Detector
  3. Phishing URL Detector
Run: python app/app.py   (then open http://127.0.0.1:5000 in browser)
100% offline - no external API calls, no internet needed after models are trained.
"""
from flask import Flask, render_template, request, jsonify
import joblib
import os
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

app = Flask(__name__)

# A fresh random ID generated every time the server starts.
# The frontend compares this against what it has stored — if it
# doesn't match, it means the server restarted, so all local
# history/stats get wiped for a clean slate.
SESSION_ID = str(uuid.uuid4())

# ---------- Load all models once at startup ----------
def safe_load(path):
    if os.path.exists(path):
        return joblib.load(path)
    return None

pi_model = safe_load(os.path.join(MODEL_DIR, "prompt_injection_model.pkl"))
pi_vectorizer = safe_load(os.path.join(MODEL_DIR, "prompt_injection_vectorizer.pkl"))

ai_model = safe_load(os.path.join(MODEL_DIR, "ai_text_model.pkl"))
ai_vectorizer = safe_load(os.path.join(MODEL_DIR, "ai_text_vectorizer.pkl"))

url_model = safe_load(os.path.join(MODEL_DIR, "phishing_url_model.pkl"))
url_features = safe_load(os.path.join(MODEL_DIR, "phishing_url_features.pkl"))

SUSPICIOUS_WORDS = ["secure", "verify", "update", "login", "account", "confirm",
                     "signin", "webscr", "banking", "alert", "suspend", "reward"]
SUSPICIOUS_TLDS = [".xyz", ".tk", ".ml", ".ga", ".cf", ".top", ".info", ".click"]


def extract_url_features(url):
    length = len(url)
    num_dots = url.count(".")
    has_at = int("@" in url)
    has_https = int(url.startswith("https://"))
    host = url.split("//")[-1].split("/")[0]
    host_parts = host.split(".")
    has_ip = int(all(p.isdigit() for p in host_parts) and len(host_parts) == 4)
    num_hyphens = url.count("-")
    num_subdomains = host.count(".")
    suspicious_word_count = sum(1 for w in SUSPICIOUS_WORDS if w in url.lower())
    has_suspicious_tld = int(any(url.lower().endswith(t) or f"{t}/" in url.lower() for t in SUSPICIOUS_TLDS))
    url_depth = url.count("/") - 2 if url.count("/") > 2 else 0
    has_query = int("?" in url)
    return [[length, num_dots, has_at, has_https, has_ip, num_hyphens,
             num_subdomains, suspicious_word_count, has_suspicious_tld,
             url_depth, has_query]]


@app.route("/")
def home():
    return render_template("index.html", session_id=SESSION_ID)


@app.route("/api/check-prompt", methods=["POST"])
def check_prompt():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "Please enter some text."}), 400
    if pi_model is None:
        return jsonify({"error": "Model not trained yet. Run train_prompt_injection.py first."}), 500

    vec = pi_vectorizer.transform([text])
    pred = pi_model.predict(vec)[0]
    proba = pi_model.predict_proba(vec)[0]
    confidence = round(float(max(proba)) * 100, 2)
    label = "⚠️ Prompt Injection / Jailbreak Detected" if pred == 1 else "✅ Safe Prompt"
    return jsonify({
        "result": label,
        "malicious": bool(pred),
        "confidence": confidence,
        "proba": {"safe": round(float(proba[0]) * 100, 2), "malicious": round(float(proba[1]) * 100, 2)}
    })


@app.route("/api/check-ai-text", methods=["POST"])
def check_ai_text():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "Please enter some text."}), 400
    if ai_model is None:
        return jsonify({"error": "Model not trained yet. Run train_ai_text.py first."}), 500

    vec = ai_vectorizer.transform([text])
    pred = ai_model.predict(vec)[0]
    proba = ai_model.predict_proba(vec)[0]
    confidence = round(float(max(proba)) * 100, 2)
    label = "🤖 Likely AI-Generated" if pred == 1 else "🧑 Likely Human-Written"
    return jsonify({
        "result": label,
        "ai_generated": bool(pred),
        "confidence": confidence,
        "proba": {"human": round(float(proba[0]) * 100, 2), "ai": round(float(proba[1]) * 100, 2)}
    })


@app.route("/api/check-url", methods=["POST"])
def check_url():
    url = request.json.get("url", "").strip()
    if not url:
        return jsonify({"error": "Please enter a URL."}), 400
    if not url.startswith("http"):
        url = "http://" + url
    if url_model is None:
        return jsonify({"error": "Model not trained yet. Run train_phishing_url.py first."}), 500

    features = extract_url_features(url)
    pred = url_model.predict(features)[0]
    proba = url_model.predict_proba(features)[0]
    confidence = round(float(max(proba)) * 100, 2)
    label = "🚨 Phishing URL Detected" if pred == 1 else "✅ Legitimate URL"
    f = features[0]
    feature_map = {
        "URL length": f[0],
        "Number of dots": f[1],
        "Has @ symbol": f[2],
        "Uses HTTPS": f[3],
        "Is raw IP address": f[4],
        "Number of hyphens": f[5],
        "Subdomain count": f[6],
        "Suspicious word count": f[7],
        "Suspicious TLD": f[8],
        "URL path depth": f[9],
        "Has query params": f[10],
    }
    return jsonify({
        "result": label,
        "phishing": bool(pred),
        "confidence": confidence,
        "proba": {"legit": round(float(proba[0]) * 100, 2), "phishing": round(float(proba[1]) * 100, 2)},
        "features": feature_map
    })


if __name__ == "__main__":
    print("\n===== AI Security Guardian =====")
    print("Module 1 (Prompt Injection):", "Loaded" if pi_model else "NOT TRAINED")
    print("Module 2 (AI Text Detector):", "Loaded" if ai_model else "NOT TRAINED")
    print("Module 3 (Phishing URL):    ", "Loaded" if url_model else "NOT TRAINED")
    print("Open http://127.0.0.1:5000 in your browser\n")
    app.run(debug=True, port=5000)
