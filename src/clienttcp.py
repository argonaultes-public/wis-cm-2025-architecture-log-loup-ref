import socket
import json

HOST, PORT = "localhost", 9999

# Create a socket (SOCK_STREAM means a TCP socket)

def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(message, "utf-8"))
        sock.sendall(b"\n")

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")

    print("Sent:    ", message)
    print("Received:", received)
    return received

if __name__ == '__main__':
    action = ''
    while action != 'q':
        action = input('action (q: quitter, p: participer, d: deplacer, c: carte): ')
        if action == 'p':
            login = input('login: ')
            message_obj = {
                "action": "participer",
                "login": login
            }
            send_message(json.dumps(message_obj))
