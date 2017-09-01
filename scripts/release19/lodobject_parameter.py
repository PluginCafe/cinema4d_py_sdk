# This example checks the current criteria of the active LOD object 'op'.
# If it is "User LOD Level" the current level is set to the maximum level.

import c4d

# get current criteria from active LOD object
criteria = op[c4d.LOD_CRITERIA]

# check if User LOD Level
if criteria == c4d.LOD_CRITERIA_MANUAL:
    # get maximum level
    maxLevel = op.GetLevelCount() - 1
    # set current level to max level
    op[c4d.LOD_CURRENT_LEVEL] = maxLevel
    c4d.EventAdd()
