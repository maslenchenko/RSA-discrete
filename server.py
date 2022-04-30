import socket
import threading
import cryptography_funcs
import json
import time
from hash_message import to_hash

class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.keys = {}

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)
        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            time.sleep(0.01)
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            keys = c.recv(1024).decode()
            time.sleep(0.01)
            self.username_lookup[c] = username
            self.keys[username] = keys.split(" ")
            self.clients.append(c)
            for client in self.clients:
                client.send(json.dumps(self.keys).encode())
                time.sleep(0.01)
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:
            time.sleep(0.1)
            username = self.username_lookup[client]
            n = int(self.keys[username][0])
            e = int(self.keys[username][1])
            enc_msg = cryptography_funcs.encode(msg, e, n) + "}" + str(to_hash(msg))
            client.send(enc_msg.encode())
            time.sleep(0.01)

    def handle_client(self, c: socket, addr): 
        while True:
            msg = c.recv(1024).decode()
            time.sleep(0.01)
            if "|" in msg:
                message = msg.split("|")
                usernames = message[0].split()
                message = message[1]
                for client in self.clients:
                    for username in usernames:
                        if client != c:
                            if username == self.username_lookup[client]:
                                client.send(msg.encode())
                                time.sleep(0.01)
            else:
                second_part = msg.split()[-1]
                receiver = second_part.split("}")[0]
                hashed = second_part.split("}")[1]
                for client in self.clients:
                    if self.username_lookup[client] == receiver:
                        message = msg[:-(len(second_part))] + "}" + str(hashed) 
                        client.send(message.encode())

if __name__ == "__main__":
    s = Server(9001)
    s.start()
