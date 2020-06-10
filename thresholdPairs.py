# the funtion that will generate n pairs of threholds
def getPartialOrderByThresholdPair(n,f):
    orders = set()
    with open(f,'r') as file:
        line = file.readline().strip()
        while line:
            line = tuple(map(lambda x: int(x), line.split(' ')))
            orders.add(line)
            line = file.readline().strip()
    #print(len(orders))
    for i in range(n,0,-1):
        currorders = set()
        currorders = set([tuple(binsort2(list(order))) for order in pairInsert(i,orders)])
        orders = currorders
        #print(orders)
    return orders
 
# function will insert +n -n into the partial order with (-1,+1,..., -(n-1),+(n-1)) already 
# inserted
def pairInsert(n,preorders):
    ret = set()
    for preorder in preorders:
        l = len(preorder)
        for j in range(l+1):
            for k in range(j+1,l+2):
                currorder = list(preorder).copy()
                currorder[j:j] = ['-{}'.format(n)]
                currorder[k:k] = ['+{}'.format(n)]
                yield tuple(currorder)
    return ret     

# sort the bins separated by  -+k and -+j
def binsort2(l):
    strindex = []
    for i in range(len(l)):
        if isinstance(l[i],str):
            strindex.append(i)
    strindex = [-1] + strindex + [ len(l) ]     
    #print(strindex)
    for i in range(1,len(strindex)):
        prev, curr = strindex[i-1], strindex[i]
        #print(prev, curr)
        #print(l[prev+1:curr])
        l[prev+1:curr] = sorted(l[prev+1:curr])
    return tuple(l)
        