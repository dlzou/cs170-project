from networkx.algorithms.shortest_paths.weighted import dijkstra_path, bellman_ford_path
from networkx.exception import NetworkXNoPath
from networkx import is_connected
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
from os.path import basename, normpath, exists, dirname
from os import makedirs
import sys
import glob
import itertools


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
    rm_node, max_sp = brute_force_node(G)
    for v in rm_node:
        G.remove_node(v)
        c.append(v)

    while len(k) <= k_max:
        SP_nodes, SP_edges, SP = get_SP(G, s, t)
        rm_edge = (None, SP)
        for edge in SP_edges:
            G_temp = G.copy()
            G_temp.remove_edge(*edge)
            if is_connected(G_temp):
                _, _, SP_temp = get_SP(G_temp, s, t)
                if SP_temp >= rm_edge[1]:
                    rm_edge = (edge, SP_temp)
        if rm_edge[0] and len(k) < k_max:
            G.remove_edge(*rm_edge[0])
            k.append(rm_edge[0])
        else:
            break

    return c, k




def find_complement(G, edges, nodes):
    c, k = [], []
    for v in G.nodes:
        if not v in nodes:
            c.append(v)
    for e in G.edges:
        if not e in edges:
            k.append(e)
    return c, k


def brute_force_node(G):
    num_nodes = G.number_of_nodes()
    c_max, k_max = get_constraints(num_nodes)
    res, max = None, -1
    candidates = list(itertools.combinations(G.nodes, c_max))
    curr_res, curr_max = best_sol(G, candidates)
    if curr_max >= max:
        res, max = curr_res, curr_max
    return res, max

def best_sol(G, candidate):
    res, max = None, -1
    num_nodes = G.number_of_nodes()
    s, t = 0, num_nodes - 1
    for curr in candidate:
        if s in curr or t in curr:
            continue
        G_temp = G.copy()
        for node in curr:
            G_temp.remove_node(node)
        if is_connected(G_temp):
            _, _, SP_temp = get_SP(G_temp, s, t)
            if SP_temp >= max:
                res, max = curr, SP_temp
    return res, max


def get_constraints(nodes):
    "Return constraints for c, k"
    if nodes <= 30:
        return 1, 15
    elif nodes <= 50:
        return 3, 50
    return 5, 100


def get_SP(G, s, t):
    try:
        SP_nodes = dijkstra_path(G, s, t)
        SP_edges = [(SP_nodes[i-1], SP_nodes[i]) for i in range(1, len(SP_nodes))]
        SP = sum([G.edges[e]["weight"] for e in SP_edges])
        return SP_nodes, SP_edges, SP
    except NetworkXNoPath as e:
        raise e


# Here's an example of how to run your solver.

# Usage: python3 solver.py inputs/inputs/small/small-1.in

# if __name__ == "__main__":
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     filename = path.split("/")[-1].split(".")[0]
#     size = filename.split("-")[0]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))


#     if not exists(dirname(f"outputs/{size}/")):
#         try:
#             makedirs(dirname(f"outputs/{size}/"))
#         except OSError as e: # Guard against race condition
#             raise e
#     write_output_file(G, c, k, f"outputs/{size}/{filename}.out")


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
#
if __name__ == '__main__':
    if len(sys.argv) == 3:
        size = sys.argv[2]
        if size == "small" or size == "medium" or size == "large":
            inputs = glob.glob(f"inputs/{size}/*.in")
            for input_path in inputs:
                filename = basename(normpath(input_path))[:-3]
                size = filename.split("-")[0]
                output_path = "outputs/output-2/" + size + "/" + filename + ".out"
                G = read_input_file(input_path)
                print(f"Path difference for {filename}: ", end="")
                c, k = solve(G)
                is_valid_solution(G, c, k)
                distance = calculate_score(G, c, k)
                print(distance)
                write_output_file(G, c, k, output_path)
        else:
            print("Second argument must be small, medium, or large")

    elif len(sys.argv) == 2:
        path = sys.argv[1]
        filename = path.split("/")[-1].split(".")[0]
        size = filename.split("-")[0]
        G = read_input_file(path)
        c, k = solve(G)
        is_valid_solution(G, c, k)
        print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))

        if not exists(dirname(f"outputs/output-2/{size}/")):
            try:
                makedirs(dirname(f"outputs/output-2/{size}/"))
            except OSError as e: # Guard against race condition
                raise e
        write_output_file(G, c, k, f"outputs/output-2/{size}/{filename}.out")

    else:
        inputs = glob.glob("inputs/*/*.in")
        for input_path in inputs:
            filename = basename(normpath(input_path))[:-3]
            size = filename.split("-")[0]
            output_path = "outputs/output-2/" + size + "/" + filename + ".out"
            G = read_input_file(input_path)
            print(f"Path difference for {filename}: ", end="")
            c, k = solve(G)
            is_valid_solution(G, c, k)
            distance = calculate_score(G, c, k)
            print(distance)
            write_output_file(G, c, k, output_path)