from log import log
from graph import ActorsGraph
from collections import deque, defaultdict
import itertools


class ActorToActorPath(ActorsGraph):

    @staticmethod
    def search(actors_graph, start_id, end_id):
        assert start_id in actors_graph.indices, "{}: actor is not in the graph".format(start_id)
        assert end_id in actors_graph.indices, "{}: actor is not in the graph".format(end_id)

        graph_path = ActorToActorPath(start_id, end_id)

        # Breadth First Search will return all visited actors on the path to the target actor;
        # It also returns depth index on each visited actor, and the max depth reached.
        visited_actors, max_depth = ActorToActorPath.bfs(actors_graph, start_id, end_id)

        # Next, the reverse search is executed. Using depth information it traverses visited
        # actors backwards, from end_id to start_id. It constructs ActorToActorPath path along
        # the way. Resulting ActorToActorPath contains all possible shortest paths from
        # start_id to end_id.
        previously_connected = {end_id}
        for d in reversed(range(max_depth + 1)):
            connected = set()

            for actor_id in visited_actors[d]:
                if actor_id in previously_connected:
                    for other_actor_id, films in actors_graph.get_connections(actor_id):
                        if other_actor_id in visited_actors[d - 1]:
                            graph_path.add_connection(actor_id, other_actor_id, films)
                            connected.add(other_actor_id)
            if connected:
                log.debug("connected: {}".format(", ".join(connected)))
                previously_connected.update(connected)

        return graph_path

    @staticmethod
    def bfs(actors_graph, start_id, end_id):
        depth = 0
        visited_actors = {start_id: depth}
        visited_actors_by_depth = defaultdict(set)
        visited_actors_by_depth[depth] = start_id
        queue = deque([(start_id, depth)])

        while len(queue) > 0:
            actor_id, depth = queue.pop()
            depth = depth + 1

            for other_actor_id, _ in actors_graph.get_connections(actor_id):
                if other_actor_id not in visited_actors:
                    visited_actors[other_actor_id] = depth
                    visited_actors_by_depth[depth].add(other_actor_id)

                    if other_actor_id == end_id:
                        return visited_actors_by_depth, depth

                    queue.appendleft((other_actor_id, depth))

        return None

    def __init__(self, from_id, to_id):
        super().__init__(actor_ids=[from_id, to_id])
        self.from_id = from_id
        self.to_id = to_id

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        if set(self.actor_ids) != set(other.actor_ids):
            return False

        for id1, id2 in list(itertools.combinations(self.actor_ids, 2)):
            if self.get_edge(id1, id2) != other.get_edge(id1, id2):
                return False

        return True

    def __repr__(self):
        text = "{}\n".format(", ".join(self.actor_ids))
        return text + "\n".join(str(line) for line in self.graph)

    def add_connection(self, actor_id, other_actor_id, movie_id):
        assert actor_id in self.indices, "{}: first passed actor is not in the path".format(actor_id)

        self.add_actor(other_actor_id)

        if type(movie_id) is set:
            for mid in movie_id:
                self.add_edge(actor_id, other_actor_id, mid)
        else:
            self.add_edge(actor_id, other_actor_id, movie_id)

    def add_actor(self, actor_id):
        """Add actor to the underlying matrix, to indices and to actors list"""
        if actor_id not in self.indices:
            self.actor_ids.append(actor_id)
            self.indices[actor_id] = len(self.actor_ids) - 1

            for row in self.graph:
                row.append(None)
            self.graph.append([None for _ in self.actor_ids])

    def format_connections(self, from_actor_id, visited_connections=None):
        if visited_connections is None:
            visited_connections = set()

        text = ""
        for other_actor_id, movies_ids in self.get_connections(from_actor_id, visited_connections):
            visited_connections.add((from_actor_id, other_actor_id))

            text += "({}--[{}]--{}) ".format(from_actor_id, ", ".join(movies_ids), other_actor_id)
            text += self.format_connections(other_actor_id, visited_connections)

        return text
