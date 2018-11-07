from socket import *
import os
import sys
from threading import Thread
import traceback
from phue import Bridge

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
    url = (data.decode()).split(' ')
    file_name = url[1]
    print(file_name)

    if len(file_name.split('?')) > 1 :
        query = file_name.split('?')[1]
        data = query.split('&')
        hue_num = data[0].split('=')[0]
        light = data[1].split('=')[1]
        color_x = data[2].split('=')[1]
        color_y = data[3].split('=')[1]
        hue(hue_num, light, color_x, color_y)
    
    # if method = GET
    if url[0] == 'GET':
        if os.path.isfile('.'+file_name):
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

def hue(hue_num, light, color_x, color_y):
    b = Bridge('192.168.1.139')
    b.connect()

    lights = b.lights
    print(lights)
    light = int(light)
    color_x = float(color_x)
    color_y = float(color_y)

    if hue_num == 'on1':
        lights[0].on = True
        lights[0].brightness = light
        lights[0].xy = [color_x, color_y]
    elif hue_num == 'off1':
        lights[0].on = False

    if hue_num == 'on2':
        lights[1].on = True
        lights[1].brightness = light
        lights[1].xy = [color_x, color_y]
    elif hue_num == 'off2':
        lights[1].on = False

    if hue_num == 'on3':
        lights[2].on = True
        lights[2].brightness = light
        lights[2].xy = [color_x, color_y]
    elif hue_num == 'off3':
        lights[2].on = False


# variable
is_file = b'HTTP/1.1 200 OK\n'
none_file = b'HTTP/1.1 404 Not Found\n'

ip_addr = '127.0.0.1'
port_num = int(sys.argv[1])
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
