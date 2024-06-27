def parseFile(filename):
    f = open(filename, "r")

    tid = 0
    prevTabCount = 0
    parents = []

    topicNames = {}
    topicPaths = {}
    topicIDs = {}
    levels = {}

    for line in f:
        if line != "\n":
            tid += 1

            name = line.strip("\t")
            name = name.strip("\n")
            if name[0] == " ":
                name = name[1:]

            tabCount = line.count("\t")

            if tabCount == 0:
                parent = 0
                parents.append(parent)

            elif tabCount > prevTabCount:
                parent = tid - 1
                parents.append(parent)

            elif tabCount < prevTabCount:
                for i in range(prevTabCount - tabCount):
                    parents.pop()
                parent = parents[-1]

            else:
                parent = parents[-1]

            name = name.lower().strip()

            topicNames[name] = tid
            topicIDs[tid] = name
            topicPaths[tid] = parent
            levels[tid] = tabCount + 1

            prevTabCount = tabCount

    f.close()

    return topicNames, topicPaths, topicIDs, levels


def getPath(keyword, topicNames, topicPaths, topicIDs):
    topicId = topicNames[keyword]
    path = [keyword]
    topicParent = topicPaths[topicId]

    while topicParent != 0:
        curr = topicIDs[topicParent]
        path.append(curr)
        topicParent = topicPaths[topicParent]

    return path
