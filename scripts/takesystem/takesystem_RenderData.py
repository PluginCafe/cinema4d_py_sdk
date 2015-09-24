import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    takeData = doc.GetTakeData()
    if takeData is None:
        return
    
    
    # This code gets the first RenderData and loops through all RenderData objects in that list.
    # This won't loop through all RenderData elements since it ignores the child objects of these elements.
    
    renderData = doc.GetFirstRenderData()
    
    while renderData is not None:
        
        renderDataTake = takeData.AddTake("Take for RenderData " + renderData.GetName(), None, None)
        
        if renderDataTake is not None:
            renderDataTake.SetRenderData(takeData, renderData)
        
        renderData = renderData.GetNext()
        
    c4d.EventAdd()
    

if __name__=='__main__':
    main()
