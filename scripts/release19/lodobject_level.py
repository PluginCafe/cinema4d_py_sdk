# This example hides the objects of the active LOD object 'op' current level.

import c4d

# get active LOD object current level
currentLevel = op.GetCurrentLevel()

# hide current level
showControlID = op.GetShowControlDescID(currentLevel)
if showControlID is not None:
    op[showControlID] = False
    c4d.EventAdd()
