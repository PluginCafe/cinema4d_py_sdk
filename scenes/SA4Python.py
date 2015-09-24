# This is the Python code used in the Python Tag in SA4Python.c4d
#strange attractor for Py4D by smart-page.net

import c4d
import math

#number of particles
num = 10000


def main():

    global tp
    global doc
    global res
    
    frame = doc.GetTime().GetFrame(doc.GetFps())
    
    #attractor parameters  
    _a = 2.24
    _b = 0.43
    _c = -0.65
    _d = -2.43
    _e = 1.0

    cx = 1
    cy = 1
    cz = 1

    mx = 0
    my = 0
    mz = 0  

    lt = c4d.BaseTime(1000)
    
    if frame==0:
        tp.FreeAllParticles()
        tp.AllocParticles(num) 
 
        v = c4d.Vector()
       
        for i in tp.GetParticles():
           mx = math.sin(_a*cy)-cz*math.cos(_b*cx)
           my = cz*math.sin(_c*cx)-math.cos(_d*cy)
           mz = _e*math.sin(cx)

           cx = mx
           cy = my
           cz = mz

           v.x=mx*50
           v.y=my*50
           v.z=mz*50

           tp.SetLife(i, lt)
           tp.SetPosition(i, v)