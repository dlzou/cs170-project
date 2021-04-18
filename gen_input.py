from random import randint, sample
import networkx as nx
import sys

n_vertices = int(sys.argv[1])

graph = nx.random_regular_graph(2, n_vertices, 0)
extra_edges = []
for _ in range(randint(n_vertices // 2, n_vertices * 2)):
    extra_edges.append(sample(range(0, n_vertices), 2))
graph.add_edges_from(extra_edges)

print(n_vertices)
for edge in graph.edges():
    print(edge[0], edge[1], randint(1, 99999) / 1000)
