from networkx.algorithms.shortest_paths.weighted import dijkstra_path, dijkstra_path_length
from networkx.exception import NetworkXNoPath
from networkx import is_connected
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_score
from os.path import basename, normpath, exists, dirname
from os import makedirs
from math import exp, log
import random
import glob
import shutil

if __name__ == '__main__':
    out_folders =  glob.glob(f"cs170-outputs/outputs_*/small")
    for i in range (1, 301):
        filename = "small-"+str(i)
        max_path, max_score = "cs170-outputs/outputs_1/small"+".out"+ filename, -1
        input_path = "inputs/small/" + filename + ".in"
        G_in = read_input_file(input_path)
        for folder_path in out_folders:
            curr_path = folder_path +"/" + filename + ".out"
            curr_dist = read_output_file(G_in, curr_path)
            print(curr_dist)
            if curr_dist > max_score:
                max_score = curr_dist
                max_path = curr_path
        
        print(f"Path difference for {filename}: ", end="")
        print(max_score)
        write_path = "cs170-outputs/res/small"
        shutil.copy(max_path, write_path)
        
