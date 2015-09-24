# This is the Python code used in the Python Tag in LightIntensity.c4d
import math
import c4d
#Welcome to the world of Python


def main():
    #get the light object of the tag
    light=op.GetObject()

    #get the current frame of the document
    frame=doc.GetTime().GetFrame(doc.GetFps())

    #the frame count controls the intensity of the light
    light[c4d.LIGHT_BRIGHTNESS]=float(frame/100.0)
