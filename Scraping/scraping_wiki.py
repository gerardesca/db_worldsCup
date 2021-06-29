"""
Project on the FIFA World Cup Squads 
from 1950 to 2018
By: Gerardo Jaime Escareño, gjaimeescareno@gmail.com
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
Lists
"""
years = list(range(1930, 1939, 4)) + list(range(1950,2019,4))
editions = []
teams =[]

"""
Functions
"""
#Editions
def edition(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = []
    year = url[30:34]
    for groups in soup.find_all('li', 'toclevel-1'):
        group = groups.find('span','toctext').text
        test = groups.find('li', 'toclevel-2')
        if group == 'Player statistics' or group == 'Statistics' or group == 'References' or group == 'External links' or group == 'Player representation by league' or group == 'Notes' or group == 'Player representation by club' or group == 'Footnotes':
            break
        else:
            if test is None:
                edition = [year, None, group]
                result.append(edition)
            else:
                for teams in groups.find_all('li', 'toclevel-2'):
                    team = teams.find('span','toctext').text
                    edition = [year, group, team]
                    result.append(edition)
    return result

#Teams
def team(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = []
    table = soup.find_all('table', 'wikitable sortable')[0]
    for tr in table.find_all('tr')[1:]:
        cells = [td.text.strip() for td in tr.find_all('td')]
        result.append(cells)
    return result

"""
Main program
"""
for year in years:
    url = "https://en.wikipedia.org/wiki/"+str(year)+"_FIFA_World_Cup_squads"
    editions += edition(url)
    
url = "https://en.wikipedia.org/wiki/National_team_appearances_in_the_FIFA_World_Cup"
teams = team(url)

pd.DataFrame(editions).to_csv('editions_wiki.csv', 
                            index=False,
                            #header=['edition','group','team'],
                            header=None, 
                            encoding='utf-8')

pd.DataFrame(teams).to_csv('teams_wiki.csv', 
                            index=False, 
                            header=['team','apps','record_streak','active_streak','debut','most_recent','best_result'], 
                            encoding='utf-8')
