import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    

    path = '/myprojects/topnotchproject/$take/beautiful.tif'
    
    root = c4d.modules.tokensystem.StringExtractRoot(path)
    print(root)
    
    root = c4d.modules.tokensystem.FilenameExtractRoot(path)
    print(root)
    
    res = c4d.modules.tokensystem.FilenameSlicePath(path)
    print(res)

if __name__=='__main__':
    main()
