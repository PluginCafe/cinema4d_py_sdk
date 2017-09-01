"""
Preference
Copyright: MAXON Computer GmbH
Written for Cinema 4D R19

Modified Date: 31/08/2017
"""

import c4d
from c4d import plugins


# Unique plugin ID obtained from www.plugincafe.com
PLUGIN_ID = 1039699

# Unique plugin ID for world preference container obtained from www.plugincafe.com
WPREF_PYPREFERENCE = 1039700

WPREF_PYPREFERENCE_CHECK = 1000
WPREF_PYPREFERENCE_NUMBER = 1001


class Preference(plugins.PreferenceData):

    # Returns WPREF_PYPREFERENCE container instance
    def GetPreferenceContainer(self):
        world = c4d.GetWorldContainerInstance()
        if world is None:
            return None

        bc = world.GetContainerInstance(WPREF_PYPREFERENCE)
        if bc is None:
            world.SetContainer(WPREF_PYPREFERENCE, c4d.BaseContainer())
            bc = world.GetContainerInstance(WPREF_PYPREFERENCE)
            if bc is None:
                return None

        return bc

    def GetDDescription(self, node, description, flags):

        if not description.LoadDescription("pypreference"):
            return False

        if flags & c4d.DESCFLAGS_DESC_NEEDDEFAULTVALUE:
            # Set default values
            self.InitValues(c4d.DescID(c4d.DescLevel(c4d.PYPREFERENCE_CHECK, c4d.DTYPE_BOOL, 0)), description)
            self.InitValues(c4d.DescID(c4d.DescLevel(c4d.PYPREFERENCE_NUMBER, c4d.DTYPE_LONG, 0)), description)

        return (True, flags | c4d.DESCFLAGS_DESC_LOADED)

    def GetDParameter(self, node, id, flags):

        bc = self.GetPreferenceContainer()
        if bc is None:
            return False

        # Retrieves either check or number preference value

        paramID = id[0].id
        if paramID == c4d.PYPREFERENCE_CHECK:
            return (True, bc.GetBool(WPREF_PYPREFERENCE_CHECK), flags | c4d.DESCFLAGS_GET_PARAM_GET)
        elif paramID == c4d.PYPREFERENCE_NUMBER:
            return (True, bc.GetInt32(WPREF_PYPREFERENCE_NUMBER), flags | c4d.DESCFLAGS_GET_PARAM_GET)

        return False

    def SetDParameter(self, node, id, data, flags):

        bc = self.GetPreferenceContainer()
        if bc is None:
            return False

        # Changes either check or number preference value

        paramID = id[0].id
        if paramID == c4d.PYPREFERENCE_CHECK:
            bc.SetBool(WPREF_PYPREFERENCE_CHECK, data)
            return (True, flags | c4d.DESCFLAGS_SET_PARAM_SET)
        elif paramID == c4d.PYPREFERENCE_NUMBER:
            bc.SetInt32(WPREF_PYPREFERENCE_NUMBER, data)
            return (True, flags | c4d.DESCFLAGS_SET_PARAM_SET)

        return False

    def GetDEnabling(self, node, id, t_data, flags, itemdesc):

        paramID = id[0].id
        if paramID == c4d.PYPREFERENCE_CHECK:
            return True
        elif paramID == c4d.PYPREFERENCE_NUMBER:
            # Number preference is enabled only if check is on
            bc = self.GetPreferenceContainer()
            if bc is None:
                return False

            return bc.GetBool(WPREF_PYPREFERENCE_CHECK)

        return False

    def Init(self, node):

        # Init default values

        self.InitValues(c4d.DescID(c4d.DescLevel(c4d.PYPREFERENCE_CHECK, c4d.DTYPE_BOOL, 0)))
        self.InitValues(c4d.DescID(c4d.DescLevel(c4d.PYPREFERENCE_NUMBER, c4d.DTYPE_LONG, 0)))

        return True

    def InitValues(self, id, description=None):

        bc = self.GetPreferenceContainer()
        if bc is None:
            return False

        # Set default values

        id = id[0].id
        if id == c4d.PYPREFERENCE_CHECK:
            self.InitPreferenceValue(WPREF_PYPREFERENCE_CHECK, True, description, id, bc)
        elif id == c4d.PYPREFERENCE_NUMBER:
            self.InitPreferenceValue(WPREF_PYPREFERENCE_NUMBER, 10, description, id, bc)

        return True


if __name__ == '__main__':
    plugins.RegisterPreferencePlugin(id=PLUGIN_ID, g=Preference, name="Py-Preference", description="pypreference", parentid=0, sortid=0)
