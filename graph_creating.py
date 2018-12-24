from graph import ActorsGraph
import csv
import imdb


if __name__ == "__main__":
    id_list = []
    ia = imdb.IMDb()

    with open('actors_id.csv', newline='') as csvfile:
        for row in csv.reader(csvfile, delimiter=','):
            id_list.append(row[0])

    graph = ActorsGraph.generate(id_list[:10], ia)
    graph.save()
