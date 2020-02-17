import hashlib
import pickle
import time

def int_to_bit(ip):
    ip = ip.split('.') # 150.23.14.42
    i_bin = ""
    for i in range(0,4):
        i_bin += bin(int(ip[i])).split('0b')[1].zfill(8)
    return i_bin

with open('../trie/pre.txt', 'r', encoding='utf8') as f:
    hashTable = {}
    while True:
        line = f.readline()
        if not line:
            break

        network = line.split(' ')[0] # ex) 150.23.14.42/24
        ip = network.split('/')[0] # ex) 150.23.14.42
        mask = int(network.split('/')[1]) # ex) 24
        nextHop = line.split(' ')[1].split('\n')[0]
        
        bit = int_to_bit(ip)
        hash_key = hash(bit[:mask])
        
        value = [bit, nextHop]

        if hash_key in hashTable:
            print('Hashkey is exist')
            break
        else:
            hashTable[hash_key] = value

#    print(hashTable)

outputList = list()
starttime = time.time()

with open('../trie/random_ip_list.pickle', 'rb') as f1:
    with open('hashtable_result.pickle', 'wb') as f2:
        total_l = []
        ip_list = pickle.load(f1)
        for ip in ip_list:
            nextHop = ""
            for prefix in range(8, 33):
                ip_add = int_to_bit(ip)[:prefix]
                hash_code = hash(ip_add)
                if hash_code in hashTable:
                    nextHop = hashTable[hash_code][1]
            if nextHop == "":
                print([ip, None])
                total_l.append([ip, None])
            else:
                print([ip, nextHop])
                total_l.append([ip, nextHop])
#            outputList.append(value)

#        for i in range(len(outputList)):
#            total_l.append([outputList[i][0], outputList[i][1]])
        
        pickle.dump(total_l, f2)
    f2.close()
f1.close()
