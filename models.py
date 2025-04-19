# models.py
# Trains Random Forest classifier for email type prediction
# Handles Incident, Request, Problem, Change
# Author: Dhanush
# Date: April 19, 2025

import pandas as pd
import logging
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline
import joblib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Dataset loaded successfully. Shape: {df.shape}")
        logger.info(f"Type counts:\n{df['type'].value_counts()}")
        return df
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        exit(1)

def train_model():
    df = load_data("emails_masked.csv")
    X = df["email_masked"]
    y = df["type"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline = make_pipeline(TfidfVectorizer(max_features=5000), RandomForestClassifier(n_estimators=100, random_state=42))
    
    logger.info("Training Random Forest...")
    pipeline.fit(X_train, y_train)
    
    logger.info("Evaluating Random Forest...")
    y_pred = pipeline.predict(X_test)
    report = classification_report(y_test, y_pred)
    logger.info(f"Classification Report:\n{report}")

    joblib.dump(pipeline, "rf_model.pkl")
    logger.info("Model saved to rf_model.pkl")

if __name__ == "__main__":
    train_model()