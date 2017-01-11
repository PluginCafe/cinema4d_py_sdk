# This example sets a weight of 1.0 for all clones of the active Cloner object

import c4d
from c4d.modules import mograph

def main():
    # Aborts if no active object or if it is not a Cloner
    if op is None or op.GetType() != 1018544:
        return
    
    # Builds list for clones weights values
    weights = [1.0]*op[c4d.MG_LINEAR_COUNT]
    
    # Sets clones weights values
    mograph.GeSetMoDataWeights(op, weights)
    
    c4d.EventAdd()


if __name__=='__main__':
    main()
