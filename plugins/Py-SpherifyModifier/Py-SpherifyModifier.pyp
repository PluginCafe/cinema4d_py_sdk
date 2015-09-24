"""
SpherifyModifier
Copyright: MAXON Computer GmbH
Written for Cinema 4D R13.058

Modified Date: 18/04/2012
"""

import os
import sys
import c4d
from c4d import plugins, utils, bitmaps, gui

# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1025252


class SpherifyModifier(plugins.ObjectData):
    """Spherify Modifier"""

    HANDLECOUNT = 2
    

    def Message(self, node, type, data):
        if type==c4d.MSG_MENUPREPARE:
            node.SetDeformMode(True)
        return True
    

    def Init(self, op):
        self.InitAttr(op, float, [c4d.PYSPHERIFYDEFORMER_RADIUS])
        self.InitAttr(op, float, [c4d.PYSPHERIFYDEFORMER_STRENGTH])
        
        op[c4d.PYSPHERIFYDEFORMER_RADIUS]= 200.0
        op[c4d.PYSPHERIFYDEFORMER_STRENGTH] = 0.5
        
        return True
    

    def GetDimension(self, op, mp, rad):
        mp.x = 0.0
        mp.y = 0.0
        mp.z = 0.0
        
        radius = op[c4d.PYSPHERIFYDEFORMER_RADIUS]
        rad.x = radius
        rad.y = radius
        rad.z = radius
    

    def GetHandleCount(op):
        return SpherifyModifier.HANDLECOUNT


    def GetHandle(self, op, i, info):
        data = op.GetDataInstance()
        if data is None: return
        
        if i==0:
            info.position = c4d.Vector(data.GetReal(c4d.PYSPHERIFYDEFORMER_RADIUS), 0.0, 0.0)
            info.direction = c4d.Vector(1.0, 0.0, 0.0)
            info.type = c4d.HANDLECONSTRAINTTYPE_LINEAR
        elif i==1:
            info.position = c4d.Vector(data.GetReal(c4d.PYSPHERIFYDEFORMER_STRENGTH) * 1000.0, 0.0, 0.0)
            info.direction = c4d.Vector(1.0, 0.0, 0.0)
            info.type = c4d.HANDLECONSTRAINTTYPE_LINEAR
    
    
    def DetectHandle(self, op, bd, x, y, qualifier):
        if qualifier&c4d.QUALIFIER_CTRL: return c4d.NOTOK
        
        mg = op.GetMg()
        ret = c4d.NOTOK
        
        for i in xrange(self.GetHandleCount()):
            info = c4d.HandleInfo()
            self.GetHandle(op, i, info)
            if bd.PointInRange(info.position*mg, x, y):
                ret = i
                if not qualifier&c4d.QUALIFIER_SHIFT: break
        
        return ret
    

    def MoveHandle(self, op, undo, mouse_pos, hit_id, qualifier, bd):
        dst = op.GetDataInstance();
        
        info = c4d.HandleInfo()
        val = mouse_pos.x
        self.GetHandle(op, hit_id, info)
        
        if bd is not None:
            mg = op.GetUpMg()*undo.GetMl()
            pos = bd.ProjectPointOnLine(info.position*mg, info.direction^mg, mouse_pos.x, mouse_pos.y)
            val = (pos[0]*~mg)*info.direction
        
        if hit_id==0:
            dst.SetReal(c4d.PYSPHERIFYDEFORMER_RADIUS, utils.FCut(val, 0.0, sys.maxint))
        elif hit_id==1:  
            dst.SetReal(c4d.PYSPHERIFYDEFORMER_STRENGTH, utils.FCut(val*0.001, 0.0, 1.0))

        return True


    def Draw(self, op, drawpass, bd, bh):
        if drawpass==c4d.DRAWPASS_OBJECT:
            rad = op[c4d.PYSPHERIFYDEFORMER_RADIUS]
            m = bh.GetMg()
            
            m.v1 *= rad
            m.v2 *= rad
            m.v3 *= rad
            
            bd.SetMatrix_Matrix(None, c4d.Matrix())
            bd.SetPen(bd.GetObjectColor(bh, op))
            bd.DrawCircle(m)
            h = m.v2
            m.v2 = m.v3
            m.v3 = h
            bd.DrawCircle(m)
            h = m.v1
            m.v1 = m.v3
            m.v3 = h
            bd.DrawCircle(m)
            
            return c4d.DRAWRESULT_OK
            
        elif drawpass==c4d.DRAWPASS_HANDLES:
            i = 0
            bd.SetMatrix_Matrix(None, bh.GetMg())
            
            hitid = op.GetHighlightHandle(bd)
            
            for i in xrange(self.HANDLECOUNT):
                info = c4d.HandleInfo()
                self.GetHandle(op, i, info)
                if i==hitid:
                    bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_SELECTION_PREVIEW))
                else:
                    bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
                    
                bd.DrawHandle(info.position, c4d.DRAWHANDLE_BIG, 0)
            
            info = c4d.HandleInfo()
            self.GetHandle(op, 1, info)
            
            bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
            bd.DrawLine(info.position, c4d.Vector(0), 0)
            
            return c4d.DRAWRESULT_OK
        
        return c4d.DRAWRESULT_SKIP
    
    
    def ModifyObject(self, mod, doc, op, op_mg, mod_mg, lod, flags, thread):
        p = c4d.Vector()
        pcnt = int(0)
        rad = mod[c4d.PYSPHERIFYDEFORMER_RADIUS]
        strength = mod[c4d.PYSPHERIFYDEFORMER_STRENGTH]
        s = float(0.0)
        
        if not op.CheckType(c4d.Opoint): return True
        
        padr = op.GetAllPoints()
        pcnt = op.GetPointCount()
        
        if pcnt == 0: return True
        
        weight = op.CalcVertexmap(mod)
        
        m = (~mod_mg)*op_mg # op -> world -> modifier
        im = ~m
        for i, point in enumerate(padr):
            p = m*point
            s = strength
            if weight is not None:
                s *= weigth[i]
            p = s*((p.GetNormalized())*rad)+(1.0-s)*p
            op.SetPoint(i, p*im)
        
        op.Message(c4d.MSG_UPDATE)

        return True


if __name__ == "__main__":
    path, fn = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(path, "res", "opyspherifydeformer.tif"))
    plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="Py-SpherifyModifier",
                                g=SpherifyModifier,
                                description="opyspherifydeformer", icon=bmp,
                                info=c4d.OBJECT_MODIFIER)
