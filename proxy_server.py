#!/usr/bin/env python
import socket, sys
import threading

try:
    listening_port = int(input("[*] Enter Listening Port Number: "))
except KeyboardInterrupt:  # to handle ctrl-c request to exit
    print("\n[*] User Requested An Interrupt")
    print(" [*] Application Exiting ...")
    sys.exit()

max_conn = 5  # max connection queues to hold
buffer_size = 10240  # max socket buffer size


def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initiate socket
        s.bind(('', listening_port))  # bind socket for listening
        s.listen(max_conn)
        print("[*] Initializing Sockets ... Done")
        print("[*] Sockets binded Successfully ...")
        print("[*] Server Started Successfully [ %d ]\n" % (listening_port))
    except Exception:

        print("[*] Unable to Initialize Socket")
        sys.exit(2)

    while 1:
        try:
            conn, addr = s.accept()  # Accept connection from client
            data = conn.recv(buffer_size)  # Receive client data
            print("Received: %s" % (data) )
            t = threading.Thread(target=conn_string, args=(conn, data, addr))
            t.daemon = True
            t._daemonic = True
            t.start()
        except KeyboardInterrupt:
            s.close()
            print("\n[*] Proxy Server Shutting Down ...")
            print("[*] Have A Nice Day")
            sys.exit()

    s.close()


def conn_string(conn, data, addr):  # Client Browser Requests Appear Here
    try:
        print("data %s" % (data) )
        data_parsed = data.splitlines()
        print("data_parsed %s" % (data_parsed))
        first_line = data_parsed[0]
        print("first_line %s" % (first_line))
        line_split = first_line.split()
        print("line_split %s" % (line_split))
        url = line_split[1]
        print("url: %s" % (url) )

        //http_pos = url.find("://")  # Find Position of ://
        print("http_pos = %d" % (http_pos))
        if http_pos == -1:
            temp = url
        else:

            temp = url[(http_pos+3):]   # get the rest of the url

        port_pos = temp.find(":")   # find the pos of the port if any

        webserver_pos = temp.find("/")  # find the end of the web server
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if (port_pos==-1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            #port is specified
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]
        print("proxy_srvr call")
        proxy_srvr(webserver, port, conn, addr, data)
    except Exception:
        pass



def proxy_srvr(webserver, port, conn, data, addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(webserver, port)
        s.send(data)

        while 1:    # read reply or data from end web server
            reply = s.recv(buffer_size)

            if (len(reply) > 0):
                conn.send(reply)    # send reply back to client
                # custom message to server
                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                print("[*] Request done: %s => %s <=" % (str(addr[0]),str(dar)))
            else:
                # Break connection if receiving data fails
                break
            # close server sockets
            s.close()
            # close client sockets
            conn.close()
    except socket.error:
        s.close()
        conn.close()
        sys.exit(1)

start()