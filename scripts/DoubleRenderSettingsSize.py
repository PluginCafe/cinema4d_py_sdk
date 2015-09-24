"""
Double Render Settings Size

This script doubles the output render size.
"""

import c4d


def main():
    # Get the current active render settings
    rdata = doc.GetActiveRenderData()
    
    # Double the output size
    rdata[c4d.RDATA_XRES] *= 2
    rdata[c4d.RDATA_YRES] *= 2

    # Send global event message to update the RenderSettings dialog
    c4d.EventAdd()

if __name__=='__main__':
    main()
