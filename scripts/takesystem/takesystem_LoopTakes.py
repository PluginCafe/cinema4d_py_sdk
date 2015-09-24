import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    takeData = doc.GetTakeData()  
    if takeData is None:
        return
    
    # This example loops through all takes that are direct child takes of the main take.
    
    mainTake = takeData.GetMainTake()
    take = mainTake.GetDown()
    
    while take is not None:
        
        print("Take Name: %s." % take.GetName())
        
        take = take.GetNext()

if __name__=='__main__':
    main()
