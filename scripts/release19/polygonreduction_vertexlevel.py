# This example reduces the active PolygonObject to the given vertex count.

import c4d
from c4d import gui, utils

def main():
    #get polygon object

    polyObject = doc.GetActiveObject()
    if polyObject is None:
        return

    if not polyObject.IsInstanceOf(c4d.Opolygon):
        return

    # settings for PolygonReduction.PreProcess()
    settings = c4d.BaseContainer()
    settings[c4d.POLYREDUXOBJECT_PRESERVE_3D_BOUNDARY] = True
    settings[c4d.POLYREDUXOBJECT_PRESERVE_UV_BOUNDARY] = True

    # data for PolygonReduction.PreProcess()
    data = {}
    data['_op'] = polyObject
    data['_doc'] = doc
    data['_settings'] = settings
    data['_thread'] = None # synchronous pre-processing and reduction

    # create PolygonReduction object
    polyReduction = utils.PolygonReduction()
    if polyReduction is None:
        return

    # pre process
    if not polyReduction.PreProcess(data):
      return

    # ask for number of vertex level
    while True:
        input = gui.InputDialog("Enter number of vertex level:")
        if input == "":
            # operation was cancelled
            polyObject.Message(c4d.MSG_UPDATE)
            c4d.EventAdd()
            return
        # try to convert to integer
        try:
            vertexLevel = int(input)
            break
        except ValueError:
            gui.MessageDialog("Please enter a number.")

    # check entered number of vertex level is valid
    if vertexLevel < polyReduction.GetMinVertexLevel():
        return
    if vertexLevel > polyReduction.GetMaxVertexLevel():
       return

    # set vertex level
    polyReduction.SetVertexLevel(vertexLevel)

    # get number of vertex level after reduction
    realVertexResult = polyReduction.GetVertexLevel()
    print "Vertex Result: " + str(realVertexResult)

    # update original PolygonObject
    polyObject.Message(c4d.MSG_UPDATE)
    c4d.EventAdd()

if __name__=='__main__':
    main()
