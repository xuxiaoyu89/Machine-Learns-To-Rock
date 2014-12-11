import process as proc
from process import NOTE_LEN, PITCH_LEN

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
  #for k in Q.keys():
    # print "key: ", k
    #for k1 in Q[k].keys():
      # print k1
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
    if len(t) < 2: t = "0"+t
    # print "rythm: "+t

    if melody.keys() == [] :
      print "...empty melody"
      for k in Q.keys():
        # print "key: ", k
        if k[(PITCH_LEN-NOTE_LEN):] == t: melody[k] = 0

      pool = getSum(Q, melody.keys())
      for k in melody.keys(): melody[k] = scale*float(getSum(Q, [k]))/pool

    else:
      old = list(melody.keys())
      for h in old: #current seq
        prev = h[-NOTE_LEN:] #last note on current seq
        p_h = melody[h] #pirio prob of current seq
        pool = getSum(Q, [prev]) #count for last note
        # print prev, pool 
        if pool != 0:
          # print len(Q[prev].keys())
          for q in Q[prev].keys():
	    # print q[3], t
            if q[PITCH_LEN:] == t: melody[h+q] = scale*p_h*float(Q[prev][q])/pool
        del melody[h]
    print "...%d seq available"%len(melody.keys())

  print "\ndone!\n"

  notes_t = sorted(melody.items(), key = lambda x: x[1])
  notes_t.reverse()

  """
  max_p, res = 0, "0"*NOTE_LEN
  for k in melody.keys():
    print "melody: ", k
    if melody[k] > max_p:
      max_p, res = melody[k], k
      
  print res, max_p

  notes_l = []
  for i in xrange(0, len(res)/NOTE_LEN):
    note = res[i*NOTE_LEN:(i+1)*NOTE_LEN]
    note_ = [int(note[:PITCH_LEN]), int(note[PITCH_LEN:])]
    notes_l.append(note_)
  """
  for x in notes_t:
    notes_l = list(x[0][i*NOTE_LEN:(i+1)*NOTE_LEN] for i in xrange(0, len(x[0])/NOTE_LEN))
    for i in xrange(len(notes_l)):
      notes_l[i] = "%3s-%2s"%(int(notes_l[i][:PITCH_LEN]), int(notes_l[i][PITCH_LEN:]))

    notes_s = " ".join(notes_l)
    print notes_s, x[1]
  return notes_t
  

"""
Q = importQ("tmp")
print Q.values()
print Q.keys()
"""
