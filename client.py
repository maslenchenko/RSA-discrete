import socket
import threading
import cryptography_funcs
import json
import time
import argparse
from hash_message import to_hash

class Client:
    def __init__(self, server_ip: str, port: int, username: str, n=None, e=None, d=None, all_public_keys=None) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username
        self.n, self.e, self.d = cryptography_funcs.generate_keys()
        self.all_public_keys = dict() if all_public_keys is None else all_public_keys

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())
        time.sleep(0.01)
        self.s.send(f"{self.n} {self.e}".encode())
        time.sleep(0.01)

        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self):
        while True:
            message = self.s.recv(1024).decode()
            if "|" in message:
                messages1 = message.split("|")
                message = messages1[1]
                messages = message.split("}")
                hashed = messages[1]
                message = messages[0]
                encoded, N2, fict_nums = message.split("/")
                encoded = encoded.split(" ")
                message = cryptography_funcs.decode(encoded, self.d, self.n, int(N2), int(fict_nums))
                if hashed != to_hash(message):
                    print(hashed)
                    print(to_hash(message))
                    print("message received with error")
                    print(message)
                else:
                    print(message)
            elif "{" in message:
                self.all_public_keys = json.loads(message)
            else:
                message = message.split("}")
                hashed = message[1]
                message = message[0]
                encoded, N2, fict_nums = message.split("/")
                encoded = encoded.split()
                result = cryptography_funcs.decode(encoded, self.d, self.n, int(N2), int(fict_nums))
                if hashed == to_hash(result):
                    print(result)
                else:
                    print("message received with error")

    def write_handler(self):
        while True:
            message = input()
            if "|" in message:
                message = message.split("|")
                usernames = message[0].split()
                for username in usernames:
                    if username in self.all_public_keys.keys():
                        keys = self.all_public_keys[username]
                        info = message[1]
                        hashed = to_hash(message[1])
                        info = f"{username}|" + cryptography_funcs.encode(info, int(keys[1]), int(keys[0])) + "}" + f"{hashed}"
                        self.s.send(info.encode())
                        time.sleep(0.01)
                    elif username not in self.all_public_keys.keys():
                        print(f"not found {username}")
            else:
                hashed = to_hash(message)
                for username in self.all_public_keys.keys():
                    if username != self.username:
                        keys = self.all_public_keys[username]
                        info = cryptography_funcs.encode(message, int(keys[1]), int(keys[0]))
                        info += f" {username}" + "}" + f"{hashed}"
                        self.s.send(info.encode())
                        time.sleep(0.01)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    args = parser.parse_args()
    cl = Client("127.0.0.1", 9001, args.username)
    cl.init_connection()
