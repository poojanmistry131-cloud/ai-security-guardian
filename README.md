# AI Security Guardian

An offline web dashboard with three machine-learning detectors: prompt injection, AI-generated text, and phishing URLs. The app runs on your computer and does not send scan inputs to an external API.

## How to Run (For Beginners)

### Before you start

- Install Python 3 from [python.org](https://www.python.org/downloads/). On Windows, enable **Add Python to PATH** in the installer.
- Install [VS Code](https://code.visualstudio.com/) if you do not already have it.
- Internet is needed once to install the Python packages. After setup, the dashboard runs locally.

### 1. Download the project

**Option A: Download ZIP**

1. Open this repository on GitHub.
2. Click **Code**, then **Download ZIP**.
3. Extract the ZIP and open the extracted `ai-security-guardian` folder in VS Code.

**Option B: Clone with Git**

```bash
git clone https://github.com/poojanmistry131-cloud/ai-security-guardian.git
cd ai-security-guardian
```

### 2. Open the project folder in VS Code

Open the folder containing `requirements.txt`, `train_all.py`, and the `app`, `datasets`, and `models` folders. Open the VS Code terminal with **Ctrl + `**.

### 3. Create and activate a virtual environment

On Windows PowerShell:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the dashboard

```bash
python app/app.py
```

Open **http://127.0.0.1:5000** in your browser. Keep the terminal open while using the app; press **Ctrl + C** in the terminal to stop it.

## Features

- **Prompt Injection Detector** - classifies text as benign or a possible prompt injection.
- **AI-Generated Text Detector** - classifies text as human-written or AI-generated.
- **Phishing URL Detector** - classifies a URL using URL structure and other handcrafted features.
- **Local dashboard** - runs locally after dependencies are installed; no external API is required for scans.

## Requirements

- Python 3
- Packages listed in `requirements.txt` (Flask, scikit-learn, XGBoost, and supporting libraries)
- A browser to open the local dashboard

## Train the models (Optional)

Pre-trained model files are included in `models/`, so you can run the app without training. To regenerate the synthetic datasets and train all three models, run this from the project root:

```bash
python train_all.py
```

Training prints evaluation metrics and saves the resulting models in `models/`.

## How the detectors work

- **Prompt injection:** TF-IDF text features and a Logistic Regression classifier.
- **AI-generated text:** a separate TF-IDF and Logistic Regression pipeline.
- **Phishing URL:** handcrafted URL features evaluated with an XGBoost classifier.

The datasets are generated locally from rule-based templates. They are intended for a project demonstration, not as evidence of real-world detection accuracy or as a production security control.

## Project Structure

```text
ai-security-guardian/
|-- app/
|   |-- app.py
|   |-- train_ai_text.py
|   |-- train_phishing_url.py
|   |-- train_prompt_injection.py
|   `-- templates/index.html
|-- datasets/
|   |-- ai_text_dataset.csv
|   |-- phishing_url_dataset.csv
|   |-- prompt_injection_dataset.csv
|   `-- make_*.py
|-- models/                 # Pre-trained model files
|-- train_all.py
|-- requirements.txt
`-- README.md
```

## Common Problems

- **`python` is not recognized:** install Python and enable **Add Python to PATH**, then reopen the terminal. On Windows, try `py` instead of `python`.
- **`pip` is not recognized:** use `python -m pip install -r requirements.txt` from the project root.
- **`No such file or directory: requirements.txt`:** the terminal is not in the project root. Change directory until `requirements.txt` is visible.
- **`ModuleNotFoundError`:** activate the project's virtual environment and run `python -m pip install -r requirements.txt` again.
- **PowerShell blocks environment activation:** run `venv\Scripts\python.exe -m pip install -r requirements.txt`, then start the app with `venv\Scripts\python.exe app\app.py`.
- **The page does not load:** make sure `python app/app.py` is still running, then open `http://127.0.0.1:5000`.
