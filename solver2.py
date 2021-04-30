# from networkx.algorithms.shortest_paths.weighted import dijkstra_path, bellman_ford_path
# from networkx.exception import NetworkXNoPath
# from networkx import is_connected
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
from os.path import basename, normpath, exists, dirname
from os import makedirs
import sys
import glob
import itertools
import networkx as nx


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
    s, t = 0, num_nodes - 1
    c_max, k_max = get_constraints(num_nodes)
    c, k = [], []
    rm_node, rm_edge, max_sp = brute_force(G)
    for v in rm_node:
        G.remove_node(v)
        c.append(v)
    for e in rm_edge:
        G.remove_edge(*e)
        k.append(e)
    return c, k

def longest_path(G):
    G = G.copy()


def brute_force(G):
    num_nodes = G.number_of_nodes()
    c_max, k_max = get_constraints(num_nodes)
    candidate_v = list(itertools.combinations(G.nodes, c_max))
    res_edge, res_node, max_sp = None, None, -1
    num_nodes = G.number_of_nodes()
    s, t = 0, num_nodes - 1
    for curr_nodes in candidate_v:
        v_res_curr = []
        if s in curr_nodes or t in curr_nodes:
            continue
        G_temp = G.copy()
        for node in curr_nodes:
            G_temp.remove_node(node)
            v_res_curr.append(node)
        path_tree = list(nx.dfs_edges(G_temp, 0))
        candidate_e = list(itertools.combinations(path_tree, 15))
        for curr_edges in candidate_e:
            e_res_curr = []
            G_curr = G_temp.copy()
            for e in curr_edges:
                if e[0] == s or e[0] == t or e[1] == s or e[1] == t:
                    continue
                G_curr.remove_edge(*e)
                if not nx.is_connected(G_temp):
                    G_curr.add_edge(*e)
                else:
                    e_res_curr.append(e)
            _, _, SP_temp = get_SP(G_curr, s, t)
            if SP_temp > max_sp:
                res_edge, res_node, max_sp = e_res_curr, curr_nodes, SP_temp
    return res_edge, res_node, max_sp


def get_constraints(nodes):
    "Return constraints for c, k"
    if nodes <= 30:
        return 1, 15
    elif nodes <= 50:
        return 3, 50
    return 5, 100


def get_SP(G, s, t):
    try:
        SP_nodes = nx.dijkstra_path(G, s, t)
        SP_edges = [(SP_nodes[i-1], SP_nodes[i]) for i in range(1, len(SP_nodes))]
        SP = sum([G.edges[e]["weight"] for e in SP_edges])
        return SP_nodes, SP_edges, SP
    except nx.NetworkXNoPath as e:
        # raise e
        return None, None, -1


# Here's an example of how to run your solver.

# Usage: python3 solver.py inputs/inputs/small/small-1.in

if __name__ == "__main__":
    assert len(sys.argv) == 2
    path = sys.argv[1]
    filename = path.split("/")[-1].split(".")[0]
    size = filename.split("-")[0]
    G = read_input_file(path)
    c, k = solve(G)
    assert is_valid_solution(G, c, k)
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))


    if not exists(dirname(f"outputs/{size}/")):
        try:
            makedirs(dirname(f"outputs/{size}/"))
        except OSError as e: # Guard against race condition
            raise e
    write_output_file(G, c, k, f"outputs/{size}/{filename}.out")


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
#
# if __name__ == '__main__':
#     if len(sys.argv) == 2:
#         path = sys.argv[1]
#         filename = path.split("/")[-1].split(".")[0]
#         size = filename.split("-")[0]
#         G = read_input_file(path)
#         c, k = solve(G)
#         is_valid_solution(G, c, k)
#         print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#
#         if not exists(dirname(f"outputs/{size}/")):
#             try:
#                 makedirs(dirname(f"outputs/{size}/"))
#             except OSError as e: # Guard against race condition
#                 raise e
#         write_output_file(G, c, k, f"outputs/{size}/{filename}.out")
#
#     else:
#         inputs = glob.glob('inputs/*/*.in')
#         for input_path in inputs:
#             filename = basename(normpath(input_path))[:-3]
#             size = filename.split("-")[0]
#             output_path = 'outputs/' + size + '/' + filename + '.out'
#             G = read_input_file(input_path)
#             print(f'Path difference for {filename}: ', end='')
#             c, k = solve(G)
#             is_valid_solution(G, c, k)
#             distance = calculate_score(G, c, k)
#             print(distance)
#             write_output_file(G, c, k, output_path)
