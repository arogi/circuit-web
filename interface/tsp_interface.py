#!/usr/bin/python

import cgi, cgitb
import json
import warnings
import pipes
import GISOps
import sys
#import numpy as np
#from scipy.spatial.distance import cdist
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import argparse

warnings.filterwarnings("ignore")

def main():
  ReadJSONandSolve()

def ReadJSONandSolve():
    SD = read_problem(receivedMarkerData)

def read_problem(file):
    global numSites
    global numFeatures
    global numDemands
    global numForced
    global facilityIDs
    global demandIDs
    global siteArray
    global demandArray
    global js
    global demandTotal

    #Although this is a tsp problem, since I am reading the js files developed for MCLP I am leaving the default values for convenience.  Strictly speaking these values are not needed for the TSP
    p = -1
    SD = -1

    # read data from string object
    ###print 'Reading JSON String Object!'
    try:
      js = json.loads(file) # Convert the string into a JSON Object
    except IOError:
      print "unable to read file"

    numFeatures = len(js['features'])

    # if the geoJSON includes p and SD values, use these rather than any input arguments
    try:
      p = js['properties']['pValue']
    except IOError:
      print "geoJSON has no pValue"
    try:
      SD = js['properties']['distanceValue']*1000
    except IOError:
      print "geoJSON has no distanceValue"

    xyPointArray = [[None for k in range(2)] for j in range(numFeatures)]
    xyPointArray = GISOps.GetCONUSeqDprojCoords(js) # Get the Distance Coordinates in CONUS EqD Projection

    facilityIDs = []
    demandIDs = []
    demandTotal = 0

    # rowID holds the index of each feature in the JSON object
    rowID = 0

    # typeFD = Field Codes Represent:
    #  1 = demand only
    #  2 = potential facility only
    #  3 = both demand and potential facility
    for element in js['features']:
        if element['properties']['typeFD']==3: # Both Facility/Demand
            facilityIDs.append(rowID)
            demandIDs.append(rowID)
            demandTotal += element['properties']['pop']
            element['properties']['fillColor'] = '#46A346'
        elif element['properties']['typeFD']==2: # Facility Site Only
            facilityIDs.append(rowID)
            element['properties']['fillColor'] = '#FDBC43'
        elif element['properties']['typeFD']==1: # Demand Point Only
            demandIDs.append(rowID)
            demandTotal += element['properties']['pop']
            element['properties']['fillColor'] = '#6198FD'
        rowID += 1

    numSites = len(facilityIDs)
    numDemands = len(demandIDs)

    siteArray = [[None for k in range(3)] for j in range(numSites)]
    demandArray = [[None for k in range(3)] for j in range(numDemands)]

    # assemble pertinent data for the model into multidimensional arrays
    i = 0
    j = 0
    k = 0
    for line in js['features']:
      if line['properties']['typeFD']>=2:  # Potential facility site
        siteArray[i][0] = xyPointArray[k][0]
        siteArray[i][1] = xyPointArray[k][1]
        siteArray[i][2] = line['properties']['forcedLocation']
        i += 1
      if line['properties']['typeFD'] % 2 == 1:  # Demand point
        demandArray[j][0] = xyPointArray[k][0]
        demandArray[j][1] = xyPointArray[k][1]
        demandArray[j][2] = line['properties']['pop']
        j += 1
      k += 1

    numForced = sum(zip(*siteArray)[2])
    demandTotal = sum(zip(*demandArray)[2])
    js['properties']['demandTotal'] = demandTotal

    ###print 'Finished Reading the Data!'
    print [p, SD]
    return [p, SD]

if len(sys.argv) >= 1:
    file = sys.argv[1]
    print "Problem instance from", file
    p = read_problem(file)
    main(p)
else:
    main(None)





"""


def Distance(i,j):
    return dist[i][j]



def main(nodes):
    #Process info from web

    # Create routing model
    if nodes > 0:
        # TSP of size args.tsp_size
        # Second argument = 1 to build a single tour (it's a TSP).
        # Nodes are indexed from 0 to parser_tsp_size - 1, by default the start of
        # the route is node 0.
        routing = pywrapcp.RoutingModel(nodes, 1)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        # Setting first solution heuristic (cheapest addition).
        search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        routing.SetArcCostEvaluatorOfAllVehicles(Distance)

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
#main(nodes)




#from ortools.linear_solver import pywraplp

###########################################################
##################### The main controller code starts here.
###########################################################

# Create instance of FieldStorage and get data
form = cgi.FieldStorage()
receivedMarkerData = form.getvalue('useTheseMarkers')
## convert the received json string into a Python object
#receivedGeoJson = json.loads(receivedMarkerData)

# the magic happens here...
#main()

# prepare for output... the GeoJSON should be returned as a string
#transformedMarkerData = json.dumps(js)
print "Content-type:text/html\r\n\r\n"
print str(main(nodes))

"""
