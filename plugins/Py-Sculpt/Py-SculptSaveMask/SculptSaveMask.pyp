"""
Save a Sculpt Objects Mask to a Bitmap
This is a very basic, and slow, script that demonstrates how to access the mask data 
on a sculpt object and do something useful with it. In this case, rasterizing the mask data
to a bitmap using the first found UV tag on the sculpt object.

Copyright: MAXON Computer GmbH
Author: Kent Barber
Written for CINEMA 4D R15
Modified Date: 10/19/2012
"""

import c4d
from c4d.modules import sculpting as sculpt
from c4d import bitmaps, documents, threading, gui, plugins
import math

"""
The following code uses the same approach as the simple rasterization algorithm described on Josh Beams website.
http://joshbeam.com/articles/triangle_rasterization/
"""

PLUGIN_ID = 1031644

class Edge:
    def __init__(self, color1, x1, y1, color2, x2, y2):
        if y1 < y2:
            self.color1 = color1
            self.x1 = x1
            self.y1 = math.floor(y1)
            self.color2 = color2
            self.x2 = x2
            self.y2 = math.ceil(y2)
        else:
            self.color1 = color2
            self.x1 = x2
            self.y1 = math.floor(y2)
            self.color2 = color1
            self.x2 = x1
            self.y2 = math.ceil(y1)

class Span:
    def __init__(self, color1, x1, color2, x2):
        if x1 < x2:
            self.color1 = color1
            self.x1 = x1
            self.color2 = color2
            self.x2 = x2
        else:
            self.color1 = color2
            self.x1 = x2
            self.color2 = color1
            self.x2 = x1

def DrawSpan(bmp, span, y):
    xdiff = math.ceil(span.x2) - math.floor(span.x1)
    if xdiff == 0:
        return

    colordiff = span.color2 - span.color1
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
    
    for x in xrange(int(math.floor(span.x1)), int(math.ceil(span.x2))):
        col = span.color1 + (colordiff * factor)
        bmp.SetPixel(x,y, int(col.x * 255), int(col.y * 255), int(col.z * 255))
        factor += factorStep

def DrawSpansBetweenEdges(bmp, e1, e2):
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
    e1colordiff = e1.color2 - e1.color1
    e2colordiff = e2.color2 - e2.color1

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
        span  = Span(e1.color1 + (e1colordiff * factor1), e1.x1 + int(e1xdiff * factor1), e2.color1 + (e2colordiff * factor2), e2.x1 + int(e2xdiff * factor2))
        DrawSpan(bmp, span, y)
        # increase factors
        factor1 += factorStep1
        factor2 += factorStep2

def DrawTriangle(bmp, color1, x1, y1, color2, x2, y2, color3, x3, y3):
    # create edges for the triangle
    edges = [ 
        Edge(color1, x1, y1, color2, x2, y2), 
        Edge(color2, x2, y2, color3, x3, y3), 
        Edge(color3, x3, y3, color1, x1, y1) ]
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
    DrawSpansBetweenEdges(bmp, edges[longEdge], edges[shortEdge1]);
    DrawSpansBetweenEdges(bmp, edges[longEdge], edges[shortEdge2]);


def Process(bmp):                                 
    doc = documents.GetActiveDocument()
    sculptObject = sculpt.GetSelectedSculptObject(doc);
    if not sculptObject:
        print("No Sculpt Object Select")
        return

    imageWidth = 1024
    imageHeight = 1024

    if bmp.Init(imageWidth,imageHeight,32) != c4d.IMAGERESULT_OK:
        print("Could not initialize bitmap")
        return

    polyObject = sculptObject.GetPolygonCopy(sculptObject.GetCurrentLevel(), True)
    if not polyObject:
        print("Could not get polygon object from sculpt object")
        return

    uvs = polyObject.GetTag(c4d.Tuvw)
    if not uvs:
        print("Sculpt Object has no UVs")
        return

    layer = sculptObject.GetCurrentLayer()
    if not layer:
        print("Could not get the current layer from the SculptObject")
        return
    
    polyCount = polyObject.GetPolygonCount()
    for polyIndex in xrange(polyCount):
        status = float(polyIndex) / float(polyCount) * 100.0;
        c4d.StatusSetBar(status)
            
        poly = polyObject.GetPolygon(polyIndex)
        uvwdict = uvs.GetSlow(polyIndex)
        aX = uvwdict["a"].x * imageWidth;
        aY = uvwdict["a"].y * imageHeight;
        bX = uvwdict["b"].x * imageWidth;
        bY = uvwdict["b"].y * imageHeight;
        cX = uvwdict["c"].x * imageWidth;
        cY = uvwdict["c"].y * imageHeight;
        dX = uvwdict["d"].x * imageWidth;
        dY = uvwdict["d"].y * imageHeight;
        
        maskA = layer.GetMask(poly.a)
        maskB = layer.GetMask(poly.b)
        maskC = layer.GetMask(poly.c)
        maskD = layer.GetMask(poly.d)
    
        colA = c4d.Vector(maskA)
        colB = c4d.Vector(maskB)
        colC = c4d.Vector(maskC)
        colD = c4d.Vector(maskD)

        DrawTriangle(bmp, colA, aX, aY, colB, bX, bY, colC, cX, cY);
        if poly.c != poly.d:
            DrawTriangle(bmp, colA, aX, aY, colC, cX, cY, colD, dX, dY);
                                         
    c4d.StatusClear()
	
class CreateMaskImageCmd(plugins.CommandData):
	def Execute(self, doc):
		bmp = bitmaps.BaseBitmap();
		Process(bmp)
		bitmaps.ShowBitmap(bmp)
		return True
		
if __name__ == "__main__":
	plugins.RegisterCommandPlugin(
			id=PLUGIN_ID,
			str="Python Sculpt Save Mask",
			info=0,
			help="Bake the sculpt mask to an image", 
			dat=CreateMaskImageCmd(),
			icon=None)
