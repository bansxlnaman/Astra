# Backend API for Astra IRCTC Bot Detector
# This script uses FastAPI and now logs every prediction to a CSV file.

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime
import csv

# --- Configuration & Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

LOG_FILE = '../logs/api_log.csv'
artifacts = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs on startup
    logger.info("Starting up Astra API...")
    try:
        artifacts['model'] = joblib.load('models/astra_model.joblib')
        artifacts['scaler'] = joblib.load('models/astra_scaler.joblib')
        artifacts['feature_columns'] = joblib.load('models/feature_columns.joblib')
        logger.info("Artifacts loaded successfully!")

        os.makedirs('../logs', exist_ok=True)
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                header = ['Timestamp', 'is_bot', 'decision', 'confidence_score'] + artifacts['feature_columns']
                writer.writerow(header)
    except FileNotFoundError as e:
        logger.error(f"Error loading artifacts: {e}. Please ensure model files are in 'models'.")
        artifacts['model'] = None
    yield
    logger.info("Shutting down Astra API...")

# Initialize the FastAPI app
app = FastAPI(
    title="Astra IRCTC Bot Detector API",
    description="An API to predict if a user session is from a human or a bot based on behavioral data.",
    version="1.0.0",
    lifespan=lifespan
)

# --- Add CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. For production, restrict this to your frontend's domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Data Model for incoming data
class SessionData(BaseModel):
    login_duration: float
    journey_planner_duration: float
    train_selection_duration: float
    form_fill_duration: float
    captcha_duration: float
    session_duration: float
    mouse_movements: int
    page_scrolls: int
    form_corrections: int
    avg_keystroke_interval_ms: float
    mouse_idle_time_sec: float
    backspace_count: int
    account_age_days: int

def log_prediction(log_data: dict):
    """Appends a prediction result to the CSV log file."""
    try:
        header = ['Timestamp', 'is_bot', 'decision', 'confidence_score'] + artifacts.get('feature_columns', [])
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
            writer.writerow(log_data)
    except Exception as e:
        logger.error(f"Error writing to log file: {e}")

@app.get("/")
async def root():
    return {"message": "Astra IRCTC Bot Detector API is running."}

@app.post("/predict", tags=["Prediction"])
async def predict_bot(session_data: SessionData, request: Request):
    if not artifacts.get('model'):
        raise HTTPException(status_code=503, detail="Model is not available.")
    try:
        prediction_result = await _make_prediction(session_data)
        log_entry = {
            'Timestamp': datetime.now().isoformat(),
            **prediction_result,
            **session_data.dict()
        }
        log_prediction(log_entry)
        return prediction_result
    except Exception as e:
        logger.error(f"An error occurred during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")

async def _make_prediction(session_data: SessionData) -> dict:
    """Helper function to run the model prediction."""
    input_df = pd.DataFrame([session_data.dict()])
    input_df = input_df[artifacts['feature_columns']]
    input_scaled = artifacts['scaler'].transform(input_df)
    prediction = artifacts['model'].predict(input_scaled)
    prediction_proba = artifacts['model'].predict_proba(input_scaled)
    is_bot = int(prediction[0])
    decision = "BLOCK" if is_bot == 1 else "ALLOW"
    confidence_score = float(prediction_proba[0][is_bot])
    return {"is_bot": is_bot, "decision": decision, "confidence_score": confidence_score}

# To run: uvicorn src.backend:app --reload --port 3000
if __name__ == "__main__":
    uvicorn.run("src.backend:app", host="127.0.0.1", port=3000, reload=True)
