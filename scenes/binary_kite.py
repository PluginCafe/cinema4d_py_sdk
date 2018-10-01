# This is the Python code used in the Python Generator in binary_kite.c4d
#"binary kite" 4 Py4D by Jan-C.Frischmuth (smart-page.net)
#inspired by Mikael Hvidtfeldt Christensen (structuresynth.sourceforge.net)

import c4d
import random
import math


def main():

    clone = op[c4d.ID_USERDATA, 2]
    mat1  = op[c4d.ID_USERDATA, 3]
    mat2  = op[c4d.ID_USERDATA, 4]

    x = op[c4d.ID_USERDATA, 6]
    y = op[c4d.ID_USERDATA, 7]
    z = op[c4d.ID_USERDATA, 8]

    if clone==None or mat1==None or mat2==None or x==0 or y==0 or z==0:
        return    
    
    scale  = op[c4d.ID_USERDATA, 10]
    if scale != 0:
        scale = 1-1/float(z/2)*scale
    else :
        scale = 1

    wiggle = op[c4d.ID_USERDATA, 11]
    val    = op[c4d.ID_USERDATA, 12]
    seed   = op[c4d.ID_USERDATA, 13]
    speed  = op[c4d.ID_USERDATA, 14]
    size   = clone.GetRad()  

    rnd   = random.Random()
    frame = doc.GetTime().GetFrame(doc.GetFps())
    null  = c4d.BaseObject(c4d.Onull)        


    for i in xrange(0, x):

        for j in xrange(0, y):

            c4d.StatusSetBar(int(float(100)/(x*y)*(i+j)))

            par = c4d.BaseObject(c4d.Onull)
            par.InsertUnder(null)
            par.SetRelPos(c4d.Vector((i-x)*size.x*2+size.x*(x+1), (j-y)*size.y*2+size.y*(y+1), -size.y))

            for k in xrange(0, z):

                cube2 = c4d.BaseObject(c4d.Oinstance)
                cube2[c4d.INSTANCEOBJECT_LINK] = clone
                cube2[c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE] = c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE_SINGLEINSTANCE
                cube2.InsertUnder(par)

                mtag = cube2.MakeTag(c4d.Ttexture)
                   
                rnd.seed((i, j, k, seed))

                if rnd.random() > 0.5:
                    mtag[c4d.TEXTURETAG_MATERIAL] = mat1
                else:
                    mtag[c4d.TEXTURETAG_MATERIAL] = mat2

                tmpval = val*.1*k/z  
                tx = wiggle*.01*(math.sin(frame*speed + math.pi*k/z))+rnd.random()*tmpval*2-tmpval
                rnd.jumpahead(9999)
                ty = rnd.random()*tmpval*2-tmpval
                rnd.jumpahead(9999)
                tz = rnd.random()*tmpval*2-tmpval
                
                if k > 0:
                    cube2.SetRelPos(c4d.Vector(0, 0, size.z*2))  
                cube2.SetRelRot(c4d.Vector(tx, ty, tz))
                cube2.SetRelScale(c4d.Vector(scale))

                par = cube2

    c4d.StatusClear()
    return null