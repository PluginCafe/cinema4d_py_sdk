# This example shows how to use Description.CreatePopupMenu() to obtain a BaseContainer with all the parameters of an object

import c4d
from c4d import gui


def main():
    # Checks active object
    if not op: return

    # Retrieves the active object's description
    desc = op.GetDescription(c4d.DESCFLAGS_DESC_0)
    if not desc: return

    # Retrieves the container with all the object's parameters
    menu = desc.CreatePopupMenu()

    # Shows the menu as a popup dialog
    gui.ShowPopupDialog(cd=None, bc=menu, x=c4d.MOUSEPOS, y=c4d.MOUSEPOS)


if __name__=='__main__':
    main()
