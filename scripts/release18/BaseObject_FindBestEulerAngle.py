# This example checks the rotation tracks of the active object.

import c4d

def main():
    # Check active object
    if op is None:
        return

    # Recalculates the existing keys to find the best angles
    op.FindBestEulerAngle(c4d.ID_BASEOBJECT_REL_ROTATION, True, False)

    # Animate the object so that it uses the new key values
    doc.AnimateObject(op, doc.GetTime(), c4d.ANIMATEFLAGS_0)

    c4d.EventAdd()

if __name__=='__main__':
    main()
