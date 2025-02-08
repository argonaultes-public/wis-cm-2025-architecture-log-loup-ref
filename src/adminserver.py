import admin_pb2_grpc
import grpc
from concurrent import futures
import admin_pb2
from models import Base, Login
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


class AdminServicer(admin_pb2_grpc.AdminServicer):

    def __init__(self):
        self.engine = create_engine("sqlite:///db.sqlite3", echo=True)
        Base.metadata.create_all(self.engine)

    
    def CheckValidLogin(self, request, context):
        login = request.login
        session = Session(self.engine)
        nblogins = session.query(Login).where(Login.login.is_(login)).count()
        if nblogins > 0:
            return admin_pb2.Status(status = False)
        else:
            new_login = Login(login=login)
            session.add(new_login)
            session.commit()
            return admin_pb2.Status(status = True)



def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    admin_pb2_grpc.add_AdminServicer_to_server(AdminServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()