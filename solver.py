from networkx.algorithms.shortest_paths.weighted import dijkstra_path, dijkstra_path_length
from networkx.exception import NetworkXNoPath
from networkx import is_connected
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
from os.path import basename, normpath, exists, dirname
from os import makedirs
from math import exp, log
import random
import sys
import glob


def solve_greedy(G):
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
    _, _, GSP = get_SP(G, s, t)

    while len(c) <= c_max and len(k) <= k_max:
        SP_nodes, SP_edges, SP = get_SP(G, s, t)
        # print(SP - GSP)

        rm_node = (None, SP)
        for node in SP_nodes:
            G_temp = G.copy()
            G_temp.remove_node(node)
            if is_connected(G_temp):
                _, _, SP_temp = get_SP(G_temp, s, t)
                if SP_temp >= rm_node[1]:
                    rm_node = (node, SP_temp)

        rm_edge = (None, SP)
        for edge in SP_edges:
            G_temp = G.copy()
            G_temp.remove_edge(*edge)
            if is_connected(G_temp):
                _, _, SP_temp = get_SP(G_temp, s, t)
                if SP_temp >= rm_edge[1]:
                    rm_edge = (edge, SP_temp)

        if rm_node[0] and len(c) < c_max and rm_node[1] >= rm_edge[1]:
            G.remove_node(rm_node[0])
            c.append(rm_node[0])
        elif rm_edge[0] and len(k) < k_max:
            G.remove_edge(*rm_edge[0])
            k.append(rm_edge[0])
        else:
            break

    return c, k


# def solve_greedy_2(G):
#     H = G.copy()
#     num_nodes = H.number_of_nodes()
#     s, t = 0, num_nodes - 1
#     c_max, k_max = get_constraints(num_nodes)
#     c, k = [], []
#     T = int(0.5 * num_nodes ** 2)

#     for i in range(1, T):
#         # Probability of backtracking by removing random node from c or edge from k
#         back_prob = exp(-i / num_nodes)
#         if back_prob > random.random() and len(c) + len(k) > 0:
#             a = random.choice(c + k)
#             if isinstance(a, int):
#                 c.remove(a)
#                 H.add_node(a)
#                 for v in range(t):
#                     if G.has_edge(a, v):
#                         H.add_edge(a, v, **G.get_edge_data(a, v))
#             else:
#                 k.remove(a)
#                 H.add_edge(*a, **G.get_edge_data(*a))
#             continue

#         # Run greedy algorithm
#         SP_nodes, SP_edges, SP = get_SP(H, s, t)
#         rm_node = (None, SP)
#         for node in SP_nodes:
#             H_temp = H.copy()
#             H_temp.remove_node(node)
#             if is_connected(H_temp):
#                 _, _, SP_temp = get_SP(H_temp, s, t)
#                 if SP_temp >= rm_node[1]:
#                     rm_node = (node, SP_temp)
#         rm_edge = (None, SP)
#         for edge in SP_edges:
#             H_temp = H.copy()
#             H_temp.remove_edge(*edge)
#             if is_connected(H_temp):
#                 _, _, SP_temp = get_SP(H_temp, s, t)
#                 if SP_temp >= rm_edge[1]:
#                     rm_edge = (edge, SP_temp)

#         if rm_node[0] and len(c) < c_max and rm_node[1] >= rm_edge[1]:
#             H.remove_node(rm_node[0])
#             c.append(rm_node[0])
#         elif rm_edge[0] and len(k) < k_max:
#             H.remove_edge(*rm_edge[0])
#             k.append(rm_edge[0])
#         else:
#             continue
#     return c, k


def solve_anneal(G):
    H = G.copy()
    num_nodes = H.number_of_nodes()
    s, t = 0, num_nodes - 1
    c_max, k_max = get_constraints(num_nodes)
    c, k = set(), set()
    best = {"c": c, "k": k, "SP": float("-inf")}
    i, i_max = 1, int(log(num_nodes)) * num_nodes ** 2
    T0 = i_max

    while i < i_max:
        # if i % 100 == 0:
        #     GSP = dijkstra_path_length(G, s, t)
        #     SP = dijkstra_path_length(H, s, t)
        #     print(SP - GSP)

        # Create search space for neighbors
        SP_nodes, SP_edges, SP = get_SP(H, s, t)
        move_space = {}
        for a in c | k:
            move_space[a] = 0 # Remove from c or k
        if len(c) < c_max:
            for a in SP_nodes:
                move_space[a] = 1 # Add to c
        if len(k) < k_max:
            for a in SP_edges:
                move_space[a] = 1 # Add to k

        # Pick a neighbor
        a, add_to = random.choice(list(move_space.items()))
        H_temp = H.copy()
        if add_to:
            if isinstance(a, int): # Check if a is node
                H_temp.remove_node(a)
            else:
                H_temp.remove_edge(*a)
        else:
            if isinstance(a, int):
                H_temp.add_node(a)
                for v in G.neighbors(a):
                    if v not in c and (a, v) not in k and (v, a) not in k:
                        H_temp.add_edge(a, v, **G.get_edge_data(a, v))
            else:
                H_temp.add_edge(*a, **G.get_edge_data(*a))
        if not is_connected(H_temp):
            i += 1
            continue

        # Make move with probability
        _, _, SP_move = get_SP(H_temp, s, t)
        if SP_move > SP:
            prob = 1
        else:
            T = T0 / i
            prob = exp((SP_move - SP) / T)
        if prob > random.random():
            if add_to:
                if isinstance(a, int):
                    c.add(a)
                else:
                    k.add(a)
            else:
                if isinstance(a, int):
                    c.remove(a)
                else:
                    k.remove(a)
            H = H_temp

        if SP_move > best["SP"]:
            best["c"] = c.copy()
            best["k"] = k.copy()
            best["SP"] = SP_move
        i += 1

    return best["c"], best["k"]


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
        return SP_nodes[1:-1], SP_edges, SP
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
solve = solve_greedy

if __name__ == '__main__':
    if len(sys.argv) == 3:
        size = sys.argv[2]
        if size == "small" or size == "medium" or size == "large":
            inputs = glob.glob(f"inputs/{size}/*.in")
            for input_path in inputs:
                filename = basename(normpath(input_path))[:-3]
                size = filename.split("-")[0]
                output_path = "outputs/output-1/" + size + "/" + filename + ".out"
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

        if not exists(dirname(f"outputs/output-1/{size}/")):
            try:
                makedirs(dirname(f"outputs/output-1/{size}/"))
            except OSError as e: # Guard against race condition
                raise e
        write_output_file(G, c, k, f"outputs/output-1/{size}/{filename}.out")

    else:
        inputs = glob.glob("inputs/*/*.in")
        for input_path in inputs:
            filename = basename(normpath(input_path))[:-3]
            size = filename.split("-")[0]
            output_path = "outputs/output-1/" + size + "/" + filename + ".out"
            G = read_input_file(input_path)
            print(f"Path difference for {filename}: ", end="")
            c, k = solve(G)
            is_valid_solution(G, c, k)
            distance = calculate_score(G, c, k)
            print(distance)
            write_output_file(G, c, k, output_path)