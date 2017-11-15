"""
Liquid Painter
Copyright: MAXON Computer GmbH
Written for Cinema 4D R12.016

Modified Date: 15/11/2017
"""

import c4d
import os

from c4d import gui, plugins, bitmaps

#be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1025247

#for GeLoadString
#values must match with the header file
IDS_PRIMITIVETOOL = 50000


class SettingsDialog(gui.SubDialog):
    parameters = None

    def __init__(self, arg):
        self.parameters = arg

    def CreateLayout(self):
        self.GroupBegin(id=1000, flags=c4d.BFH_SCALEFIT, cols=2, rows=1)
        self.GroupBorderSpace(10, 10, 10, 10)
        self.element = self.AddStaticText(id=1001, flags=c4d.BFH_MASK, initw=120, name="Sphere Size", borderstyle=c4d.BORDER_NONE)

        value = self.parameters['sphere_size']

        self.AddEditNumberArrows(id=1002, flags=c4d.BFH_MASK)
        self.SetReal(id=1002, value=value, min=0, max=20)
        self.GroupEnd()
        return True


    def Command(self, id, msg):
        if id==1002:
            self.parameters['sphere_size'] = self.GetLong(1002)
        
        return True


class LiquidTool(plugins.ToolData):
    """Inherit from ToolData to create your own tool"""

    def __init__(self):
        self.data = {'sphere_size':15}
    
    
    def GetState(self, doc):
        if doc.GetMode()==c4d.Mpaint: return 0
        return c4d.CMD_ENABLED
    
    
    def KeyboardInput(self, doc, data, bd, win, msg):
        key = msg.GetLong(c4d.BFM_INPUT_CHANNEL)
        cstr = msg.GetString(c4d.BFM_INPUT_ASC)
        if key==c4d.KEY_ESC:
            #do what you want
            
            #return True to signal that the key is processed
            return True
        return False


    def MouseInput(self, doc, data, bd, win, msg):
        mx = msg[c4d.BFM_INPUT_X]
        my = msg[c4d.BFM_INPUT_Y]

        device = 0
        if msg[c4d.BFM_INPUT_CHANNEL]==c4d.BFM_INPUT_MOUSELEFT:
            device = c4d.KEY_MLEFT
        elif msg[c4d.BFM_INPUT_CHANNEL]==c4d.BFM_INPUT_MOUSERIGHT:
             device = c4d.KEY_MRIGHT
        else:
            return True
        
        null = c4d.BaseObject(c4d.Ometaball)
        null[c4d.METABALLOBJECT_SUBEDITOR] = 10
        null.MakeTag(c4d.Tphong)
        
        doc.AddUndo(c4d.UNDO_NEW, null)
        
        doc.InsertObject(null)
        doc.SetActiveObject(null)
        c4d.DrawViews(c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_ANIMATION)
        
        rad = self.data['sphere_size']
        dx = 0.0
        dy = 0.0
        
        win.MouseDragStart(button=device, mx=int(mx), my=int(my), flags=c4d.MOUSEDRAGFLAGS_DONTHIDEMOUSE|c4d.MOUSEDRAGFLAGS_NOMOVE)
        result, dx, dy, channel = win.MouseDrag()
        while result==c4d.MOUSEDRAGRESULT_CONTINUE:
            mx += dx
            my += dy
            
            #continue if user doesnt move the mouse anymore
            if dx==0.0 and dy==0.0:
                result, dx, dy, channel = win.MouseDrag()
                continue
            
            cl = c4d.BaseObject(c4d.Osphere)
            
            cl.SetAbsPos(bd.SW(c4d.Vector(mx, my, 500.0)))
            cl[c4d.PRIM_SPHERE_RAD] = rad
            cl.InsertUnder(null)

            c4d.DrawViews(c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_ANIMATION)
            result, dx, dy, channel = win.MouseDrag()
        
        if win.MouseDragEnd()==c4d.MOUSEDRAGRESULT_ESCAPE:
            doc.DoUndo(True)
        
        c4d.EventAdd()
        return True
    
    
    def Draw(self, doc, data, bd, bh, bt, flags):
        bd.SetMatrix_Matrix(None, c4d.Matrix())
        
        if flags & c4d.TOOLDRAWFLAGS_HIGHLIGHT:
            #Draw your stuff inside the highlight plane
            p = [c4d.Vector(0,0,0), c4d.Vector(100,0,0), c4d.Vector(50,100,0)]
            f = [c4d.Vector(1,0,0), c4d.Vector(1,0,0), c4d.Vector(1,0,0)]
        elif flags & c4d.TOOLDRAWFLAGS_INVERSE_Z:
            # Draw your stuff into the active plane - invisible Z
            p = [c4d.Vector(0,0,0), c4d.Vector(100,0,0), c4d.Vector(50,-100,0)]
            f = [c4d.Vector(0,0,1), c4d.Vector(0,0,1), c4d.Vector(0,0,1)]
        elif not flags:
            # Draw your stuff into the active plane - visible Z
            p = [c4d.Vector(0,0,0), c4d.Vector(-100,0,0), c4d.Vector(-50,100,0)]
            f = [c4d.Vector(0,1,0), c4d.Vector(0,1,0), c4d.Vector(0,1,0)]

        bd.DrawPolygon(p, f)
        return c4d.TOOLDRAW_HANDLES|c4d.TOOLDRAW_AXIS
    
    
    def GetCursorInfo(self, doc, data, bd, x, y, bc):
        if bc.GetId()==c4d.BFM_CURSORINFO_REMOVE:
            return True
        
        bc.SetString(c4d.RESULT_BUBBLEHELP, plugins.GeLoadString(IDS_PRIMITIVETOOL))
        bc.SetLong(c4d.RESULT_CURSOR, c4d.MOUSE_POINT_HAND)
        return True


    def AllocSubDialog(self, bc):
        return SettingsDialog(self.data) #always return new instance


if __name__ == "__main__":
    bmp = bitmaps.BaseBitmap()
    dir, file = os.path.split(__file__)
    fn = os.path.join(dir, "res", "liquid.tif")
    bmp.InitWith(fn)
    plugins.RegisterToolPlugin(id=PLUGIN_ID, str="Py-Liquid Painter",
                                info=0, icon=bmp, 
                                help="This string is shown in the statusbar",
                                dat=LiquidTool())
