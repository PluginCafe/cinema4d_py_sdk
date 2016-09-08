# This example shows how to call GeGetMoDataSelection()

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

    # Retrieves MoGraph Selection Tag from the cloner
    tag = op.GetTag(c4d.Tmgselection)
    if tag is None:
        print "Please select a MoGraph Cloner Object with a MoGraph Selection Tag"
        return

    # Retrieves the clones selection
    selection = mograph.GeGetMoDataSelection(tag)

    # Retrieves selection list
    count = op[c4d.MG_LINEAR_COUNT]

    # Retrieves selected clones indices
    indices = []
    for index in xrange(count):
        if selection.IsSelected(index):
            indices.append(index)

    print "Clones selection indices:", indices


if __name__=='__main__':
    main()
