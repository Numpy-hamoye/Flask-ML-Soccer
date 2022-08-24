from flask import Flask, render_template, request
import numpy as np
import pickle
import joblib
import pandas as pd
from utils import apply_transform_prod
from sklearn.ensemble import RandomForestClassifier


app = Flask(__name__)

## LOAD MODEL

loaded_model = joblib.load('assets/soccer_forest_15.sav')

expected_input = ['Home Team', 'Away Team', 'Half Time Score', 'Home Team Rating',
       'Home Team On Target Shots', 'Home Team Total Shots',
       'Home Team Throw Ins', 'Home Team Pass Success %',
       'Home Team Aerials Won', 'Home Team Clearances',
       'Away Team Rating', 'Away Team On Target Shots',
       'Away Team Total Shots', 'Away Team Pass Success %',
       'Away Team Aerials Won', 'Away Team Clearances',
       'Match Excitement']

def predict_test(loaded_model, example, home_team, away_team):
  """Prediction Function"""

  prediction = loaded_model.predict(example)[0]

  if len(example) == 1:
    pred_proba = max(loaded_model.predict_proba(example)[0])
    
    if prediction == 'home_win':
        pred = 'HOME WIN 🥳'
        statement = f"""We are pleased to inform you that {home_team} is
       {pred_proba*100}% likely to win against {away_team} given the present stats"""
    elif prediction == 'away_win':
        pred = 'AWAY WIN 🤯'
        statement = f"""We are pleased to inform you that {away_team} is
       {pred_proba*100}% likely to win against {home_team} given the present stats"""
    else:
        statement = f"""There is a {pred_proba*100}% that the match will likely result in a draw"""
        pred = 'DRAW 😩'

  return statement, pred

@app.route("/")
def home():
    return render_template('home.html')



@app.route("/predict/", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            user_input = list(request.form.values())

            home_team = user_input[0].upper()
            away_team = user_input[1].upper()

            for i, data in enumerate(user_input):
                try:
                    user_input[i] = float(data)
                except:
                    continue

            example_transformed, home_team, away_team = apply_transform_prod(user_input, expected_input=expected_input)
            
            statement, model_prediction = predict_test(loaded_model, 
                                                        example_transformed,
                                                        home_team,
                                                        away_team)

        except ValueError:
            return "Please Enter valid values"
        return render_template('predict.html', prediction = model_prediction, statement=statement)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")