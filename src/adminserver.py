import admin_pb2_grpc
import grpc
from concurrent import futures
import admin_pb2

class AdminServicer(admin_pb2_grpc.AdminServicer):

    LOGINS = set()
    
    def CheckValidLogin(self, request, context):
        login = request.login
        if login in self.LOGINS:
            return admin_pb2.Status(status = False)
        else:
            self.LOGINS.add(login)
            return admin_pb2.Status(status = True)



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    admin_pb2_grpc.add_AdminServicer_to_server(AdminServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()