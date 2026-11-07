# AI Security Guardian

A fully offline AI/ML security dashboard combining **3 independently trained machine learning models**:

| # | Module | Task | Model | Features |
|---|--------|------|-------|----------|
| 1 | Prompt Injection Detector | Detects LLM jailbreak / prompt injection attempts | TF-IDF + Logistic Regression | Text (TF-IDF, 1-2 grams) |
| 2 | AI-Generated Text Detector | Classifies text as human-written vs AI-generated | TF-IDF + Logistic Regression | Text (TF-IDF, 1-2 grams) |
| 3 | Phishing URL Detector | Flags phishing vs legitimate URLs | XGBoost | 11 handcrafted URL features |

Everything — dataset generation, training, and the web dashboard — runs **100% locally**, no internet/API calls needed after the one-time `pip install`.

---

## 1. Setup (one-time, needs internet)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## 2. Train all 3 models (fully offline)

```bash
python train_all.py
```

This will:
1. Generate 3 datasets locally (`datasets/*.csv`) — no downloads, pure Python generation
2. Train all 3 models and save them to `models/`
3. Print accuracy, precision/recall, and confusion matrix for each module

Pre-trained model files are already included in `models/` as a backup — if training
ever fails on your machine for any reason, the app will still work using those.

## 3. Run the app (fully offline)

```bash
python app/app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## Project Structure

```
ai-security-guardian/
├── datasets/
│   ├── make_prompt_injection_dataset.py   # generates prompt_injection_dataset.csv
│   ├── make_ai_text_dataset.py            # generates ai_text_dataset.csv
│   ├── make_phishing_url_dataset.py       # generates phishing_url_dataset.csv
├── app/
│   ├── train_prompt_injection.py          # trains Module 1
│   ├── train_ai_text.py                   # trains Module 2
│   ├── train_phishing_url.py              # trains Module 3
│   ├── app.py                             # Flask app (loads all 3 models)
│   └── templates/index.html               # dashboard UI
├── models/                                # saved .pkl model files
├── train_all.py                           # runs everything in one command
├── requirements.txt
└── README.md
```

## How each module works (for your viva/verification)

**Module 1 — Prompt Injection Detector**
- Dataset: labeled examples of jailbreak-style prompts ("ignore previous instructions...",
  "you are DAN...", etc.) vs normal/benign prompts.
- Text is converted to numeric vectors using **TF-IDF** (term frequency–inverse document
  frequency) with unigrams + bigrams.
- A **Logistic Regression** classifier is trained on these vectors to output
  malicious/benign with a confidence score.

**Module 2 — AI-Generated Text Detector**
- Dataset: AI-style text (formal, hedging, structured with "in conclusion", "furthermore",
  numbered points) vs human-style text (casual, contractions, informal tone).
- Same TF-IDF + Logistic Regression pipeline as Module 1, trained on a separate dataset.

**Module 3 — Phishing URL Detector**
- Instead of raw text, 11 numeric features are extracted from each URL: length, number
  of dots, presence of `@`, HTTPS usage, IP-address hostname, hyphen count, subdomain
  count, count of suspicious words (verify/secure/login/etc.), suspicious TLD
  (.xyz/.tk/.top/etc.), URL path depth, and presence of query parameters.
- An **XGBoost** classifier is trained on these features.
- Feature importance is printed after training so you can explain *why* the model
  flags a URL (useful for viva questions).

## Notes on the datasets

The datasets are **synthetically generated** using rule-based templates (see the
`datasets/make_*.py` scripts) rather than downloaded from the internet, so the whole
project works with zero internet dependency at run/train time. This is worth mentioning
in your report: real-world deployment would use larger, human-labeled datasets
(e.g. public jailbreak-prompt collections, the HC3 human-vs-AI corpus, or the
UCI/Kaggle phishing URL datasets), but the same pipeline (TF-IDF/feature extraction →
classical ML classifier → Flask serving layer) would apply unchanged.

## Extending this project (optional, mention in report as "future work")

- Add a 4th module (e.g. toxic content classifier or malware feature classifier)
- Swap Logistic Regression for a fine-tuned DistilBERT for higher accuracy
- Add SHAP explainability to show which words/features triggered a prediction
- Persist scan history to a local SQLite database
