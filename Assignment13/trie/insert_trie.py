import pickle
import os

class Node(object):
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.children = {}

class Trie(object):
    def __init__(self):
        self.head = Node(None)
    
    def insert(self, insertIP, nextHop):
        curr_node = self.head

        for char in insertIP:
            if char not in curr_node.children:
                curr_node.children[char] = Node(char)

            curr_node = curr_node.children[char]

        curr_node.data = nextHop

        return self.head

with open('pre.txt', 'r', encoding='utf8') as f:
    t = Trie()
    
    # if pickle file is exist
    while True:
        line = f.readline()
        if not line:
            with open('trietree.pickle', 'wb') as f1:
                pickle.dump(tree, f1)
                break
            
        insertIP = line.split(' ')[0].split('/')[0].split('.')
        mask = line.split(' ')[0].split('/')[1]
        nextHop = line.split(' ')[1]

        i_bin = ""
        for i in range(0,4):
            i_bin += bin(int(insertIP[i])).split('0b')[1].zfill(8)
        tree = t.insert(i_bin[:int(mask)], nextHop)
