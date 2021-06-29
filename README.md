# CS 170 Project Spring 2021

We competed with other Berkeley students to find the most optimal solutions for a set of inputs to an NP-hard graph problem. The problem can roughly be summarized as follows: given a graph G and two vertices s and t, remove a limited number of vertices and edges from G to maximize the distance of the shortest s-t path.

We wrote a greedy algorithm and a simulated annealing algorithm, as well as several scripts to compute solutions across multiple computers. We reached top 30 overall out of 200+ teams.


## Usage

Run on all inputs:
``` sh
python solver.py
```

Run one input:
``` sh
python solver.py path/to/input.in
```

Run on one set of inputs (small, medium, or large):

``` sh
python solver.py -- small
```

Running on specific number of inputs:
``` sh
python solve_selected.py [num iterations] [size] [list of input numbers, separated by space]
```
