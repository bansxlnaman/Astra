import pandas as pd
import numpy as np
import os
import random

# --- Configuration ---
INPUT_FILENAME = '../data/tatkal_sessions.csv'
OUTPUT_FILENAME = '../data/tatkal_sessions_enhanced.csv'

def enhance_features(df):
    """
    Adds new, more sophisticated behavioral features to the existing dataset.
    The values are generated based on whether the session belongs to a human or a bot.
    """
    print("Enhancing dataset with new features...")
    
    # Create lists to hold the new feature data
    avg_keystroke_intervals = []
    mouse_idle_times = []
    backspace_counts = []
    account_ages = []

    # Iterate over each row of the DataFrame
    for index, row in df.iterrows():
        is_bot = row['is_bot']
        
        if is_bot == 0:  # If the row represents a Human
            # Generate realistic human-like values
            avg_keystroke_intervals.append(random.uniform(80, 250))  # Slower, variable typing in ms
            mouse_idle_times.append(random.uniform(1.0, 8.0))      # Pauses to think/read
            backspace_counts.append(random.randint(0, 7))          # Makes occasional typos
            account_ages.append(random.randint(30, 1500))          # Established account in days
        
        else:  # If the row represents a Bot
            # Generate bot-like, efficient values
            avg_keystroke_intervals.append(random.uniform(5, 20))   # Near-instantaneous, programmatic typing
            mouse_idle_times.append(random.uniform(0.0, 0.5))      # No pauses
            backspace_counts.append(0)                             # Perfect input, no corrections
            account_ages.append(random.randint(0, 5))              # Brand new account
            
    # Add the new lists as columns to the DataFrame
    df['avg_keystroke_interval_ms'] = avg_keystroke_intervals
    df['mouse_idle_time_sec'] = mouse_idle_times
    df['backspace_count'] = backspace_counts
    df['account_age_days'] = account_ages
    
    print("New features added successfully.")
    return df

# --- Main Execution ---
if __name__ == "__main__":
    # Check if the input file exists
    if not os.path.exists(INPUT_FILENAME):
        print(f"Error: The data file '{INPUT_FILENAME}' was not found.")
        print("Please make sure your CSV file is in the same directory as this script.")
    else:
        print(f"Loading original dataset from '{INPUT_FILENAME}'...")
        original_df = pd.read_csv(INPUT_FILENAME)
        
        # Enhance the dataframe with new features
        enhanced_df = enhance_features(original_df.copy())
        
        # Save the new dataframe to a new file
        enhanced_df.to_csv(OUTPUT_FILENAME, index=False)
        
        print(f"\nEnhanced dataset saved to '{OUTPUT_FILENAME}'")
        print("\nPreview of the new data (first 5 rows):")
        print(enhanced_df.head())
        
        print("\nPreview of the new data (last 5 rows to show bot data):")
        print(enhanced_df.tail())
