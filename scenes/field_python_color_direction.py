# Code used for the Python field in field_python_color_direction.c4d

import c4d
import c4d
import random

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

    # Samples color
    if info._flags & c4d.FIELDSAMPLE_FLAG_COLOR  or info._flags & c4d.FIELDSAMPLE_FLAG_ALL:
        if len(outputs._color):
            for index in xrange(0, inputs._blockCount):
                random.seed(index)
                outputs.SetValue(index, random.random())

    # Samples direction
    if info._flags & c4d.FIELDSAMPLE_FLAG_DIRECTION or info._flags & c4d.FIELDSAMPLE_FLAG_ALL:
        if len(outputs._direction):
            for index in xrange(0, inputs._blockCount):
                outputs.SetValue(index, 1)
                pos = inputs._position[index]
                targetPos = Curl3D(pos)
                direction = c4d.Vector(targetPos - pos)
                outputs.SetDirection(index, c4d.Vector(direction))

    return True

# Calculates a 3D curl Noise according the given position
def Curl3D(pos):

    x = pos.x
    y = pos.y
    z = pos.z
    eps = 100.0

    n1 = c4d.utils.noise.Noise(c4d.Vector(x, y + eps, z))
    n2 = c4d.utils.noise.Noise(c4d.Vector(x, y - eps, z))
    a = (n1 - n2) / (2 * eps)

    n1 = c4d.utils.noise.Noise(c4d.Vector(x, y, z + eps))
    n2 = c4d.utils.noise.Noise(c4d.Vector(x, y, z - eps))
    b = (n1 - n2) / (2 * eps)
    curl_x = a - b

    a = b
    n1 = c4d.utils.noise.Noise(c4d.Vector(x + eps, y, z))
    n2 = c4d.utils.noise.Noise(c4d.Vector(x - eps, y, z))
    b = (n1 - n2) / (2 * eps)
    curl_y = a - b

    a = b
    n1 = c4d.utils.noise.Noise(c4d.Vector(x + eps, y, z + eps))
    n2 = c4d.utils.noise.Noise(c4d.Vector(x - eps, y, z - eps))
    b = (n1 - n2) / (2 * eps)
    curl_z = a - b

    return c4d.Vector(curl_x, curl_y, curl_z)