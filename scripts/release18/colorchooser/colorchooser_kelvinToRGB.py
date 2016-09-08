# This example calculates a RGB value from a light color and applies it to the given "Light" object.

import c4d
from c4d import gui
from c4d.modules import colorchooser as cc

def main():
    #Retrieves active object
    if op is None:
        return

    # Checks active object is a light
    if not op.IsInstanceOf(c4d.Olight):
        return

    # Initializes Kelvin temperature
    kelvin = 2600.0 # Light bulb
    # Converts Kelvin temperature to RGB color
    rgb = cc.ColorKelvinTemperatureToRGB(kelvin)
    # Sets the result RGB color as the light object's color
    op.SetParameter(c4d.LIGHT_COLOR, rgb, c4d.DESCFLAGS_SET_0)

    c4d.EventAdd()

if __name__=='__main__':
    main()
