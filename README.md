# IPL Match Predictor

This is an AI-powered IPL match predictor web application that uses machine learning to forecast the winning team based on team combinations, venue, and recent match performance. 
It includes a FastAPI backend and a React-based frontend interface.

## Features
- Predicts IPL match outcomes based on input team names, venue, and recent performance.
- Provides predicted winner, score estimation, and a basic reasoning explanation.
- Built with FastAPI (backend), React (frontend), and scikit-learn (ML).
- Swagger UI available for API exploration.

## Model Architecture & Training

- **Model**: `DecisionTreeClassifier` from scikit-learn.
- **Features Used**:
  - Team 1 and Team 2 (label encoded)
  - Venue and Venue Team (label encoded)
  - Recent wins and matches
- **Target**: Match Winner
- **Training Data**: Manually created dataset with a small number of entries for demonstration purposes.
- **Training Code**: Available in `model_training.ipynb` or embedded within the backend script.


## Data Processing Pipeline

1. **Input**: User inputs teams, venue, and recent stats.
2. **Preprocessing**: All inputs are encoded using LabelEncoder.
3. **Prediction**:
   - Model predicts the winner team.
   - Mock logic generates score estimates.
4. **Output**: Prediction includes winner, scores, and reasoning.

---
