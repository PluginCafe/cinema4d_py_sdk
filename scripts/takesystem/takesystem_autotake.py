import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    if op is None:
        return
    
    if op.GetType() != c4d.Osphere:
        return
    
    # This example edits the given sphere object
    # If auto take is enabled, the current take is used.
    
    undoObject = op.GetClone(c4d.COPYFLAGS_0)
    
    op.SetParameter(c4d.DescID(c4d.DescLevel(c4d.PRIM_SPHERE_RAD)), 100.0, c4d.DESCFLAGS_SET_0)
    
    takeData = doc.GetTakeData()
    if takeData is not None and takeData.GetTakeMode() == c4d.TAKE_MODE_AUTO:
        
        currentTake = takeData.GetCurrentTake()
        
        if currentTake is not None:
            currentTake.AutoTake(takeData, op, undoObject)
    
 
    c4d.EventAdd()

if __name__=='__main__':
    main()