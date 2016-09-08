# This example loops through the graphs of the given substance asset
# The graph is then used to loop through the inputs and outputs

import c4d
from c4d import modules


def main():
    # Retrieve first substance
    substance = modules.substance.GetFirstSubstance(doc)
    if substance is None:
        return

    # Loop through graphs
    graph, graphName = modules.substance.GetSubstanceGraph(substance) 
    while graph is not None:

        print("Graph Name: " + graphName)

        # Loop through inputs
        input, inputUid, firstId, numElements, inputType, inputName = modules.substance.GetSubstanceInput(substance, graph)
        while input is not None:
            print("Input: " + inputName)
            input, inputUid, firstId, numElements, inputType, inputName = modules.substance.GetSubstanceInput(substance, graph, input)

        # Loop through outputs
        output, outputUid, outputType, outputName, outputBmp = modules.substance.GetSubstanceOutput(substance, graph, True)
        while output is not None:
            print("Output: " + outputName)
            output, outputUid, outputType, outputName, outputBmp = modules.substance.GetSubstanceOutput(substance, graph, True, output) 

        graph, graphName = modules.substance.GetSubstanceGraph(substance, graph)


if __name__=='__main__':
    main()
