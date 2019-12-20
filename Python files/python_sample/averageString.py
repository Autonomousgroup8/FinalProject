import collections as coll
def getAverage(strings,length = 100):
    tempGen = ""
    for j in range(length):
        for i in range(len(strings)):
                tempGen += strings[i][j]
        mcl = (coll.Counter(tempGen).most_common(1))
        return mcl
