# Customer Churn Prediction

## 📌 Project Overview

This project predicts whether a telecom customer is likely to churn using machine learning.

The project includes data preprocessing, exploratory data analysis, machine learning model training, and a Streamlit dashboard for making predictions.

## 📂 Project Structure

```text
Customer_Churn_Project/
├── .streamlit/
├── dashboard/
│   └── app.py
├── data/
│   ├── processed/
│   └── raw/
├── models/
│   ├── logistic_regression_model.joblib
│   └── preprocessing.joblib
├── notebooks/
│   └── 01_data_inspection.ipynb
└── src/
```

## 🤖 Machine Learning

The project uses a **Logistic Regression** model to predict customer churn.

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Jupyter Notebook
* Joblib

## 📊 Dataset

The project uses the Telco Customer Churn dataset for analysis and prediction.

## 🚀 Run the Dashboard

First install the required Python packages:

```bash
pip install -r requirements.txt
```

Then run the Streamlit application:

```bash
streamlit run dashboard/app.py
```

## 🎯 Goal

The goal of this project is to identify customers who are likely to leave a telecom service so that businesses can take steps to retain them.
