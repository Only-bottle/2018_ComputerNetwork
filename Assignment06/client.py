from socket import *
import sys
from bs4 import BeautifulSoup
import concurrent.futures
import time as t
import matplotlib.pyplot as plt

def vs(list1, list2, list3):
    box_plot_data = [list1, list2, list3]

    plt.boxplot(box_plot_data)
    plt.xlabel("Number of Clients")
    plt.ylabel("Download Time(5)")
    plt.xticks([1,2,3], [10,20,30])
    plt.show()

def parseHTML(html_data):
    soup = BeautifulSoup(html_data, features="html.parser")
    img_list = soup.find_all('img')
    return img_list

def single_client(list):
    start_time = t.time()
    serverIP = '192.168.1.171'
    serverPort = int(sys.argv[3])

    clnt_sock = socket(AF_INET, SOCK_STREAM)
    clnt_sock.connect((serverIP, serverPort))
    print('Connect to Server....')
    clnt_msg = sys.argv[1] + ' ' + sys.argv[2]
    clnt_sock.send(clnt_msg.encode())
    print("Send Message to Server....")

    src_list = []
    recv_data = ''
    
    # recv request
    recv_data = clnt_sock.recv(1500).decode().split('\n\n')
    header = recv_data[0].split('\n')
    msg = header[0]
    file_size = int(header[1])
    
    html_data = recv_data[1].encode()
    download_status = 1024
    
    while download_status < file_size:
        html_data = html_data + clnt_sock.recv(1024)
        download_status = download_status + 1024

    img_list = parseHTML(html_data)
    
    for img in img_list:
        src = img['src'][1:]
        src_list.append(src)
    
    for src in src_list:
        clnt_sock = socket(AF_INET, SOCK_STREAM)
        clnt_sock.connect((serverIP, serverPort))

        send_data = 'GET '+ src
        clnt_sock.send(send_data.encode())

        recv_data = clnt_sock.recv(1500).split(b'\n\n')
        
        header = recv_data[0].decode().split('\n')
        msg = header[0]
        file_size = int(header[1])
        
        download_status = 1024
        
        while download_status < file_size:
            clnt_sock.recv(1024)
            download_status = download_status + 1024
        
        end_time = t.time()
        list.append((end_time - start_time) * 100)
        print((end_time - start_time) * 100)

def multiprocess_func(num, list):
    with concurrent.futures.ProcessPoolExecutor(max_workers=num) as executor:
        for i in range(0, num):
            executor.submit(single_client(list))

list1 = []
list2 = []
list3 = []

multiprocess_func(10, list1)
print('finish 10')
multiprocess_func(20, list2)
print('finish 20')
multiprocess_func(30, list3)
print('finish 30')
vs(list1, list2, list3)
