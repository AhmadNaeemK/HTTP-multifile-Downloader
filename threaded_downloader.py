import socket
import os,os.path
import threading
import time
import File_Merger


write_lock = threading.Lock()
def write_file(msg,fname,ftype,direct):
        os.chdir(direct)
        f = open(fname+'.' +ftype, 'ab')
        f.write(msg)
        f.close()
        
def write_file_new(msg,fname,ftype,direct):
        os.chdir(direct)
        f = open(fname+'.' +ftype, 'wb')
        f.write(msg)
        f.close()
        
def get_server_addess(site):
#procssing to string to sepearate server and address for http request
        if site.startswith('http://'):
                site = site[7:]
        server,address = site.split('/',1)
        address = '/' + address
        return (server,address)

def connect(server):
        #tcp connection establish
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server,80)
        cs.connect(server_address)
        return cs

def byte_range_download(s,q,contentlength,address,server,cs,type1,folder,flname,byterange,total_bytes):
        if b'bytes' in s[b'Accept-Ranges']:
                        q=10 #Incase of multiple connection we get this variable from user
                        write_lock.acquire()
                        request = 'GET ' + address + ' HTTP/1.1\r\nHOST: ' + server + '\r\nRange:bytes=' + byterange + '\r\n\r\n'
                        request_header = bytes(request,'utf-8')  
                        cs.send(request_header)

                        byterange = byterange.split('-')
                        
                        if int(byterange[1])>contentlength:
                                flag = contentlength
                        full_msg = 0
                        new_msg= True
                        c=True
                        start = time.time()
                        bytesRecv = 0
                        while c:
                                msg = cs.recv(15000)    
                                if new_msg:
                                        head = msg.split(b'\r\n\r\n')
                                        msg = head[1]
                                        new_msg = False
                                
                                full_msg += len(msg)
                                write_file(msg,flname,type1,folder)
                                bytesRecv +=len(msg)
                                total_bytes +=len(msg)
                                

                                if (time.time()- start >= 0.00005):
                                        print(flname+"Download speed = ", (bytesRecv/(time.time()-start))/1024 ,'kB/sec')  

                                        print("% Download Completion = ", (total_bytes/contentlength)*100)
                                        start = time.time()
                                        bytesRecv = 0

                                      
                                if full_msg== int(byterange[1])+1-int(byterange[0]):
                                        write_lock.release()
                                        new_msg = True
                                        full_msg =0
                                        c= False
                
def download_file(site,download_dir,filename,rflag):

        server,address = get_server_addess(site)
        cs = connect(server)

        #generating request and sending to know length of data
        request = 'HEAD ' + address + ' HTTP/1.1\r\nHOST: ' + server +'\r\n\r\n'
        request_header = bytes(request,'utf-8') 
        cs.send(request_header)
        
        #processing header to find content length of file to be downloaded
        header = cs.recv(4096)
        header = header.split(b'\r\n')
        
        s = {}
        for i in range(1,len(header)-2):
            y = header[i].split(b':')
            s[y[0]] = y[1]


        contentlength = int(s[b'Content-Length'])
        type1 = s[b'Content-Type'].split(b'/')[1]
        type1 = str(type1,'utf-8')

        #if file is resumable
        if b'Accept-Ranges' in s and rflag:
                startbyte = 0
                endbyte = contentlength//10
                threads_list = []
                for i in range(10):
                        byterange = "%s-%s"%(startbyte,endbyte)
                        name = filename+str(i)
                        resume_flag = File_Merger.getFileSize(name+'.'+type1,download_dir)
                        print(resume_flag,'flag')
                        if resume_flag-1 == endbyte-startbyte or resume_flag-1 ==contentlength%(contentlength//10):
                                print( name, 'Completely Donwloaded' )
                                startbyte = endbyte+1
                                endbyte += contentlength//10
                                
                                continue
                        elif resume_flag !=0:
                                print("this one executed")
                                startbyte = resume_flag
                              
                        print(name)
                        t = threading.Thread(target = byte_range_download , name = name , args = (s,10,contentlength,address,server,cs,
                                                                                                  type1,download_dir,name,byterange,startbyte))
                        startbyte = endbyte+1
                        endbyte += contentlength//10
                        threads_list.append(t)
                        t.start()
                for t in threads_list:
                        t.join()
                cs.close()
                #mergin all the downloaded chunks into one file
                File_Merger.mergeFiles(10, filename,type1 ,download_dir)
                print(filename, ' done')

        else:   #if file is not resumable
                if rflag:
                        print('Simulataneous connection not allowed using single connection')
                request = 'GET ' + address + ' HTTP/1.1\r\nHOST: ' + server + '\r\n\r\n'
                
                request_header = bytes(request,'utf-8')  
                cs.send(request_header)

                full_msg = b''
                new_msg= True
                c=True
                #variables for metrics
                total_time = time.time()
                start = time.time()
                bytesRecv = 0
                filesize=0
                while c:
                    msg = cs.recv(4096)
                            
                    if new_msg :
                        head = msg.split(b'\r\n\r\n')
                        header=(len(head[0]))+4
                        msg = head[1]
                        new_msg = False
                    #full_msg += msg
                    bytesRecv += len(msg) 
                    filesize += len(msg)
                    #calculating metrics
                    if (time.time()-start >= 1):
                            print(filename,"Download speed = ", (bytesRecv/(time.time()-start))/1024)
                            print(filename,"% Download Completion = ", (filesize/contentlength)*100)
                            start = time.time()
                            bytesRecv = 0
                    write_file(msg,filename,type1,download_dir)
                #breaking the loop if full file is recieved
                    if filesize== contentlength:
                        print(filename, "% Download Completion = ", (filesize/contentlength)*100)
                        print(filename,"Total Download speed = ", (filesize/(time.time()-total_time))/1024)
                        new_msg = True
                        #write_file(msg,filename,type1,download_dir)
                        full_msg = ""
                        filesize = 0
                        c= False
                        cs.close()         

                

                

site = 'http://i.imgur.com/z4d4kWk.jpg'

ddir= "C:\project"
download_file(site,ddir,'Cat',True)
