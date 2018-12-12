import urllib.request
import bs4 as bs
import csv
import unicodedata

page = urllib.request.urlopen("https://en.wikipedia.org/wiki/List_of_actors_with_Hollywood_Walk_of_Fame_motion_picture_stars").read()
soup = bs.BeautifulSoup(page, 'lxml')

table = soup.find('table', class_='sortable wikitable')
table_rows = table.find_all('tr')
del table_rows[0]
data = []

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    del row[-1]
    if row:
       #row[0] = unicodedata.normalize('NFKD', row[0]).encode('ascii', 'ignore')
       data.append(row) 

with open('actors.csv', 'w', newline='', encoding='utf-8') as actors:
    a = csv.writer(actors, delimiter=',')
    a.writerows(data)

print("done")