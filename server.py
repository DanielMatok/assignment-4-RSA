import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

HOST = '0.0.0.0'
PORT = 5000

with open("C:\\Users\\Daniel\PycharmProjects\pythonProject2\.venv\Lib\private.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

cipher = PKCS1_OAEP.new(private_key)

clients = []

def broadcast(message, source_conn):
    for client in clients:
        if client != source_conn:
            try:
                client.sendall(message.encode())
            except:
                pass

def handle_client(conn, addr):
    print(f"לקוח התחבר מ: {addr}")
    while True:
        try:
            data = conn.recv(512)
            if not data:
                print(f"לקוח {addr} התנתק")
                clients.remove(conn)
                conn.close()
                break

            decrypted = cipher.decrypt(data).decode()
            print(f"הודעה מ{addr}: {decrypted}")

            broadcast(f"{addr}: {decrypted}", conn)

        except Exception as e:
            print(f"שגיאה: {e}")
            clients.remove(conn)
            conn.close()
            break

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print(f"שרת מאזין על {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
