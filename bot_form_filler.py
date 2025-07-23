# Bot Form Filler for Astra Frontend
# This script uses Selenium to automate the process of filling the booking form
# with bot-like speed and efficiency to demonstrate the detection system.

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
# The name of your frontend HTML file
FRONTEND_FILE = 'index.html'

def run_bot_simulation():
    """
    Launches a browser, fills the form like a bot, and submits it.
    """
    print("--- Starting Astra Bot Simulation ---")

    # --- Setup WebDriver ---
    # This automatically downloads and manages the correct driver for your Chrome version.
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        print("WebDriver initialized successfully.")
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        print("Please ensure you have Google Chrome installed.")
        return

    # --- Navigate to the local HTML file ---
    # Gets the absolute path to the file to ensure it works from any directory.
    file_path = os.path.abspath(FRONTEND_FILE)
    if not os.path.exists(file_path):
        print(f"Error: The file '{FRONTEND_FILE}' was not found in this directory.")
        driver.quit()
        return
        
    driver.get(f"file:///{file_path}")
    print(f"Opened frontend: {file_path}")
    time.sleep(1) # Give the page a moment to load

    try:
        # --- Bot Actions: Fill the form with superhuman speed ---
        
        # 1. Fill passenger name instantly
        passenger_name_field = driver.find_element(By.ID, 'passenger-name')
        passenger_name_field.send_keys("Bot User")
        print("Filled passenger name.")

        # 2. Fill passenger age instantly
        passenger_age_field = driver.find_element(By.ID, 'passenger-age')
        passenger_age_field.send_keys("99")
        print("Filled passenger age.")

        # 3. Get the correct CAPTCHA text and fill it instantly
        captcha_text_element = driver.find_element(By.ID, 'captcha-text')
        correct_captcha = captcha_text_element.text
        
        captcha_input_field = driver.find_element(By.ID, 'captcha-input')
        captcha_input_field.send_keys(correct_captcha)
        print(f"Solved CAPTCHA: {correct_captcha}")

        # 4. Find and click the submit button immediately
        # The button becomes enabled via JavaScript, so we add a tiny wait.
        time.sleep(0.1) 
        submit_button = driver.find_element(By.ID, 'submit-button')
        submit_button.click()
        print("Clicked 'Proceed to Payment'.")

        # --- Wait to observe the result ---
        print("\nSimulation complete. The browser will show the result.")
        print("Waiting for 10 seconds before closing the browser...")
        time.sleep(10)

    except Exception as e:
        print(f"\nAn error occurred during the simulation: {e}")
    finally:
        # --- Cleanup ---
        print("Closing browser.")
        driver.quit()

# --- Main Execution ---
if __name__ == "__main__":
    run_bot_simulation()
