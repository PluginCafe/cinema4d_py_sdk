"""
Python Twist Brush
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
PLUGIN_ID = 1031350  

#for GeLoadString
#values must match with the header file
IDS_PYTHON_BRUSH_TWIST = 10000

class SculptBrushTwistTool(plugins.SculptBrushToolData):
	"""Inherit from SculptBrushToolData to create your own sculpting tool"""

	def __init__(self):
		return None
	
	def GetToolPluginId(self):
		return PLUGIN_ID

	def GetResourceSymbol(self):
		return "pythontwistbrush"
		
	def OverwriteLoadedPresetSettings(self, data):
		data[c4d.MDATA_SCULPTBRUSH_STAMP_FOLLOW] = False
		
	def ApplyDab(self,dab):
		poly = dab.GetPolygonObject()
		normal = dab.GetNormal()
		mat = poly.GetMg()
		hitPointWorld = mat * dab.GetHitPoint()

		twistGrabMoveAmnt = (dab.GetMousePos3D() - hitPointWorld)
		mat.off = c4d.Vector(0,0,0);
		twistGrabMoveAmnt = ~mat * twistGrabMoveAmnt;

		#TwistGrab along the normal
		dot = normal.Dot(twistGrabMoveAmnt)
		twistGrabMoveAmnt = normal * twistGrabMoveAmnt.GetLength()
		if dot < 0:
			twistGrabMoveAmnt *= -1

		pointAndNormal = dab.GetAveragePointAndNormal()

		pointCount = dab.GetPointCount()
		mirrored = dab.IsMirroredDab()

		hitScreenSpace = dab.GetBaseDraw().WS(hitPointWorld)
		currentDrawLocation = dab.GetBaseDraw().WS(dab.GetMousePos3D())

		xVal = currentDrawLocation.x - hitScreenSpace.x
		rotation = c4d.utils.Rad(xVal)
		
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

			#Get the original points on the surface of the object. These points are the state of the object when the
			#user first clicks on the model to do a mouse stroke. This allows you to compare where the points are during
			#a stroke, since you have moved them, when the original positions.
			original = dab.GetOriginalPoint(pointIndex)
			
			#Get the vector of the point we are going to change.
			currentPoint = dab.GetPoint(pointIndex)
			
			rotationMatrix = c4d.utils.RotAxisToMatrix(pointAndNormal["normal"], rotation * fallOff)

			#If the point has been touched and we are in mirror mode then do something special
			if mirrored and dab.IsPointModified(pointIndex):
				newPosition = currentPoint - hitPointWorld
				newPosition = rotationMatrix * newPosition
				newPosition += hitPointWorld
				newOffset = newPosition - currentPoint
				dab.OffsetPoint(pointIndex, newOffset,nullptr)
			else:
				newPosition = original - hitPointWorld
				newPosition = rotationMatrix * newPosition
				newPosition += hitPointWorld
				offset = newPosition - currentPoint
				dab.OffsetPoint(pointIndex, offset)
				
		dab.DirtyAllPoints(c4d.SCULPTBRUSHDATATYPE_POINT)
		return True

if __name__ == "__main__":
	params = sculpting.SculptBrushParams();
	params.EnableStencil(False)
	params.EnableStamp(False)
	params.SetBrushMode(c4d.SCULPTBRUSHMODE_GRAB)
	params.SetUndoType(c4d.SCULPTBRUSHDATATYPE_POINT)	
	plugins.RegisterSculptBrushPlugin(id=PLUGIN_ID, str="Python Twist Brush",
								info=0, icon=None, 
								help="Python Twist Brush",sculptparams=params,
								dat=SculptBrushTwistTool())