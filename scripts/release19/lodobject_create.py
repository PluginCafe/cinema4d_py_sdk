# This example creates a new LOD object and adds it to the active BaseDocument

import c4d

lodObject = c4d.LodObject()
lodObject.SetName("New LOD Object")
doc.InsertObject(lodObject)
c4d.EventAdd()
