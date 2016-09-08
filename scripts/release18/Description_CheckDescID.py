# This example shows how to use Description.CheckDescID() to obtain a complete DescID (with data type and creator IDs) from another DescID

import c4d


def main():
    if op is None: return
    if op.GetClassification() != c4d.Obase: return
    
    # Retrieves the active object's description
    desc = op.GetDescription(c4d.DESCFLAGS_DESC_0)
    if not desc: return

    # Builds the object's X position parameter DescID
    descid = c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION, 0, 0), c4d.DescLevel(c4d.VECTOR_X, 0, 0))
    # Prints previously built DescID
    print descid

    # Calls CheckDescID() to retrieve the complete DescID for the object's X position parameter
    ret = desc.CheckDescID(descid, [op])
    if ret is None:
        print "Could not check description ID"
        return

    # Prints the complete DescID
    print ret


if __name__=='__main__':
    main()
