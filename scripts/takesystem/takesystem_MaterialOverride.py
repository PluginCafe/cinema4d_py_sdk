import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    takeData = doc.GetTakeData()
    if takeData is None:
        return
    
    # This example creates ten takes with different overrides of the material color.
    
    material = doc.GetActiveMaterial()
    if material is None:
        return
    
    if material.GetType() != c4d.Mmaterial:
        return
    
    for i in xrange(10):
        
        takeName = "Variation " + str(i)
        materialVariation = takeData.AddTake(takeName, None, None)
        
        if materialVariation is not None:
            
            materialColorParameter = c4d.DescID(c4d.DescLevel(c4d.MATERIAL_COLOR_COLOR, c4d.DTYPE_COLOR, 0))
            
            hsv = c4d.Vector(float(i) * 0.1, 1.0, 1.0)
            rgb = c4d.utils.HSVToRGB(hsv)
            
            overrideNode = materialVariation.FindOrAddOverrideParam(takeData, material,materialColorParameter, rgb)
            
            if overrideNode is not None:
                overrideNode.UpdateSceneNode(takeData, materialColorParameter )
                
    
    c4d.EventAdd()
    
 
    

if __name__=='__main__':
    main()