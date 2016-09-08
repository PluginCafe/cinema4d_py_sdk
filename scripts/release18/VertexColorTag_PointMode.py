# This example shows how to get and set Vertex Colors in Point mode
# This simple script changes all black Vertex Colors to red
# Note only RGB vertex colors are supported by this script

import c4d
from c4d import VertexColorTag


def main():
    # Checks if there is an active object
    if op is None: return

    # Retrieves the Vertex Color Tag
    tag = op.GetTag(c4d.Tvertexcolor)
    if tag is None: return

    # Checks in Point mode
    if not tag.IsPerPointColor():
        # If not changes to Point mode
        tag.SetPerPointMode(True)

    # Obtains vertex colors data R/W addresses
    addrR = tag.GetDataAddressR()
    addrW = tag.GetDataAddressW()

    # Initializes black and red colors
    black = c4d.Vector4d(0, 0, 0, 0)
    red = c4d.Vector4d(1, 0, 0, 0)

    # By default the Vertex Color Tag is in Point mode
    # So GetDataCount() returns the number of points
    count = tag.GetDataCount()
    for idx in xrange(count):
        # If point color is black then changes it to red
        point = VertexColorTag.GetPoint(addrR, None, None, idx)
        if point == black:
            VertexColorTag.SetPoint(addrW, None, None, idx, red)

    c4d.EventAdd()


if __name__=='__main__':
    main()
