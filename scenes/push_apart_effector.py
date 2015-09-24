# This is the Python code used in the Python Effector in push_apart_effector.c4d
#############################################################
## CINEMA 4D SDK                                           ##
#############################################################
## (c) 1989-2011 MAXON Computer GmbH, all rights reserved  ##
#############################################################

import c4d
from c4d.modules import mograph as mo

def main():
    md = mo.GeGetMoData(op)
    if md==None: return
    cnt = md.GetCount()
    
    #matrix list of clones
    marr = md.GetArray(c4d.MODATA_MATRIX)
    
    #flag list of clones
    farr = md.GetArray(c4d.MODATA_FLAGS)
    
    hide = op[c4d.ID_USERDATA, 3]
    radius = op[c4d.ID_USERDATA, 1]
    iterations = op[c4d.ID_USERDATA, 2]
    seperation = (1.0 / float(iterations)) * 0.5
    
    ustart = (iterations-1) if hide==0 else (0)
    

    for u in xrange(ustart, iterations): 
        for i in xrange(0, cnt): #iterate over clones
            if ((farr[i]&(1<<0)) and (not (farr[i]&(1<<1)))): #Only if the clone is visible
                for o in xrange(i-1):
                    if ((farr[o]&(1<<0)) and (not (farr[o]&(1<<1))) and (marr[i].off - marr[o].off).GetLength() < radius):
                        if hide==0: #hide the clone
                            farr[i] &= ~(1<<0)
                            break #next clone
                        elif hide==1:
                            marr[i].off = marr[i].off +(marr[i].v3*radius)
                        elif hide==2:
                            delta = (marr[i].off-marr[o].off)*radius*seperation
                            delta.Normalize()
                            
                            marr[i].off +=delta
                            marr[o].off -=delta
                            
    #handle the modified flag list back to mograph
    md.SetArray(c4d.MODATA_FLAGS, farr, True)
    
    #handle the modified matrix list back to mograph
    md.SetArray(c4d.MODATA_MATRIX, marr, True)
