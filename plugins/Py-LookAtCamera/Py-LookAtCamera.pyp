"""
Look at Camera
Copyright: MAXON Computer GmbH
Written for Cinema 4D R13.058

Modified Date: 08/05/2012
"""

import os

import c4d
from c4d import bitmaps, plugins, utils

# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1028284


class LookAtCamera(plugins.TagData):
    """Look at Camera"""
    
    def Init(self, node):
        tag = node
        data = tag.GetDataInstance()
        
        data.SetBool(c4d.PYLOOKATCAMERA_PITCH, True)
        pd = tag[c4d.EXPRESSION_PRIORITY]
        if pd is not None:
            pd.SetPriorityValue(c4d.PRIORITYVALUE_CAMERADEPENDENT, True)
            tag[c4d.EXPRESSION_PRIORITY] = pd
        
        return True
    
    def Execute(self, tag, doc, op, bt, priority, flags):
        bd = doc.GetRenderBaseDraw()
        if bd is None: return c4d.EXECUTIONRESULT_OK
        data = tag.GetDataInstance()
        if data is None: return c4d.EXECUTIONRESULT_OK
        
        cp = bd.GetSceneCamera(doc)
        if cp is None: cp = bd.GetEditorCamera()
        if cp is None: return c4d.EXECUTIONRESULT_OK

        local = cp.GetMg().off * (~(op.GetUpMg() * op.GetFrozenMln())) - op.GetRelPos()
        hpb = utils.VectorToHPB(local)
        
        if not data.GetBool(c4d.PYLOOKATCAMERA_PITCH):
            hpb.y = op.GetRelRot().y
        
        hpb.z = op.GetRelRot().z

        op.SetRelRot(hpb)
        
        return c4d.EXECUTIONRESULT_OK


if __name__ == "__main__":
    bmp = bitmaps.BaseBitmap()
    dir, file = os.path.split(__file__)
    fn = os.path.join(dir, "res", "tpylookatcamera.tif")
    bmp.InitWith(fn)
    plugins.RegisterTagPlugin(id=PLUGIN_ID, str="Py - LookAtCamera",
                              info=c4d.TAG_EXPRESSION|c4d.TAG_VISIBLE, g=LookAtCamera,
                              description="Tpylookatcamera", icon=bmp)