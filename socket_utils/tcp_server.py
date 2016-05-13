"""
Some simple tcp servers.

"""
import socket
import sys

__author__ = "Alex Young"
__copyright__ = "Copyright 2012"
__credits__ = "Alex Young"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alex Young"
__email__ = "alex.young@vt.edu"
__status__ = "Development"


def SimpleServer(host, port, verbose=True, size=1024):
    """
    Receive data over tcp server socket.

    This fuction creates a tcp socket server and listens for a
    connection. Once a client has connected, the server will block
    to receive incoming data, and print the received data if
    `verbose` == True.

    Parameters
    ----------
    host : str
        Dotted quad ip address, e.g.: '127.0.0.1'
    port : int
        Tcp port to which to connect.
    verbose : bool, optional
        Determines whether to print the received data.
    size : int, optional
        Size of socket receive buffer.

    Returns
    -------
    None

    Raises
    ------
    None

    Examples
    --------
    >>> host, port = '127.0.0.1', 65000
    >>> SimpleServer(host, port)
    >>>
    
    """
    backlog = 5
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host,port))
    sock.listen(backlog)
    client, address = sock.accept()
    if verbose:
        print("SimpleServer: accepted connection from {0} ".format(address[0]))

    while True:
        data = client.recv(size)
        if data:
            if verbose:
                print("SimpleServer: received data: {0}".format(data))
            else:
                pass
        else:
            #TODO[ARY]: there might be a better way to shut this down,
            #if so, need to find and implement it.
            client.close()
            sys.exit(0)


def SimpleEchoServer(host, port, verbose=True, size=1024):
    """
    Receive and send data over tcp server socket.

    This fuction creates a tcp socket server and listens for a
    connection. Once a client has connected, the server will block
    to receive incoming data, print the received data if
    `verbose` == True, and send the data back to the client.

    Parameters
    ----------
    host : str
        Dotted quad ip address, e.g.: '127.0.0.1'
    port : int
        Tcp port to which to connect.
    verbose : bool, optional
        Determines whether to print the received data.
    size : int, optional
        Size of socket receive buffer.

    Returns
    -------
    None

    Raises
    ------
    None

    Examples
    --------
    >>> host, port = '127.0.0.1', 65000
    >>> SimpleEchoServer(host, port)
    >>>
    
    """
    backlog = 5
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host,port))
    sock.listen(backlog)
    client, address = sock.accept()
    if verbose:
        print("SimpleEchoServer: accepted connection from {0} ".format(address[0]))

    while True:
        data = client.recv(size)
        if data:
            if verbose:
                print("SimpleEchoServer: received data: {0}".format(data))
            client.send(data)
        else:
            #TODO[ARY]: there might be a better way to shut this down,
            #if so, need to find and implement it.
            client.close()
            sys.exit(0)


        
