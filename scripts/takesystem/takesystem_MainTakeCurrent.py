import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    # This example checks if the current Take is the main take. If not, the main take becomes the current take.
    
    takeData = doc.GetTakeData()
    
    if takeData is None:
        return
    
    currentTake = takeData.GetCurrentTake()
    
    if currentTake.IsMain() == False:
        mainTake = takeData.GetMainTake()
        takeData.SetCurrentTake(mainTake)
        
        c4d.EventAdd()

if __name__=='__main__':
    main()
