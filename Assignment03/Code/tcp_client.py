import socket
import sys

serverIP = '127.0.0.1'
serverPort = 2345

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clnt_sock.connect((serverIP, serverPort))
print("Connect to Server...")

clnt_msg = sys.argv[1] + " " + sys.argv[2]
clnt_sock.send(clnt_msg.encode())
print("Send Message to Server...")

recv_data = (clnt_sock.recv(1024)).decode('utf-8')
status = recv_data.split(' ')[1]

if status == "200":
    f = open("recv_data.html", 'w')
    f.write(recv_data.split('\n\n')[1])
    f.close()

elif status == "404":
    print("404 Not Found")
