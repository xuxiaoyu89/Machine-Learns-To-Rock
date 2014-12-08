import process as proc

def exportQ(Q, filename, minsup):
  # @Q is map of [notes] --> int (count)
  # @save to file
  f = open(filename, 'w')
  for k in Q.keys():
    if Q[k] >= minsup:
      f.write(k+"\t"+str(Q[k])+"\n")
  f.close()

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

csv_header='0, 0, Header, 1, 13, 384\n1, 0, Start_track\n1, 0, Time_signature, 4, 2, 24, 8\n1, 0, Key_signature, 0, "major"\n1, 0, Tempo, 451127\n1, 0, End_track\n2, 0, Start_track\n2, 0, MIDI_port, 0\n2, 0, Title_t, "E. Piano"\n'

csv_tail="0, 0, End_of_file"

def export2CSV(notes, filename):
  f = open(filename, 'w')
  #csv_header.lstrip("\n")
  time, step = 0, 1000/proc.INTERVAL_PACE
  f.write(csv_header)

  for e in notes:
    #2, 0, Note_on_c, 1, 81, 79
    #2, 960, Note_off_c, 1, 81, 0
    l1 = "2, %d, Note_on_c, 1, %d, 79\n"%(time*step,e[0])
    time += e[1]
    l2 = "2, %d, Note_off_c, 1, %d, 0\n"%(time*step,e[0])
    f.write(l1)
    f.write(l2)
  f.write("2, %d, End_Track\n"%(time*step))
  f.write(csv_tail)
  f.close()

def getSum(Q, k):
  # serve for compose, 
  # take list of keys in Q, return total counts in Q[k] <-- a map
  n = 0
  for e in k:
    try: n += sum(Q[e].values())
    except KeyError: pass
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
      for k in Q.keys():
        if k[2] == t: melody[k] = 0

      pool = getSum(Q, melody.keys())
      for k in melody.keys(): melody[k] = scale*float(getSum(Q, [k]))/pool

    else:
      old = list(melody.keys())
      for h in old: #current seq
        prev = h[-3:] #last note on current seq
        p_h = melody[h] #pirio prob of current seq
        pool = getSum(Q, [prev]) #count for last note
        if pool != 0:
          for q in Q[prev].keys():
            if q[2] == t: melody[h+q] = scale*p_h*float(Q[prev][q])/pool
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
    note_ = [int(note[0:2]), int(note[2])]
    notes_l.append(note_)

  return notes_l
  



"""
Q = importQ("tmp")
print Q.values()
print Q.keys()
"""
