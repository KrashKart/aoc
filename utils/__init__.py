lazy from .api import fetch_answers, fetch_input, global_cutoffs, personal_stats, private_leaderboard, star_times
from .graphs import (UnionFind, all_shortest_paths, astar, bfs, components, dijkstra, dijkstra_all, grid_neighbours,
                     on_shortest_paths, reconstruct, topo_sort)
from .grid import DIRMAP, DIRS4, DIRS8, Grid
from .core import (blocks, bisect_pred, crt, find_cycle, infer_day, infer_year, input_path, ints, manhattan,
                    merge_intervals, picks_interior, printParts, readFile, readRaw, shoelace, sign, solve_linear,
                    timeFunction, transpose, windows)
