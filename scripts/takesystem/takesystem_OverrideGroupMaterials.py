import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    takeData = doc.GetTakeData()
    if takeData is None:
        return
    
    # This code creates a take with an override group for each selected material and adds the object "object" to the newly created group.
 
    obj = doc.GetActiveObject()
    if obj is None:
        return
    
    materials = doc.GetActiveMaterials()
    
    for material in materials:
        
        take = takeData.AddTake(material.GetName(), None, None)
        
        if take is not None:
            group = take.AddOverrideGroup()
            
            if group is not None:
                group.AddToGroup(takeData, obj)
                
                tag = group.AddTag(takeData, c4d.Ttexture, material)
                
                if tag is not None:
                    tag.SetParameter(c4d.TEXTURETAG_PROJECTION, c4d.TEXTURETAG_PROJECTION_UVW, c4d.DESCFLAGS_SET_0)
                    
    
    c4d.EventAdd()
 
    
    
    

if __name__=='__main__':
    main()