# This example prints all the tracks of the active Motion Tracker object.

import c4d

def main():
    # Check active object
    if op is None:
        return

    # Check active object is a Motion Tracker object
    if not op.IsInstanceOf(c4d.Omotiontracker):
        return

    # Retrieve tracking data
    data = op.Get2dTrackData()
    if data is None:
        return

    # Loop through all tracks
    trackCount = data.GetTrackCount()
    for trackIdx in xrange(trackCount):
        track = data.GetTrackByIndex(trackIdx)
        if track is None:
            break

        # Check track status
        statusStr = ""
        if status == c4d.INVALID_TRACK:
            statusStr = "invalid"
        if status == c4d.UNTRACKED:
            statusStr = "untracked"
        if status == c4d.TRACKED_VALID:
            statusStr = "valid"
        if status == c4d.TRACKED_STALE:
            statusStr = "stale"

        # Print track information
        print "Track #" + str(trackIdx) + ": " + track.GetName() + " is "+ statusStr

if __name__=='__main__':
    main()
