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
from ortools.linear_solver import pywraplp
from bisect import bisect


printModel = False


def RunPMedianBEAMR(optimization_problem_type, p):

    #p-median program using BEAMR
    solver = pywraplp.Solver('RunIntegerExampleCppStyleAPI', optimization_problem_type)

    #h_i_init = int(numFacilities /(p+1))
    h_i_init = 50
    print "h-i-init = %d" % h_i_init

    # 1 if demand i is served by facility j
    X = [[0 for j in range(numFacilities)] for i in range(numDemands)]
    # 1 if facility at site j is located
    Y = [0]*numFacilities
    # 1 if demand i is assigned to facility outside of h_i neighborhood
    F = [0]*numDemands
    # The set of |h_i| for each demand i
    H = [h_i_init]*numDemands

    start_time = time.time()
    solverIterations = 1

    PreComputeDistances()
    #DEBUG: quick print of dist matrix
    #print d
    """
    BuildModel(solver, p, X, Y, F, H, solverIterations, objLB)
    start = time.time()
    SolveModel(solver)
    print time.time()-start
    optimal = CheckOutput(solver, X, Y, F, H, p)


    while optimal == False:
        objLB = solver.Objective().Value()
        solver.Clear()
        solverIterations += 1
        BuildModel(solver, p, X, Y, F, H, solverIterations, objLB)
        start = time.time()
        SolveModel(solver)
        print time.time()-start
        optimal = CheckOutput(solver, X, Y, F, H, p)

    total_time = time.time()-start_time
    displaySolution(solver, Y, F, H, p, solverIterations, total_time)
"""

def PreComputeDistances():

    #declare a couple variables
    global dSort
    global d

    A = [demandArray[i][0:2] for i in range(numDemands)]
    B = [facilityArray[j][0:2] for j in range(numFacilities)]

    d = cdist(A, B,'euclidean')
    dSort = np.argsort(d, axis=1)


"""
def BuildModel(solver, p, X, Y, F, H, solverIterations, objLB):

    infinity = solver.infinity()

    #declare a couple variables
    global FIDindex
    global LIDindex
    name = ''

    # DECLARE CONSTRAINTS
    # declare facility location constraints
    c1 = [None]*numDemands
    # declare allocation constraints
    c2 = [None]*(numDemands*numFacilities)
    # explicitly declare and initialize the p-facility constraint
    c3 = solver.Constraint(p,p)  # equality constraint equal to p

    # declare the objective
    objective = solver.Objective()
    objective.SetMinimization()

    # Generate the objective function and constraints
    for j in range(numFacilities):
        # initialize the Y site location variables
        name = "Y,%d" % (j+1)
        Y[j] = solver.BoolVar(name)
        # set coefficients of the Y variables in constraint 3
        c3.SetCoefficient(Y[j], 1)

    for i in range(numDemands):

        # initialize c1 equality constraints = 1
        c1[i] = solver.Constraint(1, 1)
        name = "F,%d" % (i+1)
        F[i] = solver.BoolVar(name)

        # if H(i) is less than the number of facilities,
        #   - add f(i) to the objective function
        #   - add f(i) to the assignment constraint (c1)
        if (H[i] < numFacilities):
            objective.SetCoefficient(F[i], demandArray[i][2]*d[i,dSort[i,H[i]]])
            c1[i].SetCoefficient(F[i], 1)

        #for j in range(numFacilities):
        for k in range(H[i]):
            # facility j is the kth closest facility from i, zero indexed
            j = dSort[i,k]
            # initialize the X assignment variables and add them to the objective function
            name = 'X,%d,%d' % (i+1,j+1)
            X[i][k] = solver.BoolVar(name)
            objective.SetCoefficient(X[i][k], demandArray[i][2]*d[i,j])

            # set the variable coefficients of the sum(Xij) = 1 for each i
            c1[i].SetCoefficient(X[i][k], 1)

            # Yj - Xij >= 0 <--- canonical form of the assignment constraint
            c2[i*numFacilities+k] = solver.Constraint(0, infinity) # c2 rhs
            c2[i*numFacilities+k].SetCoefficient(X[i][k], -1)
            c2[i*numFacilities+k].SetCoefficient(Y[j], 1)

    # add a lower bound objective constraint
    if (solverIterations > 1):
        c4 = solver.Constraint(objLB,infinity)
        for i in range(numDemands):
            if (H[i] < numFacilities):
                c4.SetCoefficient(F[i], demandArray[i][2]*d[i,dSort[i,H[i]]])
            for k in range(H[i]):
                c4.SetCoefficient(X[i][k], demandArray[i][2]*d[i,j])
"""

def SolveModel(solver):
  """Solve the problem and print the solution."""
  result_status = solver.Solve()

  # The problem has an optimal solution.
  assert result_status == pywraplp.Solver.OPTIMAL, "The problem does not have an optimal solution!"

  # The solution looks legit (when using solvers others than
  # GLOP_LINEAR_PROGRAMMING, verifying the solution is highly recommended!).
  assert solver.VerifySolution(1e-7, True)

"""
def CheckOutput(solver, X, Y, F, H, p):

  optimal = True
  H_old = H[:]

  # The set of selected facilities
  FIDindex = [None]*p
  LIDindex = [None]*p

  #print 'Problem solved in %f milliseconds' % solver.WallTime()

  # The objective value of the solution.
  #print 'Optimal objective value = %f' % solver.Objective().Value()

  # print the selected sites
  count = 0
  iterator = 0
  for j in facilityIDs:
    if (Y[count].SolutionValue() == True):
      FIDindex[iterator] = count
      LIDindex[iterator] = j
      iterator += 1
      #print "Facility selected %d" % (js['features'][j]['properties']['pointID'])
    count += 1

  noFselected = True
  for i in range(numDemands):
    if (F[i].SolutionValue() == True):
      # If the next closest H(i+1) facility was selected, then this is part of an optimal solution
      # Assign the demamd to the H(i+1) closest facility
      if facilityIDs[dSort[i,H[i]]] in LIDindex:
          # if next nearest facility is a located solution, assign to that
          js['features'][demandIDs[i]]['properties']['assignedTo'] = facilityIDs[dSort[i,H[i]]]
          # increment H[i]
          H[i] += 1
      else:
          optimal = False
          # otherwise, increase H to the nearest located facility
          H[i] = int(np.where(d[i,dSort[i,:]]==min(d[i,FIDindex[:]]))[0])+1
          # also add this allocation to the upper bound
    count += 1
  if (optimal == True):
      generateGEOJSON(X, Y, H_old, p)

  return optimal
"""

def displaySolution(solver, Y, F, H, p, solverIterations, total_time):

    print 'Last iteration solved in %f milliseconds, with' % solver.WallTime()
    print 'Number of variables = %d' % solver.NumVariables()
    print 'Number of constraints = %d' % solver.NumConstraints()
    print
    print 'Total problem solved in %f seconds over %d iterations' % (total_time, solverIterations)
    print
    # The objective value of the solution.
    print 'Optimal objective value = %f' % solver.Objective().Value()

    # Print out the facilities that are located
    count = 0
    for j in facilityIDs:
      if (Y[count].SolutionValue() == True):
        print "Facility selected %d" % (js['features'][j]['properties']['pointID'])
      count += 1
    print
    print "Max H = %d, Ave H = %f" % (max(H),np.mean(H))
    print

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


def Announce(solver, api_type):
  print ('---- Integer programming example with ' + solver + ' (' +
         api_type + ') -----')


#
# Read a problem instance from a file
#
def read_problem(file, p, readType):
  global dSort
  global d
  global numFeatures
  global numFacilities
  global facilityIDs
  global facilityArray
  global numForced
  global numDemands
  global demandIDs
  global demandArray
  global js
  global jsonRowDictionary
  global objLB
  global objUB


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

  facilityIDs = []
  demandIDs = []

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
      elif element['properties']['typeFD']==2: # Facility Site Only
          facilityIDs.append(rowID)
      elif element['properties']['typeFD']==1: # Demand Point Only
          demandIDs.append(rowID)
      rowID += 1

  numFacilities = len(facilityIDs)
  numDemands = len(demandIDs)

  print("Number of Sites: {0}".format(numFacilities))
  print('Number of Demands: {0}'.format(numDemands))
  print('p = {0}'.format(p))

  facilityArray = [[None for k in range(3)] for j in range(numFacilities)]
  demandArray = [[None for k in range(3)] for j in range(numDemands)]

  i = 0
  j = 0
  k = 0
  for line in js['features']:
    if line['properties']['typeFD']>=2:
      facilityArray[i][0] = xyPointArray[k][0]
      facilityArray[i][1] = xyPointArray[k][1]
      facilityArray[i][2] = line['properties']['forcedLocation']
      i += 1
    if line['properties']['typeFD'] % 2 == 1:
      demandArray[j][0] = xyPointArray[k][0]
      demandArray[j][1] = xyPointArray[k][1]
      demandArray[j][2] = line['properties']['pop']
      j += 1
    k += 1

  numForced = sum(zip(*facilityArray)[2])
  # check if valid for the given p
  try:
    if numForced > p:
      raise DataError('numForcedGreaterThanP')
  except DataError:
    print 'number of forced facilities is greater than p'
    raise

  return p


def readJSONstrObjANDsolve(jsonStrObj,p):
  readType = 1

  p = read_problem(jsonStrObj, p, readType)
  #main(p)
  return js

def main(p):
  print "Setting up and solving problem!"
  if hasattr(pywraplp.Solver, 'CBC_MIXED_INTEGER_PROGRAMMING'):
    Announce('CBC', 'C++ style API')
    RunPMedianBEAMR(pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING, p)
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
