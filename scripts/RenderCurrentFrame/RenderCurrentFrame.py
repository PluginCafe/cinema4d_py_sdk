"""
Render Current Frame

Copyright: Patrick Goski, patrick@maxon.net
Written for Cinema 4D R12.018

Name-US: Render Current Frame
Description-US: This script automatically adjusts your render settings to render the current frame based on user settings.
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


#next four lines set various render parameters
rd[c4d.RDATA_FRAMESEQUENCE] = 1 #sets render range to current frame
rd[c4d.RDATA_SAVEIMAGE] = False #turns off save image
rd[c4d.RDATA_MULTIPASS_SAVEIMAGE] = False #turns off save multipass


#calls the renderer
c4d.CallCommand (12099)

#send the values stored by rdback back to rd (resets render setting to user settings)
rdback.CopyTo(rd,0)

#force a refresh
c4d.EventAdd()