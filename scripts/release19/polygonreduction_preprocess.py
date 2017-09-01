 # This example configures the given PolygonReduction object and reduces the given PolygonObject to 25%.

import c4d
from c4d import utils

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

    # reduce
    polyReduction.SetReductionStrengthLevel(0.75)

    # update original PolygonObject
    polyObject.Message(c4d.MSG_UPDATE)
    c4d.EventAdd()

if __name__=='__main__':
    main()
