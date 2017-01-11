# This example selects all clones of the active Cloner object

import c4d
from c4d.modules import mograph

def main():
    # Aborts if no active object or if it is not a Cloner
    if op is None or op.GetType() != 1018544:
        return
    
    # Builds list for clones selection states
    states = [1]*op[c4d.MG_LINEAR_COUNT]
    
    # Creates new BaseSelect and sets it to states list
    selection = c4d.BaseSelect()
    selection.SetAll(states)
    
    # Sets clones selection states
    mograph.GeSetMoDataSelection(op, selection)
    
    c4d.EventAdd()


if __name__=='__main__':
    main()
