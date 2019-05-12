import sys
import threaded_downloader

#This whole code is for CLi arguments and for downloading those files  
inputargs = {}
sites = []
ddir = []

if '-r' in sys.argv:
    i=2
    r=True
else:
    i=1
    r=False
print(sys.argv)
while i < sys.argv.index('-f'):
       inputargs[sys.argv[i]] = float(sys.argv[i+1])
       i+=2
       
xy = sys.argv.index('-f')
xye = int(inputargs['-nf'])

print(inputargs)
print(sys.argv)
name = ['cat','dog'] 
for zxy in range(xye):
        sites.append(sys.argv[xy+zxy+1])
        ddir.append(sys.argv[xy+zxy+2+xye])

print(inputargs)
for i in range(len(sites)):
       threaded_downloader.download_file(sites[i],ddir[i],name[i],r)



'''
import sys
from threaded_downloader import *
#This whole code is for CLi arguments and for downloading those files  
inputargs = {}
site = []
ddir=[]
i=1
name = 'Cat'
while i < sys.argv.index('-f'):
       inputargs[sys.argv[i]] = float(sys.argv[i+1])
       i+=2
       
xy = sys.argv.index('-f')
xye = int(inputargs['-nf'])
siters = []
ddirr =[]
for zxy in range(xye):
        site.append(sys.argv[xy+zxy+1])
        ddir.append(sys.argv[xy+zxy+2+xye])
for i in range(len(site)):
        download_file(site[i],ddir[i],name,True)
'''
