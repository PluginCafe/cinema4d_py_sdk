# This example shows how to call BodyPaint 3D UV commands

import c4d
from c4d import utils
from c4d.modules import bodypaint


def main():
    # Retrieves active UVSet
    handle = bodypaint.GetActiveUVSet(doc, c4d.GETACTIVEUVSET_ALL)
    if not handle:
        print "No active UVSet!"
        return

    # Prints UVSet information
    print "UV handle data:"
    print "handle:", handle
    print "handle Mode:", handle.GetMode()
    print "handle Points:", handle.GetPoints()
    print "handle Polygons:", handle.GetPolys()
    print "handle Polygon selection:", handle.GetPolySel()
    print "handle hidden Polygons:", handle.GetPolyHid()
    print "handle Point selection:", handle.GetUVPointSel()
    print "handle Point count:", handle.GetPointCount()
    print "handle Polygon count:", handle.GetPolyCount()
    print "handle Object:", handle.GetBaseObject()
    print "handle Editable:", handle.IsEditable()
    uvw = handle.GetUVW()
    print "handle UVW:", uvw
    print "handle set UVW:", handle.SetUVW(uvw)
    print "handle set UVW (from texture view):", handle.SetUVWFromTextureView(uvw, True, True, True)

    # Builds UVCOMMAND_TRANSFORM container for the command settings
    settings = c4d.BaseContainer()
    settings[c4d.UVCOMMAND_TRANSFORM_MOVE_X] = 0
    settings[c4d.UVCOMMAND_TRANSFORM_MOVE_Y] = 0
    settings[c4d.UVCOMMAND_TRANSFORM_SCALE_X] = 1
    settings[c4d.UVCOMMAND_TRANSFORM_SCALE_Y] = 1
    settings[c4d.UVCOMMAND_TRANSFORM_ANGLE] = utils.Rad(90)

    # Calls UVCOMMAND_TRANSFORM
    ret = bodypaint.CallUVCommand(handle.GetPoints(), handle.GetPointCount(), handle.GetPolys(), handle.GetPolyCount(), 
                                  handle.GetUVW(), handle.GetPolySel(), handle.GetUVPointSel(), op, handle.GetMode(), c4d.UVCOMMAND_TRANSFORM, settings)
    if not ret:
        print "CallUVCommand() failed!"
        return

    # Tries to set UVW from Texture View
    print "CallUVCommand() successfully called"
    if handle.SetUVWFromTextureView(handle.GetUVW(), True, True, True):
        print "UVW from Texture View successfully set"
    else:
        print "UVW from Texture View failed to be set!"

    # Releases active UVSet
    bodypaint.FreeActiveUVSet(handle)


if __name__=='__main__':
    main()
