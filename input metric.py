

import ahmeddd
print('enter -n	Total number of simultaneous connections')
      
n=input('enter here')


print('enter -i	Time interval in seconds between metric reporting')

i=input('write value')



print('enter nf Number of files to download')
nf=int(input())

filename=[]
for x in range(nf):
   
    print('enter file:',x)
    filename.append(input())


print(filename)


print( "enter -o    Addresses pointing to the location where the files are downloaded")

print('directory is preset')


ahmeddd.download_file(filename[0])
