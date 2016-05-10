# Copyright 2015-2016 Arogi Inc
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Antonio Medrano and Timothy J. Niblett

"""A Traveling Salesman example that imports a JSON file problem definition and
   solves using the Google OR-Tools solver using constraint progrmming. Note
   that our test files include other data used to solve both the MCLP and
   p-Median problems.
"""

import cgi
import sys
import json
import GISOps
import time
import numpy as np
from scipy.spatial.distance import cdist
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from bisect import bisect
import warnings

warnings.filterwarnings("ignore")

printModel = False

readType = 1

def main():
  #print "Setting up and solving problem!"
  readJSONandSolve()

def readJSONandSolve():
  read_problem(receivedMarkerData)
  RunTSP(nodes)

def RunTSP(nodes):
    #TSP using Google OR-Tools Constraint Programming model example
    warnings.filterwarnings("ignore")
    start_time = time.time()
    PreComputeDistances() #compute the distances between points
    #DEBUG: quick print of dist matrix
    #print d
    SolveModel(start_time)

    total_time = time.time()-start_time
    print "The total solution time is: " + str(total_time)

def PreComputeDistances():

    #declare a couple variables
    global d

    A = xyPointArray
    B = xyPointArray

    d = cdist(A, B,'euclidean')
    #dSort = np.argsort(d, axis=1)
    #print d

def Distance(i,j):
    return d[i][j]

def SolveModel(start_time):
  """Solve the problem and print the solution."""
  global route
  global routeCoord
  warnings.filterwarnings("ignore")
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
      assignment = routing.Solve()
      if assignment:
          # Solution cost.
          print "TSP Objective for " + str(nodes) + " nodes is: " + str(assignment.ObjectiveValue())
          # Inspect solution.
          # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
          route_number = 0
          node = 0
          i = 0
          route = ''
          routeCoord = {}
          while not routing.IsEnd(node):
              route += str(node) + ' -> '
              prevNode = int(node)
              node = assignment.Value(routing.NextVar(node))
              routeCoord[i] = [prevNode, int(node), xyPointArray[prevNode], xyPointArray[node]]
              i += 1
          route += '0'
          routeCoord[i] = [prevNode, 0, xyPointArray[prevNode], xyPointArray[0]]
          #routeCoord += str(xyPointArray[0])
          #print(route)
          #print(routeCoord)
      else:
          print('No solution found.')
  else:
      print('Specify an instance greater than 0.')

#
# Read a problem instance from a file
#
def read_problem(file):
  global d
  global numFeatures
  global js
  global jsonRowDictionary
  global nodes
  global xyPointArray
  global nodeID

  if readType == 1:
    #print 'Reading JSON String Object'
    js = json.loads(file)
  elif readType == 2:
    print 'readFile({0})'.format(file)
    with open(file,"r") as f:
      js = json.load(f)
  else:
    print "READ TYPE ERROR!!"
  numFeatures = len(js['features'])
  xyPointArray = [[None for k in range(2)] for j in range(numFeatures)]
  xyPointArray = GISOps.GetCONUSeqDprojCoords(js) # Get the Distance Coordinates in CONUS EqD Projection
  #print xyPointArray
  nodeID = []
  # rowID holds the index of each feature in the JSON object
  rowID = 0
  for element in js['features']:
      if element['properties']['pointID'] != None: #Parse through node ID's
          nodeID.append(rowID)
      rowID += 1
  nodes = len(nodeID)
  #print("Number of Nodes: {0}".format(nodes))

### This function will return a geojson formatted string to send back to the web
### Since it is based on the p-Median/MCLP data files we can use some of those
### atributes to send back. In this case facilityLocated represents the 'from
### node' and assignedTo represents the 'to node' for the TSP.
def generateGEOJSON():
    assignment = -1
    located = -1
    node = 0
    stop = False
    i = 0
    while stop == False:
        js['features'][nodeID[routeCoord[i][0]]]['properties']['facilityLocated'] = routeCoord[i][2]
        js['features'][nodeID[routeCoord[i][0]]]['properties']['assignedTo'] = routeCoord[i][3]
        i +=1
        if i >= len(nodes):
            stop = True
    ### As of this moment js is the output file... ready to be delivered back to
    ### as the solution
    return 1

###########################################################
##################### The main controller code starts here.
###########################################################

# Create instance of FieldStorage and get data
form = cgi.FieldStorage()
receivedMarkerData = form.getvalue('useTheseMarkers')
## convert the received json string into a Python object
#receivedGeoJson = json.loads(receivedMarkerData)

# the magic happens here...
main()

# prepare for output... the GeoJSON should be returned as a string
transformedMarkerData = json.dumps(js)
print "Content-type:text/html\r\n\r\n"
print transformedMarkerData
