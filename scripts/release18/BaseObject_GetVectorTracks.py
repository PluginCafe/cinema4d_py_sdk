# This example accesses the vector components tracks of the active object's position track.

import c4d

def main():
    # Check active object
    if op is None:
        return

    # Create ID_BASEOBJECT_REL_POSITION DescID
    trackID = c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_REL_POSITION, c4d.DTYPE_VECTOR, op.GetType()))

    # Retrieve ID_BASEOBJECT_REL_POSITION vector tracks
    ret, trackX, trackY, trackZ = op.GetVectorTracks(trackID)
    if ret:
        print "c4d.ID_BASEOBJECT_REL_POSITION tracks:"
        print "Track X:", trackX
        print "Track Y:", trackY
        print "Track Z:", trackZ
    else:
        print "Could not get vector tracks!"

if __name__=='__main__':
    main()
