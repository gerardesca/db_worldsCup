"""
Project about the squads FIFA World Cup
By: Gerardo Jaime Escareño
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

def squads(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = []
    year = url[30:34]
    for table in soup.find_all('table', 'plainrowheaders'):
        if "wikitable" not in table:
            squad = table.find_previous('span','mw-headline').text
            for tr in table.find_all('tr')[1:]:
                cells = [th.text.strip() for th in tr.find_all('th')]
                cells += [td.text.strip() for td in tr.find_all('td')]
                cells += [squad, year]
                result.append(cells)
    return result

#years = list(range(1930, 1939, 4)) + list(range(1950,2019,4))
years = list(range(2014,2019,4)) 
result = []
for year in years:
    url = "https://en.wikipedia.org/wiki/"+str(year)+"_FIFA_World_Cup_squads"
    result += squads(url)

pd.DataFrame(result).to_csv('squads_wiki.csv', 
                            index=False, 
                            header=['player','No','pos','age','caps','goals','club','squad','year'], 
                            encoding='utf-8')


