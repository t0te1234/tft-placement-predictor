# TFT Placement Predictor
This project processes **Teamfight Tactics (TFT) match data** and trains a regression model to predict a player's placement based on their board state (traits, champions, items, and level).  

---

## Features

- **Data preprocessing**  
  - Converts raw match data (traits, units, items) into structured numerical features.  
  - Encodes traits by level, units by presence/tier, and items by presence.

- **Feature engineering**  
  - Builds a consistent feature vector for every match.  
  - Exports processed data to `processed.csv`.

- **Regression modeling**  
  - Current most accurate model is Random Forest.  
  - Predicts final placement (1–8).  
  - Includes evaluation with Mean Squared Error (MSE) and R² score.  

- **Feature importance analysis**  
  - Identifies which traits, units, or items have the most impact on placement.

---

## Workflow
1. **Leaderboard WebScraping**
   - Using Selenium, scrapes the highest ranked 100 players in North America:
   - ```bash
     python Webscraping.py
     ```
   - Results are saved in `players.csv`
3. **Data Extraction**  
   - Collect raw TFT match data (traits, units, items, placements) through Riot API.
   - ```bash
     python Webscraping.py
     ```
   - Saved matches are in `data.csv`

4. **Preprocessing**  
   - Run the preprocessing script:  
     ```bash
     python EncodeData.py
     ```
   - This creates a `processed.csv` with clean feature vectors.

5. **Model Training**  
   - Train a regression model on the processed data:  
     ```bash
     python Model.py
     ```
   - Evaluates predictions and prints metrics (MSE, R²).

---
## Requirements
Install dependencies with:
```bash
pip install -r requirements.txt
