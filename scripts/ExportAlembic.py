"""
Export Settings Example

This example shows how to change an exporter settings.
This works also for importers/scene loaders.
"""

import c4d
from c4d import documents, plugins, storage

def main():
    # Get Alembic export plugin, 1028082 is its ID
    plug = plugins.FindPlugin(1028082, c4d.PLUGINTYPE_SCENESAVER)
    if plug is None:
        return
    
    # Get a path to save the exported file
    filePath = storage.LoadDialog(title="Save File for Alembic Export", flags=c4d.FILESELECT_SAVE, force_suffix="abc")
    if filePath is None:
        return
    
    op = {}
    # Send MSG_RETRIEVEPRIVATEDATA to Alembic export plugin
    if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):
        print op
        if "imexporter" not in op:
            return
        
        # BaseList2D object stored in "imexporter" key hold the settings
        abcExport = op["imexporter"]
        if abcExport is None:
            return
        
        # Change Alembic export settings
        abcExport[c4d.ABCEXPORT_SELECTION_ONLY] = True
        abcExport[c4d.ABCEXPORT_PARTICLES] = True
        abcExport[c4d.ABCEXPORT_PARTICLE_GEOMETRY] = True
        
        # Finally export the document
        if documents.SaveDocument(doc, filePath, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, 1028082):
            print "Document successfully exported to:"
            print filePath
        else:
            print "Export failed!"


if __name__=='__main__':
    main()
