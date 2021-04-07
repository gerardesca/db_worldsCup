import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.fifa.com/worldcup/archive/russia2018/groups/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

groups_table = soup.find('div', class_= 'fi-standings-list')

groups = list()
teams = list()

for tables in groups_table.find_all('table'):
    group = tables.find('caption', class_ = 'fi-table__caption clearfix').text.strip()
    #print(group)
    #groups.append(group)
    body = tables.find('tbody')
    for i in body.find_all('td', class_ = 'fi-table__teamname teamname-nolink'):
        team = i.find('span', class_ = 'fi-t__nText').text
        #print(team)
        teams.append(team)
        groups.append(group)

print(groups, teams)

df = pd.DataFrame({'group':groups, 'team':teams})

df.to_csv('groups_2018.csv')


