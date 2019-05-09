import socket
import os,os.path

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('httpbin.org', 80)
#server_address = ('wikimedia.org', 80)
#server_address = ("open-up.eu",80)
cs.connect(server_address)


#request_header = b'HEAD /files/Berlin%20group%20photo.jpg HTTP/1.1\r\nHOST: open-up.eu\r\n\r\n' 
request_header = b'HEAD /image/png HTTP/1.1\r\nHOST: httpbin.org\r\n\r\n'
cs.send(request_header)

header = cs.recv(2096)
header = header.split(b'\r\n')
s = {}
for i in range(1,len(header)-2):
    y = header[i].split(b':')
    s[y[0]] = y[1]
    print(y)
contentlength = int(s[b'Content-Length'])
#header = len(header)
#print(header)
#request_data = b'GET /files/Berlin%20group%20photo.jpg HTTP/1.1\r\nHOST: open-up.eu\r\n\r\n' 
request_data = b'GET /image/png HTTP/1.1\r\nHOST: httpbin.org\r\n\r\n'
cs.send(request_data)


full_msg = b''
new_msg= True
c=True
while c:
    msg = cs.recv(4096)
    if new_msg:
        head = msg.split(b'\r\n\r\n')
        header=(len(head[0]))+4
        print(header)

        new_msg = False

#    print(msg)
    full_msg += msg 
#    print(len(full_msg))


    if len(full_msg)-header== contentlength:
        print(full_msg[header:])
        print('Done')
        f = open('Socket8.jpg', 'wb')
        f.write(full_msg[header:])
        f.close()
        new_msg = True
        full_msg = ""
        new_msg = True
        c= False
        cs.close()
