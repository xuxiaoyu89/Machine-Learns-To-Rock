def exportQ(Q, filename):
  # @Q is map of [notes] --> int (count)
  # @save to file
  f = open(filename, 'w')
  for k in Q.keys():
    for n in k:
      f.write(n,",")
    f.write("\t")
    f.write(Q[k], "\n")
  close(f)

def importQ(filename, l = 2):
  # @file where Q is stored (format as exportQ)
  # @l arbitary length of notes to be imported
  # @return a map: Q
  Q = {}
  f = open(filename, 'r')
  for line in f:

    line = line.strip("\n").split("\t")
    if len(line) != 2: continue

    ns = line[0].strip(" ").split(",")
    if len(ns) != l: continue

    h, count = ns[0], int(line[1])
    try: Q[h]
    except KeyError: Q[h] = {}
    
    try: Q[h][ns[1]] += count
    except KeyError: Q[h][ns[1]] = count

  return Q


def compose(Q, S, F=[]):
  # The automaton machine
  # @Q is the set of all states
  # @S is sigma, the input sequence
  # @F is the final states, default empty
  # transitions and q0(initial)  will be computed
  first = True
  while S != []:
    t = "%s"%S.pop(0)
    if first:
      first = False
      



"""
Q = importQ("tmp")
print Q.values()
print Q.keys()
"""
