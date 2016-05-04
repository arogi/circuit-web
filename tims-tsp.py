#!/usr/bin/python

import cgi, cgitb
import json
#import GISOps
import numpy as np
from scipy.spatial.distance import cdist
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import argparse


def Distance(i,j):
    return dist[i][j]

def main(nodes):
    # Create routing model
    if nodes > 0:
        # TSP of size args.tsp_size
        # Second argument = 1 to build a single tour (it's a TSP).
        # Nodes are indexed from 0 to parser_tsp_size - 1, by default the start of
        # the route is node 0.
        routing = pywrapcp.RoutingModel(nodes, 1)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        # Setting first solution heuristic (cheapest addition).
        search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        routing.SetArcCostEvaluatorOfAllVehicles(Distance)
        print pywrapcp.Solver
        assignment = routing.Solve()
        if assignment:
            # Solution cost.
            print(assignment.ObjectiveValue())
            # Inspect solution.
            # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
            route_number = 0
            node = 0
            route = ''
            while not routing.IsEnd(node):
                route += str(node) + ' -> '
                node = assignment.Value(routing.NextVar(node))
            route += '0'
            print(route)
        else:
            print('No solution found.')
    else:
        print('Specify an instance greater than 0.')

# start here!!!
dist = {0: [0,9,60,60,10],
        1: [9,0,10,45,100],
        2: [60,10,0,15,90],
        3: [60,45,15,0,12],
        4: [10,100,90,12,0]}

nodes = len(dist)

# main(parser.parse_args())
main(nodes)
