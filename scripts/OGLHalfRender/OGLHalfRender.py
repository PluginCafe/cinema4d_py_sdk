"""
OGL HalfRender

Copyright: Patrick Goski, patrick@maxon.net
Written for Cinema 4D R12.018

Name-US: OGL HalfRender
Description-US: This script automatically adjusts your render settings to produce a halfsize OGL render. After it resets back to your origional settings.
"""

import c4d
from c4d import documents, bitmaps, gui

#get the current document
doc = documents.GetActiveDocument()
#get the current documents render settings
rd = doc.GetActiveRenderData()
#store a copy of those settings
rdback = rd.GetClone()
#access the basedraw of the render view (filters etc.)
bd = doc.GetRenderBaseDraw()



#basedraw stuff to set filters (If you don't want to change filters delete these lines as these functions do not sample your current viewport filters)
bd[c4d.BASEDRAW_DISPLAYFILTER_OBJECTHANDLES] = False
bd[c4d.BASEDRAW_DISPLAYFILTER_WORLDAXIS] = False
bd[c4d.BASEDRAW_DISPLAYFILTER_GRID] = False
bd[c4d.BASEDRAW_DISPLAYFILTER_DEFORMER] = False
bd[c4d.BASEDRAW_DISPLAYFILTER_HORIZON] = False

#next two lines halve the x/y resolution
rd[c4d.RDATA_XRES] /= 2
rd[c4d.RDATA_YRES] /= 2

#next four lines set various render parameters
rd[c4d.RDATA_FRAMESEQUENCE] = 3 #sets render range to preview
rd[c4d.RDATA_SAVEIMAGE] = False #turns off save image
rd[c4d.RDATA_MULTIPASS_SAVEIMAGE] = False #turns of multipass save image
rd[c4d.RDATA_RENDERENGINE] = 300001061 #sets render engine to OGL

#calls the renderer
c4d.CallCommand (12099)

#send the values stored by rdback back to rd after calling the renderer.
rdback.CopyTo(rd,0)

#manual reset of filters (If you don't want to change filters delete these lines)
#basedraw stuff to set filters
bd[c4d.BASEDRAW_DISPLAYFILTER_OBJECTHANDLES] = True
bd[c4d.BASEDRAW_DISPLAYFILTER_WORLDAXIS] = True
bd[c4d.BASEDRAW_DISPLAYFILTER_GRID] = True
bd[c4d.BASEDRAW_DISPLAYFILTER_DEFORMER] = True
bd[c4d.BASEDRAW_DISPLAYFILTER_HORIZON] = True

#force a refresh
c4d.EventAdd()