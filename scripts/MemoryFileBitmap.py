"""
MemoryFile Bitmap

Example for:
MemoryFileStruct
HyperFile
ByteSeq

This example shows how to write/read a bitmap to/from a memory file using the important storage class MemoryFileStruct.
"""

import c4d
from c4d import bitmaps, storage

def WriteBitmap(bmp, format=c4d.FILTER_B3D,settings=c4d.BaseContainer()):
    """
    Write an hyper file image to a buffer object
    
    @return: The byte sequence or None
    
    @img: The image to convert into a buffer object
    @format: The filter type
    @settings: Optional settings
    """
    
    mfs = storage.MemoryFileStruct()
    mfs.SetMemoryWriteMode()
    
    hf = storage.HyperFile()
    if hf.Open(0, mfs, c4d.FILEOPEN_WRITE, c4d.FILEDIALOG_NONE):
        if not hf.WriteImage(bmp,format,settings):
            return None
        hf.Close()
    
    byteseq, size = mfs.GetData()
    return byteseq, size

def ReadBitmap(byteseq):
    """
    Creates a bitmap from a buffer object.
    
    @return: The image if succeeded, otherwise False
    
    @byteseq: The buffer object.
    """
    
    bmp = bitmaps.BaseBitmap()
    hf = storage.HyperFile()
    mfs = storage.MemoryFileStruct()
    
    bmp = None
    mfs.SetMemoryReadMode(byteseq, len(byteseq))
    if hf.Open(0, mfs, c4d.FILEOPEN_READ, c4d.FILEDIALOG_NONE):
        bmp = hf.ReadImage()
        hf.Close()
    
    return bmp


def main():
    path = storage.LoadDialog(type=c4d.FILESELECTTYPE_IMAGES, title="Please Choose an Image:")
    if not path: return
    
    # Create and initialize selected image
    img = bitmaps.BaseBitmap()
    if img.InitWith(path)[0] != c4d.IMAGERESULT_OK:
        gui.MessageDialog("Cannot load image \"" + path + "\".")
        return
    
    byteseq, size = WriteBitmap(img) # Save image to hyper file in byte sequence
    bmp = ReadBitmap(byteseq) # Read image from the byte sequence
    
    bitmaps.ShowBitmap(bmp)

if __name__=='__main__':
    main()
