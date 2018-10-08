import socket
import sys
import threading

def recv_message(message_socket):
    while True:
        message = message_socket.recv(1024)
        print(message.decode())
        if message[7:11].lower() == 'quit':
            break
        
    print('Host Disconnected')

def main():
    if len(sys.argv) != 4:
        print('python groupchatclient.py [IPADDRESS] [PORTNUMBER] [Client ID]')
        sys.exit()

    ip_address = sys.argv[1]
    port_number = int(sys.argv[2])
    client_id = sys.argv[3]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port_number))

    print('Host connected')

    client_socket.send(client_id.encode())

    threading.Thread(target = recv_message, args = (client_socket,)).start()

    while True:
        message = input('')
        send_msg = '[' + client_id + ']' +  message
        client_socket.send(send_msg.encode())

        if message[0:4].lower() == 'quit':
            break

    print('Host Disconnected')
    client_socket.close()

if __name__=="__main__":
    main()
