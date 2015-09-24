import c4d
from c4d import documents, plugins, storage

#Author: Joey Gaspe
#SketchUp import settings example

def main():

    # Get SketchUp import plugin, 1033845 is its ID
    plug = plugins.FindPlugin(1033845, c4d.PLUGINTYPE_SCENELOADER)
    if plug is None:
        return

    # Get a path to load the imported file
    selectedFile = c4d.storage.LoadDialog(title="Load File for SketchUp Import", type=c4d.FILESELECTTYPE_ANYTHING, force_suffix="skp")

    if selectedFile is None:
        return

    op = {}
    # Send MSG_RETRIEVEPRIVATEDATA to SketchUp import plugin
    if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):
        print op
        if "imexporter" not in op:
            return

        # BaseList2D object stored in "imexporter" key hold the settings
        skpImport = op["imexporter"]
        if skpImport is None:
            return

        # Define the settings
        # Examples of SketchUp settings from the UI (either True or False):
        skpImport[c4d.SKPIMPORT_DAYLIGHT_SYSTEM_PHYSICAL_SKY] = True
        skpImport[c4d.SKPIMPORT_CAMERA] = True
        skpImport[c4d.SKPIMPORT_SKIP_HIDDEN_OBJECTS] = True
        skpImport[c4d.SKPIMPORT_SPLIT_OBJECTS_BY_LAYER] = True
        skpImport[c4d.SKPIMPORT_SHOW_STATISTICS_IN_CONSOLE] = True

        # Import without dialogs
        c4d.documents.MergeDocument(doc, selectedFile, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS, None)

        c4d.EventAdd()

if __name__=='__main__':
    main()
