"""
ColorSwatch Create Materials

Example:
c4d.modules.colorchooser.SwatchData
c4d.modules.colorchooser.SwatchGroup
maxon.ColorA

Reads all the colors from the first swatch group in the active document and creates a material for each one.
"""

import c4d
from c4d.modules import colorchooser

def main():

    # Creates a swatch data
    swatchData = colorchooser.ColorSwatchData()
    if swatchData is None:
        return

    # Loads the swatches data from the active document
    swatchData.Load(doc)

    # Makes sure the document contains at least a swatch group
    if swatchData.GetGroupCount(c4d.SWATCH_CATEGORY_DOCUMENT) == 0:
        return

    # Retrieves the first swatch group
    group = swatchData.GetGroupAtIndex(0, c4d.SWATCH_CATEGORY_DOCUMENT)
    if group is not None:
        groupName = group.GetName()
        colorCount = group.GetColorCount()
        for colorIndex in xrange(colorCount):
            # Gets the current color
            color = group.GetColor(colorIndex)[0]

            # Creates a material for the current color
            mat = c4d.BaseMaterial(c4d.Mmaterial)
            # Sets the name with the group name and color index
            mat.SetName(groupName + str(colorIndex))

            # Converts maxon.ColorA to c4d.Vector to set the material color
            mat[c4d.MATERIAL_COLOR_COLOR] = c4d.Vector(color.r, color.g, color.b)

            # Inserts the material into the active document
            doc.InsertMaterial(mat)

    # Updates Cinema 4D
    c4d.EventAdd()

if __name__=='__main__':
    main()