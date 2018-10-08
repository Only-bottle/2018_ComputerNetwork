""" A simple chat TCP server """
import socket
import select

def broadcast_data(message):
    """ Sends a message to all sockets in the connection list. """
    # 서버를 제외한 모든 client에게 메세지를 뿌려준다.
    for sock in CONNECTION_LIST:
        if sock != SERVER_SOCKET:
            try:
                sock.sendall(message)  # 모든 데이터를 송신한다.
            except Exception as msg:  # 에러 처리
                print(type(msg).__name__)
                sock.close()
                try:
                    CONNECTION_LIST.remove(sock)
                except ValueError as msg:
                    print("{}:{}".format(type(msg).__name__, msg))


CONNECTION_LIST = [] # 연결된 client를 저장할 리스트를 선언한다.
RECV_BUFFER = 4096 
PORT = 1234 # 포트를 지정해준다.

SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SO_REUSEADDR 옵션으로 기존의 바인딩된 주소를 다시 사용할 수 있게 한다.
SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER_SOCKET.bind(("", PORT))  # 

input_listen = input('연결 가능한 Client 개수 : ')
print("Listening...")
SERVER_SOCKET.listen(int(input_listen))  # xx개의 socket을 기다린다.

CONNECTION_LIST.append(SERVER_SOCKET)
print("Server started!")

while True:
    # Select 함수를 사용하는 부분이다. Read_Socket으로 COnnection_List를 사용하였고
    # 나머지 Write_socket, Error_Socket은 빈 리스트로 놓았다.
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(CONNECTION_LIST, [], [])
    
    for SOCK in READ_SOCKETS:  # 새로운 접속이 생길 경우
        # SERVER_SOCKET은 listen받는 소켓이다.
        if SOCK == SERVER_SOCKET:
            SOCKFD, ADDR = SERVER_SOCKET.accept()
            CONNECTION_LIST.append(SOCKFD)  # 연결된 소켓을 CONNECTION_LIST에 추가한다.
            # 사용자가 들어왔다는 메시지 출력과 broadcast를 통해 send한다.
            print("\rClient ({0}, {1}) connected".format(ADDR[0], ADDR[1]))
            broadcast_data("Client ({0}:{1}) entered room\n"
                            .format(ADDR[0], ADDR[1]).encode())
        else:  # SERVER_SOCKET이 아닌 입력이 들어온 경우
            try:  
                DATA = SOCK.recv(RECV_BUFFER)  # client로 부터 데이터를 받는다.
                if DATA:
                    ADDR = SOCK.getpeername()  # socket의 client 사용자 정보를 얻는다.
                    message = "\r[{}:{}]: {}".format(
                        ADDR[0], ADDR[1], DATA.decode())
                    print(message, end="")
                    broadcast_data(message.encode())
            except Exception as msg: # client가 disconnect일 경우
                print(type(msg).__name__, msg) # 메시지를 출력해준다.
                print("\rClient ({0}, {1}) disconnected.".format(
                    ADDR[0], ADDR[1]))
                broadcast_data("\rClient ({0}, {1}) is offline\n"
                               .format(ADDR[0], ADDR[1]).encode())
                SOCK.close()
                try:
                    CONNECTION_LIST.remove(SOCK) # CONNECTION_LIST에서 삭제한다.
                except ValueError as msg:
                    print("{}:{}.".format(type(msg).__name__, msg))
                continue

SERVER_SOCKET.close()
