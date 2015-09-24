# This is the Python code used in the Python Tag in cs_buildon.c4d
# Original source from Chris Smith (c) 2009
# Blog: http://circlesofdelusion.blogspot.com/

import math
import c4d

from c4d import utils
from math import pi

def FrameStart(doc, fs):
    t = doc.GetTime().Get()
    delta = 1/float(doc.GetFps())
    return utils.Clamp(0, 999999, (t-(fs*delta)))

def main():
    obj = op.GetObject()
    
    object = obj[c4d.ID_USERDATA, 1]
    if object is None: return
    
    fs = obj[c4d.ID_USERDATA, 2]
    delay = obj[c4d.ID_USERDATA, 3]
    mass = abs(obj[c4d.ID_USERDATA, 4] * 100-100)
    bounce = .5 + abs(obj[c4d.ID_USERDATA, 5] * 100-100)
    rotations = obj[c4d.ID_USERDATA, 8]
    h_amount = obj[c4d.ID_USERDATA, 9]
    p_amount = obj[c4d.ID_USERDATA, 10]
    b_amount = obj[c4d.ID_USERDATA, 11]
    
    t = FrameStart(doc, fs)
    i = 0
    current_object = object.GetDown()
    if current_object is None: return
    
    obj_scale   = c4d.Vector(1)
    ob_rot      = c4d.Vector();
    index_time = 0
    
    while current_object:
        i += 1
        index_time = utils.Clamp(0,999999,t-(i*delay))
        result = math.cos(index_time*mass)/math.exp(bounce*index_time);
        
        obj_scale = c4d.Vector(1-result)
        obj_rot    = c4d.Vector(result * h_amount * pi, result * p_amount  * pi, result * b_amount * pi)
        
        current_object.SetRelScale(obj_scale)
        if rotations:
            current_object.SetRelRot(obj_rot)
            
        current_object = current_object.GetNext()
