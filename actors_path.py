from log import log
from graph import ActorsGraph


class ActorToActorPath(ActorsGraph):

    @staticmethod
    def search(actors_graph, actor_id, another_actor_id):
        assert actor_id in actors_graph.indices, "{}: actor is not in the graph".format(actor_id)
        assert another_actor_id in actors_graph.indices, "{}: actor is not in the graph".format(another_actor_id)

        graph_path = ActorToActorPath(actor_id, another_actor_id)
        # TODO: breadth first search goes here.
        # TODO: use graph_path.add_connection to populate graph_path

        return graph_path

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
