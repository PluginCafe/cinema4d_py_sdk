# This example checks if the active object uses quaternion interpolation.

import c4d

def main():
    # Check active object
    if op is None:
        return

    # Check if the object uses quaternion interpolation
    if not op.IsQuaternionRotationMode():
        # Enable quaternion interpolation
        # This will update the object's rotation animation tracks
        op.SetQuaternionRotationMode(True, False);
        c4d. EventAdd()

if __name__=='__main__':
    main()
