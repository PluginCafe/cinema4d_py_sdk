# This example synchronizes the keys for the tracks of the active cube's "Size" parameter.
# If a track has a key at a certain time, keys for the other synchronized tracks will be created.

import c4d

def main():
    # Check active object
    if op is None:
        return

    # Synchronize keys
    op.SynchronizeVectorTrackKeys(c4d.PRIM_CUBE_LEN, False)

    c4d.EventAdd()

if __name__=='__main__':
    main()
