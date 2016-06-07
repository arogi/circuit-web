#!/usr/bin/python

# Copyright 2015-2016 Arogi Inc
# Copyright 2010-2014 Google
#
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
import json
import GISOps
import numpy as np
from scipy.spatial.distance import cdist
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import warnings

warnings.filterwarnings("ignore")

def main():
    objective = readJSONandSolve()
    generateGEOJSON(objective)

def readJSONandSolve():
    read_problem(receivedMarkerData, 1)
    objective = RunTSP()
    return objective

def RunTSP():
    #TSP using Google OR-Tools Constraint Programming model example
    PreComputeDistances() #compute the distances between points
    objective = SolveModel()

    return objective


def PreComputeDistances():
    #declare a couple variables
    global d
    global xyPointArray
    # Get the Distance Coordinates in CONUS EqD Projection
    xyPointArray = GISOps.GetCONUSeqDprojCoords(js)
    d = cdist(xyPointArray, xyPointArray,'euclidean')
    return 1

def Distance(i,j):
    return d[i,j]

def SolveModel():
  """Solve the problem and print the solution."""
  global route
  global routeCoord
  warnings.filterwarnings("ignore")

  # Ensure that the data is valid for making at TSP route
  if numFeatures > 1:
      # TSP of size args.tsp_size
      # Second argument = 1 to build a single tour (it's a TSP).
      # Nodes are indexed from 0 to parser_tsp_size - 1, by default the start of
      # the route is node 0.
      routing = pywrapcp.RoutingModel(numFeatures, 1)
      search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
      # Setting first solution heuristic (cheapest addition).
      search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
      routing.SetArcCostEvaluatorOfAllVehicles(Distance)
      assignment = routing.Solve()

      if assignment:
          # Inspect solution.
          # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
          i = 0
          route_number = 0
          node = routing.Start(route_number)
          routeCoord = [None]*numFeatures
          while not routing.IsEnd(node):
              prevNode = int(node)
              node = assignment.Value(routing.NextVar(node))
              routeCoord[i] = [prevNode, int(node)]
              i += 1
          routeCoord[numFeatures-1] = [prevNode, int(routing.Start(route_number))]
          #print(route)
          #print(routeCoord)
      else:
          print('No solution found.')
  else:
      print('Specify an instance greater than 0.')
  return assignment.ObjectiveValue()

#
# Read a problem instance from a file
#
def read_problem(file, readType):
  global numFeatures
  global js

  try:
      if readType == 1:
          #print 'Reading JSON String Object'
          js = json.loads(file)
      elif readType == 2:
          #print 'readFile({0})'.format(file)
          with open(file,"r") as f:
              js = json.load(f)
  except IOError:
      print 'Error reading file'
      raise

  # count the number of point features to connect
  numFeatures = len(js['features'])
  return 1



### This function will return a geojson formatted string to send back to the web
### In this case thisNode represents the 'from node' and nextNode represents the 'to node'
### for the TSP.
def generateGEOJSON(objective):

    for i in range(numFeatures):
        node = routeCoord[i][0]
        nextNode = routeCoord[i][1]
        js['features'][node]['properties']['thisNode'] = node
        js['features'][node]['properties']['nextNode'] = nextNode

    # if properties does not exist in the geojson, create it
    if 'properties' not in js:
        js['properties'] = {}
    # write the objective value into the geojson
    js['properties']['objective'] = objective
    ### As of this moment js is the output file... ready to be delivered back to
    ### as the solution
    return 1


###########################################################
##################### The main controller code starts here.
###########################################################

# Create instance of FieldStorage and get data
form = cgi.FieldStorage()
receivedMarkerData = form.getvalue('useTheseMarkers')

# the magic happens here...
main()

# prepare for output... the GeoJSON should be returned as a string
transformedMarkerData = json.dumps(js)
print "Content-type:text/html\r\n\r\n"
print transformedMarkerData
