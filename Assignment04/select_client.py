""" TCP Client """

import socket
import select
import sys

if len(sys.argv) < 3: 
    print("Usage : python {0} hostname port".format(sys.argv[0]))
    sys.exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])

MASTER_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MASTER_SOCK.settimeout(200)

# Server와 연결이 된 경우
try:
    MASTER_SOCK.connect((HOST, PORT))
except Exception as msg:
    print(type(msg).__name__)
    print("Unable to connect")
    sys.exit()

print("Connected to remote host. Start sending messages")

while True:
    # SOCKET_LIST에 입력과 자신의 SOCKET 리스트를 생성한다.
    SOCKET_LIST = [sys.stdin, MASTER_SOCK]
    # thread 대신 select를 이용하여 read,write,error등 준비된 socket을 처리한다.
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(SOCKET_LIST, [], [])

    # READ_SOCKET으로 통신을 한다.
    for sock in READ_SOCKETS:  
        if sock == MASTER_SOCK:
            data = sock.recv(4096) # 받은 데이터를 저장한다. 
            if not data: # 데이터가 아니라면
                print('\nDisconnected from chat server')
                sys.exit() # 연결을 끊는다.
            else:  # 데이터이면 출력한다.
                print(data.decode(), end="")
        else:  
            msg = sys.stdin.readline() # 줄바꿈을 문자를 제거하기 위해서 end파라미터를 설정한다.
            print("\x1b[1A" + "\x1b[2K", end="")  
            MASTER_SOCK.sendall(msg.encode()) # 모든 데이터를 송신한다.
