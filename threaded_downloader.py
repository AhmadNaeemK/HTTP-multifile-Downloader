import socket
import os,os.path
import threading
import time
import File_Merger

write_lock = threading.Lock()
def write_file(msg,fname,ftype,direct):
        os.chdir(direct)
        #f = open('Socket'+str(x)+'.' +ftype, 'ab')
        f = open(fname+'.' +ftype, 'ab')
        f.write(msg)
        f.close()
def write_file1(msg,fname,ftype,direct):
        os.chdir(direct)
        #f = open('Socket'+str(x)+'.' +ftype, 'wb')
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

def byte_range_download(s,q,contentlength,address,server,cs,type1,folder,flname,byterange):
        if b'bytes' in s[b'Accept-Ranges']  :
                        q=10 #Incase of multiple connection we get this variable from user
                        write_lock.acquire()
                        
                        request = 'GET ' + address + ' HTTP/1.1\r\nHOST: ' + server + '\r\nRange:bytes=' + byterange + '\r\n\r\n'
                        request_header = bytes(request,'utf-8')  
                        cs.send(request_header)

                        byterange = byterange.split('-')
                        
                        if int(byterange[1])>contentlength:
                                flag = contentlength
                        full_msg = b''
                        new_msg= True
                        c=True
                                
                        while c:
                                msg = cs.recv(15000)
                                print(flname)    
                                if new_msg:
                                        head = msg.split(b'\r\n\r\n')
                                        msg = head[1]
                                        new_msg = False
                                
                                full_msg = full_msg + msg
                                write_file(msg,flname,type1,folder)
                                
                                if len(full_msg)== int(byterange[1])+1-int(byterange[0]):
                                        write_lock.release()
                                        print('Done through special loop')
                                        new_msg = True
                                        c= False
                
def download_file(site,download_dir,filename,rflag):

        server,address = get_server_addess(site)
        cs = connect(server)

        #generating request and sending to know length of data
        request = 'HEAD ' + address + ' HTTP/1.1\r\nHOST: ' + server +'\r\nAccept-Ranges: bytes\r\n\r\n'
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
        
        if b'Accept-Ranges' in s and rflag:
                startbyte = 0
                endbyte = contentlength//10
                threads_list = []
                for i in range(10):
                        byterange = "%s-%s"%(startbyte,endbyte)
                        name = filename+str(i)
                        print(name)
                        t = threading.Thread(target = byte_range_download , name = name , args = (s,10,contentlength,address,server,cs,
                                                                                                  type1,download_dir,name,byterange))
                        startbyte = endbyte+1
                        endbyte += contentlength//10
                        threads_list.append(t)
                        t.start()
                for t in threads_list:
                        t.join()
                cs.close()
                File_Merger.mergeFiles(10, filename,type1 ,download_dir)
        else:
                if rflag:
                        print('Simulataneous connection not allowed using single connection')
                request = 'GET ' + address + ' HTTP/1.1\r\nHOST: ' + server + '\r\n\r\n'
                
                request_header = bytes(request,'utf-8')  
                cs.send(request_header)

                full_msg = b''
                new_msg= True
                c=True
                
                while c:
                    msg = cs.recv(4096)
                    if new_msg :
                        head = msg.split(b'\r\n\r\n')
                        header=(len(head[0]))+4
                        msg = head[1]
                        new_msg = False
                    full_msg += msg
                    write_file1(msg,filename,type1,download_dir)
                    if len(full_msg)== contentlength:
                        print('Done')
                        new_msg = True
                        full_msg = ""
                        c= False
                        cs.close()         

                

                
#Main Function
site = 'http://open-up.eu/files/Berlin%20group%20photo.jpg?width=600&height=600'
#site = 'http://people.unica.it/vincenzofiorentini/files/2012/04/Halliday-Fundamentals-of-Physics-Extended-9th-HQ.pdf'
#site = 'http://africhthy.org/sites/africhthy.org/files/styles/slideshow_large/public/Lukuga.jpg?itok=M6ByJTZQ'
#site = 'http://ipaeg.org/sites/ipaeg.org/files/styles/medium/public/IMG_0499.JPG?itok=U8KP8f4j'
#site = 'http://s0.cyberciti.org/images/misc/static/2012/11/ifdata-welcome-0.png'
#site = 'http://i.imgur.com/z4d4kWk.jpg'

#server,address = get_server_address(site)
ddir= "C:\Project"
download_file(site,ddir,'Cat',True)
