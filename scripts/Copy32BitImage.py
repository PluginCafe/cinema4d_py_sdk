"""
Copy 32-bit Image

Example:
SetPixelCnt/GetPixelCnt

This example shows how to copy the internal data of a 32 bit per-channel image to a new one.
"""

import c4d
from c4d import bitmaps, gui, storage


def main():
    path = storage.LoadDialog(type=c4d.FILESELECTTYPE_IMAGES, title="Please Choose a 32-bit Image:")
    if not path: return
    
    # Create and initialize selected image
    orig = bitmaps.BaseBitmap()
    if orig.InitWith(path)[0] != c4d.IMAGERESULT_OK:
        gui.MessageDialog("Cannot load image \"" + path + "\".")
        return
    
    # Check if channel depth is really 32 bit
    if orig.GetBt()/3 != 32:
        gui.MessageDialog("The image \"" + path + "\" is not a 32 bit per-channel image.")
        return
    
    # Get selected image infos
    width, height = orig.GetSize()
    bits = orig.GetBt()
    
    # Create the copy and initialize it
    copy = bitmaps.BaseBitmap()
    copy.Init(width, height, bits)
    
    # Calculate the number of bytes per pixel
    inc = orig.GetBt()/8 # Each pixel has RGB bits, so we need an offset of 'inc' bytes per pixel
                         # the image has 32 bits per-channel : (32*3)/8 = 12 bytes per pixel (1 byte = 8 bits)
                         # the image has 3 channels per pixel (RGB) : 12/3 = 4 bytes per component = 1 float
    
    # Create a byte sequence buffer large enough to store the copied image pixels
    sq = storage.ByteSeq(None, width*height*inc)
    
    for row in xrange(height):
        offset = sq.GetOffset(row*(width*inc)) # Offset on bitmap row + offset bytes per pixel
        orig.GetPixelCnt(0, row, width, offset, inc, c4d.COLORMODE_RGBf, c4d.PIXELCNT_0) # Read pixels from the original bitmap into the buffer
    
    #Example: RGB value of first pixel (only for 32 bits)
    #import struct
    #r, g, b = struct.unpack("fff", sq[0:12])
    #print r, g, b
    
    for row in xrange(height):
        offset = sq.GetOffset(row*(width*inc)) # Offset on bitmap row + offset bytes per pixel
        copy.SetPixelCnt(0, row, width, offset, inc, c4d.COLORMODE_RGBf, c4d.PIXELCNT_0) # Set pixels in bitmap copy
    
    bitmaps.ShowBitmap(orig) # Show original
    bitmaps.ShowBitmap(copy) # Show copied image

if __name__=='__main__':
    main()
