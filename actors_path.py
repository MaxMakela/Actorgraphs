from log import log
import csv
from os import path
from graph import ActorsGraph


class ActorToActorPath(ActorsGraph):
    def __init__(self, from_id, to_id):
        super().__init__(actor_ids=[from_id, to_id])
        self.from_id = from_id
        self.to_id = to_id

    def __eq__(self, other):
        if self.actor_ids != other.actor_ids:
            return False
        for row in self.graph:
            for other_row in other.graph:
                if row != other_row:
                    return False
        return True

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

    def format_connection(self, graph, from_actor_id):
        text = ""
        for other_actor_id, movies_ids in graph.get_connections(from_actor_id):
            graph.remove_edge(from_actor_id, other_actor_id)

            text += "({}--[{}]--{}) ".format(from_actor_id, ", ".join(movies_ids), other_actor_id)
            text += self.format_connection(graph, other_actor_id)

        return text

    def pretty_print(self):
        text = "nodes: {}\npath: ".format(", ".join(self.actor_ids))
        return text + self.format_connection(self.clone(), self.from_id)


if __name__ == "__main__":
    g = ActorToActorPath("Max", "Elena")
    g.add_connection("Max", "Kostya", "Sumy")
    g.add_connection("Kostya", "Svetlana", "Moscow")
    s = g.pretty_print()
    print(s)
