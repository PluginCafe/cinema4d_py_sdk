"""
Dynamic Parameters Object
Copyright: MAXON Computer GmbH
Written for Cinema 4D R18.020

Last Modified Date: 31/08/2016
"""

import c4d
from c4d import bitmaps, documents, plugins

import copy
import random

# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1037871

# Dynamic groug and parameters IDs
OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP = 1100
OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP_FIRSTPARAMETER = OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP+1

# Dynamic Object plugin Example for the Dynamic Description additions in R18 Python API
#
# Parameter ID 1000: Dynamic Group
# Parameters ID 1100+: Dynamic float parameters
# Parameter ID 1001: REAL parameter OPYDYNAMICPARAMETERSOBJECT_TRANSLATED_PHONG_ANGLE (refers the first attached Phong tag PHONGTAG_PHONG_ANGLE parameter, see TranslateDescID() below)
# Parameter ID 1002: LONG parameter OPYDYNAMICPARAMETERSOBJECT_PARAMETERSNUMBER for the number of parameters in the dynamic group
class DynamicParametersObjectData(plugins.ObjectData):

    def __init__(self):
        self.parameters = []         # Dynamic parameters value
        self.randomID = 0            # Random dynamic parameter ID to disable (see GetDEnabling() below)
                                     # The value is updated in each call of GetDDescription()


    def Init(self, node):

        data = node.GetDataInstance()
        data.SetInt32(c4d.OPYDYNAMICPARAMETERSOBJECT_PARAMETERSNUMBER, 10)

        return True


    def CopyTo(self, dest, snode, dnode, flags, trn):

        # Copy dynamic parameters value
        dest.parameters = copy.copy(self.parameters)

        return True


    def Read(self, node, hf, level):

        # Read dynamic parameters value

        # First, read the number of dynamic parameters
        count = 0
        count = hf.ReadInt32()

        # Then read the dynamic parameters value
        for idx in xrange(count):
            value = hf.ReadFloat32()
            self.parameters.append(value)

        return True


    def Write(self, node, hf):

        # First, write the number of dynamic parameters
        count = len(self.parameters)
        hf.WriteInt32(count)

        # Then write the dynamic parameters value
        for value in self.parameters:
            hf.WriteFloat32(value)

        return True


    # GetDDescription(node, description, flags)
    # node: The GeListNode connected to the NodeData
    # description: The description to modify
    # flags: The input flags for the description operation (DESCFLAGS_DESC)
    #
    # Return tuple(bool,int) or bool
    # tuple[0]: Return bool status
    # tuple[1]: Output flags (DESCFLAGS_DESC)
    def GetDDescription(self, node, description, flags):

        data = node.GetDataInstance()

        # Before adding dynamic parameters, load the parameters from the description resource
        if not description.LoadDescription(node.GetType()):
            return False

        # Get description single ID
        singleID = description.GetSingleDescID()

        # Declare dynamic group DescID
        dynamicGroupID = c4d.DescID(c4d.DescLevel(OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP, c4d.DTYPE_GROUP, node.GetType()))

        # Check if dynamic group needs to be added
        addDynamicGroup = singleID is None
        if not addDynamicGroup:
            addDynamicGroup = dynamicGroupID.IsPartOf(singleID)[0]

        # Add dynamic group
        if addDynamicGroup:
            bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_GROUP)
            bc.SetString(c4d.DESC_NAME, "Dynamic Group")
            bc.SetInt32(c4d.DESC_COLUMNS, 1)
            if not description.SetParameter(dynamicGroupID, bc, c4d.DescID(c4d.DescLevel((c4d.ID_OBJECTPROPERTIES)))):
                return False

        # Declare REAL parameter container
        bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_REAL)
        bc.SetInt32(c4d.DESC_CUSTOMGUI, c4d.CUSTOMGUI_REALSLIDER)
        bc.SetFloat(c4d.DESC_MIN, 0.0)
        bc.SetFloat(c4d.DESC_MAX, 1.0)
        bc.SetFloat(c4d.DESC_MINSLIDER, 0.0)
        bc.SetFloat(c4d.DESC_MAXSLIDER, 1.0)
        bc.SetFloat(c4d.DESC_STEP, 0.01)
        bc.SetInt32(c4d.DESC_UNIT, c4d.DESC_UNIT_FLOAT)
        bc.SetInt32(c4d.DESC_ANIMATE, c4d.DESC_ANIMATE_ON)
        bc.SetBool(c4d.DESC_REMOVEABLE, False)

        # Initialize/Update parameters value list if needed 
        parametersNum = data.GetInt32(c4d.OPYDYNAMICPARAMETERSOBJECT_PARAMETERSNUMBER)
        parametersLen = len(self.parameters)
        if parametersLen == 0:
            self.parameters = [0.0]*parametersNum
        elif parametersLen != parametersNum:
            if parametersLen < parametersNum:
                while parametersLen < parametersNum:
                    self.parameters.append(0.0)
                    parametersLen += 1
            else:
                while parametersLen > parametersNum:
                    self.parameters.pop()
                    parametersLen -= 1

        # Add dynamic REAL parameters
        for idx in range(parametersNum):
            descid = c4d.DescID(c4d.DescLevel(OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP_FIRSTPARAMETER+idx, c4d.DTYPE_REAL, node.GetType()))
            addParameter = singleID is None
            if not addParameter:
                addParameter = descid.IsPartOf(singleID)[0]

            if addParameter:
                name = "Dynamic REAL " + str(idx+1)
                bc.SetString(c4d.DESC_NAME, name)
                bc.SetString(c4d.DESC_SHORT_NAME, name)
                if not description.SetParameter(descid, bc, dynamicGroupID):
                    break

        # Calculate random ID in the dynamic parameters range
        self.randomID = random.randrange(OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP_FIRSTPARAMETER, OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP+parametersNum-1)

        # After dynamic parameters have been added successfully, return True and c4d.DESCFLAGS_DESC_LOADED with the input flags
        return (True, flags | c4d.DESCFLAGS_DESC_LOADED)


    # SetDParameter(node, id, data, flags)
    # node: The GeListNode connected to the NodeData
    # id: The ID of the parameter to set
    # data: The parameter data to set
    # flags: The input flags for the description operation (DESCFLAGS_SET)
    #
    # Return tuple(bool,int) or bool
    # tuple[0]: Return bool status
    # tuple[1]: Output flags (DESCFLAGS_SET)
    def SetDParameter(self, node, id, data, flags):

        # Get parameter ID
        paramID = id[0].id

        # Get number of parameters
        parametersLen = len(self.parameters)

        # Check passed parameter ID is a dynamic parameter
        if paramID >= OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP_FIRSTPARAMETER and paramID <= OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP+parametersLen:
            # Set parameter data 
            self.parameters[paramID-OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP_FIRSTPARAMETER] = data
            return (True, flags | c4d.DESCFLAGS_SET_PARAM_SET)

        return False


    # GetDParameter(node, id, flags)
    # node: The GeListNode connected to the NodeData
    # id: The ID of the parameter to get
    # flags: The input flags for the description operation (DESCFLAGS_GET)
    #
    # Return tuple(bool,any,int) or bool
    # tuple[0]: Return bool status
    # tuple[1]: Return data (any type)
    # tuple[2]: Output flags (DESCFLAGS_GET)
    def GetDParameter(self, node, id, flags):

        # Get parameter ID
        paramID = id[0].id

        # Get number of parameters
        parametersLen = len(self.parameters)

        # Check passed parameter ID is a dynamic parameter
        if paramID >= OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP_FIRSTPARAMETER and paramID <= OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP+parametersLen:
            # Get parameter data 
            data = self.parameters[paramID-OPYDYNAMICPARAMETERSOBJECT_DYNAMICGROUP_FIRSTPARAMETER]
            return (True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET)

        return False


    # TranslateDescID()
    # node: The GeListNode connected to the NodeData
    # id: The source ID of the parameter to translate
    #
    # Return tuple(bool,DescID,atom) or bool
    # tuple[0]: Return bool status
    # tuple[1]: Return target description ID
    # tuple[2]: Return target object
    def TranslateDescID(self, node, id):

        # Get parameter ID
        paramID = id[0].id

        # Check parameter ID is OPYDYNAMICPARAMETERSOBJECT_TRANSLATED_PHONG_ANGLE
        # OPYDYNAMICPARAMETERSOBJECT_TRANSLATED_PHONG_ANGLE references the first attached Phong tag PHONGTAG_PHONG_ANGLE parameter
        if paramID == c4d.OPYDYNAMICPARAMETERSOBJECT_TRANSLATED_PHONG_ANGLE:
            # Get first Phong Tag
            tag = node.GetTag(c4d.Tphong)
            if tag:
                # Get Phong Tag description
                desc = tag.GetDescription(c4d.DESCFLAGS_DESC_0)
                if not desc:
                    return False

                # Retrieve the complete DescID for the PHONGTAG_PHONG_ANGLE parameter
                # First, build a DescID with only the parameter ID
                descid = c4d.DescID(c4d.DescLevel(c4d.PHONGTAG_PHONG_ANGLE))
                # Then DescLevel members type and creator are filled with Description.CheckDescID()
                completeid = desc.CheckDescID(descid, None)

                return (True, completeid, tag)

        return False


    # GetDEnabling()
    # node: The GeListNode connected to the NodeDat
    # id: The ID of the parameter
    # t_data:  The current data for the parameter
    # flags: Not used currently
    # itemdesc: The description for the parameter, encoded to a container
    #
    # Return bool: True if the parameter should be enabled, otherwise False
    def GetDEnabling(self, node, id, t_data, flags, itemdesc):

        # Get parameter ID
        paramID = id[0].id

        # Check parameter is the random ID to disable
        if paramID == self.randomID:
            return False

        return True


    def GetBubbleHelp(self, node):
        return "Dynamic Object Bubble Help"



if __name__ == "__main__":
    plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="Py-DynamicParametersObject",
                                 g=DynamicParametersObjectData,
                                 description="opydynamicparametersobject", icon=bitmaps.InitResourceBitmap(c4d.Onull),
                                 info=c4d.OBJECT_GENERATOR)
