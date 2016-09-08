# This example checks the interpolation of the first key for an object's rotation track.
# If the interpolation is linear (SLERP) it is changed to cubic.
# Note: The object has to be in in quaternion rotation mode.

import c4d

def main():
    # Check active object
    if op is None:
        return

    # Only continue if object is in quaternion rotation mode
    if not op.IsQuaternionRotationMode():
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

    # Do not continue if there are no keys inside curve
    if curve.GetKeyCount() == 0:
        return

    # Get first key
    key = curve.GetKey(0)
    if key is None:
        return

    # Check quaternion interpolation is linear (SLERP)
    if key.GetQuatInterpolation() == c4d.ROTATIONINTERPOLATION_QUATERNION_SLERP:
        # If yes, change it to cubic 
        key.SetQuatInterpolation(curve, c4d.ROTATIONINTERPOLATION_QUATERNION_CUBIC)
        c4d.EventAdd()

if __name__=='__main__':
    main()
