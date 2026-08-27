# 🏠 House Price Prediction

**SyntecXHub Virtual Internship — Project 1**

A machine learning project that predicts California housing prices using Linear Regression, based on the classic California Housing dataset. The project covers the full ML pipeline: data cleaning, exploratory data analysis (EDA), geospatial visualization, feature engineering, model training, and evaluation.

---

## 📌 Problem Statement & Objectives

Housing prices depend on a combination of geographic, demographic, and economic factors. The objective of this project is to:

- Build a regression model that predicts the **median house value** of a California district (block group) based on features such as location, income, population, and housing characteristics.
- Perform thorough data cleaning and exploratory analysis to understand feature relationships.
- Evaluate model performance using standard regression metrics (RMSE, R²).
- Interpret which features have the greatest influence on housing prices via coefficient analysis.
- Persist the trained model for future inference/deployment.

---

## 🛠️ Tech Stack & Libraries Used

| Category | Tools |
|---|---|
| Language | Python 3 |
| Data Handling | pandas, numpy |
| Visualization | matplotlib, seaborn, folium |
| Machine Learning | scikit-learn |
| Model Persistence | joblib |
| Environment | Jupyter Notebook |

---

## 🔄 Step-by-Step Workflow

### 1. Data Loading & Cleaning
- Loaded the `housing.csv` dataset (20,640 rows × 10 columns).
- Inspected data types and missing values with `data.info()`.
- Found 207 missing values in `total_bedrooms`; removed them using `dropna()`, resulting in a clean dataset of 20,433 rows.

### 2. Train/Test Split
- Split features (`X`) and target (`y = median_house_value`).
- Used `train_test_split` with `test_size=0.2` and `random_state=42` for reproducibility.

### 3. Exploratory Data Analysis (EDA)
- Plotted histograms for all numerical features to inspect distributions.
- Visualized geographic density of housing districts using a **Folium heatmap** (latitude/longitude).
- Generated a **correlation heatmap** (Seaborn) on the training set to identify relationships between numeric features and the target variable.
- Analyzed the categorical feature `ocean_proximity` (5 categories: `<1H OCEAN`, `INLAND`, `NEAR OCEAN`, `NEAR BAY`, `ISLAND`) via value counts.

### 4. Feature Engineering & Preprocessing
- One-hot encoded the categorical `ocean_proximity` feature using `pd.get_dummies()`.
- Aligned train/test columns after encoding using `.align()` to ensure consistent feature sets (`fill_value=0`).
- Imputed any remaining missing values using `SimpleImputer(strategy='median')`.
- Scaled all features using `StandardScaler` for normalized input to the linear model.

### 5. Model Training
- Trained a **Linear Regression** model (`sklearn.linear_model.LinearRegression`) on the scaled training data.

### 6. Model Evaluation
- Evaluated the model on the held-out test set using:
  - **RMSE** (Root Mean Squared Error)
  - **R² Score** (coefficient of determination)

### 7. Model Export
- Saved the trained model as `linear_regression_model.pkl` using `joblib`.
- Generated example predictions comparing actual vs. predicted prices.

---

## 📊 Model Training & Performance Metrics

| Metric | Value |
|---|---|
| **RMSE** | ~$69,297.72 |
| **R² Score** | 0.6488 |

**Interpretation:** The model explains approximately **65% of the variance** in median house values, with an average prediction error of roughly **$69,300**.

### Sample Predictions

| Actual Price | Predicted Price |
|---|---|
| $245,800 | $201,882.96 |
| $137,900 | $147,279.68 |
| $218,200 | $207,796.61 |
| $220,800 | $180,487.58 |
| $170,500 | $190,323.92 |

---

## 🔍 Key Insights & Feature Importance (Coefficient Analysis)

Coefficients from the trained Linear Regression model (on standardized features), sorted by impact:

| Feature | Coefficient | Effect |
|---|---|---|
| `median_income` | +74,538.74 | **Strongest positive driver** — higher income areas → higher prices |
| `total_bedrooms` | +42,999.85 | Positive |
| `households` | +16,307.34 | Positive |
| `housing_median_age` | +13,600.09 | Positive (older neighborhoods, likely closer to city centers) |
| `ocean_proximity_ISLAND` | +2,894.17 | Slight positive |
| `ocean_proximity_NEAR OCEAN` | +1,062.55 | Slight positive |
| `ocean_proximity_NEAR BAY` | -1,970.76 | Slight negative |
| `total_rooms` | -13,613.10 | Negative |
| `ocean_proximity_INLAND` | -18,234.40 | Negative — inland location reduces value |
| `population` | -41,119.07 | Negative |
| `longitude` | -54,375.71 | Strong negative |
| `latitude` | -54,808.04 | **Strongest negative driver** — geographic location strongly shapes price |

**Key Takeaways:**
1. **Median income** is by far the strongest predictor of house value — wealthier areas command higher prices.
2. **Location** (`latitude`, `longitude`, and `ocean_proximity`) plays a major role, confirming the real-estate principle of "location, location, location."
3. Properties located **inland** are associated with notably lower prices than coastal ones.

---

## 🚀 How to Run the Project Locally

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/house-price-prediction.git
cd house-price-prediction
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add the dataset
Place the `housing.csv` file (California Housing dataset) in the project root directory.

### 5. Run the notebook
```bash
jupyter notebook house_price_prediction.ipynb
```

---

## 📁 Repository Structure

```
house-price-prediction/
│
├── house_price_prediction.ipynb   # Main Jupyter Notebook (full pipeline)
├── housing.csv                    # Dataset (California Housing data)
├── linear_regression_model.pkl    # Saved trained model (joblib export)
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## 📈 Future Improvements

- Experiment with more advanced models (Random Forest, Gradient Boosting, XGBoost) to improve R² beyond 0.65.
- Apply feature engineering such as `rooms_per_household`, `bedrooms_per_room`, and `population_per_household`.
- Perform hyperparameter tuning and cross-validation for more robust evaluation.
- Handle outliers and skewed distributions (e.g., log-transform `median_house_value`).

---

## 👤 Author

**Sargis Sargsyan**
Python / Machine Learning Engineer
*SyntecXHub Virtual Internship — Project 1*
