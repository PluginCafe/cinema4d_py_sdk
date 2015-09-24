"""
MemoryFile Data

Example for:
MemoryFileStruct
HyperFile
ByteSeq

This example shows how to write/read simple data to/from a memory file using the important storage class MemoryFileStruct.
"""

import c4d
from c4d.storage import HyperFile, MemoryFileStruct


def WriteMemoryFile():
    """
    Write data to a memory file
    
    @return: The byte sequence or None
    """
    
    mfs = MemoryFileStruct()
    # Set the memory file ready to be written to
    mfs.SetMemoryWriteMode()
    
    file = HyperFile()
    # Open the memory file as an HyperFile
    file.Open(0, mfs, c4d.FILEOPEN_WRITE, c4d.FILEDIALOG_NONE)
    
    # Write a string to the memory file
    file.WriteString("MemoryFileStruct Example")
    # Write an integer to the memory file
    file.WriteLong(1214)
    
    #Close the file
    file.Close()
    
    # Return the memory file data
    return mfs.GetData()[0]


def ReadMemoryFile(data):
    """
    Read data from a memory file
    """
    
    mfs = MemoryFileStruct()
    # Set the memory file ready to be read from
    mfs.SetMemoryReadMode(data, len(data))
    
    file = HyperFile()
    # Open the memory file and set it ready for reading
    file.Open(0, mfs, c4d.FILEOPEN_READ, c4d.FILEDIALOG_NONE)
    
    # Read the string from the memory file
    value = file.ReadString()
    print "The string value is :", value
    
    # Read the int from the memory file
    value = file.ReadLong()
    print "The int value is :", value
    
    # Close file
    file.Close()


def main():
    bytes = WriteMemoryFile()
    ReadMemoryFile(bytes)

if __name__=='__main__':
    main()
