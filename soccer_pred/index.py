from flask import Flask, render_template, request
import numpy as np
import pickle
import joblib
import pandas as pd
from utils import apply_transform_prod
from sklearn.ensemble import RandomForestClassifier


app = Flask(__name__)

def predict_test(loaded_model, example, le_classes):
  """Prediction Function"""

  prediction = loaded_model.predict(example)[0]

  if len(example) == 1:
    pred_proba = max(loaded_model.predict_proba(example)[0])
    home_team = team_reverse_code[example['Home Code'].values[0]]
    away_team = team_reverse_code[example['Away Code'].values[0]]
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


# Load Model
loaded_model = joblib.load('assets/soccer_forest.sav')

# Load team code and team_reverse_code and le_classes
with open('assets/team_code.pickle', 'rb') as handle:
    team_code= pickle.load(handle)

with open('assets/team_reverse_code.pickle', 'rb') as handle:
    team_reverse_code= pickle.load(handle)

with open('assets/le_classes.pickle', 'rb') as handle:
    le_classes= pickle.load(handle)

@app.route("/predict/", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        home_team = request.form.get('home team')
        away_team = request.form.get('away team')
        try: 
            home_team = request.form.get('home team')
            away_team = request.form.get('away team')
            half_time_score = request.form.get('half score')
            home_rating = float(request.form.get('home rating'))
            home_possesion = float(request.form.get('home possession %'))
            home_off_shot = float(request.form.get('home off shot'))
            home_on_shot = float(request.form.get('home on shot'))
            home_total_shot = float(request.form.get('home total shot'))
            home_block_shot = float(request.form.get('home block shot'))
            home_corners = float(request.form.get('home corners'))
            home_throws = float(request.form.get('home throws'))
            home_pass = float(request.form.get('home pass %'))
            home_aerial_won = float(request.form.get('home aerial won'))
            home_clearances = float(request.form.get('home clearances'))
            home_fouls = float(request.form.get('home fouls'))
            home_yellow = float(request.form.get('home yellow'))
            home_second_yellow = float(request.form.get('home second yellow'))
            home_red = float(request.form.get('home red'))
            away_rating = float(request.form.get('away rating'))
            away_possesion = float(request.form.get('away possession %'))
            away_off_shot = float(request.form.get('away off shot'))
            away_on_shot = float(request.form.get('away on shot'))
            away_total_shot = float(request.form.get('away total shot'))
            away_block_shot = float(request.form.get('away block shot'))
            away_corners = float(request.form.get('away corners'))
            away_throws = float(request.form.get('away throws'))
            away_pass = float(request.form.get('away pass %'))
            away_aerial_won = float(request.form.get('away aerial won'))
            away_clearances = float(request.form.get('away clearances'))
            away_fouls = float(request.form.get('away fouls'))
            away_yellow = float(request.form.get('away yellow'))
            away_second_yellow = float(request.form.get('away second yellow'))
            away_red = float(request.form.get('away red'))
            match_excitement = float(request.form.get('Match Excitement'))

            example = [home_team.upper(), away_team.upper(), half_time_score,
            home_rating, home_possesion, home_off_shot, home_on_shot,
            home_total_shot, home_block_shot, home_corners,
            home_throws, home_pass, home_aerial_won, home_clearances, home_fouls,
            home_yellow, home_second_yellow, home_red, away_rating,
            away_possesion, away_off_shot, away_on_shot, away_total_shot, away_block_shot,
            away_corners, away_throws, away_pass, away_aerial_won,
            away_clearances, away_fouls, away_yellow,
            away_second_yellow, away_red, match_excitement
                ]

            example_transformed = apply_transform_prod(example, team_code)
            
            statement, model_prediction = predict_test(loaded_model, example_transformed, le_classes=le_classes)
        

        except ValueError:
            return "Please Enter valid values"
        return render_template('predict.html', prediction = model_prediction, statement=statement)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")