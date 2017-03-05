#import socket module
from socket import *

serverSocket= socket(AF_INET, SOCK_STREAM)

'''
Prepare a server socket
'''

#Get IP Address of server (IPv6 not supported)
hostName= gethostname()
serverAddress=gethostbyname(hostName)

#Set up port
serverPort=90

#Bind socket to the port
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

while True:
    #Establish a connection
    print('Ready to serve...')
    connectionSocket, addr= serverSocket.accept()

    try:
        message= connectionSocket.recv(1024)
        filename= message.split()[1]
        f= open(filename[1:])

        lines= f.readlines()
        outputdata=[]
        for line in lines:
            b=bytearray()
            b.extend(map(ord,line))
            outputdata.append(b)
     
        '''Send 1 HTTP header line into socket'''

        connectionSocket.send(b'HTTP/1.0 200 OK\r\n')
        connectionSocket.send(b'Content-Type:text/html\r\n\r\n')

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
        connectionSocket.send(b'\r\n')

        #Close the connection socket
        connectionSocket.close()

    except IOError:
        '''Send response message for file not found'''
        connectionSocket.send(b'HTTP/1.0 200 OK\r\n')
        connectionSocket.send(b'Content-Type:text/html\r\n\r\n')
        connectionSocket.send(b'<html><body><h1>404 File Not Found</h1></body></html>')

        connectionSocket.close()

serverSocket.close()

            
        
