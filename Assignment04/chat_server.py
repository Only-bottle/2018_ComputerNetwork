import socket
import threading
import sys

clnt_list = []

def recv_msg(client_socket):
    global clnt_list
    while True:
        message = client_socket.recv(1024).decode()
        print(message) # 서버에 각 사용자들의 채팅을 출력한다.

        # 현재 접속해있는 사용자들에게 메시지를 뿌려준다.
        for i in range(len(clnt_list)):
            if clnt_list[i] is not client_socket:
                clnt_list[i].send(message.encode())

        if message[9:13].lower() == 'quit':
            break
    print('Client Disconnected')

def main():
        if len(sys.argv) != 2:
            print('python chat server.py [PORTNUMBER]')
            sys.exit()

        port_number = int(sys.argv[1])

        chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        chat_server_socket.bind(('', port_number))
        chat_server_socket.listen(5) # 5명을 받아주기 위해 인자 값을 5로지정

        while True:
            (client_socket, addr) = chat_server_socket.accept()
            clnt_list.append(client_socket)

            client_id = client_socket.recv(1024).decode()
            print(client_id + ' Client connect')

            for i in range(len(clnt_list)):
                if clnt_list[i] is not client_socket:
                    clnt_list[i].send(('client' + client_id + '- enter').encode())

            threading.Thread(target = recv_msg, args = (client_socket,)).start()
     
        print('Client Disconnected')
        chat_server_socket.close()

if __name__ == "__main__":
    main()
