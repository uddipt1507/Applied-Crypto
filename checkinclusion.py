#!/usr/bin/python3
import ast,sys,hashlib

def parseFile():
    f = open("merkle.tree","r")
    tree ={}
    for line in f:
        lineArray = line.split(" ")
        if lineArray[0] == 'Parent(concatenation':
            tree[lineArray[6]] = lineArray[10]
        else:
            tree[lineArray[3]] = lineArray[7]
    return tree

def checkInclusion(inputString,tree):
    out = []
    for key,value in tree.items():
        if inputString in key:
            out.append(value)
            inputString = value
    return out

inputString = sys.argv[1]
tree = parseFile()
out = checkInclusion(inputString,tree)
if(len(out)> 0):
    print("yes",out)
else:
    print("no")