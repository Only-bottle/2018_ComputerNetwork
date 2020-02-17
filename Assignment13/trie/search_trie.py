import pickle
import os
import time

class Node(object):
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.children = {}

class Trie(object):
    def __init__(self, object):
        self.head = object
    
    def search(self, searchIP):
        curr_node = self.head
        nextHop = ""

        # 하나의 입력값이 들어오면 반복을 실행
        for char in searchIP:
            if char in curr_node.children:
                curr_node = curr_node.children[char]
                
                if curr_node.data != None:
                    nextHop = curr_node.data
            else:
                return nextHop
             
        if (curr_node.data != None):
            nextHop = curr_node.data
            return nextHop
        else:
            return None

starttime = time.time()

# if pickle file is exist
if os.path.isfile('trietree.pickle'):
    with open('trietree.pickle', 'rb') as f:
        tree = pickle.load(f) # type tree
        t = Trie(tree)
        total_l = []
        # if pickle file is exist
        if os.path.isfile('random_ip_list.pickle'):
            with open('random_ip_list.pickle', 'rb') as f1:
                _list = pickle.load(f1) # random IP load

                for ip in _list:
                    s_bin = "" # search IP -> binary
                    _ip = ip.split('.')

                    for i in range(0,4): # create binary
                        s_bin += bin(int(_ip[i])).split('0b')[1].zfill(8)
                    nextHop = t.search(s_bin)
                        
                    a = []
                    # [searchIP(binary), nextHop]
                    if not nextHop:
                        a = [ip, nextHop]
                    else:
                        a = [ip, nextHop.split('\n')[0]]
                        
                    total_l.append(a)
        # save trie_ip_list            
        with open('trie_ip_list.pickle', 'wb') as f3:
            pickle.dump(total_l, f3)
        print("sucess")
        finish = str(time.time() - starttime)
        print(finish)
