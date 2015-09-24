# This is the Python code used in the Python Tag in boid_simulation.c4d
#Boids for Py4D by smart-page.net

import c4d
import math
import random


#environment
minx = -2000
maxx = 2000
miny = 1000
maxy = 3000
minz = -2000
maxz = 2000

#boids params
boids_number    = 100
target_maxspeed = 60
boid_maxspeed   = 50
boid_distance   = 200

frame = None
rand = None
target = c4d.Vector()
targetvec = c4d.Vector(0)

bpos = None
bvel = None


def main():

    global tp
    global doc
    global frame
    global bpos
    global bvel
    
    frame = doc.GetTime().GetFrame(doc.GetFps())
    if frame==0:
        tp.FreeAllParticles()
        tp.AllocParticles(boids_number)    
    
    lt = c4d.BaseTime(1000)

    bpos = []
    bvel = []

    for i in tp.GetParticles():
        tp.SetLife(i, lt)

        bpos.append(tp.Position(i))
        bvel.append(tp.Velocity(i))

        moveboids(i)
    
    set_target()    
    movetarget()   


def set_target():

    v = c4d.Vector()

    for x in bpos:
        v +=x

    v = v / len(tp.GetParticles())

    op[c4d.ID_USERDATA, 1].SetRelPos(v)
    
    
def moveboids(c):
   
    bvel[c] += rule1(c) + rule2(c) + rule3(c) + rule4(c)
    bvel[c] = limitspeed(bvel[c], boid_maxspeed)

    tp.SetVelocity(c, bvel[c])

    vel=bvel[c].GetNormalized()

    side = c4d.Vector(c4d.Vector(0,1,0).Cross(vel)).GetNormalized()
    up = vel.Cross(side)
    m = c4d.Matrix(c4d.Vector(0), side, up, vel)

    tp.SetAlignment(c, m)
    tp.SetPosition(c, bpos[c] + bvel[c])


def rule1(c):
        
    v = c4d.Vector()
    
    for i, b_pos in enumerate(bpos):
        boid_pos = bpos[c]

        if b_pos == boid_pos:
            continue
           
        v += boid_pos - b_pos

    v /= len(tp.GetParticles())
    
    return (bvel[c] -v) / 100
    

def rule2(c):

    d = 0
    k = 0

    for i, b_pos in enumerate(bpos):
        if (b_pos - bpos[c]).GetLength() < boid_distance:
            k += 1
            pos = bpos[c]
            dif = (pos - b_pos)
            
            if dif.GetLength() >= 0: 
                dif = math.sqrt(boid_distance) - dif
            elif dif.GetLength() < 0: 
                dif = -math.sqrt(boid_distance) - dif
            
            d += dif 

    if k == 0: return

    return bvel[c] - d / 4
    

def rule3(c):

    v = c4d.Vector()

    for i in bpos:
        v += bvel[c]

    v /= len(tp.GetParticles())

    return bvel[c] + v / 30


def rule4(c):

    return (target - bpos[c]) / 100


def movetarget():

    global target
    global targetvec
   
    rand = random.Random(1)
    rand.seed(frame) 
        
    if target.x < minx or target.y < miny or target.z < minz: 
        targetvec.x += rand.random() * target_maxspeed
        targetvec.y += rand.random() * target_maxspeed
        targetvec.z += rand.random() * target_maxspeed

    if target.x > maxx or target.y > maxy or target.z > maxz:
        targetvec.x -= rand.random() * target_maxspeed
        targetvec.y -= rand.random() * target_maxspeed
        targetvec.z -= rand.random() * target_maxspeed
    
    targetvec = limitspeed(targetvec, target_maxspeed)
        
    target += targetvec
    

def limitspeed(v, speed):

    if v.GetLength() > speed:
       v = v*(speed / v.GetLength())

    return v