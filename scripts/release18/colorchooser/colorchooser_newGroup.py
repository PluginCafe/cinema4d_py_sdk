# This example adds a new color group to the active document.

import c4d
from c4d.modules import colorchooser as cc

def main():
    # Creates a new ColorSwatchData
    swatchData = cc.ColorSwatchData(doc)
    if swatchData is None:
        return

    # Adds a group to the newly created ColorSwatchData
    group = swatchData.AddGroup("New Group", False)
    if group is None:
        return

    # Adds red, green and blue colors to the ColorSwatchGroup
    group.AddColor(c4d.Vector(1.0, 0.0, 0.0), True)   
    group.AddColor(c4d.Vector(0.0, 1.0, 0.0), False) 
    group.AddColor(c4d.Vector(0.0, 0.0, 1.0), False)

    # Assigns the new group
    swatchData.SetGroupAtIndex(swatchData.GetGroupCount() - 1, group)

    # Saves the color groups into the active document
    swatchData.Save(doc)

    c4d.EventAdd()

if __name__=='__main__':
    main()
