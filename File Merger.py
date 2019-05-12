import os
#filename without number or extension
def mergeFiles(noFiles, fileName,ftype ,directory):
    os.chdir(directory)
    data = b''
    for i in range(noFiles):
        f = open(fileName + str(i)+'.' + ftype,'rb')
        data += f.read()
        f.close()
    
    for i in range(noFiles):
        f = open(fileName + str(i)+'.' + ftype,'rb')
        f.close()
        os.remove(fileName + str(i)+'.' + ftype)
    
    
    file = open(fileName + '.' + ftype, 'wb')
    file.write(data)
    file.close()

#filename  including extension
def getFileSize(filename,directory):
    os.chdir(directory)
    fileSize = os.stat(filename).st_size
    fileSize = int (fileSize)
    print (fileSize)
    
mergeFiles(10,'Cat','jpeg', 'C:\Project')
