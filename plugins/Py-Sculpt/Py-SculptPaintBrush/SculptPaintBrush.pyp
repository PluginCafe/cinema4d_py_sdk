"""
Python Paint Brush.

This brush will rasterize the stencil onto the polygons touched by the brush. 
You will need an active stencil for the brush to work.
This brush is very slow and is just used to illustrate the ability to access the stencil for a
brush and also how to access the bodypaint layer to apply paint.

Copyright: MAXON Computer GmbH
Author: Kent Barber
Written for CINEMA 4D R16
Modified Date: 04/11/2013
"""

import c4d
import os
import math

from c4d import gui, plugins, bitmaps, modules, threading, documents, storage
from c4d.modules import sculpting
from c4d.modules import bodypaint

#be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1031348 

#for GeLoadString
#values must match with the header file
IDS_PYTHON_BRUSH_PAINT = 10000

"""
The following code uses the same approach as the simple rasterization algorithm described on Josh Beams website.
http://joshbeam.com/articles/triangle_rasterization/
"""

class Edge:
	def __init__(self, point1, x1, y1, point2, x2, y2):
		if y1 < y2:
			self.point1 = point1
			self.x1 = x1
			self.y1 = math.floor(y1)
			self.point2 = point2
			self.x2 = x2
			self.y2 = math.ceil(y2)
		else:
			self.point1 = point2
			self.x1 = x2
			self.y1 = math.floor(y2)
			self.point2 = point1
			self.x2 = x1
			self.y2 = math.ceil(y1)

class Span:
    def __init__(self, point1, x1, point2, x2):
		if x1 < x2:
			self.point1 = point1
			self.x1 = x1
			self.point2 = point2
			self.x2 = x2
		else:
			self.point1 = point2
			self.x1 = x2
			self.point2 = point1
			self.x2 = x1
			
def DrawSpan(dab, bmp, span, y):
	xdiff = math.ceil(span.x2) - math.floor(span.x1)
	if xdiff == 0:
		return
		
	pointdiff = span.point2 - span.point1
	factor = 0.0
	factorStep = 1.0 / float(xdiff)
  
	if span.x1 < 0:
		return;
		
	if span.x2 < 0:
		return;
		
	if span.x1 > bmp.GetBw():
		return;    

	if span.x2 > bmp.GetBw():
		return;
	
	currentPixel = 0
	startPixel = int(math.floor(span.x1))
	endPixel = int(math.ceil(span.x2))
	
	fillTool = dab.IsFillTool()

	# Create a byte sequence buffer for 3 bytes	
	numPixels = endPixel - startPixel
	sq = storage.ByteSeq(None, numPixels*c4d.COLORBYTES_RGB)
		
	#get the current colors of the bitmap
	bmp.GetPixelCnt(startPixel,y,numPixels,sq,c4d.COLORMODE_RGB,c4d.PIXELCNT_0)
	
	for x in xrange(startPixel,endPixel):
	
		#get the location on the object for this part of the triangle that we are rasterizing
		pos = span.point1 + (pointdiff * factor)
		
		#get the stencil color that should be applied to the pixel at this position
		stencilData = dab.GetStencilColor(pos)
		stencilCol = stencilData["color"]
		
		#get the falloff for the brush for this position
		falloff = 1.0
		if fillTool == False:
			falloff = dab.GetBrushFalloffFromPos(pos)
				
		#get the rgb colors from the byte sequence
		r = ord(sq[currentPixel])
		g = ord(sq[currentPixel+1])
		b = ord(sq[currentPixel+2])
		
		#calculate the new color by multiplying the color (0.0 to 1.0) by 255
		newR = stencilCol.x * 255.0
		newG = stencilCol.y * 255.0
		newB = stencilCol.z * 255.0
		
		#blend the current and new color together using the falloff
		mixR = r * (1.0-falloff) + newR * falloff
		mixG = g * (1.0-falloff) + newG * falloff
		mixB = b * (1.0-falloff) + newB * falloff	
		
		#set the data back into the byte sequence so that we can set it on the bitmap agian 
		sq[currentPixel] = chr(int(mixR))
		sq[currentPixel+1] = chr(int(mixG))
		sq[currentPixel+2] = chr(int(mixB))
		
		currentPixel = currentPixel + 3
		
		factor += factorStep
		
	#set the new color of this pixel
	bmp.SetPixelCnt(startPixel,y,numPixels,sq,c4d.COLORBYTES_RGB,c4d.COLORMODE_RGB,c4d.PIXELCNT_0)

def DrawSpansBetweenEdges(dab, bmp, e1, e2):
    # calculate difference between the y coordinates
    # of the first edge and return if 0
	e1ydiff = float(e1.y2 - e1.y1)
	if e1ydiff == 0.0:
		return

    # calculate difference between the y coordinates
    # of the second edge and return if 0
	e2ydiff = float(e2.y2 - e2.y1)
	if e2ydiff == 0.0:
		return

    # calculate differences between the x coordinates
    # and colors of the points of the edges
	e1xdiff = float(e1.x2 - e1.x1)
	e2xdiff = float(e2.x2 - e2.x1)
	e1pointdiff = e1.point2 - e1.point1
	e2pointdiff = e2.point2 - e2.point1
	
    # calculate factors to use for interpolation
    # with the edges and the step values to increase
    # them by after drawing each span
	factor1 = float(e2.y1 - e1.y1) / e1ydiff
	factorStep1 = 1.0 / e1ydiff
	factor2 = 0.0
	factorStep2 = 1.0 / e2ydiff
	
	# loop through the lines between the edges and draw spans
	for y in xrange(int(e2.y1), int(e2.y2)):
		# create and draw span
		span  = Span(e1.point1 + (e1pointdiff * factor1), e1.x1 + int(e1xdiff * factor1), e2.point1 + (e2pointdiff * factor2), e2.x1 + int(e2xdiff * factor2))
		DrawSpan(dab, bmp, span, y)
		# increase factors
		factor1 += factorStep1
		factor2 += factorStep2
		

def Round(x):
	return int(math.floor(x+0.5))
		
def DrawTriangle(dab, bmp, point1, x1, y1, point2, x2, y2, point3, x3, y3):
	# create edges for the triangle
	edges = [ 
		Edge(point1, Round(x1), Round(y1), point2, Round(x2), Round(y2)), 
		Edge(point2, Round(x2), Round(y2), point3, Round(x3), Round(y3)), 
		Edge(point3, Round(x3), Round(y3), point1, Round(x1), Round(y1)) ]
	maxLength = 0
	longEdge = 0

    # find edge with the greatest length in the y axis
	for i in xrange(0,3):
		length = edges[i].y2 - edges[i].y1
		if length > maxLength:
			maxLength = length
			longEdge = i
			
	shortEdge1 = (longEdge + 1) % 3
	shortEdge2 = (longEdge + 2) % 3
    
    # draw spans between edges; the long edge can be drawn
    # with the shorter edges to draw the full triangle
	DrawSpansBetweenEdges(dab, bmp, edges[longEdge], edges[shortEdge1]);
	DrawSpansBetweenEdges(dab, bmp, edges[longEdge], edges[shortEdge2]);

class PaintBrushTool(plugins.SculptBrushToolData):
	"""Inherit from SculptBrushToolData to create your own sculpting tool"""

	def __init__(self):
		return None
	
	def GetToolPluginId(self):
		return PLUGIN_ID

	def GetResourceSymbol(self):
		return "pythonpaintbrush"

	def ApplyDab(self,dab):
		strength = dab.GetBrushStrength()
		if strength == 0:
			return True
			
		brushRadius = dab.GetBrushRadius()
		bc = dab.GetData()
		polyCount = dab.GetPolyCount()
		polyObj = dab.GetPolygonObject()
		uvs = polyObj.GetTag(c4d.Tuvw);
		if uvs == None:
			return False

		texture = bodypaint.PaintTexture.GetSelectedTexture();
		if texture == None:
			return False
			
		layer = texture.GetActive()
		if layer == None:
			return False
		
		paintLayerBmp = layer.ToPaintLayerBmp()
		if paintLayerBmp == None:
			return False;
			
		width = paintLayerBmp.GetBw()
		height = paintLayerBmp.GetBh()
		
		minX = width
		minY = height
		maxX = 0
		maxY = 0
					
		#Loop over very polygon for this dab and rasterize the stencil to it.
		for a in xrange(0,polyCount):
			#Get the index of the point on the PolygonObject.
			polyData = dab.GetPolyData(a)
			polyIndex = polyData["polyIndex"]
			poly = polyObj.GetPolygon(polyIndex)
			polyUVs = uvs.GetSlow(polyIndex)

			pointA = polyObj.GetPoint(poly.a);
			pointB = polyObj.GetPoint(poly.b);
			pointC = polyObj.GetPoint(poly.c);
			pointD = polyObj.GetPoint(poly.d);
			
			destA = polyUVs["a"]
			destB = polyUVs["b"]
			destC = polyUVs["c"]
			destD = polyUVs["d"]
			
			destA.x *= width
			destA.y *= height
			destB.x *= width
			destB.y *= height
			destC.x *= width
			destC.y *= height
			destD.x *= width
			destD.y *= height
			
			#Calculate the region touched by the brush
			if destA.x > maxX:
				maxX = destA.x	
			if destB.x > maxX:
				maxX = destB.x
			if destC.x > maxX:
				maxX = destC.x
			if destD.x > maxX:
				maxX = destD.x	
		
			if destA.y > maxY:
				maxY = destA.y	
			if destB.y > maxY:
				maxY = destB.y
			if destC.y > maxY:
				maxY = destC.y	
			if destD.y > maxY:
				maxY = destD.y
				
			if destA.x < minX:
				minX = destA.x	
			if destB.x < minX:
				minX = destB.x
			if destC.x < minX:
				minX = destC.x
			if destD.x < minX:
				minX = destD.x	
		
			if destA.y < minY:
				minY = destA.y	
			if destB.y < minY:
				minY = destB.y
			if destC.y < minY:
				minY = destC.y	
			if destD.y < minY:
				minY = destD.y
				
			DrawTriangle(dab, paintLayerBmp,
				pointA,destA.x,destA.y,
				pointB,destB.x,destB.y,
				pointC,destC.x,destC.y)

			if poly.c != poly.d:
				DrawTriangle(dab, paintLayerBmp,
					pointA,destA.x,destA.y,
					pointC,destC.x,destC.y,
					pointD,destD.x,destD.y)

		#paintLayerBmp.UpdateRefreshAll(c4d.UPDATE_STD,True)
		paintLayerBmp.UpdateRefresh(int(minX), int(minY), int(maxX), int(maxY), c4d.UPDATE_STD)
		return True

if __name__ == "__main__":
	params = sculpting.SculptBrushParams();
	plugins.RegisterSculptBrushPlugin(id=PLUGIN_ID, str="Python Paint Brush",
								info=0, icon=None, 
								help="Python Paint Brush",sculptparams=params,
								dat=PaintBrushTool())