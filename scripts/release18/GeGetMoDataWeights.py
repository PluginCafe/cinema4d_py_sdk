# This example shows how to call GeGetMoDataWeights()

import c4d
from c4d.modules import mograph


def main():
    # Checks if there is an active object
    if op is None:
        print "Please select a MoGraph Cloner Object"
        return

    # Checks if the active object is a MoGraph Cloner Object
    if op.GetType() != 1018544:
        print "Please select a MoGraph Cloner Object"
        return

    # Retrieves MoGraph Weight Tag from the cloner
    tag = op.GetTag(c4d.Tmgweight)
    if tag is None:
        print "Please select a MoGraph Cloner Object with a MoGraph Weight Tag"
        return

    # Retrieves the clones weight values
    weights = mograph.GeGetMoDataWeights(tag)

    # Prints clones weights
    print "'" + op.GetName() + "'", "Clones Weights:"
    count = len(weights)
    for index in weights:
        print index, ":", weights[index]


if __name__=='__main__':
    main()
