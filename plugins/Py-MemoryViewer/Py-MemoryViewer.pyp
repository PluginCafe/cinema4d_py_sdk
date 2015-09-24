"""
Memory Viewer
Copyright: MAXON Computer GmbH
Written for Cinema 4D R12.016

Modified Date: 08/30/2010
"""

import c4d
from c4d import gui, plugins, utils, bitmaps, storage

import collections, os

#be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1025249

def CalcValueToMB(value):
    """Returns MB"""
    return value/1024.0/1024.0

class MemoryInfo(gui.GeUserArea):
    
    values = None
    division = 40
    
    value_max = 0
    value_min = 0
    
    highlight_line = c4d.Vector(0, 0.6, 0)
    black = c4d.Vector(0)
    shadow_line = c4d.Vector(0.15)
    
    def Init(self):
        self.values = collections.deque([0,]*self.division)
        self.Update()
        return True
    
    def DrawMsg(self, x1, y1, x2, y2, msg_ref):
        #init draw region
        self.OffScreenOn()
        self.SetClippingRegion(x1, y1, x2, y2)
        self.DrawRectangle(x1, y1, x2, y2)
        
        
        self.DrawSetPen(self.black)
        self.DrawRectangle(x1, y1, x2, y2)
        
        x_step = int((x2-x1)/self.division+1)
        y_step = int((y2-y1)/self.division+1)
        
        self.DrawSetPen(self.shadow_line)
        #draw guides
        for i in xrange(int(self.division)):
            self.DrawLine(x_step*i, y2-y1, x_step*i, y2-y2)
            self.DrawLine(x1, y2-(y_step*i), x2, y2-(y_step*i))
        
        offset = 10
        self.DrawSetPen(self.highlight_line)
        for i, v in enumerate(self.values):
            if i==len(self.values)-1:
                continue
            
            l_x1 = int(i*x_step)
            l_y1 = int(utils.RangeMap(v, self.value_min, self.value_max, y1+offset, y2-offset, False))
            l_x2 = int((i+1)*x_step)
            
            self.value_min+10, self.value_max, y1+offset, y2-offset, False
            l_y2 = int(utils.RangeMap(self.values[i+1], self.value_min+10, self.value_max, y1+offset, y2-offset, False))
            #2 and 3 too much
            self.DrawLine(l_x1, y2-l_y1, l_x2, y2-l_y2)
            
        #draw legend
        self.DrawSetTextCol(self.highlight_line, self.black)
        vmax = ("%.3f MB" % (CalcValueToMB(self.value_max)))
        vmin = ("%.3f MB" % (CalcValueToMB(self.value_min)))
        self.DrawText(vmax, 0, 0)
        self.DrawText(vmin, 0, y2-self.DrawGetFontHeight())
        
        return
    
    def Update(self):
        bc = storage.GeGetMemoryStat()
        self.values.rotate(-1)
        v = bc[c4d.C4D_MEMORY_STAT_MEMORY_INUSE]
        if v>self.value_max:
            self.value_max = v
        elif v<self.value_min:
            self.value_min = v
        
        self.values[self.division-1] = v
        self.Redraw()
        return bc #return to make available

class Test(gui.GeDialog):
    
    mem_info = MemoryInfo()
    cur_mem_info = None
    
    def __init__(self):
        self.AddGadget(c4d.DIALOG_NOMENUBAR, 0)#disable menubar
    
    def CreateLayout(self):
        
        bc = c4d.GetMachineFeatures()
        self.SetTitle(bc[c4d.MACHINEINFO_COMPUTERNAME])
        self.GroupBegin(id=0, flags=c4d.BFH_SCALEFIT, rows=1, title="", cols=2, groupflags=c4d.BORDER_GROUP_IN)
        self.AddGadget(c4d.DIALOG_PIN, 0)#enable WindowPin
        self.cur_mem_info = self.AddStaticText(id=0, initw=0, inith=0, name="", borderstyle=0, flags=c4d.BFH_SCALEFIT)
        self.GroupEnd()
        
        self.AddSeparatorH(inith=0)
        
        self.GroupBegin(id=0, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, title="", rows=1, cols=1, groupflags=c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(5, 5, 5, 5)
        
        #give really unique ID to userarea, otherwise the update process will fail!
        area = self.AddUserArea(id=1001, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT)
        self.AttachUserArea(self.mem_info, area)
        self.GroupEnd()
        return True
    
    def InitValues(self):
        self.SetTimer(500)
        return True
    
    def Timer(self, msg):
        bc = self.mem_info.Update()
        self.SetString(self.cur_mem_info, ("Current: %.3f MB" % (CalcValueToMB(bc[c4d.C4D_MEMORY_STAT_MEMORY_INUSE]))))

class BitmapManagerCommandData(c4d.plugins.CommandData):
    dialog = None

    def Execute(self, doc):
        """Just create the dialog when the user clicked on the entry
        in the plugins menu to open it."""
        if self.dialog is None:
           self.dialog = Test()

        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaulth=400, defaultw=400)

    def RestoreLayout(self, sec_ref):
        """Same for this method. Just allocate it when the dialog
        is needed"""
        if self.dialog is None:
           self.dialog = Test()

        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)

if __name__ == "__main__":
     bmp = bitmaps.BaseBitmap()
     dir, f = os.path.split(__file__)
     fn = os.path.join(dir, "res", "mviewer.tif")
     bmp.InitWith(fn)
     c4d.plugins.RegisterCommandPlugin(id=PLUGIN_ID, str="Py-MemoryViewer",
                                      help="Show the current mem usage of Cinema 4D.",info=0,
                                        dat=BitmapManagerCommandData(), icon=bmp)
