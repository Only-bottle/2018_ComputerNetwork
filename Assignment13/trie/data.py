with open('oix-full-snapshot-2018-11-01-2200') as f:
    with open('pre.txt', 'w', encoding='utf8') as f1:
        tmp = []
        count = 0
        while True:
            count = count + 1
            line  = f.readline()
            if not line: # empty -> finish
                break
            if count > 5:# data filtering
                s = line.split()
                if len(tmp) == 0: # tmp is empty
                    tmp = s
                else:
                    if tmp[1] == s[1]: # network is same
                        if int(tmp[5]) < int(s[5]): # weight 
                            tmp = s
                            continue
                        else:
                            if int(tmp[4]) < int(s[4]): # local
                                tmp = s
                                continue
                            else:
                                if len(tmp) > len(s): # path length
                                    tmp = s
                                    continue
                    else:
                        f1.write(tmp[1]+" "+tmp[2]+"\n")
                        print(tmp)
                        tmp = s
                       

