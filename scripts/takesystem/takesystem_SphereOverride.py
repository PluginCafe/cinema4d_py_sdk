import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    takeData = doc.GetTakeData()
    if takeData is None:
        return
    
    take = takeData.GetCurrentTake()
    if take.IsMain():
        return
    
    obj = doc.GetActiveObject()
    if obj is None:
        return
    
    # This example checks if the given take contains an override for the given sphere object.
    # If so, it is checked if the "Radius" parameter is overridden.
    # In this case, the value is increased and the node updated.
    
    if obj.GetType() != c4d.Osphere:
        return
    
    baseOverride = take.FindOverride(takeData, obj)
    
    if baseOverride is None:
        return
    
    ID = c4d.DescID(c4d.DescLevel(c4d.PRIM_SPHERE_RAD, c4d.DTYPE_REAL, 0))
    
    if baseOverride.IsOverriddenParam(ID):
        
        data = baseOverride.GetParameter(ID, c4d.DESCFLAGS_GET_0) 
        data = data + 10.0   
        baseOverride.SetParameter(ID, data, c4d.DESCFLAGS_SET_0)
        
        baseOverride.UpdateSceneNode(takeData, ID)  
        c4d.EventAdd()
    
    
    

if __name__=='__main__':
    main()