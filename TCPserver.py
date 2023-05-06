import socket
import os

def create_response(file_content, status_code):
    response_headers = {
        'Content-Type': 'text/html',
        'Content-Length': len(file_content),
        'Connection': 'close'
    }
    
    response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.items())
    
    response_proto = 'HTTP/1.1'
    response_status = status_code
    response_status_text = 'Not Found' if status_code == '404' else 'OK'
    response_status_raw = '%s %s %s\n' % (response_proto, response_status, response_status_text)
    
    response = response_status_raw + response_headers_raw + '\n' + file_content
    
    return response

def serve_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
            response = create_response(file_content, '200')
    except:
        file_content = '404 Not Found'
        response = create_response(file_content, '404')
        
    return response

def run_server():
    host = 'localhost'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print('Listening on port', port)

    while True:
        client_socket, client_address = server_socket.accept()
        request_data = client_socket.recv(1024)
        request_str = request_data.decode('utf-8')
        print('Received request:')
        print(request_str)

        request_lines = request_str.split('\n')
        request_method, request_path, request_protocol = request_lines[0].split(' ')

        if request_path == '/':
            request_path = '/index.html'
        file_path = os.getcwd() + '/public' + request_path

        response = serve_file(file_path)
        client_socket.send(response.encode('utf-8'))
        client_socket.close()
        print('Response sent\n')

if __name__ == '__main__':
    run_server()

