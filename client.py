import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

HOST = '127.0.0.1'
PORT = 5000

with open("C:\\Users\\Daniel\PycharmProjects\pythonProject2\.venv\Lib\public.pem", "rb") as f:
    public_key = RSA.import_key(f.read())

cipher = PKCS1_OAEP.new(public_key)

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("השרת ניתק")
                break
            print("\n" + data.decode() + "\n> ", end="")
        except:
            break

def main():
    s = socket.socket()
    s.connect((HOST, PORT))

    threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

    print("שלח הודעה :")

    while True:
        msg = input("> ")
        if not msg:
            break

        encrypted = cipher.encrypt(msg.encode())
        s.sendall(encrypted)

    s.close()

if __name__ == "__main__":
    main()
