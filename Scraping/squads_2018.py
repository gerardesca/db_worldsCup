import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.fifa.com/worldcup/archive/russia2018/teams/team/43922/' 
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

squad = soup.find('div', class_= 'fi-team__members') #Search start

names = list()      #Names List
positions = list()  #Positions List
numbers = list()    #Numbers List

#Names and Positions
for i in squad.find_all('div', class_ = 'fi-p__info'):
    name = i.find('span', class_ = 'fi-p__nLonger').text 
    pos = i.find('div', class_ = 'fi-p__ info--role').text
    names.append(name)
    positions.append(pos.replace('\r\n', '').replace('                ', ''))

#Numbers
for i in squad.find_all('div', class_ = 'fi-p__info'):
    num = i.find('span', class_ = 'fi-p__num')
    if num is None:
        numbers.append(num)
        continue
    numbers.append(num.text)

#Verification    
print(names, len(names),)
print(positions, len(positions),)
print(numbers, len(numbers),)

#Storage in .csv
df = pd.DataFrame({'name':names, 'pos':positions, 'num':numbers})
df.to_csv('squad.csv')