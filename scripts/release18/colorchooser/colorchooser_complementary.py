# This example reads the color value from the active material.
# The complementary color is calculated and applied to a new material.

import c4d
from c4d.modules import colorchooser as cc

def main():
    # Retrieves active material
    mat = doc.GetActiveMaterial()
    if mat is None:
        return

    # Checks active material is a standard material
    if not mat.IsInstanceOf(c4d.Mmaterial):
        return
    
    # The active material's color
    color = mat.GetParameter(c4d.MATERIAL_COLOR_COLOR, c4d.DESCFLAGS_GET_0)
    if color is None:
        return

    # Calculates the complementary color
    res = cc.ColorHarmonyGetComplementary(color, False)
    # Retrieves the complementary color
    complementaryColor = res[1]
    
    # Creates a new material with complementary color
    complementaryMat = c4d.BaseMaterial(c4d.Mmaterial)
    if complementaryMat is None:
        return

    # Sets the complementary color as material's color
    complementaryMat.SetParameter(c4d.MATERIAL_COLOR_COLOR, complementaryColor, c4d.DESCFLAGS_SET_0)
    #Inserts the material with complementary color into the active document
    doc.InsertMaterial(complementaryMat)
    
    c4d.EventAdd()

if __name__=='__main__':
    main()
