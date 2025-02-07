import socketserver
import json

class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        self.data = self.rfile.readline(10000).rstrip()
        print(f"{self.client_address[0]} wrote:")
        print(self.data.decode("utf-8"))
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        request = self.data.decode("utf-8")
        
        request_obj = json.loads(request)

        action = request_obj["action"]
        print(f'action: {action}')

        if action == 'participer':
            check_valid_login(request_obj["login"])

        self.wfile.write(b'do nothing')


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()