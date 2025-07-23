# Train Model for Astra IRCTC Bot Detector
# This script is responsible ONLY for training the model and saving the artifacts.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(filepath='../data/tatkal.csv'):
    """Load the enhanced dataset."""
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Enhanced dataset loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"Error: The data file '{filepath}' was not found. Please run the feature enhancement script first.")
        raise

def train_and_save_artifacts(df):
    """
    Prepares data, trains the model, and saves all necessary artifacts.
    """
    try:
        # 1. Define Features and Target
        feature_columns = [col for col in df.columns if col != 'is_bot']
        X = df[feature_columns]
        y = df['is_bot']
        logger.info(f"Using {len(feature_columns)} features for training.")

        # 2. Split data into 80% training and 20% testing
        # We create the split here but only use the training set for fitting.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        logger.info(f"Data split into {len(X_train)} training samples and {len(X_test)} testing samples.")

        # 3. Scale the features
        scaler = StandardScaler()
        # Fit the scaler ONLY on the training data
        X_train_scaled = scaler.fit_transform(X_train)
        logger.info("Feature scaler fitted on training data.")

        # 4. Initialize and train the Random Forest model
        logger.info("Training Random Forest model...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train_scaled, y_train)
        logger.info("Model training completed!")

        # 5. Save the artifacts
        os.makedirs('../models', exist_ok=True)
        joblib.dump(model, '../models/astra_model.joblib')
        joblib.dump(scaler, '../models/astra_scaler.joblib')
        joblib.dump(feature_columns, '../models/feature_columns.joblib')
        logger.info("Model, scaler, and feature list saved successfully to 'models/' directory.")

    except Exception as e:
        logger.error(f"An error occurred during the training process: {e}")
        raise

def main():
    """
    Main function to orchestrate the model training.
    """
    logger.info("--- Starting Astra Model Training Script ---")
    try:
        dataset = load_data()
        train_and_save_artifacts(dataset)
        print("\n" + "="*50)
        print("✅ Training complete. Artifacts are ready for testing.")
        print("="*50)
    except Exception as e:
        logger.error(f"Training script failed to run. Reason: {e}")

if __name__ == "__main__":
    main()
