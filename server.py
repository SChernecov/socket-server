import socket
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from config import LOCALHOST, PORT


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query_string = urlparse(self.path).query
        params = parse_qs(query_string)
        status_code = params.get("status", [None])[0]

        if status_code is None:
            status_code = 200
        elif not status_code.isdigit():
            status_code = 200
        elif int(status_code) == 404:
            status_code = 404
        else:
            status_code = int(status_code)

        self.send_response(status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if status_code == 200:
            status_code_message = "Request status: 200 OK"
        else:
            return self.send_error(status_code)

        content = (
            f"Request Method: {self.command}\nRequest Source: {self.client_address}\n{status_code_message}\n"
        ).encode()
        for header_name, header_value in self.headers.items():
            content += f"{header_name}: {header_value}\r\n".encode()
        self.wfile.write(content)


def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((LOCALHOST, PORT))
        server.listen(4)
        while True:
            print("Server is working...")
            client_socket, address = server.accept()
            SimpleHTTPRequestHandler(request=client_socket,
                                     client_address=address,
                                     server=None)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
        print("...Server is shutdown")


if __name__ == "__main__":
    start_server()
