# This example configures the active LOD object to use "Manual Groups".
# The selected objects referenced in the objects list are moved under the LOD object and are referenced in each group.
# Use "Manual Groups" and a manually defined number of groups.

import c4d

def main():

    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    if len(activeObjects) <= 1:
        return

    lodObject = doc.GetTargetObject()
    if lodObject.GetType() != c4d.Olod:
        return

    lodObject[c4d.LOD_MODE] = c4d.LOD_MODE_MANUAL_GROUPS
    lodObject[c4d.LOD_CRITERIA] = c4d.LOD_CRITERIA_MANUAL
    lodObject[c4d.LOD_LEVEL_COUNT_DYN] = len(activeObjects) - 1
  
    for level, object in enumerate(activeObjects):
  
        if object == lodObject:
            continue

        # make object a child object of the LOD object
        object.Remove()
        doc.InsertObject(object, lodObject)

        # insert object into "Objects" list of the given level

        listID = lodObject.GetManualModeObjectListDescID(level)
        if listID is not None:
            # create InEx data
            inExData = c4d.InExcludeData()
            if inExData is not None:
                # insert object into list
                inExData.InsertObject(object, 1)
                # set parameter
                lodObject[listID] = inExData

    c4d.EventAdd()

if __name__=='__main__':
    main()
