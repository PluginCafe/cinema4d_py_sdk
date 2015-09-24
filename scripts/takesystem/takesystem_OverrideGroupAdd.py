import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    takeData = doc.GetTakeData()
    if takeData is None:
        return
    
    take = takeData.GetCurrentTake()
    if take is None:
        return
    
    group = take.GetFirstOverrideGroup()
    if group is None:
        return
    
    # This example adds the currently selected objects to the BaseOverrideGroup "group".

    objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    
    for obj in objects:
        
        group.AddToGroup(takeData, obj)
        
    c4d.EventAdd()
    

if __name__=='__main__':
    main()