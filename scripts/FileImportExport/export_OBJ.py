import c4d
from c4d import documents, plugins, storage

#Author: Joey Gaspe
#OBJ export settings example

def main():

    # Get OBJ export plugin, 1030178 is its ID
    plug = plugins.FindPlugin(1030178, c4d.PLUGINTYPE_SCENESAVER)
    if plug is None:
        return

    # Get a path to save the exported file
    filePath = c4d.storage.LoadDialog(title="Save File for OBJ Export", flags=c4d.FILESELECT_SAVE, force_suffix="obj")

    if filePath is None:
        return

    op = {}
    # Send MSG_RETRIEVEPRIVATEDATA to OBJ export plugin
    if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):
        print op
        if "imexporter" not in op:
            return

        # BaseList2D object stored in "imexporter" key hold the settings
        objExport = op["imexporter"]
        if objExport is None:
            return

        # Define the settings
        # Example of OBJ export settings from the UI:
        objExport[c4d.OBJEXPORTOPTIONS_TEXTURECOORDINATES] = True
        objExport[c4d.OBJEXPORTOPTIONS_MATERIAL] = c4d.OBJEXPORTOPTIONS_MATERIAL_MATERIAL

        # objExport[c4d.] =

        # export without dialogs
        if c4d.documents.SaveDocument(doc, filePath, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, 1030178):
            print "Document successfully exported to:"
            print filePath
        else:
            print "Export failed!"

        c4d.EventAdd()

if __name__=='__main__':
    main()
