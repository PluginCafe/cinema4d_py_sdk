"""
Volume Command Create Sphere Volume

Example:
c4d.modules.volume.SendVolumeCommand()
c4d.VOLUMECOMMANDTYPE_CREATESPHEREVOLUME

Creates a sphere volume with the corresponding command.
"""

import c4d
from c4d.modules import volume

def main():

    # Configures settings for sphere volume command
    settings = c4d.BaseContainer()
    settings[c4d.CREATESPHEREVOLUMESETTINGS_RADIUS] = 100.0
    settings[c4d.CREATESPHEREVOLUMESETTINGS_POSITION] = c4d.Vector(0, 100, 0)
    settings[c4d.CREATESPHEREVOLUMESETTINGS_BANDWIDTH] = 2
    settings[c4d.CREATESPHEREVOLUMESETTINGS_GRIDSIZE] = 1.0

    # Creates sphere volume
    result = volume.SendVolumeCommand(c4d.VOLUMECOMMANDTYPE_CREATESPHEREVOLUME, [], settings, doc)

    # Checks command result is a list
    if type(result) != list:
        return

    if len(result) != 1:
        return

    # Gets the sphere volume result
    volumeObject = result[0]

    # Inserts the object into the active document
    doc.InsertObject(volumeObject)
    doc.SetActiveObject(volumeObject)

    # Updates Cinema 4D
    c4d.EventAdd()


# Execute main()
if __name__=='__main__':
    main()