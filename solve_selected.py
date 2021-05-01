from parse import read_input_file, read_output_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
import solver

"""
Usage:

python solve_selected.py [# iterations] [size] [list of input numbers, separated by space]
"""

if __name__ == "__main__":
    iters = sys.argv[1]
    size = sys.argv[2]
    inputs = sys.argv[3:]

    for num in inputs:
        best = {"c": set(), "k": set(), "SP": float("-inf")}
        G = read_input_file(f"inputs/{size}/{size}-{num}.in")
        for i in iters:
            c, k = solver.solve(G)
            is_valid_solution(G, c, k)
            SP = calculate_score(G, c, k)
            if SP > best["SP"]:
                best["c"] = c.copy()
                best["k"] = k.copy()
                best["SP"] = SP

        print(f"Max path difference for {size}-{num}: " + str(best["SP"]))
        output_path = f"outputs/{size}/{size}-{num}.out"
        score = read_output_file(G, output_path)
        if score < best["SP"]:
            write_output_file(G, best["c"], best["k"], output_path)
            print(f"{size}-{num}.out overwritten.")
