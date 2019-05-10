import socket
import os,os.path

def get_server_addess(site):
#procssing to string to sepearate server and address for http request
        if site.startswith('http://'):
                site = site[7:]
        server,address = site.split('/',1)
        address = '/' + address
        return (server,address)


def connect(server,address):
        #tcp connection establish
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server,80)
        cs.connect(server_address)
        return cs

def download_file(site):

        server,address = get_server_addess(site)
        cs = connect(server,address)

        #generating request and sending to know length of data
        request = 'HEAD ' + address + ' HTTP/1.1\r\nHOST: ' + server +'\r\n\r\n'
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

        #requesting again to download file
        request = 'GET ' + address + ' HTTP/1.1\r\nHOST: ' + server + '\r\n\r\n'
        request_header = bytes(request,'utf-8')  
        cs.send(request_header)

        #downloading and saving
        full_msg = b''
        new_msg= True
        c=True
        msg_1=True
        while c:
            msg = cs.recv(4096)

            if msg_1:
                msg2 = msg.split(b'\r\n\r\n')[0]
                msg2 = msg2.split(b'\r\n')
                print(msg2)
                s1 = {}
                for i in range(0,len(msg2)):
                    y1 = msg2[i]
                    print(y1)
                msg_1 = False
                    
            if new_msg:
                head = msg.split(b'\r\n\r\n')
                header=(len(head[0]))+4
                print(header)
                msg = head[1]
                new_msg = False

            full_msg += msg 

            if len(full_msg)== contentlength:
                #sprint(full_msg[header:])
                print('Done')
                write_file(full_msg,2)
                new_msg = True
                full_msg = ""
                c= False
                cs.close()
                
def write_file(msg,x):
        f = open('Socket'+str(x)+'.pdf', 'wb')
        f.write(msg)
        f.close()
                
                
#Main Function
site = 'http://open-up.eu/files/Berlin%20group%20photo.jpg?width=600&height=600'
#site = 'http://people.unica.it/vincenzofiorentini/files/2012/04/Halliday-Fundamentals-of-Physics-Extended-9th-HQ.pdf'
#server,address = get_server_address(site)
download_file(site)
