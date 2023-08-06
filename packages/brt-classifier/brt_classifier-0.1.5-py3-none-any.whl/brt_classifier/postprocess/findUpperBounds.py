
def findUpperBounds(problem, idx, data):
  constrs = set(problem["constraint"])
  upperBound = problem["upper-bound"]

  if upperBound == "":
    prevProblems = data[:idx]
    for prevProblem in prevProblems:
      prevConstrs = set(prevProblem["constraint"])
      prevUpperBound = prevProblem["upper-bound"]

      if prevUpperBound != "" and prevUpperBound != "(n)" and prevUpperBound != "(n)" and prevUpperBound != "unsolvable" and prevConstrs.issubset(constrs):
        data[idx]["upper-bound"] = prevUpperBound
        print(constrs, prevUpperBound)
        return 1

  return 0
