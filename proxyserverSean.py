from socket import *
import sys

if len(sys.argv) <= 1:
  print 'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server'
  sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start
tcpSerSock.bind((sys.argv[1],4390))
tcpSerSock.listen(1)
firstsend = "true"
# Fill in end.
while 1:
  # Start receiving data from the client
  print 'Ready to serve...'
  tcpCliSock, addr = tcpSerSock.accept()
  print 'Received a connection from:', addr
  # Fill in start
  message = tcpCliSock.recv(4096)
  # Fill in end
  print message
  # Extract the filename from the given message
  print message.split()[1]
  filename = message.split()[1].partition("/")[2]
  print filename
  fileExist = "false"
  filetouse = "/" + filename.replace("/","$")
  print filetouse
  try:
    # Check whether the file exist in the cache
    f = open(filetouse[1:], "r")
    outputdata = f.readlines()
    fileExist = "true"
    # ProxyServer finds a cache hit and generates a response message
    tcpCliSock.send("HTTP/1.0 200 OK\r\n")
    tcpCliSock.send("Content-Type:text/html\r\n")
    # Fill in start.
    for i in range(0, len(outputdata)):
      tcpCliSock.send(outputdata[i])
    # Fill in end.
    print 'Read from cache'
  # Error handling for file not found in cache
  except IOError:
    if fileExist == "false":
      # Create a socket on the proxyserver
      # Fill in start
      filenamesplit = filename.split("/",1)
      path = ""
      if len(filenamesplit) == 2:
        path = filenamesplit[1]
      c = socket(AF_INET, SOCK_STREAM)
      # Fill in end
      hostn = filenamesplit[0].replace("www.","",1)
      print hostn
      try:
        # Connect to the socket to port 80
        # Fill in start.
        c.connect((hostn, 80))          
        # Fill in end.
        # Create a temporary file on this socket and ask port 80 for the file requested by the client
        fileobj = c.makefile('r', 0)
        #print "GET " , "http://" , filename , " HTTP/1.0\r\n\r\n"
        fileobj.write(message.replace(filenamesplit[0],"",1))
        # Read the response into buffer
        # Fill in start.
        buffer1 = fileobj.readlines()
        # Fill in end.
        # Create a new file in the cache for the requested file.
        # Also send the response in the buffer to client socket and the corresponding file in the cache
        tmpFile = open("./" + filename.replace("/","$"),"wb")
        # Fill in start.
        for i in range(0, len(buffer1)):
          tcpCliSock.send(buffer1[i])
          tmpFile.write(buffer1[i])
        # Fill in end.
      except:
        print "Illegal request"
        tcpCliSock.send("HTTP/1.0 404 NOT FOUND\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")
        tcpCliSock.send("\n")
        tcpCliSock.send("""<html><body><h1>404 Not Found</body></html>""")
    else:
      # HTTP response message for file not found
      # Fill in start.
      tcpCliSock.send("HTTP/1.0 404 NOT FOUND\r\n")
      tcpCliSock.send("Content-Type:text/html\r\n")
      tcpCliSock.send("<html><body><h1>404 Not Found</body></html>")
      # Fill in end.
  # Close the client and the server sockets
  tcpCliSock.close()
# Fill in start.
tcpSerSock.close()
# Fill in end.
