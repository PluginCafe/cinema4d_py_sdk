# This example loads the swatches of the given BaseDocument and stores them as a preset.
# Note: The ColorSwatchData of the active document must contain some colors.

import c4d
from c4d.modules import colorchooser as cc

def main():
    # Creates a new ColorSwatchData
    swatchData = cc.ColorSwatchData()
    if swatchData is None:
        return

    # Loads color groups from the active document
    if not swatchData.Load(doc):
        return

    # Builds preset URL
    url = cc.GetColorSwatchPresetDirectory()
    url = url + "/newColorPreset"

    # Saves color swatches preset
    if swatchData.SavePresetByURL(url, "User", "This is my preset"):
        print "Color swatch preset saved successfully"
    else:
        print "Color swatch preset could not be saved!"
    
    c4d.EventAdd()

if __name__=='__main__':
    main()
