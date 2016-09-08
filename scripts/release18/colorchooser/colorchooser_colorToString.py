# This example reads the color parameter of the given material and prints the value as RGB and HSV.

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

    # Retrieves the material's color
    color = mat.GetParameter(c4d.MATERIAL_COLOR_COLOR, c4d.DESCFLAGS_GET_0)
    if color is None:
        return

    # Outputs the material's color in RGB and HSV formats
    print("Material Color: RGB " + cc.ColorRGBToString(color) + " - HSV " + cc.ColorHSVToString(color))

if __name__=='__main__':
    main()
