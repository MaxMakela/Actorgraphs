from graph import ActorsGraph
import csv
import imdb
from imdb.Person import Person

id_list = []
movie_id_list = []
ia = imdb.IMDb()

def get_filmography(imdb_person):
    filmography = []
    for step in imdb_person:
        if 'actor' in step:
            filmography = step['actor']
            break
    return filmography
    
with open('actors_id.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        id_list.append(row[0])

id_set = set(id_list)
films_id_set = set()

graph = ActorsGraph(id_list[:10])

for actor in id_list[:10]:
    for film in get_filmography(ia.get_person(actor)['filmography']):
        if film.movieID not in films_id_set:
            films_id_set.add(film.movieID)
            for cast_actor in ia.get_movie(film.movieID)['cast']:
                if cast_actor.personID in id_set:
                    graph.add_edge(actor, cast_actor.personID, film.movieID)


#print(len(movie_id_list))
    
graph.save()

#print(ia.get_person(id_list[6])['filmography'][0])