import socket

# inisialisasi socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# koneksi ke server
server_address = ('localhost', 8000)
client_socket.connect(server_address)

# mengirim HTTP request ke server
request_headers = 'GET /file.txt HTTP/1.1\r\n'
request_headers += 'Host: localhost:8000\r\n'
request_headers += '\r\n'
client_socket.sendall(request_headers.encode())

# menerima response dari server
response_data = client_socket.recv(1024)

# parsing HTTP response
response_lines = response_data.decode().split('\n')
response_status = response_lines[0]
response_headers = response_lines[1:-1]
response_content = b''.join(response_lines[-1].encode())

# menampilkan response
print(response_status)
print(response_headers)
print(response_content.decode())

# menutup koneksi dengan server
client_socket.close()
