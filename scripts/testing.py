# Test Script for Astra IRCTC Bot Detector
# This script loads a pre-trained model and evaluates it on the 20% test set.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
import logging
import seaborn as sns
import matplotlib.pyplot as plt

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_artifacts_and_test_data(data_path='../data/tatkal.csv'):
    """
    Loads the saved model, scaler, feature list, and the specific 20% test data split.
    """
    try:
        logger.info("Loading saved model and artifacts from 'models' directory...")
        model = joblib.load('../models/astra_model.joblib')
        scaler = joblib.load('../models/astra_scaler.joblib')
        feature_columns = joblib.load('../models/feature_columns.joblib')
        logger.info("Artifacts loaded successfully.")

        df = pd.read_csv(data_path)
        X = df[feature_columns]
        y = df['is_bot']

        # Recreate the exact same train-test split to isolate the test set
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        logger.info(f"Test data isolated successfully. Shape: {X_test.shape}")
        
        return model, scaler, X_test, y_test

    except FileNotFoundError as e:
        logger.error(f"Error: A required file was not found. {e}")
        logger.error("Please ensure you have run the training script first to generate the model files.")
        raise
    except Exception as e:
        logger.error(f"An error occurred during loading: {e}")
        raise

def main():
    """
    Main function to run the test script.
    """
    logger.info("--- Starting Astra Model Test Script ---")
    
    try:
        model, scaler, X_test, y_test = load_artifacts_and_test_data()
        
        # Scale the test data using the loaded scaler
        X_test_scaled = scaler.transform(X_test)
        
        logger.info("Making predictions on the held-out test set...")
        y_pred = model.predict(X_test_scaled)
        
        # --- Evaluation Metrics ---
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=['Human', 'Bot'])
        
        # --- Final Test Report ---
        print("\n" + "="*60)
        print("      ASTRA MODEL TEST SET EVALUATION")
        print("="*60)
        print(f"Model: ../models/astra_model.joblib")
        print(f"Test Samples: {len(X_test)}")
        print("\n--- PERFORMANCE ON UNSEEN DATA ---")
        print(f"  Accuracy:  {accuracy:.4f}  ({accuracy*100:.2f}%)")
        print(f"  Precision: {precision:.4f}  ({precision*100:.2f}%)")
        print(f"  Recall:    {recall:.4f}  ({recall*100:.2f}%)")
        print(f"  F1-Score:  {f1:.4f}  ({f1*100:.2f}%)")
        print("\n--- CLASSIFICATION REPORT ---")
        print(report)
        
        # --- Confusion Matrix Visualization ---
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Human', 'Bot'], yticklabels=['Human', 'Bot'])
        plt.title('Confusion Matrix on Test Data')
        plt.ylabel('Actual Label')
        plt.xlabel('Predicted Label')
        plt.show()
        
        print("\n✅ Testing complete.")

    except Exception as e:
        logger.error(f"An error occurred during the testing process: {e}")

if __name__ == "__main__":
    main()
