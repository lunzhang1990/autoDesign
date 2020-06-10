from total2partial import getPartialOrderByThreshold

def parser(nw):
    odegree = {}
    inodes ={}
    ilogic = {}
    inedges = {}
    with open(nw,'r') as file:
        line= file.readline()
        while line:
            line, logic = line.split('-')
            
            node, predecessors = line.split(':')
            
            ilogic[node] = logic.strip()
            
            tempinodes = predecessors.replace('(','+').replace(')','+').split('+')
            tempinodes = [rr for rr in tempinodes if rr ]
            inodes[node] = [r  if r[0]!='~' else r[1:] for r in tempinodes]
            
            tempinedges = ['A'  if r[0]!='~' else 'R' for r in tempinodes]
            inedges[node] = tempinedges
            
            line = file.readline()
    
    for node in inodes:
        outdegree = 0
        for currentnode in inodes:
            if node in inodes[currentnode]:
                outdegree+=1
        odegree[node] = outdegree
    return [odegree,inodes,ilogic,inedges]


# the order of node should be in the order of (x+y)z...
# inodes: in nodes, ilogic: in logic
# to get the polynomial index under current state
def getpindex(inodes,inedges,istates):
    s = ''
    activation = {('R','L'),('A','H')}
    repression = {('R','H'),('A','L')}
    for i in range(len(inodes)):
        node = inodes[i]
        coordstate = (inedges[i],istates[node])
        if coordstate in activation:
            s = s+'1'
        else:
            s = s+'0'
    return int(s,2)

# generate coordinate parameter nodes
# the inlogic should be in form 4_2_...
def gencoordpn(logic,odegree):
    file = logic+'_final.dat'
    coordpn = getPartialOrderByThreshold(odegree,file)
    return coordpn

# odegree: out degree
# r is the 
# coordpn: coordinates parameter node
def getcoordprop(coordpn, state, odegree,inodes,ilogic,inedges, istates):
    pindex = getpindex(inodes,inedges,istates)
    idegree = len(inedges)
    prop = 0
    if state == 'H':
        num = [r for r in coordpn if r.index(-1) < r.index(pindex)]
        prop = len(num)/len(coordpn)
    if state == 'L':
        num = [r for r in coordpn if r.index(-odegree) > r.index(pindex)]
        prop = len(num)/len(coordpn)
    return prop

# it seems for each node we need: the current state, the logic of in, the outdegree, the states of all innode
# we need to create 3 dictionary for nodes
# states of each node,  in logic of each node, out degree of each node

def computetotalprop(nw,istates):
    odegree,inodes,ilogic,inedges = parser(nw)
    prop = 1
    for node in istates:
        coordpn = gencoordpn(ilogic[node], odegree[node]) # the ilogic and odegree of node
        prop*=getcoordprop(coordpn, istates[node], odegree[node], inodes[node], ilogic[node], inedges[node], istates) # all of the node
    return prop

# for each 1-d parameter space
def countregions(r,state,numtheta,nodeindex,regions):
    nodepositions = [r[nodeindex] for r in regions]
    downtheta = [p-numtheta-1 for p in nodepositions]
    uptheta = [p-numtheta for p in nodeposition]
    count = 0
    for instance in r:
        instance = True
        if downtheta >= -numtheta:
            if r.index(state) < r.index(downtheta):
                # instance = False
                continue
        if uptheta < 0:
            if r.index(state) > r.index(uptheta):
                # instance =
                continue
        count+=1
    return count