import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    takeData = doc.GetTakeData()
    if takeData is None:
        return
    
    # This code creates a new take for each currently selected camera object.
    # get the currently selected objects
    
    selectedObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    
    for element in selectedObjects:
        
        if element.GetType() == c4d.Ocamera:
            
            cameraTake = takeData.AddTake("Take for Camera " + element.GetName(), None, None)
            
            if cameraTake is not None:
                cameraTake.SetCamera(takeData, element)
    
    c4d.EventAdd()

if __name__=='__main__':
    main()
