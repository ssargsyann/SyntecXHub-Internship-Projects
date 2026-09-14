# Credit Card Fraud Detection

**Sargis Sargsyan | SyntecXHub — Project-3 (Financial Fraud Detection)**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Model](https://img.shields.io/badge/model-XGBoost-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)

A machine learning pipeline that detects fraudulent mobile-money / credit-card
transactions under severe class imbalance (only **0.3%** of transactions are
fraudulent). The project compares Random Forest and XGBoost, applies SMOTE to
address class imbalance, and tunes the decision threshold to meet a
business-driven precision/recall trade-off.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Quick Start / Inference](#quick-start--inference)
- [Methodology](#methodology)
- [Results](#results)
- [Decision Threshold Optimization](#decision-threshold-optimization)
- [Visuals](#visuals)
- [License](#license)
- [Author](#author)

---

## Project Overview

The goal of this project is to build an ML model that reliably flags
fraudulent transactions while keeping false alarms (and the resulting
customer friction) as low as possible. The pipeline covers:

1. **Exploratory Data Analysis (EDA)** — inspect the dataset, check for
   missing values/duplicates, and quantify the class imbalance.
2. **Preprocessing & Sampling** — train/test split, then address the
   imbalance via undersampling, oversampling, and **SMOTE**.
3. **Model Training & Evaluation** — train **Random Forest** and
   **XGBoost**, and evaluate with Precision, Recall, F1-Score, and ROC-AUC.
4. **Business Decision Thresholds** — analyze the precision/recall
   trade-off and select an optimal classification threshold.

A critical **ablation study** removed synthetic `errorBalanceOrig` /
`errorBalanceDest` features that were causing data leakage (and an
unrealistic 100% precision/recall), ensuring the final model is evaluated
only on non-leaked features (`amount`, `oldbalance`, `newbalance`, `type`,
etc.) for a realistic, production-safe performance estimate.

## Dataset

This project uses the **PaySim synthetic mobile-money fraud dataset**
(~6.36M transactions, 11 columns, target column `isFraud`).

- **Source:** [PaySim — Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1)

The dataset is not bundled with this repository due to its size. To use it:

```bash
mkdir -p data
# Download PaySim1 (Kaggle account + API token required)
kaggle datasets download -d ealaxi/paysim1 -p data --unzip
```

## Repository Structure

```
Project-3-Fraud_Detection/
├── data/                                  # PaySim dataset (downloaded, not versioned)
├── models/
│   └── fraud_detection_xgb.pkl            # Trained XGBoost model + threshold + feature list
├── notebooks/
│   └── Financial_Fraud_Detection.ipynb    # Full EDA -> training -> evaluation pipeline
├── src/
│   └── predict.py                         # Standalone inference module (predict_fraud)
├── pyproject.toml
└── README.md
```

## Installation

```bash
# Clone the repository
git clone https://github.com/sargissargsyan/Project-3-Fraud_Detection.git
cd Project-3-Fraud_Detection

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the project and its dependencies
pip install -e .

# Optional: notebook / dev extras
pip install -e ".[notebook]"
pip install -e ".[dev]"
```

## Quick Start / Inference

Once `models/fraud_detection_xgb.pkl` exists (produced by running the
notebook), you can score a single transaction with the extracted
`predict_fraud` function in `src/predict.py`:

```python
from predict import predict_fraud

sample_transaction = {
    "step": 1,
    "amount": 181.0,
    "oldbalanceOrg": 181.0,
    "newbalanceOrig": 0.0,
    "oldbalanceDest": 0.0,
    "newbalanceDest": 0.0,
    "type_TRANSFER": True,
}

result = predict_fraud(sample_transaction, model_path="models/fraud_detection_xgb.pkl")
print(result)
# {'is_fraud': True, 'fraud_probability': 0.9917, 'action': 'BLOCK / REVIEW'}
```

Or, after installing the package, use the CLI entry point:

```bash
predict-fraud
```

## Methodology

| Stage | Techniques |
| :--- | :--- |
| EDA | Missing-value/duplicate checks, class-imbalance visualization |
| Preprocessing | Train/test split, undersampling, oversampling, **SMOTE** |
| Modeling | Random Forest, **XGBoost** |
| Evaluation | Precision, Recall, F1-Score, ROC-AUC, PR-AUC, confusion matrix |
| Leakage control | Ablation study removing synthetic error-balance features |
| Deployment prep | Threshold tuning, model + threshold + feature list serialized with `joblib` |

## Results

Final performance on the held-out test set:

| Metric | Score | Description / Impact |
| :--- | :---: | :--- |
| **Precision** | **93.23%** | High reliability of flagged transactions (minimal false alarms) |
| **Recall** | **88.01%** | Successfully detected **1,446** out of **1,643** actual frauds |
| **F1-Score** | **0.9054** | Excellent balance between Precision and Recall |
| **PR-AUC** | **0.9594** | Outstanding overall capability on imbalanced data |

**Verdict:** the model is production-ready — it captures **88%** of all
fraudulent transactions while keeping the false-positive rate around
**0.02%**, maximizing security with minimal disruption to legitimate
customers.

## Decision Threshold Optimization

The default classification threshold of **0.50** was tuned to an optimal
**0.8465** using the Precision-Recall curve:

| Threshold | False Positives (legit blocked) | Precision |
| :--- | :---: | :---: |
| 0.50 (default) | 1,176 | 57.50% |
| 0.8465 (optimal) | 105 | 93.23% |

This is roughly a **91% reduction** in unnecessary customer friction, at a
threshold selected specifically to match the business's tolerance for
false positives vs. missed fraud.

## Visuals

**Confusion Matrix (optimal threshold)**

![Confusion Matrix](images/confusion_matrix.png)

**Precision-Recall Curve**

![Precision-Recall Curve](images/pr_curve.png)

> Export these two plots from the notebook into an `images/` folder at the
> repo root for them to render here.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file
for details.

## Author

**Sargis Sargsyan**
Machine Learning Intern, SyntecXHub
GitHub: [@sargissargsyan]
Repository: [Project-3-Fraud_Detection]
