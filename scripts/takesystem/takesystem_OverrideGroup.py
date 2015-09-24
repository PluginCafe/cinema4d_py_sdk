import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    takeData = doc.GetTakeData()  
    if takeData is None:
        return
    
    #This code adds a new take and creates a new override group for all selected objects.
    # If a material with the name "Green" exists a texture tag referencing that material is added to the override group.
    
    selectedObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    
    mat = doc.SearchMaterial("Green")
    take = takeData.AddTake("Green Objects", None, None)
    
    if take is not None:
        group = take.AddOverrideGroup()
        group.SetName("Green Material")
        
        if mat is not None:
            group.AddTag(takeData, c4d.Ttexture, mat)
            
        for element in selectedObjects:
            group.AddToGroup(takeData, element)      
        
    c4d.EventAdd()   

if __name__=='__main__':
    main()
