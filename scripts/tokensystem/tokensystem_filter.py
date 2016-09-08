import c4d
from c4d import gui
#Welcome to the world of Python


def main():
   
    
    renderData = doc.GetActiveRenderData()
    renderSettings = renderData.GetData()
    
    path = renderSettings[c4d.RDATA_PATH]
    
    # or just 
    path = '/myprojects/topnotchproject/theimage_$frame_$prj.png'
    
    print(path)
    
    # This example applies some filters
    
    # setup RenderPathData
    rpd = {'_doc': doc, '_rData': renderData, '_rBc': renderSettings, '_frame': 1}
    
    # exclude the project name
    exclude = ['prj']
    
    finalFilename = c4d.modules.tokensystem.StringConvertTokensFilter(path, rpd, exclude)  
    print(finalFilename)
    
    finalFilename = c4d.modules.tokensystem.FilenameConvertTokensFilter(path, rpd, exclude)  
    print(finalFilename)
    
    

if __name__=='__main__':
    main()
