import socket
import ssl
from Crypto.Cipher import AES
import threading
import re

HOST = '127.0.0.1'
PORT = 9999
BUF_SIZE = 4096
blocklist = ["www.google.com", "www.youtube.com", "https://web.whatsapp.com/"]

BS = 16
def pad(s): return bytes(s + (BS - len(s) %
                              BS) * chr(BS - len(s) % BS), 'utf-8')


def unpad(s): return s[0:-ord(s[-1:])]


def do_encrypt(plaintext):
    obj = AES.new('This is a key123'.encode("utf-8"),
                  AES.MODE_CFB, 'This is an IV456'.encode("utf-8"))
    plaintext = pad(plaintext)
    ciphertext = obj.encrypt(plaintext)
    return ciphertext


def do_decrypt(ciphertext):
    obj2 = AES.new('This is a key123'.encode("utf-8"),
                   AES.MODE_CFB, 'This is an IV456'.encode("utf-8"))
    plaintext = unpad(obj2.decrypt(ciphertext))
    return plaintext.decode('utf-8')


def https(request, webserver, client_sock):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock = context.wrap_socket(
        server_sock, server_hostname=webserver, do_handshake_on_connect=False)
    server_sock.connect((webserver, 443))
    server_sock.send(f"GET / HTTP/1.1\r\nHost: {webserver}\r\n\r\n ".encode())

    chunk = ''
    data = ''

    server_sock.settimeout(1)

    while True:
        try:
            chunk = server_sock.recv(BUF_SIZE).decode(
                encoding='utf-8', errors='ignore')
            if chunk:
                data += chunk
            else:
                break
        except (socket.error, KeyboardInterrupt) as e:
            server_sock.close()
            break
    print(data)
    client_sock.send(do_encrypt(data))


def http(request, webserver, client_sock):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((webserver, 80))
    server_sock.send(f"GET / HTTP/1.1\r\nHost: {webserver}\r\n\r\n ".encode())

    chunk = ''
    data = ''

    server_sock.settimeout(1)

    while True:
        try:
            chunk = server_sock.recv(BUF_SIZE).decode(
                encoding='utf-8', errors='ignore')
            if chunk:
                data += chunk
            else:
                break
        except (socket.error, KeyboardInterrupt) as e:
            server_sock.close()
            break

    print(data)
    client_sock.send(do_encrypt(data))


def parse(request, conn):
    try:
        header = request.split(b'\n')[0]

        url = header.split(b' ')[1]

        hostIndex = url.find(b"://")
        if hostIndex == -1:
            temp = url
        else:
            temp = url[(hostIndex + 3):]
        portIndex = temp.find(b":")
        serverIndex = temp.find(b"/")

        if serverIndex == -1:
            serverIndex = len(temp)
        webserver = ""
        port = -1
        if portIndex == -1 or serverIndex < portIndex:
            port = 80
            webserver = temp[:serverIndex]
        else:
            port = int((temp[portIndex + 1:])[:serverIndex - portIndex - 1])
            webserver = temp[:portIndex]

        webserver = webserver.decode()
        method = request.split(b" ")[0]

        for i in blocklist:
            if webserver == i:
                conn.send(do_encrypt("Website is blocked."))
                print("Website is blocked")
                return

        x = re.search('www', webserver)
        if x == 'www':
            webserver = webserver.split('www')[1]

        if method == b"CONNECT":
            https(request, webserver, conn)
        if method == b"GET":
            http(request, webserver, conn)

    except (socket.error, KeyboardInterrupt) as e:
        pass


def connect_to_client():
    # client socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((HOST, PORT))
    except socket.error as e:
        print(e)

    print('[*] Socket is Listening')
    sock.listen(5)
    conn, address = sock.accept()
    print('[*] Connected To Client.')
    while True:
        try:
            request = conn.recv(BUF_SIZE)
            if request:
                request = do_decrypt(request)
                print(request)
                # threads for multiple requests
                threading.Thread(target=parse, args=(
                    request.encode(), conn,)).start()
        except (socket.error, KeyboardInterrupt) as e:
            pass


if __name__ == "__main__":
    connect_to_client()
