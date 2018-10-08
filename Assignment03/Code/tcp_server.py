import socket
import os
from threading import Thread
import traceback

ip_addr = '127.0.0.1'
port_num = 2344

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip_addr, port_num))
print("Server socket open...")

print("Listening...")
server_sock.listen(5)

def clnt_thread(clnt_sock):
    data = clnt_sock.recv(5000)

    de_data = data.decode()
    parsing_data = de_data.split(' ')

    is_file = 'HTTP/1.1 200 OK\r\n\n'.encode()
    none_file = 'HTTP/1.1 404 Not Found\r\n\n'.encode()

    file_name = parsing_data[1].split('/')[1]

    if parsing_data[0] == "GET":
        if os.path.isfile(file_name):
            f = open(file_name, 'rb')
            line = f.read()
            is_file += line
            f.close()
            print(is_file)
            clnt_sock.send(is_file)

        else:
            clnt_sock.send(none_file)

    elif parsing_data[0] == "POST":
        print("Next Time")

while True:
    clnt_sock, addr = server_sock.accept()
#    print("Connected with " + "client" + str(i))

    try:
        Thread(target=clnt_thread, args=(clnt_sock,)).start()
    except:
        print("Thread did not start.")
        traceback.print_exc()

print("Send Message back to client")

clnt_sock.close()
