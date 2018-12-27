import imdb
from log import log
from graph import ActorsGraph
from concurrent import futures


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

    @staticmethod
    def combinations(actors):
        for i, actor in enumerate(actors):
            for j in range(i + 1, len(actors)):
                yield actor.personID, actors[j].personID

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

    def filter_actors(self, cast):
        return [actor for actor in cast if actor.personID in self.actor_ids_set]

    def filter_movies(self, imdb_person, films_ids_set):
        movies = self.get_filmography(imdb_person["data"]['filmography'])
        return [movie.movieID for movie in movies if movie.movieID not in films_ids_set]

    def generate(self):
        """Generate graph for actors using IMDB API"""
        graph = ActorsGraph(self.actor_ids)
        films_ids_set = set()

        with futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for actor_id, imdb_person in self.imdb_get_persons(executor, graph.actor_ids):
                person_movie_ids = self.filter_movies(imdb_person, films_ids_set)
                log.info("imdb person found: {}: {}".format(actor_id, imdb_person["data"]["name"]))
                log.info("movies to look at: {}".format(len(person_movie_ids)))

                for movie_id, imdb_movie in self.imdb_get_movies(executor, person_movie_ids):
                    films_ids_set.add(movie_id)
                    important_actors = self.filter_actors(imdb_movie['cast'])
                    for id1, id2 in self.combinations(important_actors):
                        log.info("adding edge {}, {}: {} '{}'".format(id1, id2, movie_id, imdb_movie["title"]))
                        graph.add_edge(id1, id2, movie_id)

        return graph
