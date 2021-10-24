def processMessage(msg):
    blocks = []
    for i in range(len(msg)):
        if i%16 == 0:
            blocks.append([])
        
        blocks[-1].append(msg[i])
    
    while len(blocks[-1]) != 16:
        blocks[-1].append(ord('{'))

    return blocks

def convert_matrix(block):
    res = [[] for _ in range(4)]
    for i in range(len(res)):
        for j in range(4):
            res[i].append(block[i+(4*j)])

    return res

def convert_list(block):
    res = []
    for i in range(4):
        for j in range(4):
            res.append(block[j][i])

    return res
