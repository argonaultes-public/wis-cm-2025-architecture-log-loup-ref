import socketserver
import json
import grpc
import admin_pb2_grpc
import admin_pb2

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
        response = None

        if action == 'participer':
            login = request_obj["login"]
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = admin_pb2_grpc.AdminStub(channel)
                status = stub.CheckValidLogin(admin_pb2.Login(login = login))
                response = status.status
        self.wfile.write(f'{response}'.encode('utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()