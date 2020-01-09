import collections as coll
def getAverage(strings,length = 100):
    tempGen = ""
    mostCommonString = ""
    for j in range(length):
        for i in range(len(strings)):
                tempGen += strings[i][j]
        mostCommonString += (coll.Counter(tempGen).most_common(1))[0][0]
        tempGen = ""
    return mostCommonString


testString = ["AAAA","BBBB","DDAD","ABCD"]
print(getAverage(testString, 4))
