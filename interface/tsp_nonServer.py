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

import sys
import json
import GISOps
import time
import numpy as np
from scipy.spatial.distance import cdist
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from bisect import bisect

printModel = False

def RunTSP(nodes):
    #TSP using Google OR-Tools Constraint Programming model example
    start_time = time.time()
    PreComputeDistances() #compute the distances between points
    #DEBUG: quick print of dist matrix
    #print d
    SolveModel(start_time)

    total_time = time.time()-start_time
    print "The total solution time is: " + str(total_time)

def PreComputeDistances():

    #declare a couple variables
    global dSort
    global d

    A = xyPointArray
    B = xyPointArray

    d = cdist(A, B,'euclidean')
    dSort = np.argsort(d, axis=1)
    #print d

def Distance(i,j):
    return d[i][j]

def SolveModel(start_time):
  """Solve the problem and print the solution."""
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

"""

def generateGEOJSON(X, Y, H, p):

  unweightedObj = 0
  weightedObj = 0
  assignment = -1

  # update located facilities in the JSON
  for j in range(numFacilities):
    located = Y[j].SolutionValue()
    js['features'][facilityIDs[j]]['properties']['facilityLocated'] = located

  # update assignments in the JSON
  for i in range(numDemands):
    for k in range(H[i]):
     if (X[i][k].SolutionValue() == True):
       j = dSort[i,k]
       js['features'][demandIDs[i]]['properties']['assignedTo'] = facilityIDs[j]

  writeToGJSFile(js, p)


def writeToGJSFile(js, p):

  with open('./data/PMedianResult_s%d_p%d_B.json' % (numFeatures, p), 'w') as outfile:
    json.dump(js,outfile)
"""
#
# Read a problem instance from a file
#
def read_problem(file, p, readType):
  global dSort
  global d
  global numFeatures
  global demandIDs
  global demandArray
  global js
  global jsonRowDictionary
  global nodes
  global xyPointArray

  if readType == 1:
    print 'Reading JSON String Object'
    js = json.loads(file)
  elif readType == 2:
    print 'readFile({0})'.format(file)
    with open(file,"r") as f:
      js = json.load(f)
  else:
    print "READ TYPE ERROR!!"

  numFeatures = len(js['features'])

  # if the geoJSON includes a p value, use this rather than any input arguments
  try:
    p = js['properties']['pValue']
  except IOError:
    print "geoJSON has no pValue"

  # or manually set p
  # p = 4

  xyPointArray = [[None for k in range(2)] for j in range(numFeatures)]
  xyPointArray = GISOps.GetCONUSeqDprojCoords(js) # Get the Distance Coordinates in CONUS EqD Projection
  #print xyPointArray
  #facilityIDs = []
  #demandIDs = []
  nodeID = []
  # rowID holds the index of each feature in the JSON object
  rowID = 0

  for element in js['features']:
      if element['properties']['pointID'] != None: #Parse through node ID's
          nodeID.append(rowID)
      rowID += 1
  nodes = len(nodeID)
  print("Number of Nodes: {0}".format(nodes))

def readJSONstrObjANDsolve(jsonStrObj,p):
  readType = 1
  p = read_problem(jsonStrObj, p, readType)
  #main(p)
  return js

def main(p):
  print "Setting up and solving problem!"
  RunTSP(nodes)
  if js != None:
    return js
  else:
    print 'YOU ARE DUMB! You should be using exception handling!'
    return None

if __name__ == '__main__':
  readType = 2

  print "DEBUG: sys.argv = " + str(sys.argv)
  if len(sys.argv) > 2:
    p = float(sys.argv[1])
    file = sys.argv[2]
    print "Problem instance from", file
    p = read_problem(file, p, readType)
    main(p)
  elif len(sys.argv) > 1:
    p = float(sys.argv[1])
    main(p)
  else:
    main(None)
