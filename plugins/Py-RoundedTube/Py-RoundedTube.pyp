"""
RoundedTube
Copyright: MAXON Computer GmbH
Written for Cinema 4D R18

Modified Date: 05/12/2018
"""

import os
import math
import sys
import c4d

from c4d import plugins, utils, bitmaps, gui

# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1025250

class RoundedTube(plugins.ObjectData):
    """RoundedTube Generator"""


    # define the number of handles that will be drawn, it's actually a constant.
    HANDLECOUNT = 5


    # Enable few optimizations, take a look at the GetVirtualObjects method for more information.
    def __init__(self):
        self.SetOptimizeCache(True)


    # Helper method to set the local axis of the object.
    @staticmethod
    def SetAxis(op, axis):
        if axis is c4d.PRIM_AXIS_YP: return
        padr = op.GetAllPoints()
        if padr is None: return
        
        elif axis is c4d.PRIM_AXIS_XP:
            for i, p in enumerate(padr):
                op.SetPoint(i, c4d.Vector( p.y, -p.x, p.z))
        elif axis is c4d.PRIM_AXIS_XN:
            for i, p in enumerate(padr):
                op.SetPoint(i, c4d.Vector(-p.y, p.x, p.z))
        elif axis is c4d.PRIM_AXIS_YN:
            for i, p in enumerate(padr):
                op.SetPoint(i, c4d.Vector(-p.x, -p.y, p.z))
        elif axis is c4d.PRIM_AXIS_ZP:
            for i, p in enumerate(padr):
                op.SetPoint(i, c4d.Vector(p.x, -p.z, p.y))
        elif axis is c4d.PRIM_AXIS_ZN:
            for i, p in enumerate(padr):
                op.SetPoint(i, c4d.Vector(p.x, p.z, -p.y))
        
        op.Message(c4d.MSG_UPDATE)


    # Helper method to determine how point should be swapped according to the local axis.
    @staticmethod
    def SwapPoint(p, axis):
        if axis is c4d.PRIM_AXIS_XP:
            return c4d.Vector(p.y, -p.x, p.z)
        elif axis is c4d.PRIM_AXIS_XN:
            return c4d.Vector(-p.y, p.x, p.z)
        elif axis is c4d.PRIM_AXIS_YN:
            return c4d.Vector(-p.x, -p.y, p.z)
        elif axis is c4d.PRIM_AXIS_ZP:
            return c4d.Vector(p.x, -p.z, p.y)
        elif axis is c4d.PRIM_AXIS_ZN:
            return c4d.Vector(p.x, p.z, -p.y)
        return p


    # Override method, called when the object is initialized to set default values.
    def Init(self, op):
        self.InitAttr(op, float, [c4d.PY_TUBEOBJECT_RAD])
        self.InitAttr(op, float, [c4d.PY_TUBEOBJECT_IRADX])
        self.InitAttr(op, float, [c4d.PY_TUBEOBJECT_IRADY])
        self.InitAttr(op, float, [c4d.PY_TUBEOBJECT_SUB])
        self.InitAttr(op, int, [c4d.PY_TUBEOBJECT_ROUNDSUB])
        self.InitAttr(op, float, [c4d.PY_TUBEOBJECT_ROUNDRAD])
        self.InitAttr(op, int, [c4d.PY_TUBEOBJECT_SEG])
        self.InitAttr(op, int, [c4d.PRIM_AXIS])

        op[c4d.PY_TUBEOBJECT_RAD]= 200.0
        op[c4d.PY_TUBEOBJECT_IRADX] = 50.0
        op[c4d.PY_TUBEOBJECT_IRADY] = 50.0
        op[c4d.PY_TUBEOBJECT_SUB] = 1
        op[c4d.PY_TUBEOBJECT_ROUNDSUB] = 8
        op[c4d.PY_TUBEOBJECT_ROUNDRAD] = 10.0
        op[c4d.PY_TUBEOBJECT_SEG] = 36
        op[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_YP
        return True


    # Override method, react to some messages received to react to some event.
    def Message(self, node, type, data):

        # MSG_DESCRIPTION_VALIDATE is called after each parameter change. It allows checking of the input value to correct it if not.
        if type == c4d.MSG_DESCRIPTION_VALIDATE:
            node[c4d.PY_TUBEOBJECT_IRADX] = c4d.utils.ClampValue(node[c4d.PY_TUBEOBJECT_IRADX], 0.0, node[c4d.PY_TUBEOBJECT_RAD])
            node[c4d.PY_TUBEOBJECT_ROUNDRAD] = c4d.utils.ClampValue( node[c4d.PY_TUBEOBJECT_ROUNDRAD], 0.0, node[c4d.PY_TUBEOBJECT_IRADX])

        # MSH_MENUPREPARE is called when the user presses the Menu entry for this object. It allows to setup our object. In this case, it defines the Phong by adding a Phong Tag to the generator.
        elif type == c4d.MSG_MENUPREPARE:
            node.SetPhong(True, False, c4d.utils.DegToRad(40.0))

        return True


    # Override method, should return the number of handle.
    def GetHandleCount(self, op):
        return self.HANDLECOUNT


    # Override method, called to know the position of a handle.
    def GetHandle(self, op, i, info):
        
        rad = op[c4d.PY_TUBEOBJECT_RAD]
        if rad is None: rad = 200.0
        iradx = op[c4d.PY_TUBEOBJECT_IRADX]
        if iradx is None: iradx = 50.0
        irady = op[c4d.PY_TUBEOBJECT_IRADY]
        if irady is None: irady = 50.0
        rrad = op[c4d.PY_TUBEOBJECT_ROUNDRAD]
        if rrad is None: rrad = 10.0
        axis = op[c4d.PRIM_AXIS]
        if axis is None: return
        
        if i is 0:
            info.position = c4d.Vector(rad, 0.0, 0.0)
            info.direction = c4d.Vector(1.0, 0.0, 0.0)
        elif i is 1:
            info.position = c4d.Vector(rad+iradx, 0.0, 0.0)
            info.direction = c4d.Vector(1.0, 0.0, 0.0)
        elif i is 2:
            info.position = c4d.Vector(rad, irady, 0.0)
            info.direction = c4d.Vector(0.0, 1.0, 0.0)
        elif i is 3:
            info.position = c4d.Vector(rad+iradx, irady-rrad, 0.0)
            info.direction = c4d.Vector(0.0, -1.0, 0.0)
        elif i is 4:
            info.position = c4d.Vector(rad+iradx-rrad, irady, 0.0)
            info.direction = c4d.Vector(-1.0, 0.0, 0.0)
        
        info.position = RoundedTube.SwapPoint(info.position, axis)
        info.direction = RoundedTube.SwapPoint(info.direction, axis)
        info.type = c4d.HANDLECONSTRAINTTYPE_LINEAR


    # Override method, called when the user moves a handle. This is the place to set parameters.
    def SetHandle(self, op, i, p, info):
        data = op.GetDataInstance()
        if data is None: return
        
        tmp = c4d.HandleInfo()
        self.GetHandle(op, i, tmp)
        
        val = (p-tmp.position)*info.direction
        
        if i is 0:
            op[c4d.PY_TUBEOBJECT_RAD] = utils.FCut(op[c4d.PY_TUBEOBJECT_RAD]+val, op[c4d.PY_TUBEOBJECT_IRADX], sys.maxint)
        elif i is 1:
            op[c4d.PY_TUBEOBJECT_IRADX] = utils.FCut(op[c4d.PY_TUBEOBJECT_IRADX]+val, op[c4d.PY_TUBEOBJECT_ROUNDRAD], op[c4d.PY_TUBEOBJECT_RAD])
        elif i is 2:
            op[c4d.PY_TUBEOBJECT_IRADY] = utils.FCut(op[c4d.PY_TUBEOBJECT_IRADY]+val, op[c4d.PY_TUBEOBJECT_ROUNDRAD], sys.maxint)
        elif i is 3 or i is 4:
            op[c4d.PY_TUBEOBJECT_ROUNDRAD] = utils.FCut(op[c4d.PY_TUBEOBJECT_ROUNDRAD]+val, 0.0, min(op[c4d.PY_TUBEOBJECT_IRADX], op[c4d.PY_TUBEOBJECT_IRADY]))
    
    
    # Override method, draw additional stuff in the viewport (e.g. the handles).
    def Draw(self, op, drawpass, bd, bh):
        if drawpass!=c4d.DRAWPASS_HANDLES: return c4d.DRAWRESULT_SKIP

        rad = op[c4d.PY_TUBEOBJECT_RAD]
        iradx = op[c4d.PY_TUBEOBJECT_IRADX]
        irady = op[c4d.PY_TUBEOBJECT_IRADY]
        axis = op[c4d.PRIM_AXIS]

        bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
        
        hitid = op.GetHighlightHandle(bd)
        bd.SetMatrix_Matrix(op, bh.GetMg())
        
        for i in xrange(self.HANDLECOUNT):
            if i==hitid:
                bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_SELECTION_PREVIEW))
            else:
                bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
            
            info = c4d.HandleInfo()
            self.GetHandle(op, i, info)
            bd.DrawHandle(info.position, c4d.DRAWHANDLE_BIG, 0)

            bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))

            if i is 0:
                info2 = c4d.HandleInfo()
                self.GetHandle(op, 1, info2)
                bd.DrawLine(info.position, info2.position, 0)
                self.GetHandle(op, 2, info2)
                bd.DrawLine(info.position, info2.position, 0)
            elif i is 3:
                bd.DrawLine(info.position, RoundedTube.SwapPoint(c4d.Vector(rad+iradx, irady, 0.0), axis), 0)
            elif i is 4:
                bd.DrawLine(info.position, RoundedTube.SwapPoint(c4d.Vector(rad+iradx, irady, 0.0), axis), 0)
        
        return c4d.DRAWRESULT_OK


    # Helper method to generate a lathe over points.
    def GenerateLathe(self, cpadr, cpcnt, sub):
        op = tag = padr = vadr = None
        i = j = pcnt = vcnt = a = b = c = d = 0
        length = sn = cs = v1 = v2 = 0.0

        pcnt = cpcnt * sub
        vcnt = cpcnt * sub

        op = c4d.PolygonObject(pcnt, vcnt)
        if op is None: return None

        uvadr = [0.0]*(cpcnt+1)
        for i in xrange(cpcnt):
            uvadr[i] = length
            length += (cpadr[ (i+1)%cpcnt ] - cpadr[i] ).GetLength()

        if length > 0.0: length = 1.0/length
        for i in xrange(cpcnt):
            uvadr[i] *= length

        uvadr[cpcnt] = 1.0
        vcnt = 0
        for i in xrange(sub):
            sn, cs = utils.SinCos(math.pi*2 * float(i) / float(sub))
            v1 = float(i) / float(sub)
            v2 = float(i+1) / float(sub)
            for j in xrange(cpcnt):
                a = cpcnt*i+j
                op.SetPoint(a, c4d.Vector(cpadr[j].x*cs,cpadr[j].y,cpadr[j].x*sn))
                if i < sub:
                    b = cpcnt*i          +((j+1)%cpcnt)
                    c = cpcnt*((i+1)%sub)+((j+1)%cpcnt)
                    d = cpcnt*((i+1)%sub)+j
                    pol = c4d.CPolygon(a,b,c,d)
                    op.SetPolygon(vcnt, pol)
                    vcnt += 1

        op.Message(c4d.MSG_UPDATE)
        op.SetPhong(True, 1, utils.Rad(80.0))

        return op


    # Override method, should return the bounding box of the generated object.
    def GetDimension(self, op, mp, rad):
        rado = op[c4d.PY_TUBEOBJECT_RAD]
        if rado is None: return
        radx = op[c4d.PY_TUBEOBJECT_IRADX]
        if radx is None: return
        rady = op[c4d.PY_TUBEOBJECT_IRADY]
        if rady is None: return

        axis = op[c4d.PRIM_AXIS]
        if axis is None: return

        mp = 0.0
        if axis is c4d.PRIM_AXIS_XP or axis is c4d.PRIM_AXIS_XN:
            rad.x = rady
            rad.y = rado+radx
            rad.z = rado+radx
        elif axis is c4d.PRIM_AXIS_YP or axis is c4d.PRIM_AXIS_YN:
            rad.x = rado+radx
            rad.y = rady
            rad.z = rado+radx
        elif axis is c4d.PRIM_AXIS_ZP or axis is c4d.PRIM_AXIS_ZN:
            rad.x = rado+radx
            rad.y = rado+radx
            rad.z = rady


    # Override method, should generate and return the object.
    def GetVirtualObjects(self, op, hierarchyhelp):

        # Disabled the following lines because cache flag was set
        # So the cache build is done before this method is called
        #dirty = op.CheckCache(hierarchyhelp) or op.IsDirty(c4d.DIRTY_DATA)
        #if dirty is False: return op.GetCache(hierarchyhelp)

        rad = op[c4d.PY_TUBEOBJECT_RAD]
        if rad is None: rad = 200.0
        iradx = op[c4d.PY_TUBEOBJECT_IRADX]
        if iradx is None: iradx = 50.0
        irady = op[c4d.PY_TUBEOBJECT_IRADY]
        if irady is None: irady = 50.0
        rrad = op[c4d.PY_TUBEOBJECT_ROUNDRAD]
        if rrad is None: rrad = 10.0

        num_sub = op[c4d.PY_TUBEOBJECT_SUB]
        if num_sub is None: num_sub = 1
        sub = utils.CalcLOD(num_sub, 1, 1, 1000)

        num_rsub = op[c4d.PY_TUBEOBJECT_ROUNDSUB]
        if num_rsub is None: num_rsub = 8
        rsub = utils.CalcLOD(num_rsub, 1, 1, 1000)

        num_seg = op[c4d.PY_TUBEOBJECT_SEG]
        if num_seg is None: num_seg = 36
        seg = utils.CalcLOD(num_seg, 1, 3, 1000)

        i = 0
        sn = 0.0
        cs = 0.0

        cpcnt = 4*(sub+rsub)
        cpadr = [c4d.Vector()]*cpcnt

        for i in xrange(sub):
            cpadr[i]                 = c4d.Vector(rad-iradx, (1.0 - float(i)/sub*2.0)*(irady-rrad), 0.0)
            cpadr[i+sub+rsub]        = c4d.Vector(rad+(float(i)/sub*2.0-1.0)*(iradx-rrad), -irady, 0.0)
            cpadr[i+2*(sub+rsub)]    = c4d.Vector(rad+iradx, (float(i)/float(sub)*2.0-1.0)*(irady-rrad), 0.0)
            cpadr[i+3*(sub+rsub)]    = c4d.Vector(rad+(1.0-float(i)/float(sub)*2.0)*(iradx-rrad), irady, 0.0)
        
        pi05 = 1.570796326
        for i in xrange(rsub):
            sn, cs = utils.SinCos(float(i)/rsub*pi05)
            cpadr[i+sub]              = c4d.Vector(rad-(iradx-rrad+cs*rrad), -(irady-rrad+sn*rrad), 0.0)
            cpadr[i+sub+(sub+rsub)]   = c4d.Vector(rad+(iradx-rrad+sn*rrad), -(irady-rrad+cs*rrad), 0.0)
            cpadr[i+sub+2*(sub+rsub)] = c4d.Vector(rad+(iradx-rrad+cs*rrad), +(irady-rrad+sn*rrad), 0.0)
            cpadr[i+sub+3*(sub+rsub)] = c4d.Vector(rad-(iradx-rrad+sn*rrad), +(irady-rrad+cs*rrad), 0.0)
        
        ret = self.GenerateLathe(cpadr, cpcnt, seg)
        if ret is None: return None

        axis = op[c4d.PRIM_AXIS]
        if axis is None: return None

        RoundedTube.SetAxis(ret, axis)
        ret.SetName(op.GetName())

        return ret


 # This code is called at the startup, it register the class RoundedTube as a plugin to be used later in Cinema 4D. It have to be done only once.
if __name__ == "__main__":

    # Get the curren path of the file
    dir, file = os.path.split(__file__)

    # Load the oroundedtube.tif from res folder as a c4d BaseBitmap to be used as an icon.
    icon = bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(dir, "res", "oroundedtube.tif"))

    # Register the class RoundedTube as a Object Plugin to be used later in Cinema 4D.
    plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="Py-RoundedTube",
                                g=RoundedTube,
                                description="roundedtube", icon=icon,
                                info=c4d.OBJECT_GENERATOR)
