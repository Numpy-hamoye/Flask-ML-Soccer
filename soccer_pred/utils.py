import pandas as pd

# HELPER FUNCTIONS
def apply_transform_prod(sample, team_encoding):
  """
  Carries out all needed transforms on the sample
  
  input: sample -> list or numpy array
  output: sample_df -> dataframe object
  """

  def lead_margin(score):
    """Check for half time lead margin"""
    home, away= score.split('-')
    return abs(int(home) - int(away))


  sample_df = pd.DataFrame(sample, 
                           index = ['Home Team', 'Away Team', 'Half Time Score', 'Home Team Rating',
       'Home Team Possession %', 'Home Team Off Target Shots', 'Home Team On Target Shots',
       'Home Team Total Shots', 'Home Team Blocked Shots', 'Home Team Corners',
       'Home Team Throw Ins', 'Home Team Pass Success %',
       'Home Team Aerials Won', 'Home Team Clearances', 'Home Team Fouls',
       'Home Team Yellow Cards', 'Home Team Second Yellow Cards',
       'Home Team Red Cards', 'Away Team Rating', 'Away Team Possession %',
       'Away Team Off Target Shots', 'Away Team On Target Shots',
       'Away Team Total Shots', 'Away Team Blocked Shots', 'Away Team Corners',
       'Away Team Throw Ins', 'Away Team Pass Success %',
       'Away Team Aerials Won', 'Away Team Clearances', 'Away Team Fouls',
       'Away Team Yellow Cards', 'Away Team Second Yellow Cards',
       'Away Team Red Cards', 'Match Excitement']).T

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

  sample_df['lead_margin'] = sample_df['Half Time Score'].apply(lead_margin)
  sample_df['Home Code'] = sample_df['Home Team'].map(lambda x: team_encoding[x])
  sample_df['Away Code'] = sample_df['Away Team'].map(lambda x: team_encoding[x])

  X_sample = sample_df[['Home Code', 'Away Code', 'Home Team Rating', 'Home Team Possession %', 
       'Home Team Off Target Shots', 'Home Team On Target Shots',
       'Home Team Total Shots', 'Home Team Blocked Shots', 'Home Team Corners',
       'Home Team Throw Ins', 'Home Team Pass Success %',
       'Home Team Aerials Won', 'Home Team Clearances', 'Home Team Fouls',
       'Home Team Yellow Cards', 'Home Team Second Yellow Cards',
       'Home Team Red Cards', 'Away Team Rating', 'Away Team Possession %',
       'Away Team Off Target Shots',
       'Away Team On Target Shots', 'Away Team Total Shots',
       'Away Team Blocked Shots', 'Away Team Corners', 'Away Team Throw Ins',
       'Away Team Pass Success %', 'Away Team Aerials Won',
       'Away Team Clearances', 'Away Team Fouls', 'Away Team Yellow Cards',
       'Away Team Second Yellow Cards', 'Away Team Red Cards',
       'Match Excitement', 'lead_margin', 'who_leads_draw', 'who_leads_home_leads']]



  return X_sample

