import os
import pickle

#with open('random_ip_list.pickle', 'rb') as f:

with open('trie_ip_list.pickle', 'rb') as f1:
    a = pickle.load(f)
    for ip in a:
        print(ip)
    for i in range(0, 10):
        print(a[i])

print('----------------------------------------')

with open('trietree_resultset.pickle', 'rb') as f2:
    b = pickle.load(f2)
    for j in range(0, 10):
        print(b[j])
