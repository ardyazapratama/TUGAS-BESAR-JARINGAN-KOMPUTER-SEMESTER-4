import socket
import os

# inisialisasi socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket ke alamat dan port tertentu
server_address = ('localhost', 8000)
server_socket.bind(server_address)

# listen untuk koneksi dari client
server_socket.listen(1)
print('Server is listening at', server_address)

while True:
    # menerima koneksi dari client
    client_socket, client_address = server_socket.accept()
    print('Connection from', client_address)

    # menerima data dari client
    request_data = client_socket.recv(1024).decode()

    # parsing HTTP request
    request_lines = request_data.split('\n')
    request_method, request_path, _ = request_lines[0].split()

    # mencari file yang diminta oleh client
    file_path = '.' + request_path
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            file_content = file.read()

        # membuat HTTP response message
        response_headers = 'HTTP/1.1 200 OK\r\n'
        response_headers += 'Content-Type: application/octet-stream\r\n'
        response_headers += 'Content-Disposition: attachment; filename=' + os.path.basename(file_path) + '\r\n'
        response_headers += 'Content-Length: ' + str(len(file_content)) + '\r\n'
        response_headers += '\r\n'

        response_data = response_headers.encode() + file_content

    else:
        # membuat pesan 404 Not Found jika file tidak ditemukan
        response_headers = 'HTTP/1.1 404 Not Found\r\n'
        response_headers += 'Content-Type: text/html; charset=utf-8\r\n'
        response_headers += '\r\n'

        response_data = response_headers.encode() + b'File not found'

    # mengirim response message ke client
    client_socket.sendall(response_data)

    # menutup koneksi dengan client
    client_socket.close()
