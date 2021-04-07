from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.fifa.com/worldcup/archive/russia2018/teams/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#National Teams 

team = soup.find_all('div', class_='fi-team-card__name')

teams = list()

for i in team:
    teams.append(i.get_text().replace('\r\n        ', '').replace('  ',''))
    #print(i.string)

print(teams, len(teams))

#Confederacy

data = soup.find_all('a', class_='fi-team-card fi-team-card__team')

confederacy_team = list()

for i in data:
    confederacy_team.append(i.get('data-confed'))
    #print(i.get('data-filter'))

print(confederacy_team, len(confederacy_team))

df = pd.DataFrame({'team':teams, 'confederacy':confederacy_team})
df.to_csv('teams_2018.csv')