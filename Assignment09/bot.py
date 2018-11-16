from socket import *
from phue import Bridge

port_num = 6667
servername = 'chat.freenode.net'

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((servername, port_num))
b = Bridge('192.168.1.139')
b.connect()
lights = b.lights

def hue_set(num, status, light, color_x, color_y):
    num = int(num)
    light = int(light)
    color_x = float(color_x)
    color_y = float(color_y)

    if num == 1:
        if status == 'on':
            lights[0].on = True
            lights[0].brightness = light
            lights[0].xy = [color_x, color_y]
        else:
            lights[0].on = False
    if num == 2:
        if status == 'on':
            lights[1].on = True
            lights[1].brightness = light
            lights[1].xy = [color_x, color_y]
        else:
            lights[1].on = False
    if num == 3:
        if status == 'on':
            lights[2].on = True
            lights[2].brightness = light
            lights[2].xy = [color_x, color_y]
        else:
            lights[2].on = False

sock.send("NICK U201402391\r\n".encode())
sock.send("USER U201402391 U201402391 U201402391 :cnu bot\r\n".encode())
sock.send("JOIN #CNU\r\n".encode())

while 1:
    text = sock.recv(4096)
    text = text.decode()
    parse_text = text.split(' ')
    if text.find(':U201402391_!')!= -1:
        if parse_text[6] == 'on' :
            print(parse_text[4])
            print(parse_text)
            hue_set(parse_text[4], parse_text[6], parse_text[7], parse_text[8], parse_text[9].split('\r\n')[0])
        else:
            hue_set(parse_text[4], parse_text[6], 0, 0, 0)

    print(text)

    if text.find("JOIN")!= -1:
        sock.send(('PRIVMSG #CNU :HELLO [' + text[1:11]+']\r\n').encode())

sock.close()
