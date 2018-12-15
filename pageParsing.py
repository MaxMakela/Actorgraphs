import urllib.request
import bs4 as bs
import csv
import unicodedata
from operator import itemgetter

page = urllib.request.urlopen("https://en.wikipedia.org/wiki/List_of_actors_with_Hollywood_Walk_of_Fame_motion_picture_stars").read()
soup = bs.BeautifulSoup(page, 'lxml')

table = soup.find('table', class_='sortable wikitable')
table_rows = table.find_all('tr')
del table_rows[0]
data = []
data_m = []
data_f = []
#data.append(['Name', 'Gender', 'Born', 'Die', 'Age', 'Address', 'Inducted', 'At age'])

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text.strip() for i in td]
    if row:
       if row[1]=='M':
           data_m.append(row) 
       elif row[1]=='F':
           data_f.append(row) 

data_m = sorted(data_m, key=itemgetter(2), reverse=True) 
data_f = sorted(data_f, key=itemgetter(2), reverse=True)   
data = data_m[:50] + data_f[:50]

with open('actors.csv', 'w', newline='', encoding='utf-8') as actors:
    a = csv.writer(actors, delimiter=',')   
    a.writerows(data)

print("done")