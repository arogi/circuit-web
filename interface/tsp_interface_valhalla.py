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
import requests
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
    #global xyPointArray
    # Get the Distance Coordinates in CONUS EqD Projection
    #xyPointArray = GISOps.GetCONUSeqDprojCoords(js)
    #d = cdist(xyPointArray, xyPointArray,'euclidean')

    # read in the coordinates and get their distances to each other
    numFeatures = len(js['features'])
    xyPointArray = [[None for k in range(2)] for j in range(numFeatures)]
    d = [[None for i in range(numFeatures)] for j in range(numFeatures)]
    i = 0;
    for line in js['features']:
        Lon = line['geometry']['coordinates'][0]
        Lat = line['geometry']['coordinates'][1]

        xyPointArray[i][0] = Lon
        xyPointArray[i][1] = Lat
        i += 1

    #print js

    for i in range(numFeatures):
        longi = xyPointArray[i][0]
        lati = xyPointArray[i][1]
        for j in range(numFeatures):
            longj = xyPointArray[j][0]
            latj = xyPointArray[j][1]
            text = postDataJSON(lati,longi,latj,longj)
            #print pyCurl(json.dumps(text))
            # Get the distance as a function of the network using Valhalla
            d[i][j] = pyCurl(json.dumps(text))
    #print d

def pyCurl(input): #Define function to send request
    global r #define the request object as r
    global path_length
    #Put your valhalla url here
    url = 'http://192.168.99.100:8002/route'
    #Define your headers here: in this case we are using json data
    headers = {'content-type': 'application/json'}
    #define r as equal to the POST request
    #print input
    r = requests.post(url, data = input, headers = headers)
    #print r.text
    #capture server response
    response = r.json()
    path_length = response['trip']['legs'][0]['summary']['length']
    coords = response['trip']['legs'][0]['shape']
    #print path_length
    return path_length

def postDataJSON(lati,longi,latj,longj):
    text = {"locations": [{"lat": lati,"lon": longi}, {"lat": latj,"lon": longj}],"costing": "auto","directions_options": {"units": "kilometers"}}
    return text

def Distance(i,j):
    return d[i][j]

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
### Since it is based on the p-Median/MCLP data files we can use some of those
### atributes to send back. In this case facilityLocated represents the 'from
### node' and assignedTo represents the 'to node' for the TSP.
def generateGEOJSON(objective):
    #print js
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
