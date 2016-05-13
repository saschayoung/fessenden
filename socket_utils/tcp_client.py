import socket
import sys

def simple_receive(host, port, verbose=True, size=1024):
    """
    Receive data over tcp socket.

    This function connects to a tcp socket server and receives data
    from the server. The function blocks until data is received, or
    the '' string is received, which signals the socket to close, and
    the function terminates.

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
    
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((host, port))
    while True:
        data = sock.recv(size)
        if data == '':
            sock.close()
            sys.exit()
        elif verbose:
            print("Received data: {0}".format(data))
        else:
            pass


def simple_receive_send(host, port, tx_data, verbose=True, size=1024):
    """
    Receive and send data over tcp socket.

    This function connects to a tcp socket server and receives data
    from the server. The function blocks until data is received. After
    incoming data is received, outgoing data is sent.

    Parameters
    ----------
    host : str
        Dotted quad ip address, e.g.: '127.0.0.1'
    port : int
        Tcp port to which to connect.
    tx_data : str
        Data which to send to server.
    verbose : bool, optional
        Determines whether to print the received data.
    size : int, optional
        Size of socket receive buffer.
    
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((host, port))
    while True:
        rx_data = sock.recv(size)
        if verbose:
            print("Received data: {0}".format(rx_data))
        sock.send(tx_data)
