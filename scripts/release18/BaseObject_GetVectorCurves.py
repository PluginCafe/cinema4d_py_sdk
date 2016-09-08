# This example accesses the vector components curves of the active object's rotation track curve.

import c4d

def main():
    # Check active object
    if op is None:
        return

    # Search object's rotation track
    trackID = c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_REL_ROTATION, c4d.DTYPE_VECTOR, op.GetType()))
    track = op.FindCTrack(trackID)
    if track is None:
        return

    # Get the curve for the track
    curve = track.GetCurve()
    if curve is None:
        return

    ret, curveX, curveY, curveZ = op.GetVectorCurves(curve)
    if ret:
        print "c4d.ID_BASEOBJECT_REL_ROTATION curves:"
        print "Curve H:", curveX
        print "Curve P:", curveY
        print "Curve B:", curveZ
    else:
        print "Could not get vector curves!"

if __name__=='__main__':
    main()
