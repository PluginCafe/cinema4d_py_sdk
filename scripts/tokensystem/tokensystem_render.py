import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    
    # // This example renders a BaseDocument and saves the resulting image using a filename handling tokens:

    bitmap = c4d.bitmaps.BaseBitmap()
    bitmap.Init(1280, 720)
    
    renderData = doc.GetActiveRenderData()
    renderSettings = renderData.GetData()
    renderSettings[c4d.RDATA_XRES] = 1280
    renderSettings[c4d.RDATA_YRES] = 720
    
    path = renderSettings[c4d.RDATA_PATH]
    
    res = c4d.documents.RenderDocument(doc, renderSettings, bitmap, c4d.RENDERFLAGS_NODOCUMENTCLONE, None)
    
    if res == c4d.RENDERRESULT_OK:
            
        rpd = {'_doc': doc, '_rData': renderData, '_rBc': renderSettings, '_frame': 1}
        finalFilename = c4d.modules.tokensystem.StringConvertTokens(path, rpd) + ".png"
        
        bitmap.Save(finalFilename, c4d.FILTER_PNG)

if __name__=='__main__':
    main()
