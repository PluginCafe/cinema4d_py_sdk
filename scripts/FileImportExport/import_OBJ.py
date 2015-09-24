import c4d
from c4d import documents, plugins, storage

#Author: Joey Gaspe
#OBJ import settings example

def main():

    # Get OBJ import plugin, 1030177 is its ID
    plug = plugins.FindPlugin(1030177, c4d.PLUGINTYPE_SCENELOADER)
    if plug is None:
        return

    # Get a path to load the imported file
    selectedFile = c4d.storage.LoadDialog(title="Load File for OBJ Import", type=c4d.FILESELECTTYPE_ANYTHING, force_suffix="obj")

    if selectedFile is None:
        return

    op = {}
    # Send MSG_RETRIEVEPRIVATEDATA to OBJ import plugin
    if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):
        print op
        if "imexporter" not in op:
            return

        # BaseList2D object stored in "imexporter" key hold the settings
        objImport = op["imexporter"]
        if objImport is None:
            return

        # Define the settings
        # Examples of OBJ import settings from the UI:
        objImport[c4d.OBJIMPORTOPTIONS_PHONG_ANGLE_DEFAULT] = 22.5
        objImport[c4d.OBJIMPORTOPTIONS_TEXTURECOORDINATES] = True
        objImport[c4d.OBJIMPORTOPTIONS_SPLITBY] = c4d.OBJIMPORTOPTIONS_SPLITBY_OBJECT
        objImport[c4d.OBJIMPORTOPTIONS_MATERIAL] = c4d.OBJIMPORTOPTIONS_MATERIAL_MTLFILE
        objImport[c4d.OBJIMPORTOPTIONS_POINTTRANSFORM_FLIPZ] = True

        # objImport[c4d.] = 

        # Import without dialogs
        c4d.documents.MergeDocument(doc, selectedFile, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS, None)

        c4d.EventAdd()

if __name__=='__main__':
    main()
