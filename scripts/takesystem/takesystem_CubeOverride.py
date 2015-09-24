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
    
    cube = doc.GetActiveObject()
    if cube is None:
        return
    
    if cube.GetType() != c4d.Ocube:
        return
    
    # This example adds an override to the current take for the object (that must be a cube) and changes the "Size" parameter.
    
    ID = c4d.DescID(c4d.DescLevel(c4d.PRIM_CUBE_LEN, c4d.DTYPE_VECTOR, 0), c4d.DescLevel(c4d.VECTOR_X, c4d.DTYPE_REAL, 0))
    newValue = 300.0
    
    overrideNode = take.FindOrAddOverrideParam(takeData, cube, ID, newValue)
    
    if overrideNode is not None:
        overrideNode.UpdateSceneNode(takeData, ID)
        c4d.EventAdd()
    
    
 
    

if __name__=='__main__':
    main()