from log import log
import csv
from os import path


class ActorsGraph(object):

    @staticmethod
    def load(file_path="./graph.csv"):
        """Load graph from csv file"""
        assert path.isfile(file_path), "'{}' is not a file".format(file_path)
        log.debug("loading graph from: {}".format(file_path))
        graph = None

        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, quotechar='"')
            for i, row in enumerate(reader):
                if not graph:
                    graph = ActorsGraph(row)
                else:
                    for j, movie_ids in enumerate(row):
                        for movie_id in movie_ids.split(","):
                            graph.add_edge_by_indices(i - 1, j, movie_id)

        assert graph, "graph has not been created, check '{}' file".format(file_path)
        return graph

    def __init__(self, actor_ids=None):
        if actor_ids is None:
            actor_ids = []

        self.actor_ids = actor_ids
        self.indices = dict((aid, i) for i, aid in enumerate(actor_ids))
        self.graph = [[None for _ in actor_ids] for _ in actor_ids]
        log.debug("graph {}x{} has been created".format(len(actor_ids), len(actor_ids)))

    def clone(self):
        copy = ActorsGraph(self.actor_ids)
        copy.graph = [[self.get_edge(id1, id2) for id1 in self.actor_ids] for id2 in self.actor_ids]
        return copy

    def get_index(self, actor_id):
        assert actor_id in self.indices, "{}: actor is not in the graph".format(actor_id)
        return self.indices[actor_id]

    def add_edge_by_indices(self, i1, i2, movie_id):
        if movie_id:
            log.debug("({}, {}) adding: {}".format(i1, i2, movie_id))
            if self.graph[i1][i2]:
                self.graph[i1][i2].add(movie_id)
            else:
                self.graph[i1][i2] = {movie_id}

            # TODO: matrix is symmetrical now, but could be refactored to half-matrix for memory efficiency
            self.graph[i2][i1] = self.graph[i1][i2]

    def remove_edge(self, actor_id, other_actor_id):
        i1 = self.get_index(actor_id)
        i2 = self.get_index(other_actor_id)
        self.graph[i1][i2] = None
        self.graph[i2][i1] = None

    def add_edge(self, actor_id, other_actor_id, movie_id):
        if actor_id != other_actor_id:
            i1 = self.get_index(actor_id)
            i2 = self.get_index(other_actor_id)
            self.add_edge_by_indices(i1, i2, movie_id)

    def get_edge(self, actor_id, other_actor_id):
        i1 = self.get_index(actor_id)
        i2 = self.get_index(other_actor_id)
        return self.graph[i1][i2] if self.graph[i1][i2] else self.graph[i2][i1]

    def get_connections(self, actor_id, visited_connections=None):
        if visited_connections is None:
            visited_connections = set()

        for other_actor_id in self.indices.keys():
            movies_ids = self.get_edge(actor_id, other_actor_id)
            if movies_ids \
                    and (actor_id, other_actor_id) not in visited_connections \
                    and (other_actor_id, actor_id) not in visited_connections:
                log.debug("actors {}, {}: connection found {}".format(actor_id, other_actor_id, movies_ids))
                yield (other_actor_id, movies_ids)

    def save(self, file_path="./graph.csv"):
        def concat_movie_ids(movie_ids):
            return ",".join(movie_ids) if movie_ids else ""

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            log.debug("saving graph to: {}".format(file_path))
            writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.actor_ids)
            for row in self.graph:
                movies = [concat_movie_ids(movie_ids) for movie_ids in row]
                writer.writerow(movies)
