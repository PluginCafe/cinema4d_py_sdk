"""
Global Texture Paths

Example:
c4d.SetGlobalTexturePaths()
c4d.GetGlobalTexturePaths()

Sets and gets global texture paths (Preferences->Files->Paths).
"""

import c4d
from c4d import storage

import os

def main():

    # Gets desktop and home paths
    desktopPath = storage.GeGetC4DPath(c4d.C4D_PATH_DESKTOP)
    homePath = storage.GeGetC4DPath(c4d.C4D_PATH_HOME)

    # Gets global texture paths
    paths = c4d.GetGlobalTexturePaths()

    # Checks if the paths already exist in the global paths
    desktopPathFound = False
    homePathFound = False
    for path, enabled in paths:
        if os.path.normpath(path) == os.path.normpath(desktopPath):
            desktopPathFound = True

        if os.path.normpath(path) == os.path.normpath(homePathFound):
            homePathFound = True

    # If paths are not found then add them to the global paths

    if not desktopPathFound:
        paths.append([desktopPath, True])

    if not homePathFound:
        paths.append([homePath, True])

    # Sets global texture paths
    c4d.SetGlobalTexturePaths(paths)

    # Prints global texture paths
    print(c4d.GetGlobalTexturePaths())

if __name__=='__main__':
    main()