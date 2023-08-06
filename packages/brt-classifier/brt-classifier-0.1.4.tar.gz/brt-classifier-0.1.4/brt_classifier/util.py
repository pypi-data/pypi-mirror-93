from functools import reduce

def getCanonical(constr):
  return min(constr, constr[::-1])

flatMap = lambda f, arr: reduce(lambda a, b: a + b, map(f, arr))

complexities = ["(1)", "(log* n)", "(loglog n)", "(log n)", "(n)"]
