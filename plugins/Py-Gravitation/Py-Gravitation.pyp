"""
Gravitation
Copyright: MAXON Computer GmbH
Written for Cinema 4D R12.016

Modified Date: 08/30/2010
"""

import os
import c4d
from c4d import plugins, bitmaps

# be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1025246

class Gravitation(plugins.ObjectData):
    """Gravitation Generator"""

    gravitation = 918.0 #gravitation
    
    def ModifyParticles(self, op, pp, ss, pcnt, diff):
        #doing gravitation
        
        amp = diff*self.gravitation
        img = ~op.GetMg()
        
        for s, p in zip(pp, ss):
            if not (s.bits & c4d.PARTICLEFLAGS_VISIBLE): continue
            
            vv = s.v3
            
            vv.y -=amp
            p.v += vv
            p.count += 1
        return


if __name__ == "__main__":
    path, fn = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(path, "res", "gravitation.tif"))
    plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="Py-Gravitation",
                                g=Gravitation,
                                description="gravitation", icon=bmp,
                                info=c4d.OBJECT_PARTICLEMODIFIER)
