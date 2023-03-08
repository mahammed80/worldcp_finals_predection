from bs4 import BeautifulSoup
import requests 
import pandas as pd


years = [1930,1934,1938,1950,1954,1958,1962,1966,1970,1974,1978,1982,1986,1990,1994,1998,2002,2006,2010,2014,2018,2018,2022]

def get_matches(year):
	web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
	res = requests.get(web)
	content = res.text
	soup = BeautifulSoup(content , 'lxml')

	all_matches = soup.find_all('div' , class_= 'footballbox')

	home = []
	score = []
	away = []

	for match in all_matches:
		home.append(match.find('th', class_= 'fhome').get_text())
		score.append(match.find('th', class_= 'fscore').get_text())
		away.append(match.find('th', class_= 'faway').get_text())

	dict_football = {'home' : home , 'score': score , 'away' : away}
	df_footbal = pd.DataFrame(dict_football)
	df_footbal['year'] = year
	return df_footbal

fifa = [get_matches(year) for year in years]
df_fifa = pd.concat(fifa , ignore_index=True)
df_fifa.to_csv('fifa_world_cup_historical_data.csv', index=False)

#fixture of worls cup 2022
df_fixture = get_matches(2022)
df_fixture.to_csv('fifa_world_cup_fixture.csv' , index=False)

#print(get_matches('2002'))