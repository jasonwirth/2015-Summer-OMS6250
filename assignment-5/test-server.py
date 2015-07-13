#!/usr/bin/python

"Test server - This opens up the port specified by the user in the command \
    line. Repeats back what it hears and closes."

# Based on http://pymotw.com/2/socket/tcp.html


import sys
import socket

if not (len(sys.argv) == 3):
    print "Syntax:"
    print "    python test-server.py <server-ip> <port>"
    print "  server-ip is the IP address of the server - use ifconfig to find."
    print "  port is the TCP port to open a socket on."
    exit()


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (sys.argv[1], int(sys.argv[2]))
print >>sys.stderr, 'starting up on %s port %s' % server_address
server_str = '{0} {1}'.format(*server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    client_str = '{0} {1}'.format(*client_address) 
    try:
        print >>sys.stderr, '[{server_str}] connection from {client_str}'.format(**locals())

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print >>sys.stderr, '[{server_str}] received {client_str} "{data}"'.format(**locals())
            if data:
                print >>sys.stderr, '[{server_str}] sending data back to the client {client_str}'.format(**locals())
                connection.sendall(data)
            else:
                print >>sys.stderr, '[{server_str}] no more data from {client_str}'.format(**locals())
                break
            
    finally:
        # Clean up the connection
        connection.close()
