# This example configures the display settings for each level of the active LOD object 'op'.

import c4d

# get active LOD object number of levels
levelCount = op.GetLevelCount()

for level in xrange(levelCount):

    descID = op.GetDisplayBFCDescID(level)

    # enable backface culling
    if descID is not None:
        op[descID] = True

    # currently GetDisplayStModeDescID() and GetDisplayShModeDescID() are switched up
    # use "Lines" shading
    descID = op.GetDisplayStModeDescID(level)
    if descID is not None:
        op[descID] = c4d.DISPLAYTAG_SDISPLAY_NOSHADING

    # use "Wireframe" style
    descID = op.GetDisplayShModeDescID(level)
    if descID is not None:
        op[descID] = c4d.DISPLAYTAG_WDISPLAY_WIREFRAME

c4d.EventAdd()
