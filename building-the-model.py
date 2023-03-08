###################################
#This project were build after this tut ==> https://www.youtube.com/watch?app=desktop&v=yat7soj__4w&feature=youtu.be
#Thanks for  @ThePyCoach and his beautiful channel
import pandas as pd
import pickle
#import scipy.stats as poisson
from scipy.stats import poisson

dict_table = pickle.load(open('dict_table','rb'))
df_historical_data = pd.read_csv('cleaned_fifa_data.csv')
df_fixture = pd.read_csv('clean_fifa_worldcup_fixture.csv')

#dict_table['Group A']
df_home = df_historical_data[['Home_Team','Home_goals','Away_goals']]
df_away = df_historical_data[['Away_Team','Home_goals','Away_goals']]
#print(df_home)

df_home = df_home.rename(columns={'Home_Team':'Team' , 'Home_goals': 'Goals_Scored' , 'Away_goals' : 'Goals_Cosidered'})
df_away = df_away.rename(columns={'Away_Team':'Team' , 'Home_goals': 'Goals_Considered' , 'Away_goals' : 'Goals_Scored'})

df_team_strength = pd.concat([df_home , df_away] , ignore_index=True).groupby('Team').mean()

#PREDICTIONS
def predects_points(home , away):
	if home in df_team_strength.index and away in df_team_strength.index:
		lamb_home = df_team_strength.at[home, 'Goals_Scored'] * df_team_strength.at[away , 'Goals_Cosidered']
		lamb_away = df_team_strength.at[away, 'Goals_Scored'] * df_team_strength.at[home , 'Goals_Cosidered']
		prob_home , prob_away , prob_draw = 0, 0, 0
		for x in range(0 , 11):#number of goals home team
			for y in range(0, 11):#number of goals away team
				p = poisson.pmf(x , lamb_home) * poisson.pmf(y , lamb_away)
				if x == y :
					prob_draw += p
				elif x > y:
					prob_home += p
				else : 
					prob_away += p
		points_home = 3 * prob_home + prob_away
		points_away = 3 * prob_away + prob_draw
		return (points_home , points_away)
	else:
		return (0 , 0)


#print(predects_points('Argentina' , 'Mexico'))
#print(predects_points('England' , 'United States'))
df_fixture_group_48 = df_fixture[:48].copy()
df_fixture_knockout = df_fixture[48:56].copy()
df_fixture_quarter = df_fixture[56:60].copy()
df_fixture_semi = df_fixture[60:62].copy()
df_fixture_final = df_fixture[62:].copy()
#print(df_fixture_semi)
#print(dict_table['Group A'])
#for gruop in dict_table:
#	print(dict_table[gruop]['Team'].values)

for group in dict_table:
	teams_in_group = dict_table[group]['Team'].values
	teams_in_group_6 = df_fixture_group_48[df_fixture_group_48['home'].isin(teams_in_group)]
	for index, row in teams_in_group_6.iterrows():
		home, away = row['home'], row['away']
		points_home , points_away = predects_points(home , away)
		dict_table[group].loc[dict_table[group]['Team'] == home, 'Pts'] += points_home
		dict_table[group].loc[dict_table[group]['Team'] == away, 'Pts'] += points_away
	dict_table[group] = dict_table[group].sort_values('Pts', ascending = False).reset_index()
	dict_table[group] = dict_table[group][['Team' , 'Pts']]
	dict_table[group] = dict_table[group].round(0)
#print(dict_table['Group C'])
#print(df_fixture_knockout)
for group in dict_table:
	group_winner = dict_table[group].loc[0 , 'Team']
	runners_up = dict_table[group].loc[1 , 'Team']
	df_fixture_knockout.replace({f'Winners {group}': group_winner , f'Runners-up {group}': runners_up}, inplace=True)
df_fixture_knockout['Winner'] = "?"
#print(df_fixture_knockout)

def get_winner(df_fixture_updated):
	for index, row in df_fixture_updated.iterrows():
		home , away = row['home'], row['away']
		points_home , points_away = predects_points(home , away)
		if points_home > points_away:
			winner = home 
		else:
			winner = away
		df_fixture_updated.loc[index, 'Winner'] = winner
	return df_fixture_updated

get_winner(df_fixture_knockout)

def updated_quarter(df_fixture_round_1 , df_fixture_round_2):
	for index, row in df_fixture_round_1.iterrows():
		winners = df_fixture_round_1.loc[index , 'Winner']
		match = df_fixture_round_1.loc[index , 'score']
		df_fixture_round_2.replace({f'Winners {match}' : winners}, inplace=True)
	df_fixture_round_2['Winner'] = '?'
	return df_fixture_round_2

updated_quarter(df_fixture_knockout , df_fixture_quarter)
#print(df_fixture_quarter)
get_winner(df_fixture_quarter)
updated_quarter(df_fixture_quarter , df_fixture_semi)
get_winner(df_fixture_semi)
updated_quarter(df_fixture_semi , df_fixture_final)
print(get_winner(df_fixture_final))

