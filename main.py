""" main file """

""" 
- get user input to enter the file to be compressed, and the new compressed file name
- may have to include the actual tree itself in the new compressed file


- should have a shell user interface ('>'), lets user get help, compress, or decompress
- when completed, compare an original txt file and a compressed-then-decompressed file using linux command 'diff' 
  there shouldn't be any differenc in size between the two files.

TODO: incorporate a hash map for O(1) lookup time when looking up the encodings???
"""

import huff, sys, os

#global vars, to be used so that the values are preserved for recursive function returns
stack = list(); dict = dict()


#if the file already exists, remove it, otherwise do nothing
def removeFile(compressedFileName):
    try:
        os.remove(compressedFileName)
    except:
        pass

#convert a list of ints, into a single bit string ([1,0,1] -> 0b101)
def listToBinary(l):
    rev = list(reversed(l))
    tmp = 0   #to contain the int equivalent of the bit string
    for i in range(len(rev)):  #convert the list of 1s and 0s into the integer equivalent
        tmp += rev[i]*(2**i)
        
    tmp = bin(tmp)   #this returns a bit string
    print( tmp )

    #TODO: up to here, find a way to convert the above string (tmp) into binary equivalent 
    #TODO: possibly an easier way would be to assign bits instead of ints on lines 73+78 

    return tmp

#read in from the source file, write the relevant huffman code to the compressed file
def compressFile(newFile, sourceFile):
    line = "0"
    while(line is not ""):
        line = sourceFile.readline()
        for i in line:
            newFile.write( listToBinary( dict[i]) )


#create a dictionary of the encodings for each symbol for convenient lookup
def huffmanEncoding(t): #, dict, stack):
    global stack, dict
    #iterate through the huffman tree, and create key value pairs (symbol : binary huffman code)
    #recursively visit each node in the tree, keeping track of directions via a stack 
    #(if you go left, push 1 , go right means push 0, if you return upwards, pop from stack)
    #the stack's left-right/1-0 sequence corresponds to a binary Huffman encoding, so store
    #the key:value/char:encoding pair in the dictionary...
    t.visited = 1  #mark the current node as visited

    #if the node is a Node, collect the char, assign the code, and return
    if(type(t).__name__ is "Node"):
        #print(t.val)
        #dict[t.val] = 0  
        dict.update({t.val : stack[0:len(stack)]})   #assign the symbol to its Huffman code
        stack.pop()  #pop stack element from the end
        return

    elif(type(t).__name__ is "ParentNode"):
        if(t.l is not None):   
            if(not t.l.visited):
                stack.append(1)   #store the stack values as ints?
                #print(stack)      #debugging output
                huffmanEncoding(t.l)
        if(t.r is not None):   
            if(not t.r.visited):
                stack.append(0)   #store the stack values as ints?
                #print(stack)      #debugging output
                huffmanEncoding(t.r)
        
        if(len(stack) != 0):
            stack.pop()
        return


#form the huffman tree, given the sorted list of Nodes, return the root Node of the tree
def huffmanTree(frequencyList):
    #join last two nodes via a parent node
    #parent node value = sum of child node values 
    #place parent node in the list (accoring to the ParentNode's frequency)
    #repeat until there are only two nodes left, form final node = root node

    for i in range(len(frequencyList)-1):
        if(len(frequencyList) is 2):
            break

        newNode = huff.ParentNode( frequencyList[-1].frequency + frequencyList[-2].frequency )

        newNode.l = frequencyList[-2]
        newNode.r = frequencyList[-1]
        frequencyList.pop()
        frequencyList.pop()
        
        #now place the ParentNode in the correct order in the frequencyList
        for j in range(len(frequencyList)):
            if(newNode.frequency >= frequencyList[j].frequency):
                frequencyList.insert(j, newNode)
                break
            if(j == len(frequencyList)-1):
                frequencyList.insert(len(frequencyList), newNode)

    newNode = huff.ParentNode( frequencyList[0].frequency + frequencyList[1].frequency )
    newNode.l = frequencyList[0]
    newNode.r = frequencyList[1]
    frequencyList.pop()
    frequencyList.pop()
    frequencyList.insert(0, newNode)
    return frequencyList[0]


#find whether symbol is in list, list is an array of Nodes
def inList(l, symbol):
    ret = -1
    for i in range(len(l)):
        if(l[i].val == symbol):
            ret = i
            break

    return ret

#read in each symbol from the file and store the symbol frequency in a list of Nodes
def readSymbols(f):
    l = list()
    line = f.readline()

    while(len(line) is not 0):
        for i in line:
            #if the list is empty
            if(len(l) == 0):
                l.append( huff.Node(i) )
            
            #list isn't empty, check if the symbol is already present
            else:
                ind = inList(l, i)
                if(ind == -1):  #the symbol is not in the list, needs appending
                    l.append( huff.Node(i) )
                else:           #the symbol is in the list, increment frequency by one
                    l[ind].increment()
        line = f.readline()
    return l


#find the file to be compressed
print("*** Huffman coding compression, github: LiamSkirrow ***")
fileName = input("Enter name of text file to be compressed: ")

#compressedFileName = input("Enter name of compressed file: ")  #UNCOMMENT THIS!!!!!!!
compressedFileName = "COMPRESSED.txt"

try:
    sourceFile = open(fileName, "r")
except:
    print("Error in trying to open file...")
    sys.exit()

#now read in each symbol/char from the file, and keep track of symbol frequency
frequencyList = readSymbols(sourceFile)
sourceFile.close()

#now sort the frequency list in descending order (according to Node.frequency)
frequencyList.sort(key=lambda x: x.frequency, reverse=True)

#get the root node of the huffman tree
treeRoot = huffmanTree(frequencyList)

#encode each symbol from the huffman tree
huffmanEncoding(treeRoot)
print(dict)

#remove the file if it exists
removeFile(compressedFileName)

newFile = open(compressedFileName, "ab")  #what if this file already exists?
sourceFile = open(fileName, "r")

#*** if newFile already exists, then delete it and select the "a" flag to append text ***
#*** use a try catch statement to test whether the file exists ***

compressFile(newFile, sourceFile)
newFile.close(); sourceFile.close()