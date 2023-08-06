from rooted_tree_classifier import is_log_solvable, is_log_star_solvable
from ..util import complexities

def findByExpDecider(problem, idx, data):
  constraints = set(problem["constraint"])
  lowerBound = problem["lower-bound"]
  upperBound = problem["upper-bound"]

  if upperBound == "" or lowerBound == "":
    decidedUpperBound = upperBound
    decidedLowerBound = lowerBound

    if is_log_star_solvable(constraints):
      decidedUpperBound = complexities[min(complexities.index(decidedUpperBound) if decidedUpperBound != "" else 100, complexities.index("(log* n)"))]
    else:
      decidedLowerBound = complexities[max(complexities.index(decidedLowerBound) if decidedLowerBound != "" else -1, complexities.index("(loglog n)"))]

    if is_log_solvable(constraints):
      decidedUpperBound = complexities[min(complexities.index(decidedUpperBound) if decidedUpperBound != "" else 100, complexities.index("(log n)"))]
    else:
      decidedLowerBound = complexities[max(complexities.index(decidedLowerBound) if decidedLowerBound != "" else -1, complexities.index("(n)"))]

    if (lowerBound != decidedLowerBound or upperBound != decidedUpperBound):
      data[idx]["lower-bound"] = decidedLowerBound
      data[idx]["upper-bound"] = decidedUpperBound
      print(constraints, lowerBound, upperBound, decidedLowerBound, decidedUpperBound)
      return 1

  return 0
