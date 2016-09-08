# This example shows how to get and set vertex colors in Polygon mode
# This simple script sets all vertex colors to red
# Note only RGB vertex colors are supported by this script

import c4d
from c4d import VertexColorTag


def main():
    # Checks if there is an active object
    if op is None: return

    # Retrieves Vertex Color Tag
    tag = op.GetTag(c4d.Tvertexcolor)
    if tag is None: return

    # Checks in Point mode
    if tag.IsPerPointColor():
        # If not changes to Polygon mode
        tag.SetPerPointMode(False)

    # Obtains Vertex Colors data address
    addr = tag.GetDataAddressW()

    # Initializes red color and Vertex Colors polygon
    red = c4d.Vector4d(1, 0, 0, 0)
    poly = {}
    poly['a'] = red
    poly['b'] = red
    poly['c'] = red
    poly['d'] = red

    # GetDataCount() returns the number of polygons in Polygon mode
    count = tag.GetDataCount()
    for idx in xrange(count):
        # Sets Vertex Colors red
        VertexColorTag.SetPolygon(addr, idx, poly)

    c4d.EventAdd()


if __name__=='__main__':
        main()
