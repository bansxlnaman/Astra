# Astra: IRCTC Bot Detector 🇮🇳

A machine learning-based system to detect automated bots attempting to book IRCTC tickets, helping ensure fair access to railway tickets for genuine users.

## Project Overview

Astra uses behavioral analysis to distinguish between human users and automated bots during the IRCTC ticket booking process. The system analyzes timing patterns, form-filling behavior, and session characteristics to identify suspicious automated activity.

## Features

- **Human Behavior Simulation**: Realistic simulation of human ticket booking patterns
- **Bot Behavior Simulation**: Automated bot behavior patterns for training data
- **Machine Learning Model**: XGBoost-based classifier for bot detection
- **Interactive Demo**: Streamlit web application for real-time predictions
- **Comprehensive Analysis**: EDA notebooks for data exploration and model evaluation

## Project Structure

```
ASTRA/
├── data/
│   └── tatkal.scv                 # Data for training 
├── models/                      # Trained ML models
├── scripts/                     # model training scripts\
├── src/
│   ├── __init__.py
│   ├── human_simulator.py    # Human behavior simulation
│   ├── bot_simulator.py      # Bot behavior simulation
│   └── generate_data.py      # Data generation script
├── models/                    # Trained ML models
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Data Generation
```bash
cd astra
python src/generate_data.py
```

### Model Training
1. Open `notebooks/01_EDA.ipynb` for data exploration
2. Open `notebooks/02_Model_Training.ipynb` for model training

### Interactive Demo
```bash
cd astra
streamlit run app/app.py
```

## Technical Details

- **Language**: Python 3.8+
- **ML Framework**: XGBoost, Scikit-learn
- **Web Framework**: Streamlit
- **Data Analysis**: Pandas, NumPy, Matplotlib, Seaborn
- **Web Automation**: Selenium

## Contributing

This project is designed for educational and research purposes in bot detection and cybersecurity.

## License

MIT License 