import socket
import struct
from phue import Bridge
import os

hostname = '192.168.0.153'
b = Bridge('192.168.0.150')
b.connect()
lights = b.lights

def main():
    raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    while True:
        recv_packet = raw_socket.recvfrom(5000)
        ethernet_protocol = struct.unpack('!6s6sH', (recv_packet[0])[:14])[2]

        if ethernet_protocol == 0x800:
            ip_protocol = struct.unpack('!BBHHHBBH4s4s', recv_packet[0][14:34])[6]

            if ip_protocol == 17: # UDP if 6 TCP
                udp_src_port = struct.unpack('!H', (recv_packet[0])[34:34+2])[0]

                if udp_src_port == 68: # (Server -> Client)
                    if (str(recv_packet[0][0:14])).find(r'xf8\xe6\x1a\xc8\x8eq'):
                        lights[0].on = True
                        lights[1].on = True
                        lights[2].on = True
                        print("Ethernet Header : ", recv_packet[0][0:14])
                        print("IPv4 Header : ", recv_packet[0][14:34])
                        print("UDP Header : ", recv_packet[0][34:42])
                        print("DHCP Data : ", recv_packet[0][42:])
                        
                        if b'\x03=' in recv_packet[0][42:]:
                            ip = recv_packet[0][296:300]
                            ip = struct.unpack('!1B1B1B1B',ip)
                            return str(ip[0])+'.'+str(ip[1])+'.'+str(ip[2])+'.'+str(ip[3])

                elif udp_src_port == 67:
                    print('client->server')
                    print(recv_packet[0][0:14])
                    print(recv_packet[0][14:34])
                    print(recv_packet[0][34:42])
                    print(recv_packet[0][42:])


if __name__ == '__main__':
    while True:
        ip_addr = main()
        while True:
            response = os.system("ping -c 3 " + ip_addr)
            if response != 0:
                lights[0].on = False
                lights[1].on = False
                lights[2].on = False
                break
        

