#!/usr/bin/python3
import hashlib, sys


class MerkleTree:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
        self.hash = getHash(value)


def checkConsistency(l1, l2):
    i = 0
    while i < len(l1):
        if l1[i] != l2[i]:
            break
        i += 1
    if i < len(l1):
        return []
    f = open("merkle.trees", "w")
    f.write("Merkle Tree for 1 input \n")
    root1 = createTree(l1, f)
    f.write("\n\n")
    f.write("Merkle Tree for 2 input \n")
    root2 = createTree(l2, f)
    f.close()
    out = []
    out.append(root1.hash)
    with open("merkle.trees") as f:
        data = f.readlines()

    tree2Index = 0
    for i in range(len(data)):
        if data[i].startswith("Merkle Tree 2"):
            tree2Index = i
    parentLines = []
    leftChildLines = []
    rightChildLines = []
    for i in range(tree2Index, len(data)):
        if data[i].startswith("Parent("):
            parentLines.append(data[i])

    for i in range(tree2Index, len(data)):
        if data[i].startswith("Left"):
            leftChildLines.append(data[i])

    for i in range(tree2Index, len(data)):
        if data[i].startswith("Right"):
            rightChildLines.append(data[i])
    out = []
    flag = False
    for i in range(len(parentLines)):
        if root1.hash in parentLines[i]:
            flag = True
            break
    if flag:
        values = []
        combinedHash = ''
        lc = root1.value
        while combinedHash != root2.hash:
            for i in range(len(leftChildLines)):
                if lc in leftChildLines[i].split(" ")[-6]:
                    rc = rightChildLines[i].split(" ")[-6]
                    values.append(getHash(rc))
                    break
            combinedValue = combined(getHash(lc), getHash(rc))
            combinedHash = getHash(combinedValue)
            lc = combinedValue

        out.append(root1.hash)
        out += values
        out.append(root2.hash)

    else:
        root1LeftChildValue = data[tree2Index - 5].split(" ")[-6]
        root1RightChildValue = data[tree2Index - 4].split(" ")[-6]
        root1RightChildSiblingValue = l2[l2.index(root1RightChildValue) + 1]
        values = []
        values.append(getHash(root1LeftChildValue))
        values.append(getHash(root1RightChildValue))
        values.append(getHash(root1RightChildSiblingValue))
        root1RightChildCombinedValue = combined(getHash(root1RightChildValue), getHash(root1RightChildSiblingValue))
        combinedHash = ''
        lc = root1LeftChildValue
        rc = root1RightChildCombinedValue
        while combinedHash != root2.hash:
            combinedValue = combined(getHash(lc), getHash(rc))
            combinedHash = getHash(combinedValue)
            lc = combinedValue
            for i in range(len(leftChildLines)):
                if lc in leftChildLines[i].split(" ")[-6]:
                    rc = rightChildLines[i].split(" ")[-6]
                    values.append(getHash(rc))
                    break

        out.append(root1.hash)
        out += values
        out.append(root2.hash)

    return out


def createTree(leaves, f):
    nodes = []
    for i in leaves:
        nodes.append(MerkleTree(i))

    while len(nodes) != 1:
        temp = []
        for i in range(0, len(nodes), 2):
            node1 = nodes[i]
            if i + 1 < len(nodes):
                node2 = nodes[i + 1]
            else:
                temp.append(nodes[i])
                break
            f.write("Left child : " + node1.value + " | Hash : " + node1.hash + " \n")
            f.write("Right child : " + node2.value + " | Hash : " + node2.hash + " \n")
            concatenatedHash = node1.hash + node2.hash
            parent = MerkleTree(concatenatedHash)
            parent.left = node1
            parent.right = node2
            f.write(
                "Parent(concatenation of " + node1.value + " and " + node2.value + ") : " + parent.value + " | Hash : " + parent.hash + " \n")
            temp.append(parent)
        nodes = temp
    return nodes[0]


def getHash(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def combined(value1, value2):
    combinedValue = value1 + value2
    return combinedValue


if __name__ == "__main__":
    arr1 = sys.argv[1]
    arr2 = sys.argv[2]
    l1 = arr1[1:len(arr1) - 1].split(",")
    l2 = arr2[1:len(arr2) - 1].split(",")

    val = checkConsistency(l1, l2)

    if len(val) > 0:
        print("Yes", val)
    else:
        print("No")