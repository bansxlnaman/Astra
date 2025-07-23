# Standalone Traffic Simulation Script for Astra API
# This script generates continuous human and bot data and sends it to the
# backend API to simulate real-world traffic for testing and demonstration.

import requests
import json
import random
import time
import logging

# --- Configuration ---
API_URL = "http://127.0.0.1:3000/predict"
SIMULATION_SPEED = 1.0  # requests per second
BOT_RATIO = 0.3  # 30% of traffic will be bots

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# --- Data Generation Functions ---
def generate_human_data():
    """Generates a dictionary of realistic, human-like behavioral data."""
    return {
      "login_duration": round(random.uniform(7.0, 12.0), 2),
      "journey_planner_duration": round(random.uniform(10.0, 20.0), 2),
      "train_selection_duration": round(random.uniform(8.0, 15.0), 2),
      "form_fill_duration": round(random.uniform(25.0, 50.0), 2),
      "captcha_duration": round(random.uniform(5.0, 12.0), 2),
      "session_duration": round(random.uniform(60.0, 120.0), 2),
      "mouse_movements": random.randint(3000, 9000),
      "page_scrolls": random.randint(5, 20),
      "form_corrections": random.randint(1, 5),
      "avg_keystroke_interval_ms": round(random.uniform(100, 250), 2),
      "mouse_idle_time_sec": round(random.uniform(2.0, 10.0), 2),
      "backspace_count": random.randint(1, 8),
      "account_age_days": random.randint(50, 1000)
    }

def generate_bot_data():
    """Generates a dictionary of efficient, bot-like behavioral data."""
    return {
      "login_duration": round(random.uniform(0.1, 0.5), 2),
      "journey_planner_duration": round(random.uniform(0.2, 0.8), 2),
      "train_selection_duration": round(random.uniform(0.1, 0.5), 2),
      "form_fill_duration": round(random.uniform(0.5, 1.5), 2),
      "captcha_duration": round(random.uniform(1.0, 2.5), 2),
      "session_duration": round(random.uniform(2.0, 5.0), 2),
      "mouse_movements": random.randint(10, 100),
      "page_scrolls": random.randint(0, 2),
      "form_corrections": 0,
      "avg_keystroke_interval_ms": round(random.uniform(5, 20), 2),
      "mouse_idle_time_sec": round(random.uniform(0.0, 0.5), 2),
      "backspace_count": 0,
      "account_age_days": random.randint(0, 5)
    }

# --- Main Execution Loop ---
if __name__ == "__main__":
    logger.info("Starting Astra Traffic Simulation. Press Ctrl+C to stop.")
    
    while True:
        try:
            # Decide whether to generate a bot or human session
            if random.random() < BOT_RATIO:
                session_data = generate_bot_data()
                session_type = "Bot"
            else:
                session_data = generate_human_data()
                session_type = "Human"

            # Send the request to the API
            response = requests.post(API_URL, json=session_data)
            
            if response.status_code == 200:
                logger.info(f"Sent {session_type} data. API Response: {response.json()}")
            else:
                logger.warning(f"API returned an error. Status: {response.status_code}, Body: {response.text}")

            # Control the loop speed
            time.sleep(1 / SIMULATION_SPEED)

        except requests.exceptions.ConnectionError:
            logger.error(f"Connection Error: Could not connect to the API at {API_URL}. Is the backend server running?")
            time.sleep(5) # Wait before retrying
        except KeyboardInterrupt:
            logger.info("Simulation stopped by user.")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            break
