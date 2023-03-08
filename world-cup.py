import pandas as pd
from string import ascii_uppercase as alphabet
import pickle


all_tabels = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')
dict_table = {}
for letter , i in zip(alphabet , range(9, 65 , 7)):
  df = all_tabels[i]
  df.rename(columns= {df.columns[1]:'Team'} , inplace = True)
  df.pop('Qualification')
  dict_table[f'Group {letter}'] = df

dict_table['Group A']
