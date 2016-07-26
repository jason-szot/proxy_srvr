#!/usr/bin/env python
import socket, sys
import threading

try:
    listening_port = int(input("[*] Enter Listening Port Number: "))
except KeyboardInterrupt:  # to handle ctrl-c request to exit
    print("\n[*] User Requested An Interrupt")
    print(" [*] Application Exiting ...")
    sys.exit()

max_conn = 5  # max connection queues to hold - 5 seems to work the best
buffer_size = 4096  # max socket buffer size


def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initiate socket
        s.bind(('', listening_port))  # bind socket for listening
        s.listen(max_conn)
        print("[*] Initializing Sockets ... Done")
        print("[*] Sockets binding Successfully ...")
        print("[*] Server Started Successfully [ %d ]\n" % listening_port)
    except Exception:

        print("[*] Unable to Initialize Socket")
        sys.exit(2)

    while 1:
        try:
            conn, addr = s.accept()  # Accept connection from client
            data = conn.recv(buffer_size)  # Receive client data
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
        data_parsed = data.splitlines()
        first_line = data_parsed[0]
        line_split = first_line.split()
        url = line_split[1]

        ###################     Parse TCP packet to scrape url and port for opening a socket    ########
        url_parse_1 = url.split(b'://')  # get rid of leading part
        url_1 = url_parse_1[1]             # assign webserver section
        url_parse_2 = url_1.split(b'/')     # split off the trailing /
        url_2 = url_parse_2[0].split(b':')  # split for a port, if any
        webserver = url_2[0]
        print("Received request for %s" % url_1)
        if len(url_2)==1:   # if len = 1, no port was specified
            port = 80
        else:
            port = url_2[1]
        port = 80

        #       check if file is in cache
        try:
            cache_file = open("./cache/" + url_1.replace("/","_"), "r")
            print("Cache hit")
            outputdata = cache_file.readlines()
            for i in (0, len(outputdata)):
                conn.send(outputdata[i])
            conn.close()
        except IOError: # not in cache
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((webserver, port))
                s.send(data)

                while 1:
                    temp = s.recv(buffer_size)
                    print("open file")
                    cache_file = open("./cache/" + url_1.replace("/", "_"), "wb")
                    print("Cache write")
                    cache_file.write(temp)
                    if (len(temp) > 0):
                        conn.send(temp)

                    else:
                        break
                s.close()
                conn.close()
                print("Handled request for %s from %s" % (webserver, addr[0]))
            except socket.error:
                if s:
                    s.close()
                if conn:
                    conn.close()
                print("Peer Reset")
                exit(1)
    except Exception:
        exit(1)


start()