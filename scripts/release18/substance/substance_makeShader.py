# This example creates a new substance shader linked to the given substance asset
# The asset is scanned for a bump output channel that is used in that shader

import c4d
from c4d import modules

def main():
    # Retrieve active material
    mat = doc.GetActiveMaterial()
    if mat is None:
        return

    # Check active material is a standard material
    if mat.IsInstanceOf(c4d.Mmaterial) == False:
        return

    # Retrieve first substance
    substance = modules.substance.GetFirstSubstance(doc)
    if substance is None:
        return

    # Retrieve substance graph
    graph, graphName = modules.substance.GetSubstanceGraph(substance)
    if graph is None:
        return
    
    # Create a new substance shader
    shader = modules.substance.CreateSubstanceShader(substance)
    if shader is None:
        return

    # Insert shader into material and use it in bump channel
    mat.InsertShader(shader)
    mat[c4d.MATERIAL_BUMP_SHADER] = shader
    mat[c4d.MATERIAL_USE_BUMP] = True

    # Loop trough all output channels
    output, outputUid, outputType, outputName, outputBmp = modules.substance.GetSubstanceOutput(substance, graph, True) 
    while output is not None:
        if outputType == c4d.SUBSTANCE_OUTPUT_TYPE_BUMP: # Use ID of a bump output channel
            shader.SetParameter(c4d.SUBSTANCESHADER_CHANNEL, outputUid, c4d.DESCFLAGS_SET_0)
        output, outputUid, outputType, outputName, outputBmp = modules.substance.GetSubstanceOutput(substance, graph, True, output) 

    c4d.EventAdd()


if __name__=='__main__':
    main()
