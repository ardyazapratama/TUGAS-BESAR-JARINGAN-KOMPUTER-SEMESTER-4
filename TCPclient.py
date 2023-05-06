import socket

def run_client():
    host = 'localhost'
    port = 8080

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    request_str = 'GET / HTTP/1.1\nHost: localhost\n\n'
    client_socket.send(request_str.encode('utf-8'))

    response_data = client_socket.recv(1024)
    response_str = response_data.decode('utf-8')
    print('Received response:')
    print(response_str)

    client_socket.close()

if __name__ == '__main__':
    run_client()

