# This is the Python code used in the Python Effector in python_effector.c4d
#############################################################
## CINEMA 4D SDK                                           ##
#############################################################
## (c) 1989-2011 MAXON Computer GmbH, all rights reserved  ##
#############################################################

import math

import c4d
from c4d.modules import mograph as mo

def main():
    md = mo.GeGetMoData(op)
    if not md: return False
    
    cnt = md.GetCount()
    scl = op[c4d.ID_USERDATA, 2]
    anim = op[c4d.ID_USERDATA, 3]
    mode = op[c4d.ID_USERDATA, 4]
    torus_R = op[c4d.ID_USERDATA, 6]
    torus_p = op[c4d.ID_USERDATA, 7]
    torus_q = op[c4d.ID_USERDATA, 8]
    liss_k = op[c4d.ID_USERDATA, 11]
    liss_l = op[c4d.ID_USERDATA, 12]
    speed = op[c4d.ID_USERDATA, 10]
    off_mode = op[c4d.ID_USERDATA, 5]
    offset = op[c4d.ID_USERDATA, 13]
    
    #matrix list of clones
    marr = md.GetArray(c4d.MODATA_MATRIX)
    
    pos = c4d.Vector()
    
    #extract the current time if the "Animate" attribute is enabled
    if anim:
        time = doc.GetTime().Get()
    else:
        time = 0
    
    #iter through all clones
    for i in xrange(0, cnt):
        if off_mode:
            itime = (offset/(100*cnt))*2*math.pi*i+(speed*time)
        else:
            itime = i+(speed*time)
        
        if mode==1: #Trefoil Knot A
            pos = c4d.Vector(scl*(2+math.cos(3*itime))*math.cos(2*itime),scl*(2+math.cos(3*itime))*math.sin(2*itime),scl*math.sin(3*itime))
        elif mode==2: #Trefoil Knot B
            pos = c4d.Vector(-scl*math.cos(itime)-0.2*scl*math.cos(5*itime)+1.5*scl*math.sin(2*itime),-1.5*scl*math.cos(2*itime)+scl*math.sin(itime)-0.2*scl*math.sin(5*itime),scl*math.cos(3*itime))
        elif mode==3: #Achterknoten
            pos = c4d.Vector(scl*math.cos(itime)+scl*math.cos(3*itime),0.6*scl*math.sin(itime)+scl*math.sin(3*itime),0.4*scl*math.sin(3*itime)-scl*math.sin(6*itime))
        elif mode==4: #Torus
            pos = c4d.Vector((2*scl+torus_R*math.cos(torus_p*itime))*math.cos(torus_q*itime),(2*scl+torus_R*math.cos(torus_p*itime))*math.sin(torus_q*itime),torus_R*math.sin(torus_p*itime))
        elif mode==5: #Lissajous
            pos = c4d.Vector(scl*math.cos(liss_k.x*itime+liss_l.x),scl*math.cos(liss_k.y*itime+liss_l.y),scl*math.cos(liss_k.z*itime+liss_l.z))
    
        #set the position of the clone
        marr[i].off = pos
    
    #handle the modified matrix list back to mograph
    md.SetArray(c4d.MODATA_MATRIX, marr, True)
