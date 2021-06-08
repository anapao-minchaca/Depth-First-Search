'''
Created November 5, 2020

@Authors:
- Emilio Popovits Blake (A01027265)
- Patricio Tena (A01027293)
- Ana Paola Minchaca (A01026744)
- Rodrigo Benavente (A01026973)

Learned DFS from:
https://www.tutorialspoint.com/data_structures_algorithms/depth_first_traversal.htm
'''
from os import listdir, path
class Node():
    def __init__(self, data):
        self.data = data
        self.neighbors = []

    
    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)
        

    def __eq__(self,other):
        if (isinstance(other, Node)):
            return self.data == other.data and self.neighbors == other.neighbors
        return False


def printObjectArray(array):
    tmpArray = []
    for element in array:
        tmpArray.append(element.data)
    
    return tmpArray


if __name__ == '__main__':
    # Prompt user to select file with NFA and read it
    print('Files in ./Graphs/ directory:')
    fileArray = []
    count = 1
    for file in listdir('./Graphs'):
            if file.endswith('.txt'):
                    print(path.join(str(count) + '. ', file))
                    fileArray.append(file)
                    count += 1
    
    prompt = input('\nWhich file number contains the undirected graph G that you want to run DFS on?: ')
    selectedFile = fileArray[int(prompt)-1]

    file = open('./Graphs/' + selectedFile)
    inputGraph = file.read()
    inputGraph = ''.join(inputGraph.split())

    print('\nRecieved undirected graph G string:')
    print(inputGraph)

    # Step 1: Parse input into arrays
    # inputGraph = '[[s,a,b,c,d],[[s,a],[s,b],[s,c],[a,s],[a,d],[d,a],[d,b],[d,c],[b,s],[b,d],[c,s],[c,d]]]'
    # inputGraph = '[[v1,v2,v3,v4,v5,v6,v7,v8,v9],[[v1,v2],[v1,v3],[v1,v4],[v2,v1],[v2,v3],[v2,v5],[v2,v6],[v3,v1],[v3,v2],[v3,v7],[v3,v8],[v4,v1],[v4,v8],[v5,v2],[v6,v2],[v7,v3],[v7,v9],[v8,v3],[v8,v4],[v9,v7]]]'
    inputGraph = inputGraph[1:len(inputGraph)-1]

    inputNodes = inputGraph.split('],[')[0]
    inputEdges = inputGraph.split(',[[')[1]
    inputEdges = inputEdges[0:len(inputEdges)-2].replace('],[',';').split(';')
    
    nodeList = inputNodes[1:len(inputNodes)].split(',')
    edgeList = []
    for tupple in inputEdges:
        tupple = tupple.split(',')
        edgeList.append(tupple)

    # Step 2: Build node objects and save in nodeArray
    nodeArray = []
    for node in nodeList:
        newNode = Node(node)
        nodeArray.append(newNode)

    # Step 3: Loop through every tupple in edgeList and append neighbors to each node
    for index in range(len(edgeList)):
        edge = edgeList.pop(0)

        currentNode = [None,-1]
        neighborNode = None

        for index, node in enumerate(nodeArray):
            if node.data == edge[0]:
                currentNode[0] = node
                currentNode[1] = index
        
        for node in nodeArray:
            if node.data == edge[1]:
                neighborNode = node
        
        currentNode[0].addNeighbor(neighborNode)
        nodeArray[currentNode[1]] = currentNode[0]
    
    # Step 4: Set DFS algorithm initial conditions
    stack = []
    visitedList = []
    L = []
    nextNode = nodeArray[0]

    print('\nNode Graph (Table form):')
    print('Node\tNeighbors')
    print('---------------------------')
    for node in nodeArray:
        print(node.data + '\t', printObjectArray(node.neighbors))
    
    print('\nInitial Condition:')
    print('----------------------------')
    print('Stack:', stack)
    print('Visited Node List:', visitedList)

    # Step 5: Run DFS Algorithm
    iterationCount = 0
    while iterationCount == 0 or len(stack) != 0:
        print('\nIteration ' + str(iterationCount))
        print('----------------------------')
        
        currentNode = nextNode
        L.append(currentNode)   # Add node to iteration order list L

        # Array with only node data for checking if node has been visited
        visitedListData = []
        for node in visitedList:
            visitedListData.append(node.data)
        
        # If current node has been visited, set flagVisited to True
        flagVisited = False
        try:
            visitedListData.index(currentNode.data)
            flagVisited = True
        except:
            flagVisited = False
        
        # If node has not been visited, append it to the visited list and to the stack
        if flagVisited == False:
            visitedList.append(currentNode)
            visitedListData.append(currentNode.data)
            stack.append(currentNode)

        print('Current Node: ' + currentNode.data)
        print('Current Node Neighbors: ', printObjectArray(currentNode.neighbors))
        print('Visited Node List: ', printObjectArray(visitedList))
        print('Stack: ', printObjectArray(stack))

        # If it's the first iteration, next node will be first neighbor in currentNode's neighbor array
        if len(visitedList) <= 1:
            nextNode = currentNode.neighbors[0]
            print('Next Node: ' + nextNode.data)
            iterationCount += 1
            continue
        
        # Check through all currentNode's neighbors to see if they have been visited and return the first neighbor node
        # that hasn't been visited
        neighbor = None
        for currentNeighbor in currentNode.neighbors:
            try:
                visitedListData.index(currentNeighbor.data)
            except:
                neighbor = currentNeighbor
        
        # If there is a neighbor node that has not been visited, make it the next node for iteration. Else, pop the current
        # node and return to latest node in stack
        if neighbor is not None:
            nextNode = neighbor
            print('Next Node: ' + nextNode.data)
        else:
            print('\n** No unvisited neighbors, popping node ' + currentNode.data + ' from stack **')
            stack.pop()
            print('Stack: ', printObjectArray(stack))
            # If stack has nodes, next node will be the latest node in stck. Else, finish iterating
            if len(stack) != 0:
                nextNode = stack[len(stack) - 1]
                print('Next Node: ' + nextNode.data)
            else:
                print('\nFinished Iterating.')

        iterationCount += 1
    
    print('\nOrder L of traversing graph G by DFS:')
    print('----------------------------')
    print('L: ', printObjectArray(L))