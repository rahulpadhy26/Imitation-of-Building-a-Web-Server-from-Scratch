#!/Users/rapadhy/anaconda3/bin/python

import socket


# Socket programming is a way of connecting 2 nodes on a network to communicate with each other.
# 1 socket (node) listens on a particular port at an IP, while other socket reaches out to the 1st one to form a connection.
HOST, PORT = '', 8888

# The arguments passed to socket() specify the address family and socket type.
# 'AF_INET' is the Internet address family for IPv4.
# 'SOCK_STREAM' is the socket type for TCP, the protocol that will be used for transferring messages in the network.'
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Setting this socket option avoids the error 'Address already in Use' - this may occur when starting the server and a previously used TCP socket on the same port has connections in the TIME_WAIT state
# e.g., if the server actively closed a connection, it will remain in the TIME_WAIT state for 2 minutes or more, depending on the OS.
# If an attempt is made to start the server again before the TIME_WAIT state expires, an OSError exception of 'Address already in use' is received.
# The following is a safeguard to make sure that any delayed packets in the network aren't delivered to the wrong application.
# When retrieving a a socket option, or setting it, the option name as well as the level are specified.
# When level=SOL_SOCKET, the item will be searched for in the socket itself.
# Here, its desired to set the socket option to re-use the address to 1 (ON / True) - so, SO_REUSEADDR in listen_socket is set to 1.
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind() is used to associate the socket with a specific network interface and port number.
# The values passed to bind() depend on the address family of the socket.
# Since, socket.AF_INET(IPv4) is used here, so a 2-tuple (host, port) is expected. 
listen_socket.bind((HOST, PORT))

# listen() enables a server to accept() connections; listen() makes it a 'listening' socket.
listen_socket.listen(1)

print (f'Serving HTTP on port {PORT} ...')

while True:

    # accept() blocks and waits for an incoming connection.
    # When a client connects, it returns a new socket object representing the connection and a tuple holding the address of the client.
    # The tuple will contain (host, port) for IPv4 connections or (host, port, scopeid) for IPv6.
    client_connection, client_address = listen_socket.accept()

    # This reads whatever data the client sends.
    # recv() is a blocking call, i.e., its a socket function that temporarily suspends the application.
    # Blocking calls have to wait on system calls (I/O) to complete before they can return a value.
    # recv() reads whatever data the client sends.
    # The bufsize argument of 1024 used below is the maximum amount of data to be received at once.
    # It doesn't mean that recv() will return 024 B.
    request_data = client_connection.recv(1024)
    
    print (request_data.decode('utf-8')) 
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""

    # The sendall() method continues to send data from Bytes until either all data has been sent or an error occurs.
    # None is returned on success.
    client_connection.sendall(http_response)
    
    # With TCP, its completely legal for the client or server to close their side of the connection, while the other side remains open, also referred to as a 'half-open' connection.
    # In this state, the side that has closed their end of the connection can no longer send data, they can only receive it.
    client_connection.close()

