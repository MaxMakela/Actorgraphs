from log import log
from graph import ActorsGraph
from collections import deque


class ActorToActorPath(ActorsGraph):

    @staticmethod
    def search(actors_graph, start_id, end_id):
        assert start_id in actors_graph.indices, "{}: actor is not in the graph".format(start_id)
        assert end_id in actors_graph.indices, "{}: actor is not in the graph".format(end_id)

        visited_actors = ActorToActorPath.bfs(actors_graph, start_id, end_id)
        log.debug(visited_actors)

        graph_path = ActorToActorPath(start_id, end_id)
        # TODO: breadth first search goes here.
        # TODO: use graph_path.add_connection to populate graph_path

        return graph_path

    @staticmethod
    def bfs(actors_graph, start_id, end_id):
        visited_actors = dict()
        current_depth = 0
        queue = deque([(start_id, current_depth)])

        while len(queue) > 0:
            actor_id, depth = queue.pop()
            if actor_id in visited_actors:
                continue

            visited_actors[actor_id] = depth
            if actor_id == end_id:
                return visited_actors

            current_depth = current_depth + 1
            for other_actor_id, _ in actors_graph.get_connections(actor_id):
                if other_actor_id not in visited_actors:
                    queue.appendleft((other_actor_id, current_depth))
        return None

    def __init__(self, from_id, to_id):
        super().__init__(actor_ids=[from_id, to_id])
        self.from_id = from_id
        self.to_id = to_id

    def __eq__(self, other):
        if self.__class__ != other.__class__ or self.actor_ids != other.actor_ids:
            return False
        for i, row in enumerate(self.graph):
            if row != other.graph[i]:
                return False
        return True

    def __repr__(self):
        text = "{}\n".format(", ".join(self.actor_ids))
        return text + "\n".join(str(line) for line in self.graph)

    def add_connection(self, actor_id, other_actor_id, movie_id):
        assert actor_id in self.indices, "{}: first passed actor is not in the path".format(actor_id)

        self.add_actor(other_actor_id)
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
