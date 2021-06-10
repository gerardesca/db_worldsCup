import os
import hashlib
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.fifa.com/associations/#all'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

confederacyAll = soup.find_all('div', {'data-tab':"all"})

for i in confederacyAll.find_all('div', class_= 'fi-a__n'):
    print(i)

