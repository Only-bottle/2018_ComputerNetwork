from socket import *
import os
import sys
from threading import Thread
import traceback

def file_read(file_name, clnt_sock):
    f = open('./' + file_name, 'rb')
    read_data = f.read(1024)
    clnt_sock.send(is_file + read_data)
    while True:
        if len(read_data) != 1024:
            break
        read_data = f.read(1024)
        clnt_sock.send(read_data)
    f.close()

def server_excute(clnt_sock):
    data = clnt_sock.recv(1500)
    parsing_data = (data.decode()).split(' ')
    file_name = parsing_data[1]
    print(file_name)
    
    # if method = GET
    if parsing_data[0] == 'GET':
        if os.path.isfile('.'+file_name):
            print('있어')
            f = open('.' + file_name, 'rb')
            read_data = f.read(1024)
            file_size = str(os.path.getsize('.' + file_name)).encode() + b'\n\n'
            clnt_sock.send(is_file + file_size + read_data)

            while True:
                read_data = f.read(1024)
                if not read_data:
                    break
                clnt_sock.send(read_data)
            f.close()
            clnt_sock.close()


# variable
ip_addr = '127.0.0.1'
port_num = int(sys.argv[1])

is_file = b'HTTP/1.1 200 OK\n'
none_file = b'HTTP/1.1 404 Not Found\n'

server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind((ip_addr, port_num))
print('Server socket open...')
print('Listening...')
server_sock.listen(1)

while True:
    clnt_sock, addr = server_sock.accept()
    try:
        Thread(target=server_excute, args=(clnt_sock,)).start()
    except:
        print("Thread did not start.")
        traceback.print_exc()

print("Send Message back to client")
