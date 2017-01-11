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
    print "UV Handle Data:"
    print "Handle:", handle
    print "Handle Mode:", handle.GetMode()
    print "Handle Points:", handle.GetPoints()
    print "Handle Polygons:", handle.GetPolys()
    print "Handle Polygon Selection:", handle.GetPolySel()
    print "Handle Hidden Polygons:", handle.GetPolyHid()
    print "Handle Point Selection:", handle.GetUVPointSel()
    print "Handle Point Count:", handle.GetPointCount()
    print "Handle Polygon Count:", handle.GetPolyCount()
    print "Handle Object:", handle.GetBaseObject()
    print "Handle Editable:", handle.IsEditable()
    print "Handle UVW:", handle.GetUVW()

    # Builds UVCOMMAND_TRANSFORM container for the command settings
    settings = c4d.BaseContainer()
    settings[c4d.UVCOMMAND_TRANSFORM_MOVE_X] = 0
    settings[c4d.UVCOMMAND_TRANSFORM_MOVE_Y] = 0
    settings[c4d.UVCOMMAND_TRANSFORM_SCALE_X] = 1
    settings[c4d.UVCOMMAND_TRANSFORM_SCALE_Y] = 1
    settings[c4d.UVCOMMAND_TRANSFORM_ANGLE] = utils.DegToRad(90)

    # Retrieves UVW list
    uvw = handle.GetUVW()
    if uvw is None:
        return

    # Calls UVCOMMAND_TRANSFORM to change UVW list
    ret = bodypaint.CallUVCommand(handle.GetPoints(), handle.GetPointCount(), handle.GetPolys(), handle.GetPolyCount(), uvw,
                                  handle.GetPolySel(), handle.GetUVPointSel(), op, handle.GetMode(), c4d.UVCOMMAND_TRANSFORM, settings)
    if not ret:
        print "CallUVCommand() failed!"
        return

    print "CallUVCommand() successfully called"

    # Sets the transformedUVW from Texture View 
    if handle.SetUVWFromTextureView(uvw, True, True, True):
        print "UVW from Texture View successfully set"
    else:
        print "UVW from Texture View failed to be set!"

    # Releases active UVSet
    bodypaint.FreeActiveUVSet(handle)


if __name__=='__main__':
    main()
