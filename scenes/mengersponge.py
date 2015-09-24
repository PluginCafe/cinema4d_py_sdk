# This is the Python code used in the Python Generator in mengersponge.c4d

import c4d
#Welcome to the world of Python

def CreateCubes(p, size, scale, depth):
    end = False
    if depth-1==0: end = True

    null = c4d.BaseObject(c4d.Onull)
    null.SetRelPos(p-size)
    for x in xrange(3):
        for y in xrange(3):
            for z in xrange(3):
                if x%2!=0 and y%2!=0: continue
                if z%2!=0 and y%2!=0: continue
                if x%2!=0 and z%2!=0: continue

                sx = sy = sz = size
                position = c4d.Vector(x*sx,y*sy, z*sz)
                if end:
                    cube = c4d.BaseObject(c4d.Oinstance)
                    cube[c4d.INSTANCEOBJECT_RENDERINSTANCE] = True
                    cube[c4d.INSTANCEOBJECT_LINK] = op[c4d.ID_USERDATA, 1]
                    cube.SetRelPos(position)
                    cube.SetRelScale(c4d.Vector(scale))
                else:
                    cube = CreateCubes(position, size/3.0, scale/3.0, depth-1)
                cube.InsertUnder(null)

    return null

def main():
    return CreateCubes(p=c4d.Vector(0), size=200, scale=1, depth=op[c4d.ID_USERDATA, 2])
