import requests
from bs4 import BeautifulSoup
import pandas as pd

editions = []
links = []
teams = []
competition = []
codeteams = []
squads = []

def string(variable):
    for name in globals():
        if eval(name) == variable:
            return str(name)
    
def create_df(list):
    df = pd.DataFrame(list).to_csv(string(list)+'.csv', 
                            index=True,
                            header=None, 
                            encoding='utf-8')
    return df

def fifa():
    url = 'https://www.fifa.com/tournaments/mens/worldcup'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    for link in soup.find_all('a', 'fp-tournament-timeline-item_timelineItem__3c4Xg'):
        links.append(link['href'])
        for edition in link.find_all('div', 'fp-tournament-timeline-item_timelineItemSecondLine__3Qk_e'):
            editions.append(edition.text)
    return editions, links

def linksteams(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = []
    for a in soup.find_all('a', 'ff-display-card_clickable__3VCBO'):
        result.append(a['href'][5:])
    return result

def team(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = []
    for team in soup.find_all('div', 'ff-display-card_displayCardTeam__12mcx'):
        result.append(team.text)
    return result

def competitions(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = []
    year = url[47:51]
    test = soup.find('div', 'fp-groups-overview_carouselInner__3nmnH')
    if test is None:
        url = url.replace('match-center', 'teams')
        for y in team(url):
            compe = [None, y, year]
            result.append(compe)
    else:
        for div in soup.find_all('div', 'fp-group-card_groupsTable__1cbWY'):
            group = div.find('th', 'undefined fp-group-card_alignLeft__2WDRn').text
            for td in div.find_all('td', 'fp-group-card_alignLeft__2WDRn'):
                t = td.text[1:]
                compe = [group, t, year]
                result.append(compe)
    return result

def squad(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = []
    for div in soup.find_all('div', 'fp-squad-player-card_playerDetails__2k2Nc'):
        firstname = div.find('div', 'fp-squad-player-card_firstName__1UtW_')
        lastname = div.find('div', 'fp-squad-player-card_lastName__3KJvd')
        jersey = div.find('div', 'fp-squad-player-card_jerseyNumber__1zPwG').text
        pos = div.find('div', 'fp-squad-player-card_position__17FyP').text
        team = div.find('img')
        if firstname is None or lastname is None:
            lastname = div.find('span', 'fp-squad-player-card_lastName__3KJvd').text
            cells = ['', lastname, jersey, pos, team['title']]
            result.append(cells) 
        else:
            cells = [firstname.text, lastname.text, jersey, pos, team['title']]
            result.append(cells)
    return result

editions, links = fifa()

for i in links[2:]:
    url = 'https://www.fifa.com'+str(i)+'/teams'
    teams += team(url)
    codeteams += linksteams(url)
    for i in codeteams:
        urlsquad = url+i
        squads += squad(urlsquad)
    url = url.replace('teams', 'match-center')
    competition += competitions(url) 

create_df(teams)
create_df(competition)
create_df(squads)

