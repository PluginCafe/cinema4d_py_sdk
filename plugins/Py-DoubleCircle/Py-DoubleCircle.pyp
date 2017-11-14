"""
Double Circle
Copyright: MAXON Computer GmbH
Written for Cinema 4D R19

Modified Date: 31/08/2017
"""

import math
import sys
import os
import c4d
from c4d import bitmaps, gui, plugins, utils

# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1025245


class DoubleCircleData(plugins.ObjectData):
    """CircleObject Generator"""

    HANDLECOUNT = 1

    
    def Message(self, node, type, data):
        if type==c4d.MSG_MENUPREPARE:
            doc = data
            node[c4d.PRIM_PLANE] = doc.GetSplinePlane()
        return True
    
    
    def Init(self, node):
        data = node.GetDataInstance()
        
        data.SetReal(c4d.PYCIRCLEOBJECT_RAD, 200.0)
        data.SetLong(c4d.PRIM_PLANE, c4d.PRIM_PLANE_XY)
        data.SetBool(c4d.PRIM_REVERSE, False)
        data.SetLong(c4d.SPLINEOBJECT_INTERPOLATION, c4d.SPLINEOBJECT_INTERPOLATION_ADAPTIVE)
        data.SetLong(c4d.SPLINEOBJECT_SUB, 8)
        data.SetReal(c4d.SPLINEOBJECT_ANGLE, utils.Rad(5.0))
        data.SetReal(c4d.SPLINEOBJECT_MAXIMUMLENGTH, 5.0)
        return True
    
    
    @staticmethod
    def SwapPoint(p, plane):
        if plane==c4d.PRIM_PLANE_ZY:
            return c4d.Vector(-p.z,p.y,p.x)
        elif plane==c4d.PRIM_PLANE_XZ:
            return c4d.Vector(p.x,-p.z,p.y)
        return p
    
    
    def GetHandleCount(self, op):
        return self.HANDLECOUNT
    
    
    def GetHandle(self, op, i, info):
        data = op.GetDataInstance()
        if data is None: return
        
        rad = data.GetReal(c4d.PYCIRCLEOBJECT_RAD)
        plane = data.GetLong(c4d.PRIM_PLANE)
        
        info.position = DoubleCircleData.SwapPoint(c4d.Vector(rad,0.0,0.0), plane)
        info.direction = ~DoubleCircleData.SwapPoint(c4d.Vector(1.0,0.0,0.0), plane)
        info.type = c4d.HANDLECONSTRAINTTYPE_LINEAR
    
    
    def SetHandle(self, op, i, p, info):
        data = op.GetDataInstance()
        if data is None: return
        
        val = p*info.direction
        
        data.SetReal(c4d.PYCIRCLEOBJECT_RAD, utils.FCut(val, 0.0, sys.maxint))
    
    
    def Draw(self, op, drawpass, bd, bh):
        if drawpass!=c4d.DRAWPASS_HANDLES: return c4d.DRAWRESULT_SKIP
        
        hitid = op.GetHighlightHandle(bd)
        
        m = bh.GetMg()
        bd.SetMatrix_Matrix(op, m)
        
        if hitid==0:
            bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_SELECTION_PREVIEW))
        else:
            bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
        
        info = c4d.HandleInfo()
        self.GetHandle(op, 0, info)
        
        bd.DrawHandle(info.position, c4d.DRAWHANDLE_BIG, 0)
        bd.DrawLine(info.position, c4d.Vector(0), 0)
        
        return c4d.DRAWRESULT_OK
    
    
    def GenerateCircle(self, rad):
        sub = 4
        sn = 0
        TANG = 0.415
        
        op = c4d.SplineObject(sub*2, c4d.SPLINETYPE_BEZIER)
        if not op: return None
        
        op.MakeVariableTag(c4d.Tsegment, 2)
        op[c4d.SPLINEOBJECT_CLOSED] = True
        
        segc = op.GetSegmentCount()
        if segc>0:
            op.SetSegment(id=0, cnt=4, closed=True)
            op.SetSegment(id=1, cnt=4, closed=True)
        
        for i in xrange(sub):
            sn, cs = utils.SinCos(2.0*math.pi*i/float(sub));
            op.SetPoint(i, c4d.Vector(cs*rad,sn*rad,0.0))
            
            vl = c4d.Vector(sn*rad*TANG,-cs*rad*TANG,0.0)
            vr = -vl
            op.SetTangent(i, vl, vr)
            
            op.SetPoint(i+sub, c4d.Vector(cs*rad,sn*rad,0.0)*0.5)
            vl = c4d.Vector(sn*rad*TANG,-cs*rad*TANG,0.0)*0.5
            vr = -vl
            op.SetTangent(i+sub, vl, vr)
        
        op.Message(c4d.MSG_UPDATE)
        return op
    
    
    @staticmethod
    def OrientObject(op, plane, reverse):
        pcnt = op.GetPointCount()
        points = op.GetAllPoints()
        
        if plane>=c4d.PRIM_PLANE_ZY:
            if plane==c4d.PRIM_PLANE_ZY:
                for i, point in enumerate(points):
                    x = -point.z
                    y = point.y
                    z = point.x
                    
                    op.SetPoint(i, c4d.Vector(x, y, z))
                    
                    h = op.GetTangent(i)
                    vl = h["vl"]
                    vr = h["vr"]
                    vl = c4d.Vector(-vl.z, vl.y, vl.x)
                    vr = c4d.Vector(-vr.z, vr.y, vr.x)
                    
                    op.SetTangent(i, vl, vr)
                    
            elif plane==c4d.PRIM_PLANE_XZ:
                for i, point in enumerate(points):
                    x = point.x
                    y = -point.z
                    z = point.y
                    
                    op.SetPoint(i, c4d.Vector(x, y, z))
                    
                    h = op.GetTangent(i)
                    vl = h["vl"]
                    vr = h["vr"]
                    vl = c4d.Vector(vl.x, -vl.z, vl.y)
                    vr = c4d.Vector(vr.x, -vr.z, vr.y)
                    
                    op.SetTangent(i, vl, vr)
        
        if reverse:
            to = pcnt/float(2)
            if pcnt%2:
                to+=1
            for i, point in enumerate(points[:int(to)]):
                op.SetPoint(i, points[pcnt-1-i])
                op.SetPoint(pcnt-1-i, point)
                
                h = op.GetTangent(i)
                tangents = op.GetTangent(pcnt-1-i)
                # Move from right to left
                vr, vl = tangents["vl"], tangents["vr"]
                op.SetTangent(i, vl, vr)
                
                op.SetTangent(pcnt-1-i, h["vr"], h["vl"])
                
        op.Message(c4d.MSG_UPDATE)
    
    
    def GetContour(self, op, doc, lod, bt):
        bc = op.GetDataInstance()
        bp = self.GenerateCircle(bc.GetReal(c4d.PYCIRCLEOBJECT_RAD))
        if not bp: return None
        bb = bp.GetDataInstance()
        
        bb.SetLong(c4d.SPLINEOBJECT_INTERPOLATION, bc.GetLong(c4d.SPLINEOBJECT_INTERPOLATION))
        bb.SetLong(c4d.SPLINEOBJECT_SUB, bc.GetLong(c4d.SPLINEOBJECT_SUB))
        bb.SetReal(c4d.SPLINEOBJECT_ANGLE, bc.GetReal(c4d.SPLINEOBJECT_ANGLE))
        bb.SetReal(c4d.SPLINEOBJECT_MAXIMUMLENGTH, bc.GetReal(c4d.SPLINEOBJECT_MAXIMUMLENGTH))
        
        DoubleCircleData.OrientObject(bp, bc.GetLong(c4d.PRIM_PLANE), bc.GetBool(c4d.PRIM_REVERSE))
        
        return bp
    
    
    def GetDEnabling(self, node, id, t_data, flags, itemdesc):
        data = node.GetDataInstance()
        if data is None: return
        
        inter = data.GetLong(c4d.SPLINEOBJECT_INTERPOLATION)
        if id[0].id==c4d.SPLINEOBJECT_SUB:
            return inter==c4d.SPLINEOBJECT_INTERPOLATION_NATURAL or inter==c4d.SPLINEOBJECT_INTERPOLATION_UNIFORM
        elif id[0].id==c4d.SPLINEOBJECT_ANGLE:
            return inter==c4d.SPLINEOBJECT_INTERPOLATION_ADAPTIVE or inter==c4d.SPLINEOBJECT_INTERPOLATION_SUBDIV
        elif id[0].id==c4d.SPLINEOBJECT_MAXIMUMLENGTH:
            return inter==c4d.SPLINEOBJECT_INTERPOLATION_SUBDIV

        return True


def DoubleCircleHelp(opType, baseType, group, property):
    # Prints the information passed to the plugin help callback
    print "Py-DoubleCircle - Help:", opType, baseType, group, property
    if property == "PYCIRCLEOBJECT_RAD":
        # A simple MessageDialog is shown. Instead an URL to online or local help could be opened in a browser
        gui.MessageDialog("Py - DoubleCircle - Radius of the Double Circle")

    return True


if __name__ == "__main__":
    path, file = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(path, "res", "circle.tif"))
    plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="Py-DoubleCircle",
                                g=DoubleCircleData,
                                description="Opydoublecircle", icon=bmp,
                                info=c4d.OBJECT_GENERATOR|c4d.OBJECT_ISSPLINE)

    # Registers the plugin help callback for Py-DoubleCircle
    plugins.RegisterPluginHelpCallback(PLUGIN_ID, DoubleCircleHelp)
