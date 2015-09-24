import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    material = doc.GetActiveMaterial()
    if material is None:
        return
    
    takeData = doc.GetTakeData()
    if takeData is None:
        return
    
    # This example searches for the BaseOverride of the given material and its color parameter.
    # If found, the color value is applied to the backup value to transfer the state of this take to the backup take (which might be the main take).
    
    take = takeData.GetCurrentTake()
    if take.IsMain():
        return
    
    baseOverride = take.FindOverride(takeData, material)
    
    if baseOverride is not None:
        
        id = c4d.DescID(c4d.DescLevel(c4d.MATERIAL_COLOR_COLOR, c4d.DTYPE_COLOR, 0))
        
        res = takeData.FindOverrideCounterPart(baseOverride, id)
        
        backup = res[0]
        result = res[1]
        
        if backup is not None:
            
            data = baseOverride.GetParameter(id, c4d.DESCFLAGS_GET_0)
            
            backup.SetParameter(id, data, c4d.DESCFLAGS_SET_0)
            backup.UpdateSceneNode(takeData, id)
            
            c4d.EventAdd()
        
  
  

if __name__=='__main__':
    main()