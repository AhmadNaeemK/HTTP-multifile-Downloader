import os
#filename without number or extension
def mergeFiles(noFiles, fileName,ftype ,directory):
    os.chdir(directory)
    data = b''
    for i in range(noFiles):
        f = open(fileName + str(i)+'.' + ftype,'rb')
        data += f.read()
        f.close()

    file = open(fileName + '.' + ftype, 'wb')
    file.write(data)
    file.close()
    for i in range(noFiles):     #to delete the individual chunks
        f=directory+"/"+fileName + str(i)+'.' + ftype
        print(f)
        os.remove(f)
    

mergeFiles(10,'file','png','C:/Project')
print('done')

