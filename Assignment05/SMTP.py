from socket import *
import ssl
import base64
import sys

# Variable
hostname = "smtp.naver.com"
portNumber = 465

username = sys.argv[1]
password = sys.argv[2]

# Connect
client_socket = socket(AF_INET, SOCK_STREAM)
ssl_client_sock = ssl.wrap_socket(client_socket)
ssl_client_sock.connect((hostname, portNumber))

# First recv
recv = ssl_client_sock.recv(1024)
print('S :', recv.decode('utf-8'), '\r\n')

# EHLO hostname
hello_input = 'EHLO naver.com\r\n'
ssl_client_sock.send(hello_input.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C :', hello_input)
print('S :', recv.decode('utf-8'),  '\r\n')

# AUTH LOGIN
login_command = 'AUTH LOGIN\r\n'
ssl_client_sock.send(login_command.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C :', login_command)
print('S :', recv.decode('utf-8'), '\r\n')

# base64encoded ID
username_encode = base64.b64encode(username.encode())
a = username_encode.decode() + '\r\n'
ssl_client_sock.send(a.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C: ', username_encode, '\r\n')
print('S :', recv.decode('utf-8'), '\r\n')

# base64encoded PASSWORD
userpass_encode = base64.b64encode(password.encode())
b = userpass_encode.decode() + '\r\n'
ssl_client_sock.send(b.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : pass', userpass_encode, '\r\n')
print('S :', recv.decode('utf-8'), '\r\n')

# MAIL FROM : <송신메일주소>
mail_from = 'MAIL FROM: <{0}>\r\n'.format("ssey0921@naver.com")
ssl_client_sock.send(mail_from.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : ', mail_from)
print('S : ', recv.decode('utf-8'), '\r\n')

# RCPT TO: <수신메일주소>
mail_to = 'RCPT TO: <{0}>\r\n'.format("ssey0921@gmail.com")
ssl_client_sock.send(mail_to.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : ', mail_to)
print('S : ', recv.decode('utf-8'), '\r\n')

# DATA
data = 'DATA\r\n'
ssl_client_sock.send(data.encode())
recv_1 = ssl_client_sock.recv(1024)
print('C : ', data)
print('S : ', recv.decode('utf-8'), '\r\n')

# SUBJECT, FROM, TO...
subject = "SUBJECT: {0}\r\n".format("AAAAAAAAAAA")
_from = "FROM: {0}\r\n".format("ssey0921@naver.com")
_to = "TO: {0}\r\n".format("ssey0921@gmail.com")
_content = "SMTP TEST!\r\n"
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
print('S : ', recv.decode('utf-8'), '\r\n')

# QUIT
quitcommand = 'QUIT\r\n'
ssl_client_sock.send(quitcommand.encode())
print('C : ', quitcommand)
ssl_client_sock.close()

