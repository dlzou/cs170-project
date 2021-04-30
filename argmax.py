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
    for i in range (300):
        max_path, max_score = None, -1
        input_path = "inputs/small/" + filename + ".in"
        filename = "small-"+str(i)
        G_in = read_input_file(input_path)
        for folder_path in out_folders:
            curr_path = folder_path +"/" + filename + ".out"
            curr_dist = read_output_file(G_in, curr_path)
            if curr_dist > max_score:
                max_score = curr_dist
                max_path = curr_path
        
        print(f"Path difference for {filename}: ", end="")
        print(max_score)
        write_path = "cs170-outputs/best_out/small/"+ filename + ".out"
        shutil.copy(max_path, write_path)
        
