###########################################################
# Cinema 4D SDK                                           #
###########################################################
# (c) 1989-2011 MAXON Computer GmbH, all rights reserved  #
###########################################################

#This plugin is a short example how to write custom bitmap
#saver/loader. You can try this plugin by set Py-XAMPLE
#as output format in the rendersettings of your document.

import c4d
import struct
import bz2

from c4d import plugins, gui

#be sure to use a unique ID obtained from 'plugincafe.com'
PLUGIN_ID_S = 1025254
PLUGIN_ID_L = 1025255

BMP_NAME = "Py-XAMPLE"
BMP_IDENTIFIER = "XAMPLE"
BMP_SUFFIX = "xample"

# Image bz2 compressed + 24 bits per 
# See header file after decompressed:
#
# ====================+=====================================+
# | XAMPLE(identifier)| 24 bits (bitdepth, width, height)   |
# +===================+=====================================+
# | bz2compressed(each component 1 byte (red, green, blue)  |
# +===================+=====================================+

class MyXampleLoader(plugins.BitmapLoaderData):
    """Data class to read a *.xample file"""

    def Identify(self, name, probe, size):
        #check if image starts with identifier flag
        return probe[:len(BMP_IDENTIFIER)]==BMP_IDENTIFIER
    
    def Load(self, name, bm, frame):
        with open(name, "rb") as fn:
            lines = fn.read()[len(BMP_IDENTIFIER):] #skip identifier
            size = struct.calcsize("iii")
            psize = struct.calcsize("ccc")
            
            #extract bitdepth, width and height information
            bt, width, height = struct.unpack("iii", lines[:size])
            bm.Init(width, height, bt/3)
            # remove the offset so we can start with position 0 of the pixel information
            lines = lines[size:]
            #uncompress the pixel decompress to raw data
            lines =  bz2.decompress(lines)
            for x in xrange(width):
                for y in xrange(height):
                    fr = (y*width*psize)+(x*psize)
                    #extract red, green, blue information
                    r, g, b = struct.unpack("ccc", lines[fr:fr+psize])
                    bm[x, y] = ord(r), ord(g), ord(b)
        
        return c4d.IMAGERESULT_OK


class MyXampleSaver(plugins.BitmapSaverData):
    """Data class to write a *.xample file"""

    COMPRESSION = 1000
    STANDARD_COMP = 9
    
    def Edit(self, data):
        """Dialog to change the compression level"""
        std = data.GetLong(self.COMPRESSION, self.STANDARD_COMP)
        while True:
            result = gui.InputDialog(title="Compression", preset=std)
            if result==None: return True
            
            try:
                result = int(result)
            except ValueError, e:
                gui.MessageDialog(e, c4d.GEMB_OK)
                continue
            
            if result<=1 or result>9:
                gui.MessageDialog("Value '%i' must be between 1 and 9." % (result), c4d.GEMB_OK)
                #so if not between 1 and 9, try again...
                continue
            
            #set the compress depth
            data.SetLong(self.COMPRESSION, result)
            return True
    
    
    def Save(self, fn, bmp, data, savebits):
        with open(fn, "wb") as fn:
            width, height = bmp.GetSize()
            #write identifier first...
            fn.write(BMP_IDENTIFIER)
            #.. and write some meta information
            p = struct.pack("iii", bmp.GetBt(), bmp.GetBw(), bmp.GetBh())
            fn.write(p)
            
            #including bz2 compression
            content = ""
            for y in xrange(height):
                for x in xrange(width):
                    r, g, b = bmp[x, y]
                    #write the red, green, blue component
                    content += struct.pack("ccc", chr(r), chr(g), chr(b))
            
            #lets compress the content now
            compression=data.GetLong(self.COMPRESSION, self.STANDARD_COMP)
            fn.write(bz2.compress(content, compression))
        
        return c4d.IMAGERESULT_OK


if __name__=="__main__":
    #registration routine for the bitmap loader and saver
    plugins.RegisterBitmapLoaderPlugin(id=PLUGIN_ID_L, str=BMP_NAME,
                                            info=0, dat=MyXampleLoader())
    
    plugins.RegisterBitmapSaverPlugin(id=PLUGIN_ID_S, str=BMP_NAME,
                                            info=c4d.PLUGINFLAG_BITMAPSAVER_ALLOWOPTIONS|c4d.PLUGINFLAG_BITMAPSAVER_SUPPORT_8BIT|c4d.PLUGINFLAG_BITMAPSAVER_FORCESUFFIX,
                                            dat=MyXampleSaver(), suffix=BMP_SUFFIX)
