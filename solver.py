import networkx.algorithms.shortest_paths.weighted.dijkstra_path as dijkstra_path
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
from os.path import basename, normpath
import sys
import glob


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    G = G.copy()
    num_nodes = G.number_of_nodes()
    s, t = G.nodes[0], G.nodes[num_nodes - 1]
    c_max, k_max = get_constraints(num_nodes)
    c, k = [], []

    while len(c) <= c_max and len(k) <= k_max:
        SP_nodes, SP_edges, SP = get_SP(G, s, t)
        to_remove = (None, SP)
        for node in SP_nodes:
            G_temp = G.copy()
            G_temp.remove_node(node)
            SP_nodes_temp, SP_edges_temp, SP_temp = get_SP(G_temp, s, t)


    return c, k


def get_constraints(nodes):
    "Return constraints for c, k"
    if nodes <= 30:
        return 1, 15
    elif nodes <= 50:
        return 3, 50
    return 5, 100


def get_SP(G, s, t):
    SP_nodes = dijkstra_path(G, s, t)
    SP_edges = [(SP_nodes[i-1], SP_nodes[i]) for i in range(1, len(SP_nodes))]
    SP = sum([G.edges[e]["weight"] for e in SP_edges])
    return SP_nodes, SP_edges, SP


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
