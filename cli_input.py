import sys
from client_http_ahmad import *
#This whole code is for CLi arguments and for downloading those files  
inputargs = {}
sites = []
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
        sites.append(sys.argv[xy+zxy+1])
        ddir.append(sys.argv[xy+zxy+2+xye])
for i in range(len(sites)):
        download_file_specificRange(sites[i],ddir[i],name,0,1024)
