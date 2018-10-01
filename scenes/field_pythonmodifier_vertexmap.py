# Code used for the Python modifier layer of the vertex map in field_pythonmodifier_vertexmap.c4d

import c4d
from c4d.modules import mograph as mo


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

    # Makes sure to only sample value
    if info._flags == c4d.FIELDSAMPLE_FLAG_VALUE:

        # Gets the current tag
        callerStack = info._callerStack
        if not callerStack.GetCount() and not callerStack[0].CheckType(c4d.Tvertexmap):
            return True

        # Gets the vertex color host on the same object
        obj = callerStack[0].GetObject()
        vertexColorTag = obj.GetTag(c4d.Tvertexcolor)
        if not vertexColorTag and not vertexColorTag.CheckType(c4d.Tvertexcolor):
            return True

        # Reads data from the vertex color map
        readData = vertexColorTag.GetDataAddressR()

         # Initializes luminances list for the sampling output values
        luminances = [0.0] * inputs._fullArraySize

        # Since sampling is called in a threading context, each call gets a different block of data:
        # inputs._blockOffset is equal to the start offset of the block of data
        # inputs._blockCount is equal to the length of the data within the block of data
        for index, pointId in enumerate(xrange(inputs._blockOffset, inputs._blockOffset + inputs._blockCount)):

            # Reads the color of the tag at the current pointId
            point = c4d.VertexColorTag.GetPoint(readData, None, None, pointId)

            # Gets the luminance from the color
            color = c4d.Vector(point.x, point.y, point.z)
            luminances[index] = c4d.utils.RGBToHSL(color).z

        # Sets list filled with all luminance values to the final output of the Python field
        outputs._value = luminances

    # Makes sure all sampled points are active
    outputs.ClearDeactivated(False)

    return True