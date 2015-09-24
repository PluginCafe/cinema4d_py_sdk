import c4d
from c4d import gui

#Author: s_bach
#TakeSystem Example


def main():
    
    # This example checks if the current Take is the main take. If not, the main take becomes the current take.
    
    takeData = doc.GetTakeData()
    if takeData is None:
        return
    
    folder = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Select Folder", c4d.FILESELECT_DIRECTORY)
    if folder is None:
        return
    
    # This code only loops through the child takes of the main take, but not through further child takes!
    # The folder to save the files must be defined with "folder".
    
    mainTake = takeData.GetMainTake()
    childTake = mainTake.GetDown()
    
    while childTake is not None:
        
        takeDoc = takeData.TakeToDocument(childTake)
        
        if takeDoc is not None:
            
            fileName = childTake.GetName() + ".c4d"
            fullFileName = folder + "\\" + fileName
            
            c4d.documents.SaveDocument(takeDoc, fullFileName, saveflags=c4d.SAVEDOCUMENTFLAGS_0,format=c4d.FORMAT_C4DEXPORT)
        
        childTake = childTake.GetNext()
    

if __name__=='__main__':
    main()
