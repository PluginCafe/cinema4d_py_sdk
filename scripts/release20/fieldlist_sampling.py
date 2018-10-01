"""
FieldList Sampling

Example:
c4d.FieldList
c4d.modules.mograph.FieldLayer
c4d.modules.mograph.FieldInput
c4d.modules.mograph.FieldOutput

Samples multiple fields with c4d.FieldList custom data and stores the result into a vertex color tag.
"""

import c4d
from c4d.modules import mograph

def main():

    # Checks if active object is valid
    if op is None:
        return

    # Checks if active object is a polygon object
    if not op.CheckType(c4d.Opolygon):
        return

    # Retrieves the vertex color tag on the polygon object
    pointCount = op.GetPointCount()
    vertexColor = op.GetTag(c4d.Tvertexcolor)
    if not vertexColor:
        # Creates vertex color tag if it does not exist
        vertexColor = c4d.VertexColorTag(pointCount)
        op.InsertTag(vertexColor)

    # Creates linear field and adds it to the active document
    linearField = c4d.BaseObject(c4d.Flinear)
    doc.InsertObject(linearField)

    # Creates random field and adds it to the active document
    randomField = c4d.BaseObject(c4d.Frandom)
    doc.InsertObject(randomField)

    # Creates layer for linear field and sets link
    linearFieldLayer = mograph.FieldLayer(c4d.FLfield)
    linearFieldLayer.SetLinkedObject(linearField)

    # Creates layer for random field and sets link
    randomFieldLayer = mograph.FieldLayer(c4d.FLfield)
    randomFieldLayer.SetLinkedObject(randomField)

    # Creates a field list
    fields = c4d.FieldList()
    
    # Adds layers to the field list
    fields.InsertLayer(linearFieldLayer)
    fields.InsertLayer(randomFieldLayer)

    # Prepares field input with the points to sample
    input = mograph.FieldInput(op.GetAllPoints(), pointCount)

    # Sample all the points of the polygon object
    output = fields.SampleListSimple(op, input, c4d.FIELDSAMPLE_FLAG_VALUE)

    # Writes field output values to the vertex color data
    writeData = vertexColor.GetDataAddressW()
    for pointIndex in xrange(pointCount):
        vertexColor.SetColor(writeData, None, None, pointIndex, c4d.Vector(output._value[pointIndex]))

    # Removes fields from the document
    linearField.Remove()
    randomField.Remove()

    # Updates Cinema 4D
    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()