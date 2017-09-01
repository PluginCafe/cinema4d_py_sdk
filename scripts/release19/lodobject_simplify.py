# This example configures the active LodObject 'op' to use the "Simplify" mode.
# The first level uses the "Convex Hull" mode, the second the "Null" mode.
# Use "Simplify" mode and a manual number of levels.

import c4d

op[c4d.LOD_MODE] = c4d.LOD_MODE_SIMPLIFY
op[c4d.LOD_CRITERIA] = c4d.LOD_CRITERIA_MANUAL
op[c4d.LOD_LEVEL_COUNT_DYN] = 2

# first level
descID = op.GetSimplifyModeDescID(0)
if descID is not None:
    # set mode to "Convex Hull"
    op[descID] = c4d.LOD_SIMPLIFY_CONVEXHULL
    descID = op.GetPerObjectControlDescID(0)
    if descID is not None:
        # set "Per Object" to True
        op[descID] = True

# second level
descID = op.GetSimplifyModeDescID(1)
if descID is not None:
    # set mode to "Null"
    op[descID] = c4d.LOD_SIMPLIFY_NULL
    descID = op.GetNullDisplayDescID(1)
    if descID is not None:
        # set "Display" to "Circle"
        op[descID] = c4d.NULLOBJECT_DISPLAY_CIRCLE

c4d.EventAdd()
