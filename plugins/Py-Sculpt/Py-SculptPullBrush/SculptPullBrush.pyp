"""
Python Pull Brush
Copyright: MAXON Computer GmbH
Author: Kent Barber
Written for CINEMA 4D R16
Modified Date: 04/11/2013
"""

import c4d
import os

from c4d import gui, plugins, bitmaps, modules
from c4d.modules import sculpting

#be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1031349 

#for GeLoadString
#values must match with the header file
IDS_PYTHON_BRUSH_PULL = 10000

class SculptBrushPullTool(plugins.SculptBrushToolData):
	"""Inherit from SculptBrushToolData to create your own sculpting tool"""

	def __init__(self):
		return None
	
	def GetToolPluginId(self):
		return PLUGIN_ID

	def GetResourceSymbol(self):
		return "pythonpullbrush"

	def ApplyDab(self,dab):
		strength = dab.GetBrushStrength()
		if strength == 0:
			return True
			
		brushRadius = dab.GetBrushRadius()
		bc = dab.GetData()
		pointCount = dab.GetPointCount()
		usePreview = dab.IsPreviewDab()
		polyObj = dab.GetPolygonObject()
		rad = polyObj.GetRad()

		#Pre calculate the offset vector
		dim = rad.GetLength() * 0.005
		buildup = bc.GetFloat(c4d.MDATA_SCULPTBRUSH_SETTINGS_BUILDUP) * 0.002
		pressurePreMult = strength * 10.0 * buildup * dim
		multPreMult = dab.GetNormal() * pressurePreMult

		#If the user is holding down the Ctrl Key then the OVERRIDE_INVERT flag will be set. If it is set then we invert the direction of the multiplier vector.    
		invert = dab.GetBrushOverride() & c4d.OVERRIDE_INVERT
		if invert == True:
			multPreMult = -multPreMult;
			
		#The user may also have the invert checkbox enabled in the UI. Check for this and then invert the direction of the multiplier vector again if we need to.
		if bc.GetBool(c4d.MDATA_SCULPTBRUSH_SETTINGS_INVERT) == True:
			multPreMult = -multPreMult;
			
		#Loop over very point for this dab and move it if we need to.
		for a in xrange(0,pointCount):
			#Get the index of the point on the PolygonObject.
			pointData = dab.GetPointData(a)
			pointIndex = pointData["pointIndex"]
			
			#Get the falloff for this point. This will always be a value from 0 to 1.
			#The value returned is a combination of the following values all multiplied together to give a final value.
			#- The falloff curve.
			#- The color of the stamp with its color value averaged to gray and adjusted by the Gray Value.
			#- The color of the stencil with its color value averaged to gray and adjusted by the Gray Value.
			fallOff = dab.GetBrushFalloff(a)
			
			#If the falloff value is 0 then we don't have to do anything at all.
			if fallOff == 0:
				continue
				
			#Multiply the falloff value with the multiply vector we calculated early. This will result in an offset vector that we want to move the vertex on the model by.
			res = fallOff * multPreMult
			
			#If the brush is not in preview mode (preview mode happens with in DragDab or DragRect mode) then we can offset the final point on the selected layer.
			if usePreview == False: 
				dab.OffsetPoint(pointIndex, res)
			#Otherwise we apply the offset to the preview layer.
			else:
				dab.OffsetPreviewPoint(pointIndex, res)
		return True

if __name__ == "__main__":
	params = sculpting.SculptBrushParams();
	params.EnableInvertCheckbox(True)
	params.EnableBuildup(True)
	params.EnableModifier(True)
	params.SetFloodType(c4d.SCULPTBRUSHDATATYPE_POINT)
	params.SetBrushMode(c4d.SCULPTBRUSHMODE_NORMAL)
	params.SetFirstHitPointType(c4d.FIRSTHITPPOINTTYPE_SELECTED)
	params.SetUndoType(c4d.SCULPTBRUSHDATATYPE_POINT)
	plugins.RegisterSculptBrushPlugin(id=PLUGIN_ID, str="Python Pull Brush",
								info=0, icon=None, 
								help="Python Pull Brush",sculptparams=params,
								dat=SculptBrushPullTool())