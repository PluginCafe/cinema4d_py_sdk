"""
Snapping Module Example

Example:
c4d.modules.snap

This example shows how to use the snap module functions.
"""

import c4d
from c4d.modules import snap


def main():
    
    # Check snap state
    res = snap.IsSnapEnabled(doc)
    if not res:
        # Enable snap if not activated
        snap.EnableSnap(True, doc)
        print "Snap Enabled:", snap.IsSnapEnabled(doc)
    
    # Set 3D snapping settings mode
    c4d.CallCommand(c4d.SNAP_SETTINGS_3D)
    
    # Enable point snap
    snap.EnableSnap(True, doc, c4d.SNAPMODE_POINT)
    
    # Enable quantizing
    c4d.CallCommand(c4d.QUANTIZE_ENABLED)
    c4d.EventAdd()
    print "Quantize Enabled:", snap.IsQuantizeEnabled(doc)
    
    # Set quantize scale step
    snap.SetQuantizeStep(doc, None, c4d.QUANTIZE_SCALE, 0.5)
    print "Quantize Scale Step:",  snap.GetQuantizeStep(doc, None, c4d.QUANTIZE_SCALE)
    
    # Set quantize move step
    snap.SetQuantizeStep(doc, None, c4d.QUANTIZE_MOVE, 25)
    print "Quantize Scale Step:",  snap.GetQuantizeStep(doc, None, c4d.QUANTIZE_MOVE)
    
    # Print workplane object and matrix
    print "Workplane Object:", snap.GetWorkplaneObject(doc)
    print "Workplane Matrix:", snap.GetWorkplaneMatrix(doc, None)
    
    # Check if workplane is locked
    if not snap.IsWorkplaneLock(doc):
        # Lock workplane
        snap.SetWorkplaneLock(doc.GetActiveBaseDraw(), True)
        print "Workplane Locked:", snap.IsWorkplaneLock(doc)


if __name__=='__main__':
    main()
