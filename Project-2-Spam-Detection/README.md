# Project-2-Spam-Detection

An end-to-end NLP pipeline that classifies emails as **spam** or **ham** (legitimate), built with TF-IDF feature extraction and classical machine learning models.

## Overview

This project implements a complete spam detection workflow on a labeled dataset of 5,171 emails (71.0% ham, 29.0% spam). It covers exploratory data analysis, text preprocessing, TF-IDF vectorization, training and comparing two classifiers, and packaging the best model into a reusable inference pipeline.

## Key Steps

1. **Exploratory Data Analysis (EDA)** — Inspected class balance (71.0% ham / 29.0% spam) and compared text length / word count distributions between spam and ham messages.
2. **Text Preprocessing** — Lowercased text, stripped the `Subject:` header prefix, removed numbers/punctuation/special characters, and normalized whitespace.
3. **Feature Extraction (TF-IDF)** — Converted cleaned text into numerical vectors with `TfidfVectorizer` (English stop words removed, `max_features=5000`).
4. **Model Training** — Trained two pipelines on an 80/20 stratified train-test split:
   - TF-IDF + **Multinomial Naive Bayes**
   - TF-IDF + **Logistic Regression**
5. **Evaluation** — Compared both models via classification reports and confusion matrices.

## Results

| Model | Accuracy | Ham Precision / Recall | Spam Precision / Recall |
|---|---|---|---|
| Multinomial Naive Bayes | 95.17% | 0.9737 / 0.9578 | 0.9006 / 0.9367 |
| **Logistic Regression** | **98.07%** | 0.9891 / 0.9837 | 0.9605 / 0.9733 |

**Logistic Regression was selected as the final model**, outperforming Naive Bayes across every metric. Its high ham recall (0.9837) translates to very few false positives — out of 735 ham messages in the test set, only about **12 legitimate emails were misclassified as spam**, which matters in practice since false positives (losing real emails to a spam filter) are usually costlier than false negatives.

## Project Structure

```
Project-2-Spam-Detection/
├── spam_ham_dataset.csv           # Labeled email dataset (5,171 rows)
├── NLP_Spam_Classifier.ipynb      # Full notebook: EDA -> preprocessing -> training -> evaluation
├── spam_classifier_pipeline.joblib # Saved TF-IDF + Logistic Regression pipeline
├── README.md
└── pyproject.toml
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ssargsyann/Project-2-Spam-Detection.git
   cd Project-2-Spam-Detection
   ```
2. Install dependencies (Python 3.10+):
   ```bash
   pip install .
   ```
   Or, if you prefer a virtual environment first:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install .
   ```
3. Launch the notebook to reproduce the analysis:
   ```bash
   jupyter notebook NLP_Spam_Classifier.ipynb
   ```

## Running Inference

The trained pipeline (`spam_classifier_pipeline.joblib`) bundles the TF-IDF vectorizer and the Logistic Regression classifier together, so it can classify raw text directly — no separate preprocessing step is required at inference time beyond the same cleaning function used during training.

```python
import joblib

# Load the saved pipeline
pipeline = joblib.load("spam_classifier_pipeline.joblib")

# Example emails
emails = [
    "URGENT! You have won a $1,000,000 cash prize. Claim your reward immediately by clicking here!",
    "Hi, could you please send me the updated project report by tomorrow morning?"
]

predictions = pipeline.predict(emails)
probabilities = pipeline.predict_proba(emails)[:, 1]  # spam probability

for email, pred, prob in zip(emails, predictions, probabilities):
    label = "Spam" if pred == 1 else "Ham"
    print(f"[{label}] ({prob:.1%} spam probability) — {email[:60]}...")
```

> **Note:** For best results on raw, unprocessed email text, apply the same `clean_text()` cleaning function used in the notebook before passing text to the pipeline.

## Author

**Sargis Sargsyan**
Python / Machine Learning Engineer
*SyntecXHub Virtual Internship — Project 2*
