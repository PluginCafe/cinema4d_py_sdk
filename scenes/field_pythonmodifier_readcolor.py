# Code used for the Python modifier field in field_pythonmodifier_readcolor.c4d

import c4d
import math

currentTimeRatio = 0.0

"""
Initializes sampling pass

Allocation and initializations should be performed here to speed up sampling
Return False on error to cancel sampling
InitSampling() function is not required. If it is not needed then remove it to increase performance

Arguments:
op: BaseObject: The Python field
info: FieldInfo: The sampling informations
"""
def InitSampling(op, info):

    # Multiply by 5 to play out fith
    global currentTimeRatio
    currentTimeRatio = doc.GetTime().Get() / doc.GetMaxTime().Get()
    currentTimeRatio = currentTimeRatio * 5

    return True

"""
 Calculates the output values for the specified input points

Allocations should be avoided in Sample() to maximize performance
Return False on error to cancel sampling
Sample() function is mandatory, Python field cannot function without it

Arguments:
op: BaseObject: The Python field
inputs: FieldInput: The points to sample
outputs: FieldOutput: The sampling output arrays
info: FieldInfo: The sampling informations
"""
def Sample(op, inputs, outputs, info):

    global currentTimeRatio

    # Loops over all items
    for index in xrange(inputs._blockCount):

        # Gets the current color
        colorValue = outputs.GetColor(index)

        # If the x component (Red) is egual to 1 then changes its strength to 1.0

        if colorValue.x == 1 and colorValue.y == 0 and colorValue.z == 0:
               outputs.SetValue(index, 1)

        # Otherwise makes a sinus of the strength

        else:
            if index % 2 == 0:
                value = math.sin(math.pi * currentTimeRatio)
                offsetValue = (value + 1.0) / 2.0
                outputs.SetValue(index, offsetValue)
            else:
                value = math.cos(math.pi * currentTimeRatio)
                offsetValue = (value + 1.0) / 2.0
                outputs.SetValue(index, offsetValue)

    return True