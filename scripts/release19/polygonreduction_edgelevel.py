# This example reduces the active PolygonObject to the given edge count.

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

    # ask for number of edges level
    while True:
        input = gui.InputDialog("Enter number of edges level:")
        if input == "":
            # operation was cancelled
            polyObject.Message(c4d.MSG_UPDATE)
            c4d.EventAdd()
            return
        # try to convert to integer
        try:
            edgesLevel = int(input)
            break
        except ValueError:
            gui.MessageDialog("Please enter a number.")

    # check entered number of edges level is less than the maximum edges level
    if edgesLevel > polyReduction.GetMaxRemainingEdgesLevel():
        polyObject.Message(c4d.MSG_UPDATE)
        c4d.EventAdd()
        return

    # set edges level number
    polyReduction.SetRemainingEdgesLevel(edgesLevel)

    # get number of edges level after reduction
    realEdgeResult = polyReduction.GetRemainingEdgesLevel()
    print "Edge Result: " + str(realEdgeResult)

    # update original PolygonObject
    polyObject.Message(c4d.MSG_UPDATE)
    c4d.EventAdd()

if __name__=='__main__':
    main()
