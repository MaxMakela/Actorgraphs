import imdb
from log import log
from graph import ActorsGraph
import itertools


class GraphGenerator(object):
    def __init__(self, actor_ids, ia=None):
        self.ia = ia if ia else imdb.IMDb()
        self.actor_ids = actor_ids
        self.actor_ids_set = set(self.actor_ids)

    @staticmethod
    def get_filmography(imdb_person):
        filmography = []
        for step in imdb_person:
            if 'actor' in step:
                filmography = step['actor']
                break
        return filmography

    # def combination(cast):
    #     cast_id = [actor.personID for actor in cast]
    #     return list(itertools.combinations(cast_id, 2))


    def generate(self):
        """Generate graph for actors using IMDB API"""
        graph = ActorsGraph(self.actor_ids)  
        films_ids_dict = {}

        for actor_id in graph.actor_ids:
            person = self.ia.get_person_main(actor_id)
            for film in self.get_filmography(person["data"]['filmography']):
                if film.movieID in films_ids_dict:
                    films_ids_dict[film.movieID]+=1
                else:
                    films_ids_dict[film.movieID]=1

        films_ids_list = [i for i in films_ids_dict if films_ids_dict[i]!=1]

        for film in films_ids_list:
            actors_in_cast = []
            for actor in self.ia.get_movie(film)['cast']:
                if actor.personID in actor_id:
                    actors_in_cast.append(actor.personID)
            for actor_duo in list(itertools.combinations(actors_in_cast, 2)):
                graph.add_edge(actor_duo[0], actor_duo[1], film)        


        # for actor_id in graph.actor_ids:
        #     person = self.ia.get_person_main(actor_id)
        #     log.info("imdb person found: {}: {}".format(actor_id, person["data"]["name"]))
        #     for film in self.get_filmography(person["data"]['filmography']):
        #         if film.movieID not in films_ids_set:
        #             films_ids_set.add(film.movieID)

        #             for actor_duo in list(itertools.combinations([actor.personID for actor in self.ia.get_movie(film.movieID)['cast']], 2)):
        #                  if actor_duo[0] in self.actor_ids_set and actor_duo[1] in self.actor_ids_set:
        #                     log.info("adding edge {}, {}: {} '{}'".format(
        #                         actor_duo[0],
        #                         actor_duo[1],
        #                         film.movieID,
        #                         film.data["title"]
        #                     ))
        #                     graph.add_edge(actor_duo[0], actor_duo[1], film.movieID)

        return graph
