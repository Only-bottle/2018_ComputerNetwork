from socket import *
import ssl
import base64
import sys

# Varialbe
hostname = "pop.naver.com"
portNumber = 995

username = sys.argv[1]
password = sys.argv[2]

# Connect
client_socket = socket(AF_INET, SOCK_STREAM)
ssl_client_sock = ssl.wrap_socket(client_socket)
ssl_client_sock.connect((hostname, portNumber))

# First recv
recv = ssl_client_sock.recv(1024)
print('S : ', recv.decode('utf-8'))

# Input ID
username_send = 'user ' + username + '\r\n'
ssl_client_sock.send(username_send.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : ', 'user ' + username, '\r\n')
print('S : ', recv_1.decode('utf-8'))

# Input PASSWORD
userpass_send = 'pass ' + password + '\r\n'
ssl_client_sock.send(userpass_send.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : ', 'pass ' + password, '\r\n')
print('S : ', recv_1.decode('utf-8'))

while True:
    _input = input('C : ')
    _input = _input + '\r\n'
    ssl_client_sock.send(_input.encode())
    recv_1 = ssl_client_sock.recv(4096)
    print('S : ', recv_1.decode('utf-8'))


