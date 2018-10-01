"""
ColorSwatch Rainbow Group

Example:
c4d.modules.colorchooser.SwatchData
c4d.modules.colorchooser.SwatchGroup
maxon.ColorA

Creates a swatch group and adds rainbow colors to it.
"""

import c4d
from c4d.modules import colorchooser
import maxon

def main():

    # Creates a swatch data
    swatchData = colorchooser.ColorSwatchData()
    if swatchData is None:
      return

    # Loads the swatch data from the active document
    swatchData.Load(doc)

    # Creates a swatch group
    group = swatchData.AddGroup(c4d.SWATCH_CATEGORY_DOCUMENT, "Rainbow")
    if group is not None:
      for i in xrange(20):

        # Creates rainbow colors and stores them in the previously created group
        hsv = c4d.Vector(float(i) * 0.05, 1.0, 1.0)
        rgb = c4d.utils.HSVToRGB(hsv)

        # Creates a maxon.ColorA for the current color
        col4 = maxon.ColorA()
        col4.r = rgb.x
        col4.g = rgb.y
        col4.b = rgb.z
        col4.a = 1.0
        group.AddColor(col4)

      # Inserts the swatch group
      index = swatchData.GetGroupCount(c4d.SWATCH_CATEGORY_DOCUMENT) - 1
      swatchData.SetGroupAtIndex(index, group)

      # Saves the group into the active document
      swatchData.Save(doc)

    # Updates Cinema 4D
    c4d.EventAdd()

if __name__=='__main__':
    main()