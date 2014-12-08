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


def getSum(Q, k):
  # serve for compose, 
  # take list of keys in Q, return total counts in Q[k] <-- a map
  n = 0
  for e in k:
    n += sum(Q[k].values())
  return n

def compose(Q, S, F=[], scale=10):
  # The automaton machine
  # @Q is the set of all states
  # @S is sigma, the input sequence
  # @F is the final states, default empty
  # transitions and q0(initial)  will be computed
  # scale: prevent prob from being too small
  melody = {}
  while S != []:
    t = "%s"%S.pop(0)
    print "rythm: "+t
    if melody.keys() == [] :
      print "...empty melody"
      list(melody[k] = 0 for k in Q.keys() if k[2] == t)
      pool = getSum(Q, melody.keys())
      for k in melody.keys(): melody[k] = scale*float(getSum(Q, [k]))/pool
    else:
      old = list(melody.keys())
      for h in old: #current seq
        prev = h[-3:] #last note on current seq
        p_h = melody[h] #pirio prob of current seq
        pool = getSum(Q, [Q[prev]]) #count for last note
        list(melody[h+q] = scale*p_h*float(Q[prev][q])/pool for q in Q[prev].keys() if q[2] == t)
        del melody[h]
    print "...%d seq available"%len(melody.keys())

  print "\ndone!\n"

  max_p, res = 0, "000"
  for k in melody.keys():
    if melody[k] > max_p:
      max_p, res = melody[k], k

  print res, max_p
  notes_l = []
  for i in xrange(0, len(res)/3):
    note = res[i*3:i*3+3]
    notes_l.append(note)

  return notes_l
  



"""
Q = importQ("tmp")
print Q.values()
print Q.keys()
"""
