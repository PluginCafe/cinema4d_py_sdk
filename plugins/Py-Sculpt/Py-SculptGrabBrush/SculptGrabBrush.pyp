"""
Python Grab Brush
Copyright: MAXON Computer GmbH
Author: Kent Barber
Written for CINEMA 4D R16
Modified Date: 05/21/2013
"""

import c4d
import os

from c4d import gui, plugins, bitmaps, modules
from c4d.modules import sculpting

#be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1031347  

#for GeLoadString
#values must match with the header file
IDS_PYTHON_BRUSH_GRAB = 10000

class SculptBrushGrabTool(plugins.SculptBrushToolData):
	"""Inherit from SculptBrushToolData to create your own sculpting tool"""

	def __init__(self):
		return None
	
	def GetToolPluginId(self):
		return PLUGIN_ID

	def GetResourceSymbol(self):
		return "pythongrabbrush"

	#Set our custom values. See the pythongrabbrush.res and pythongrabbrush.h files for where this value is defined.	
	def PostInitDefaultSettings(self, doc, data):
		data.SetInt32(c4d.MDATA_PYTHONGRABBRUSH_DIRMODE, c4d.MDATA_PYTHONGRABBRUSH_DIRMODE_MOUSEDIR)
		return None
		
	def ApplyDab(self,dab):
		#Get the Polygon Object so that we can get its Matrix
		polyObj = dab.GetPolygonObject()
		if polyObj == None:
			return False

		#Get the world matrix for the model so that we can turn local coordinates into world coordinates.
		mat = polyObj.GetMg();

		#Get the location of the hitpoint on the model in world coordinates
		hitPointWorld = mat * dab.GetHitPoint();

		#Zero out the offset since its no longer required
		mat.off = c4d.Vector(0, 0, 0);

		data = dab.GetData();

		#Get our custom direction value that we added to our .res file.
		dirMode = data.GetInt32(c4d.MDATA_PYTHONGRABBRUSH_DIRMODE);

		#Find the distance the mouse has moved in world coordinates by getting the world position of the mouse and subtracting the current grab brush world coordinate
		moveAmnt = dab.GetMousePos3D() - hitPointWorld

		#Transform this distance into a vector that is in the local coordinates of the model.
		invertMat = mat.__invert__()
		moveAmnt = invertMat * moveAmnt;

		normal = dab.GetNormal();

		if dirMode == c4d.MDATA_PYTHONGRABBRUSH_DIRMODE_NORMAL:
			#If we are moving the point in the direction of its normal then use the length of the distance vector to scale the normal.
			moveAmnt = normal * moveAmnt.GetLength()

			#Adjust the direction of the vector depending on if its moving above the surface or below it.
			dot = normal.Dot(moveAmnt)
			if dot < 0:
				moveAmnt *= -1

		#Get the number of points for this dab
		pointCount = dab.GetPointCount()

		#If any of the symmetry settings have been enabled, and this is a symmetry stroke instance, then this will return true.
		mirror = dab.IsMirroredDab()

		#Loop over every point on the dab and move them by the moveAmnt.
		for a in xrange(0,pointCount):
			#Get the index of the point on the PolygonObject.
			pointData = dab.GetPointData(a)
			pointIndex = pointData["pointIndex"]
			
			#Get the falloff value for this point. This value will take into account the current stencil, stamp settings and the falloff curve to create this value.
			fallOff = dab.GetBrushFalloff(a);

			#Get the original points on the surface of the object. These points are the state of the object when the
			#user first clicks on the model to do a mouse stroke. This allows you to compare where the points are during
			#a stroke, since you have moved them, when the original positions.
			original = dab.GetOriginalPoint(pointIndex)
			
			#Get the vector of the point we are going to change.
			currentPoint = dab.GetPoint(pointIndex)
			
			#If the user has any of the symmetry settings enabled and this is one of the symmetrical brush instance then mirror will be True.
			#We can check to see if another brush instance has already touched this point and moved it by calling the IsPointModified method.
			#If a point has been touched then that means it has already been moved by a certain vector by that brush instance.
			#So we just offset it by another vector and do not worry about the original location of the point.
			if mirror and dab.IsPointModified(pointIndex):
				#Adjust the offset by the new amount.
				dab.OffsetPoint(pointIndex, moveAmnt * fallOff)
			else:
				#If there is no symmetry or the point hasn't been touched then we can just set the position of the point normally.
				#First determine the offset vector by using the original location of the point and adding on the new point after it has been adjusted by the falloff value.
				newPosOffset = original + moveAmnt * fallOff

				#A new offset is calculated by using this new point and its current position.
				offset = newPosOffset - currentPoint

				#Offset the point to place it in the correct location.
				dab.OffsetPoint(pointIndex, offset)

		#Ensure that all the points for the dab are marked as dirty. This is required to ensure that they all update even if they were not directly
		#touched by this brush instance. Marking all points as dirty ensures that the normals for all points are updated. This is only required
		#for grab brushes when multiple brush instances are touching the same points.
		dab.DirtyAllPoints(c4d.SCULPTBRUSHDATATYPE_POINT);
		return True;

if __name__ == "__main__":
	params = sculpting.SculptBrushParams();
	params.SetBrushMode(c4d.SCULPTBRUSHMODE_GRAB)
	params.SetUndoType(c4d.SCULPTBRUSHDATATYPE_POINT)
	plugins.RegisterSculptBrushPlugin(id=PLUGIN_ID, str="Python Grab Brush",
								info=0, icon=None, 
								help="Python Grab Brush",sculptparams=params,
								dat=SculptBrushGrabTool())