# Demo Code by Matthew R. Niblett and Antonio Medrano. All rights reserved to Arogi April 2, 2016
#
# Demo JSON String Object Portion of Code used in 'pMedianGJS.py'
# Note that you should probably delete the compiled version of 'pMedianGJS' as it will need to be compiled with the updated form
# to import here!!

import os
import sys
import json
import tsp_nonServer as boom
#import GISOps as gisops

def main(jsonStr):
    #ReadJSONstringANDsolve(jsonStrObj,p_Fac,ServiceStandard)
    js = boom.readJSONstrObjANDsolve(jsonStr)
    #print js
    #gisops.outputBuffer(js,SD*1000)
    #print js
    # with open('./data/PMedianResult_p%d.geojson' % p, 'w') as outfile:
        # json.dump(js,outfile)

""" Main will take in 1 argument: Data to Use  """
if __name__ == '__main__':
    jsonFile = sys.argv[1]

    with open(jsonFile,'r') as f:
        jsonStr = f.read()
    #print jsonStr

    main(jsonStr)
