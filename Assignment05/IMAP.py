from socket import *
import ssl
import sys

# Commuicate
def transport():
    _input = input('C : ')
    _input = _input + '\r\n'
    ssl_client_sock.send(_input.encode())
    recv_1 = ssl_client_sock.recv(4096)
    print('S : ', recv_1.decode('utf-8'))

# Variable
hostname = 'imap.naver.com'
portNumber = 993

username = sys.argv[1]
password = sys.argv[2]

# Connect
client_socket = socket(AF_INET, SOCK_STREAM)
ssl_client_sock = ssl.wrap_socket(client_socket)
ssl_client_sock.connect((hostname, portNumber))

# First recv
recv = ssl_client_sock.recv(1024)
print('S : ', recv.decode('utf-8'))

# LOGIN
login = 'a LOGIN ' + username + ' ' + password 
login = login + '\r\n'
ssl_client_sock.send(login.encode())
recv_1 = ssl_client_sock.recv(1024)
print('S : ', recv_1.decode('utf-8'))

# INPUT
while True:
    transport()
