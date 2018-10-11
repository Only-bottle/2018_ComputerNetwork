from socket import *
import os
import ssl
import base64
import sys

# variable
ip_addr = '127.0.0.1'
port_num = 2345

# connect
server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind((ip_addr, port_num))
print("Server socket open...")
print("Listening...")
server_sock.listen(1)
clnt_sock, addr = server_sock.accept()

# recive
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
        clnt_sock.send(is_file)

    else:
        clnt_sock.send(none_file)

elif parsing_data[0] == "POST":
    print("Next Time")

clnt_sock.close()

# socket re_open
server_sock.listen(1)
clnt_sock, addr = server_sock.accept()

# variable
data = ''
recv_data = ''

# receive
data = clnt_sock.recv(5000)
de_data = data.decode()
parsing_data = de_data.split(' ')

# data setting
url = de_data.split(' ')
query = url[1].split('?')
parse_data = query[1].split('&')

_id = parse_data[0].split('=')[1]
_pass = parse_data[1].split('=')[1]

_from = parse_data[2].split('=')[1]
_from = _from.replace('%40', '@')

_to = parse_data[3].split('=')[1]
_to = _to.replace('%40', '@')

_subject = parse_data[4].split('=')[1]
_content = parse_data[5].split('=')[1]

 # Variable
hostname = "smtp.naver.com"
portNumber = 465

client_socket = socket(AF_INET, SOCK_STREAM)
ssl_client_sock = ssl.wrap_socket(client_socket)
ssl_client_sock.connect((hostname, portNumber))

recv = ssl_client_sock.recv(1024)
print('S :', recv)

# EHLO hostname
hello_input = 'EHLO naver.com\r\n'
ssl_client_sock.send(hello_input.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C :', hello_input)
print('S :', recv_1)

# AUTH LOGIN
login_command = 'AUTH LOGIN\r\n'
ssl_client_sock.send(login_command.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C :', login_command)
print('S :', recv_1)

# base64encoded ID
print(_id)
username_encode = base64.b64encode(_id.encode())
a = username_encode.decode() + '\r\n'
ssl_client_sock.send(a.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C: ', username_encode, '\r\n')
print('S :', recv_1)

# base64encoded PASSWORD
userpass_encode = base64.b64encode(_pass.encode())
b = userpass_encode.decode() + '\r\n'
ssl_client_sock.send(b.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : pass', userpass_encode, '\r\n')
print('S :', recv_1)

# MAIL FROM : <송신메일주소>
mail_from = 'MAIL FROM: <{0}>\r\n'.format(_from)
ssl_client_sock.send(mail_from.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : ', mail_from)
print('S : ', recv_1)

# RCPT TO: <수신메일주소>
mail_to = 'RCPT TO: <{0}>\r\n'.format(_to)
ssl_client_sock.send(mail_to.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : ', mail_to)
print('S : ', recv_1)

# DATA
data = 'DATA\r\n'
ssl_client_sock.send(data.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : ', data)
print('S : ', recv_1)

# SUBJECT, FROM, TO...
subject = "SUBJECT: {0}\r\n".format(_subject)
_from = "FROM: {0}\r\n".format(_from)
_to = "TO: {0}\r\n".format(_to)
_content = _content + "\r\n"
_send = ".\r\n"
ssl_client_sock.send(subject.encode())
ssl_client_sock.send(_from.encode())
ssl_client_sock.send(_to.encode())
ssl_client_sock.send(_content.encode())
ssl_client_sock.send(_send.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : ', subject)
print('C : ', _from)
print('C : ', _to)
print('C : ', _content)
print('C : ', _send)
print('S : ', recv_1)

# QUIT
quitcommand = 'QUIT\r\n'
ssl_client_sock.send(quitcommand.encode())
print('C : ', quitcommand)
ssl_client_sock.close()

print("Send Message back to client")

clnt_sock.close()
