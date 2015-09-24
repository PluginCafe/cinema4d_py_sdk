# This is the Python code used in the Python Effector in py_effector.c4d
#############################################################
## CINEMA 4D SDK                                           ##
#############################################################
## (c) 1989-2013 MAXON Computer GmbH, all rights reserved  ##
#############################################################

import math
import random

import c4d
from c4d.modules import mograph
from c4d import utils

def main():    
    #get the data object from mograph
    md = mograph.GeGetMoData(op)
    if md==None: return

    #get an list of all matrices
    marr = md.GetArray(c4d.MODATA_MATRIX)
    
    #get the userdata values:
    #y-axis offset
    yOffset = op[c4d.ID_USERDATA, 1] 
    #angle offset (0-360°)
    angleX = op[c4d.ID_USERDATA, 2]
    angleY = op[c4d.ID_USERDATA, 3]
    angleZ = op[c4d.ID_USERDATA, 4]
    #random threshold (0-1)
    randomX = op[c4d.ID_USERDATA, 5]
    randomY = op[c4d.ID_USERDATA, 6]
    randomZ = op[c4d.ID_USERDATA, 7]
    #link for an optional camera target
    cameraTarget = op[c4d.ID_USERDATA, 8]
    
    #degree2rad conversion constant (rad=degree*PI/180)
    modRad = math.pi/180
    #always create a random instance so offsetting the seed won't affect other python scripts
    rnd = random.Random()
    #temp var to store a matrix
    tmpm = None
    
    #the utils package provides the lazy man's way to create matrices
    #...translation:
    opm = utils.MatrixMove(c4d.Vector(0, yOffset, 0))
    #...rotation
    orxm = c4d.utils.MatrixRotX(angleX*modRad)
    orym = c4d.utils.MatrixRotY(angleY*modRad)
    orzm = c4d.utils.MatrixRotZ(angleZ*modRad)

    #iterate over all matrices
    for i in xrange(0, len(marr)):
            
        #skip the first object
        if i>0:
            """
            set the object's position to that of its predecessor and offset it by multiplying 
            with the translation matrix
            """
            marr[i] = tmpm*opm
        
        #on every second object...
        if i%2:
            #offset the random seed
            rnd.seed(i)

            #if random < threshold apply the rotation offset
            if rnd.random() < randomX: marr[i] *= orxm
            if rnd.random() < randomY: marr[i] *= orym
            if rnd.random() < randomZ: marr[i] *= orzm
           
        #keep the resulting matrix for the following object
        tmpm = marr[i]
    
    #catch if the link field is empty    
    if cameraTarget is not None:    
        #set the linked object's matrix
        cameraTarget.SetMg(tmpm)
 
    #handle the modified matrix list back to mograph
    md.SetArray(c4d.MODATA_MATRIX, marr, True)