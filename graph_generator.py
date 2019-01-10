import imdb
from log import log
from graph import ActorsGraph
from concurrent import futures
import itertools


class GraphGenerator(object):
    def __init__(self, actor_ids, ia=None, max_threads=32):
        self.ia = ia if ia else imdb.IMDb()
        self.actor_ids = actor_ids
        self.actor_ids_set = set(self.actor_ids)
        self.max_threads = max_threads

    @staticmethod
    def get_filmography(imdb_person):
        filmography = []
        for step in imdb_person:
            if 'actor' in step:
                filmography = step['actor']
                break
        return filmography

    def imdb_get_persons(self, executor, actor_ids):
        def imdb_get_person(actor_id):
            imdb_person = self.ia.get_person_main(actor_id)
            log.debug("person fetched: {} {}".format(actor_id, imdb_person["data"]["name"]))
            return actor_id, imdb_person

        tasks = (executor.submit(imdb_get_person, actor_id) for actor_id in actor_ids)
        for task in futures.as_completed(tasks):
            yield task.result()

    def imdb_get_movies(self, executor, movie_ids):
        def imdb_get_movie(movie_id):
            imdb_movie = self.ia.get_movie(movie_id)
            log.debug("movie fetched: {} {}".format(movie_id, imdb_movie["title"]))
            return movie_id, imdb_movie

        tasks = (executor.submit(imdb_get_movie, movie_id) for movie_id in movie_ids)
        for task in futures.as_completed(tasks):
            yield task.result()

    def generate(self):
        """Generate graph for actors using IMDB API"""
        graph = ActorsGraph(self.actor_ids)
        films_ids_dict = {}

        with futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for actor_id, person in self.imdb_get_persons(executor, graph.actor_ids):
                log.info("imdb person found: {}: {}".format(actor_id, person["data"]["name"]))
                for film in self.get_filmography(person["data"]['filmography']):
                    if film.movieID in films_ids_dict:
                        films_ids_dict[film.movieID] += 1
                    else:
                        films_ids_dict[film.movieID] = 1

        films_ids = [film_id for film_id, count in films_ids_dict.items() if count > 1]

        with futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            log.info("movies to look at: {}".format(len(films_ids)))
            for film_id, film in self.imdb_get_movies(executor, films_ids):
                actors_in_cast = [actor.personID for actor in film['cast'] if actor.personID in self.actor_ids]

                for id1, id2 in list(itertools.combinations(actors_in_cast, 2)):
                    log.info("adding edge {}, {}: {} '{}'".format(id1, id2, film_id, film["title"]))
                    graph.add_edge(id1, id2, film_id)

        return graph
