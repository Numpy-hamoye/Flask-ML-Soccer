import pandas as pd

# HELPER FUNCTION
def apply_transform_prod(sample, expected_input):
  """
  Carries out all needed transforms on the sample
  
  input: sample -> list or numpy array
  output: sample_df -> dataframe object
  """

  

  home_team = sample[0]
  away_team = sample[1]
  sample_df = pd.DataFrame(sample, 
                           index = expected_input).T

  sample_df['who_leads_draw'] = 0
  sample_df['who_leads_home_leads'] = 0


  for i, score in sample_df['Half Time Score'].items():
    home, away = score.split('-')

    if int(home) > int(away):
      sample_df.loc[i, 'who_leads_home_leads'] = 1
    elif int(home) == int(away):
      sample_df.loc[i, 'who_leads_draw'] = 1
    else:
      pass  
      
  X_sample = sample_df[['Away Team Rating', 'Home Team Rating',
                'who_leads_home_leads', 'Match Excitement',
                'Home Team On Target Shots', 'Away Team On Target Shots',
                'Away Team Clearances', 'Home Team Clearances',
                'Away Team Total Shots', 'Away Team Pass Success %',
                'Home Team Pass Success %', 'Home Team Aerials Won',
                'Home Team Throw Ins', 'Away Team Aerials Won',
                'Home Team Total Shots']]

  return X_sample, home_team, away_team