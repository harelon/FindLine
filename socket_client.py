import socket


def connection():
    connected = False  # A variable that contains whether the connection is on
    force_closed = False  # A variable that checks if the connection was forced closed
    conn_counter = 0  # A counter for connections tries
    while not connected and not force_closed:
        try:
            client_socket.connect((ip, port))
            connected = True
            while connected:
                data = b'g'
                if data is not None and connected:
                    try:
                        client_socket.sendall(data)
                    except Exception as e:
                        if e == ConnectionResetError:
                            connected = False
                        else:
                            raise ConnectionResetError
                else:
                    connected = False
        except:
            if conn_counter < 3:
                conn_counter += 1
                client_socket.close()
                connected = False
            else:
                force_closed = True
                print("The connection was closed")


def main():
    global ip
    global port
    global client_socket
    ip = '192.168.3.76'
    port = 8088
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection()


if __name__ == '__main__':
    main()
