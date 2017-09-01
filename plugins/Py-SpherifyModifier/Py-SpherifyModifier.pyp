"""
Spherify Modifier with Falloff
Copyright: MAXON Computer GmbH
Written for Cinema 4D R19

Modified Date: 31/08/2017
"""

import os
import sys
import c4d
from c4d import bitmaps, gui, plugins, utils
from c4d.modules import mograph

# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1025252


def SkipFalloff(bc):
    if bc is None:
        return True

    return bc[c4d.FALLOFF_MODE] == c4d.FALLOFF_MODE_INFINITE and bc[c4d.FALLOFF_STRENGTH] == 1.0


class SpherifyModifier(plugins.ObjectData):
    """Spherify Modifier"""

    HANDLECOUNT = 2


    def __init__(self):
        self.SetOptimizeCache(True)

        self.falloff = None


    def Message(self, node, type, data):
        bc = node.GetDataInstance()

        # Enables deform tick when created from UI
        if type == c4d.MSG_MENUPREPARE:
            node.SetDeformMode(True)

        # Passes message to falloff
        if self.falloff is not None:
            self.falloff.Message(type, bc, data)

        return True


    def Init(self, op):

        # Initializes radius and strength

        self.InitAttr(op, float, [c4d.PYSPHERIFYMODIFIER_RADIUS])
        self.InitAttr(op, float, [c4d.PYSPHERIFYMODIFIER_STRENGTH])

        op[c4d.PYSPHERIFYMODIFIER_RADIUS]= 200.0
        op[c4d.PYSPHERIFYMODIFIER_STRENGTH] = 0.5

        # Creates fallof
        if self.falloff is None:
            self.falloff = mograph.C4D_Falloff()
            if self.falloff is None:
                return False

        return True


    def GetDimension(self, op, mp, rad):
        mp.x = 0.0
        mp.y = 0.0
        mp.z = 0.0

        radius = op[c4d.PYSPHERIFYMODIFIER_RADIUS]
        rad.x = radius
        rad.y = radius
        rad.z = radius


    def GetHandleCount(self, op):
        data = op.GetDataInstance()
        if data is None:
            return 0

        if self.falloff is not None:
            return self.falloff.GetHandleCount(data) + SpherifyModifier.HANDLECOUNT

        return SpherifyModifier.HANDLECOUNT


    def GetHandle(self, op, i, info):
        data = op.GetDataInstance()
        if data is None:
            return

        if i < SpherifyModifier.HANDLECOUNT:
            if i == 0:
                # Radius handle
                info.position = c4d.Vector(data[c4d.PYSPHERIFYMODIFIER_RADIUS], 0.0, 0.0)
                info.direction = c4d.Vector(1.0, 0.0, 0.0)
                info.type = c4d.HANDLECONSTRAINTTYPE_LINEAR
            elif i == 1:
                # Strength handle
                info.position = c4d.Vector(data[c4d.PYSPHERIFYMODIFIER_STRENGTH] * 1000.0, 0.0, 0.0)
                info.direction = c4d.Vector(1.0, 0.0, 0.0)
                info.type = c4d.HANDLECONSTRAINTTYPE_LINEAR
        else:
            # Falloff handles
            if self.falloff is not None:
                self.falloff.GetHandle(i - SpherifyModifier.HANDLECOUNT, data, info)


    def SetHandle(self, op, i, p, info):
        data = op.GetDataInstance()
        if data is None:
            return

        if i < SpherifyModifier.HANDLECOUNT:

            val = p.x;

            if i == 0:
                # Radius handle
                data[c4d.PYSPHERIFYMODIFIER_RADIUS] = val
            elif i == 1:
                # Strength handle
                data[c4d.PYSPHERIFYMODIFIER_STRENGTH] = utils.ClampValue(val * 0.001, 0.0, 1.0)
        else:
            # Falloff handles
            if self.falloff is not None:
                self.falloff.SetHandle(i - SpherifyModifier.HANDLECOUNT, p, data, info)


    def Draw(self, op, drawpass, bd, bh):
        if drawpass == c4d.DRAWPASS_OBJECT:

            data = op.GetDataInstance()
            if data is None:
                return

            rad = data[c4d.PYSPHERIFYMODIFIER_RADIUS]
            m = bh.GetMg()

            skipFalloff = SkipFalloff(data)
            if self.falloff is not None and not skipFalloff and data is not None:
                if not self.falloff.InitFalloff(data, bh.GetDocument(), op):
                    return c4d.DRAWRESULT_ERROR

            m.v1 *= rad
            m.v2 *= rad
            m.v3 *= rad

            bd.SetPen(bd.GetObjectColor(bh, op))

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

            if self.falloff is not None and not skipFalloff and data is not None:
                self.falloff.Draw(bd, bh, drawpass, data)
                # Restores camera matrix as falloff changes this
                bd.SetMatrix_Camera()

        elif drawpass == c4d.DRAWPASS_HANDLES:

            bd.SetMatrix_Matrix(None, bh.GetMg())

            info = c4d.HandleInfo()
            self.GetHandle(op, 1, info)

            bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
            bd.DrawLine(info.position, c4d.Vector(0), 0)

            plugins.ObjectData.Draw(self, op, drawpass, bd, bh)

        return c4d.DRAWRESULT_OK


    def ModifyObject(self, mod, doc, op, op_mg, mod_mg, lod, flags, thread):

        data = mod.GetDataInstance()

        if not op.CheckType(c4d.Opoint):
            return True

        skipFalloff = SkipFalloff(data)
        if self.falloff is not None and not skipFalloff:
            if not self.falloff.InitFalloff(data, doc, mod):
                return False

        radius = mod[c4d.PYSPHERIFYMODIFIER_RADIUS]
        strength = mod[c4d.PYSPHERIFYMODIFIER_STRENGTH]

        points = op.GetAllPoints()
        pointCount = op.GetPointCount()

        if pointCount == 0:
            return True

        weights = op.CalcVertexmap(mod)

        # Calculates spherify deformation

        matrix = (~mod_mg) * op_mg # op -> world -> modifier
        invMatrix = ~matrix
        for index, point in enumerate(points):
            finalPoint = matrix * point
            finalStrength = strength
            if weights is not None:
                finalStrength *= weights[i]

            if self.falloff is not None and not skipFalloff:
                finalStrength *= self.falloff.Sample(op_mg * points[index])

            finalPoint = finalStrength * ((finalPoint.GetNormalized()) * radius) + (1.0 - finalStrength) * finalPoint
            op.SetPoint(index, finalPoint * invMatrix)

        # Updates input object
        op.Message(c4d.MSG_UPDATE)

        return True


    def GetDDescription(self, node, description, flags):

        data = node.GetDataInstance()
        if data is None:
            return False

        # Loads Spherify Modifier

        if not description.LoadDescription(node.GetType()):
            return False

        # Adds falloff UI to description

        if self.falloff is not None:
            if not self.falloff.SetMode(data.GetInt32(c4d.FALLOFF_MODE, c4d.FALLOFF_MODE_INFINITE), data):
                return False
            if not self.falloff.AddFalloffToDescription(description, data):
                return False

        return (True, flags | c4d.DESCFLAGS_DESC_LOADED)


    def CopyTo(self, dest, snode, dnode, flags, trn):
        if self.falloff is not None and dest.falloff is not None:
            # Copies falloff to destination Py-SpherifyModifier
            if not self.falloff.CopyTo(dest.falloff):
                return False

        return True


if __name__ == "__main__":
    path, fn = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(path, "res", "opyspherifymodifier.tif"))
    plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="Py-SpherifyModifier",
                                g=SpherifyModifier,
                                description="opyspherifymodifier", icon=bmp,
                                info=c4d.OBJECT_MODIFIER)
