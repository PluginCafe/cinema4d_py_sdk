import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    takeData = doc.GetTakeData()
    if takeData is None:
        return
    
    # This code adds the currently selected objects to a new group in the current take.
    # The objects of this group will only be visible in the renderer but not in the editor.
    
    objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    
    take = takeData.GetCurrentTake()
    if take is None:
        return
    
    group = take.AddOverrideGroup()
    
    if group is not None:
        group.SetName("Render Objects")
        group.SetEditorMode(c4d.MODE_OFF)
        group.SetRenderMode(c4d.MODE_ON)
        
        for obj in objects:
            group.AddToGroup(takeData, obj)
        
    c4d.EventAdd()
    

if __name__=='__main__':
    main()