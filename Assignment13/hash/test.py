import pickle
import os

if os.path.isfile('../trie/trie_ip_list.pickle'):
    with open('../trie/trietree_resultset.pickle', 'rb') as f1:
        a = pickle.load(f1)
        i = 0
        for ip in a:
            print(ip)
            if i == 10:
                break
            i += 1

print('-------------------------------------------------')
if os.path.isfile('hashtable_result.pickle'):
    with open('hashtable_result.pickle', 'rb') as f2:
        a = pickle.load(f2)

        i = 0
        for ip in a:
            print(ip)
            if i == 10:
                break
            i += 1
