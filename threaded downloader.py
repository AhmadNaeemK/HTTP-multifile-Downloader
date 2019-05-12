import socket
import os,os.path
import threading
import time

write_lock = threading.Lock()
def write_file(msg,x,ftype,direct):
        os.chdir(direct)
        #f = open('Socket'+str(x)+'.' +ftype, 'ab')
        f = open(x+'.' +ftype, 'ab')
        f.write(msg)
        f.close()
def write_file1(msg,x,ftype,direct):
        os.chdir(direct)
        #f = open('Socket'+str(x)+'.' +ftype, 'wb')
        f = open(x+'.' +ftype, 'wb')
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

def byte_range_download(s,q,contentlength,address,server,cs,type1,folder,name,byterange):
        if b'bytes' in s[b'Accept-Ranges']  :
                        #loop for multiple get requests
                        #new_msg= True
                        q=10 #Incase of multiple connection we get this variable from user
                        previousB= 0
                        nextB = contentlength//q
                        #nextB = 18000               
                        #write_lock.acquire()
        
                        #time.sleep(3)
                                #bRange = "%s-%s"%(previousB,nextB)
                        
                        write_lock.acquire()
                        
                        request = 'GET ' + address + ' HTTP/1.1\r\nHOST: ' + server + '\r\nRange:bytes=' + byterange + '\r\n\r\n'
                       # print(request)
                        request_header = bytes(request,'utf-8')  
                        cs.send(request_header)
                        #previousB = nextB + 1
                        #flag = nextB
                        if nextB>contentlength:
                                flag = contentlength
                        nextB += contentlength//q
                        #print(nextB)
                        byterange = byterange.split('-')
                        full_msg = b''
                        new_msg= True
                        c=True
                                
                        while c:
                                msg = cs.recv(15000)
                                print(name)    
                                #if name =='file0' and new_msg:
                                if new_msg:
                                        
                                        #print(msg)
                                        head = msg.split(b'\r\n\r\n')
                                        #header=(len(head[0]))+4
                                        #heads = (head[0])
                                        #print(header)
                                        msg = head[1]
                                        new_msg = False
                                
                                #else:
                                 #       msg = msg.split(b'')
                                  #      msg = msg[1]
                                #print(msg)
                                #contentlength1 = contentlength//10

                                #print(len(msg))
                                #c+=len(msg)
                                
                                full_msg = full_msg + msg
                                print('Fullmsg',len(full_msg))
                                print('bytres',int(byterange[1])+1-int(byterange[0]))
                                write_file(msg,name,type1,folder)
                                
                                if len(full_msg)== int(byterange[1])+1-int(byterange[0]):
                                        write_lock.release()
                                        #print(full_msg[header:])
                                        print('Done through special loop')
                                        #write_file(full_msg,3,type1)
                                        new_msg = True
                                        
                                        c= False
                                        #cs.close()
                
def download_file(site,download_dir):

        server,address = get_server_addess(site)
        cs = connect(server)

        #generating request and sending to know length of data
        request = 'HEAD ' + address + ' HTTP/1.1\r\nHOST: ' + server +'\r\nAccept-Ranges: bytes\r\n\r\n'
        request_header = bytes(request,'utf-8') 
        cs.send(request_header)
        
        #processing header to find content length of file to be downloaded
        header = cs.recv(2096)
        header = header.split(b'\r\n')
        
        s = {}
        for i in range(1,len(header)-2):
            y = header[i].split(b':')
            s[y[0]] = y[1]
            #print(y)
        contentlength = int(s[b'Content-Length'])
        type1 = s[b'Content-Type'].split(b'/')[1]
        type1 = str(type1,'utf-8')
        if b'Accept-Ranges' in s:
                startbyte = 0
                endbyte = contentlength//10
                threads_list = []
                for i in range(10):
                        byterange = "%s-%s"%(startbyte,endbyte)
                        name = 'file{}'.format(i)
                        t = threading.Thread(target = byte_range_download , name = name , args = (s,10,contentlength,address,server,cs,type1,download_dir,name,byterange))
                        startbyte = endbyte+1
                        endbyte += contentlength//10
                        threads_list.append(t)
                        t.start()
                        #byte_range_download(s,10,contentlength,address,server,cs,type1,download_dir,name)
                for t in threads_list:
                        t.join()
                cs.close()
        else:
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
                        print(head[0])
                        print(header)
                        msg = head[1]
                        new_msg = False
                        po +=1
                    #print("tis one did it" )
                    full_msg += msg
                    write_file(msg,name,type1,2,download_dir)
                    if len(full_msg)== contentlength:
                        print(full_msg[header:])
                        print('Done')
                        new_msg = True
#                                write_file(full_msg,2)
                        full_msg = ""
                        c= False
                        cs.close()         
                

                
#Main Function
site = 'http://open-up.eu/files/Berlin%20group%20photo.jpg?width=600&height=600'
#site = 'http://people.unica.it/vincenzofiorentini/files/2012/04/Halliday-Fundamentals-of-Physics-Extended-9th-HQ.pdf'
#site = 'http://africhthy.org/sites/africhthy.org/files/styles/slideshow_large/public/Lukuga.jpg?itok=M6ByJTZQ'
#site = 'http://ipaeg.org/sites/ipaeg.org/files/styles/medium/public/IMG_0499.JPG?itok=U8KP8f4j'
#site = 'http://s0.cyberciti.org/images/misc/static/2012/11/ifdata-welcome-0.png'
site = 'http://i.imgur.com/z4d4kWk.jpg'

#server,address = get_server_address(site)
ddir= "D:\Movies"
#i=1
#name = 'file{}'.format(i)
#t = threading.Thread(target = download_file , name = name , args = (site,ddir,name))
#t.start()
download_file(site,ddir)
