import json

def printStatistics(filePath):
  with open(filePath) as json_file:
    data = json.load(json_file)

    lowerBoundConstant = 0
    upperBoundConstant = 0
    constSolvable = 0

    lowerBoundLogStar = 0
    upperBoundLogStar = 0
    logStarSolvable = 0

    lowerBoundLoglog = 0
    upperBoundLoglog = 0
    loglogSolvable = 0

    lowerBoundLog = 0
    upperBoundLog = 0
    logSolvable = 0

    lowerBoundLinear = 0
    upperBoundLinear = 0
    linearSolvable = 0

    unsolvable = 0

    for p in data:
      lowerBound = p["lower-bound"]
      upperBound = p["upper-bound"]

      if lowerBound == "(1)":
        lowerBoundConstant += 1
      if upperBound == "(1)":
        upperBoundConstant += 1
      if lowerBound == "(1)" and upperBound == "(1)":
        constSolvable += 1

      if lowerBound == "(log* n)":
        lowerBoundLogStar += 1
      if upperBound == "(log* n)":
        upperBoundLogStar += 1
      if lowerBound == "(log* n)" and upperBound == "(log* n)":
        logStarSolvable += 1

      if lowerBound == "(loglog n)":
        lowerBoundLoglog += 1
      if upperBound == "(loglog n)":
        upperBoundLoglog += 1
      if lowerBound == "(loglog n)" and upperBound == "(loglog n)":
        loglogSolvable += 1

      if lowerBound == "(log n)":
        lowerBoundLog += 1
      if upperBound == "(log n)":
        upperBoundLog += 1
      if lowerBound == "(log n)" and upperBound == "(log n)":
        logSolvable += 1

      if lowerBound == "(n)":
        lowerBoundLinear += 1
      if upperBound == "(n)":
        upperBoundLinear += 1
      if lowerBound == "(n)" and upperBound == "(n)":
        linearSolvable += 1

      if lowerBound == "unsolvable":
        unsolvable += 1

    totalSize = len(data)

    print("In total: %s problems" % totalSize)
    print("Solvable in constant time: %s " % constSolvable)
    print("Solvable in log* time: %s " % logStarSolvable)
    print("Solvable in loglog time: %s " % loglogSolvable)
    print("Solvable in log time: %s " % logSolvable)
    print("Solvable in linear time: %s " % linearSolvable)
    print("Unsolvable: %s" % unsolvable)
    print("TBD: %s" % (totalSize - unsolvable - constSolvable - logStarSolvable - loglogSolvable - logSolvable - linearSolvable))
    print()

    print("Lower bounds")
    print("Constant time: %s " % lowerBoundConstant)
    print("Log* time: %s " % lowerBoundLogStar)
    print("Loglog time: %s " % lowerBoundLoglog)
    print("Log time: %s " % lowerBoundLog)
    print("Linear time: %s " % lowerBoundLinear)
    print("TBD: %s" % (totalSize - unsolvable - lowerBoundConstant - lowerBoundLogStar - lowerBoundLoglog - lowerBoundLog - lowerBoundLinear))
    print()

    print("Upper bounds")
    print("Constant time: %s " % upperBoundConstant)
    print("Log* time: %s " % upperBoundLogStar)
    print("Loglog time: %s " % upperBoundLoglog)
    print("Log time: %s " % upperBoundLog)
    print("Linear time: %s " % upperBoundLinear)
    print("TBD: %s" % (totalSize - unsolvable - upperBoundConstant - upperBoundLogStar - upperBoundLoglog - upperBoundLog - upperBoundLinear))
