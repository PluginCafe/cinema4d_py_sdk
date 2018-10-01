"""
Volume Command Spline To Volume

Example:
c4d.modules.volume.SendVolumeCommand
c4d.VOLUMECOMMANDTYPE_SPLINETOVOLUME

Creates a volume from the selected spline object.
"""

import c4d
from c4d.modules import volume

def main():

    # Checks if selected object is valid
    if op is None:
        return

    # Checks if the selected object is a spline object
    if not op.IsInstanceOf(c4d.Ospline):
        return

    # Initializes an object list and adds the spline
    objects = []
    objects.append(op)

    # Configures settings to create the spline volume
    settings = c4d.BaseContainer()
    settings[c4d.SPLINETOVOLUMESETTINGS_GRIDSIZE] = 1.0
    settings[c4d.SPLINETOVOLUMESETTINGS_BANDWIDTH] = 3
    settings[c4d.SPLINETOVOLUMESETTINGS_RADIUS] = 1.0
    settings[c4d.SPLINETOVOLUMESETTINGS_DENSITY] = 1.0

    # Creates spline volume
    result = c4d.modules.volume.SendVolumeCommand(c4d.VOLUMECOMMANDTYPE_SPLINETOVOLUME, objects, settings, doc)

    # Checks command result is a list
    if type(result) != list:
        return

    if len(result) != 1:
        return

    # Gets the spline to volume result
    volumeObject = result[0]

    # Inserts the object into the active document
    doc.InsertObject(volumeObject)
    doc.SetActiveObject(volumeObject)

    # Updates Cinema 4D
    c4d.EventAdd()

if __name__=='__main__':
    main()