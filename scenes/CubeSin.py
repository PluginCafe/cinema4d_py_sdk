# This is the Python code used in the Python Tag in CubeSin.c4d
import math
import c4d
#Welcome to the world of Python


def main():
    #get the object where the tag is attached to
    obj=op.GetObject()

    #get the current frame of the document
    frame=doc.GetTime().GetFrame(doc.GetFps())
    
    #get the position of the Cube
    pos=obj.GetRelPos()

    #change the Y component of the position with a small sin calculation
    pos.y+=math.sin(frame/10.0)*10

    #set the new position to the cube
    obj.SetRelPos(pos)
