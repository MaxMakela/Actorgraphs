import imdb
import csv
ia = imdb.IMDb()
data = []
#person = ia.search_person('Keanu Reeves')
with open('actors.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        data.append([ia.search_person(row[0])[0].personID] + row)

with open('actors_id.csv', 'w', newline='', encoding='utf-8') as actors:
    a = csv.writer(actors, delimiter=',')   
    a.writerows(data)

print("done")
#print(person[0].personID)