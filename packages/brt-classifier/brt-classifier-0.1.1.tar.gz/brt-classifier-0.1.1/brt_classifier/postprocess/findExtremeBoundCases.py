def findExtremeBoundCases(problem, idx, data):
  constrs = problem["constraint"]
  lowerBound = problem["lower-bound"]
  upperBound = problem["upper-bound"]

  if "(n)" in lowerBound and upperBound == "":
    print(constrs, "Θ(n)")
    data[idx]["upper-bound"] = lowerBound
    return 1
  elif "(1)" in upperBound and lowerBound == "":
    print(constrs, "Θ(1)")
    data[idx]["lower-bound"] = upperBound
    return 1
  
  return 0
