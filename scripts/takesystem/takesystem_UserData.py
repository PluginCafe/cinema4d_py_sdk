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
    
    # This example adds a new boolean userdata parameter to the given BaseTake.
    
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BOOL)
    bc[c4d.DESC_NAME] = "Enable"
    
    userData = take.AddUserData(bc) 
    take.SetParameter(userData, True, c4d.DESCFLAGS_SET_0)
        
    c4d.EventAdd()
    

if __name__=='__main__':
    main()