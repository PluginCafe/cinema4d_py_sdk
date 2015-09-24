import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    # This snippet simply creates a new take and makes it the current one
    
    takeData = doc.GetTakeData()
    
    if takeData is None:
        return
    
    newTake = takeData.AddTake("this is a new take", None, None)
    if newTake is not None:
        takeData.SetCurrentTake(newTake)
        c4d.EventAdd()

if __name__=='__main__':
    main()
