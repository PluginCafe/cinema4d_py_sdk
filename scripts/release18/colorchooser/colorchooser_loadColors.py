# This example loads a Cinema 4D scene file to get the stored color swatches.
# The loaded swatches are applied to the active document.

import os
import c4d
from c4d import storage
from c4d.modules import colorchooser as cc

def main():

    # Selects the c4d file to load
    filename = c4d.storage.LoadDialog(type=c4d.FILESELECTTYPE_SCENES, title="Choose File.", flags=c4d.FILESELECT_LOAD, force_suffix="c4d")
    if filename is None:
        return

    # Checks selected file is a c4d scene file
    name, suffix = os.path.splitext(filename)
    if suffix != ".c4d":
        return

    # Loads the document
    loadedDoc = c4d.documents.LoadDocument(filename, c4d.SCENEFILTER_0)
    if loadedDoc is None:
        return

    # Creates a new ColorSwatchData
    swatchData = cc.ColorSwatchData()
    if swatchData is None:
        return

    # Loads swatches from document
    swatchData.Load(loadedDoc)

    # Stores swatches into the active document
    swatchData.Save(doc)

    c4d.EventAdd()

if __name__=='__main__':
    main()
