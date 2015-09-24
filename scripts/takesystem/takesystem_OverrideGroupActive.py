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
    
    # This example loops through all override groups and checks which groups are currently selected
    
    overrideGroups = take.GetOverrideGroups()
    
    for group in overrideGroups:
        
        print("Group "+group.GetName())
        if group.GetBit(c4d.BIT_ACTIVE):
            print("This group is active")
    

if __name__=='__main__':
    main()
