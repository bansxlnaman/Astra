# Astra (Automated Script Threat Response & Analysis)
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
│   └── tatkal.csv               # Data for training 
├── models/                      # Trained ML models
│   ├── astra_model.joblib
│   ├── astra_scaler.joblib  
│   └── feature_columns.joblib        
├── scripts/                     # model training scripts
├── src/
│   ├── __init__.py
│   ├── dashboard.py             # Dashboard for frontend
│   ├── backend.py               # Backend
│   └── simulation.py            # Data simulation script           
├── README.md
└── requirements.txt
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
