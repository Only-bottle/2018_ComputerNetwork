import pickle
import time
import os

def convert_to_bit(ip):
    s = ip.split('.')
    for i in range(len(s)):
        s[i] = str((bin(int(s[i])))[2:]).zfill(8)
    total  = s[0]+s[1]+s[2]+s[3]
    return total

hash_table = {}
with open('pre.txt', 'r', encoding='utf-8') as f:
    while True:
        s = f.readline()
        if not s:
            break

        s1 = s.split()        #s1[0] = ip/24,    s1[1] = next hop
        s2 = s1[0].split('/') #s2[0] = ip(24.116.119.0), s2[1] = 24
        s3 = s2[0].split('.') #s3 = [24, 116, 119, 0]

        total = convert_to_bit(s2[0])
        
        hash_code = hash(total[:int(s2[1])])

        value = [total, s1[1]] #tuple(network, next hop)
        if hash_code in hash_table:
            print("here")
            break
            #new_value = hash_table.get(hash_code).append(value)
            #hash_table[hash_code] = new_value
        else:
            hash_table[hash_code] = value       # {key: [network, hop]}
        
    print(hash_table)

result_list = list()
starttime = time.time()
with open('../random_ip_list.pickle', 'rb') as f:
    with open('hashtable_resultdata.txt', 'w') as fw:
        ip_list = pickle.load(f)
        for i in ip_list: # select a random ip
            bit_ip = convert_to_bit(i)
            next_hop = ""
            for prefix_length in range(8, 33):
                ip_addr = bit_ip[:prefix_length]
                hash_code = hash(ip_addr)
                if hash_code in hash_table:
                    next_hop = hash_table[hash_code][1] # value = [network, hop]
            if next_hop == "":
                tup = (i, None)
            else:
                tup = (i, next_hop)
            result_list.append(tup)

        for i in range(len(result_list)):
            print(result_list[i][0],"  ",result_list[i][1])
            fw.write(result_list[i][0]+"  "+str(result_list[i][1])+"\n")

        fw.write("=================================================\n")
        fw.write("Timestamp => " + str(time.time() - starttime))
