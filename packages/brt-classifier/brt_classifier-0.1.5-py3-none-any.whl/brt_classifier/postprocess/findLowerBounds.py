def findLowerBounds(problem, idx, data):
  constrs = set(problem["constraint"])
  lowerBound = problem["lower-bound"]

  if lowerBound == "":
    prevProblems = data[idx+1:]
    for prevProblem in prevProblems:
      prevConstrs = set(prevProblem["constraint"])
      prevLowerBound = prevProblem["lower-bound"]

      if prevLowerBound != "" and prevLowerBound != "(1)" and prevLowerBound != "(1)" and prevLowerBound != "unsolvable" and constrs.issubset(prevConstrs):
        data[idx]["lower-bound"] = prevLowerBound
        print(constrs, prevConstrs, prevLowerBound)
        return 1

  return 0
