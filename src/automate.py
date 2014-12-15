import process as proc
from process import NOTE_LEN, PITCH_LEN
import random as rand

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
  csv_header.lstrip("\n")
  time, step = 0, proc.MIN_NOTE
  f.write(csv_header)

  for e in notes:
    pitch = int(e[:PITCH_LEN])
    length = round(step*2**int(e[PITCH_LEN:]))
    #2, 0, Note_on_c, 1, 81, 79
    #2, 960, Note_off_c, 1, 81, 0
    l1 = "2, %d, Note_on_c, 1, %d, 79\n"%(time, pitch)
    time += length
    l2 = "2, %d, Note_off_c, 1, %d, 0\n"%(time, pitch)
    f.write(l1)
    f.write(l2)
  f.write("2, %d, End_Track\n"%(time))
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


def randomPick(Q, t):
  # Q is dict, t is length_of_notes in string
  # return a notes (string) randomly (by probability)
  # that has length in Q
  candidates = []
  for k in Q.keys():
    if k[PITCH_LEN:] == t:
      for occur in xrange(getSum(Q, [k])):
        candidates.append(k)

  rand.shuffle(candidates)
  return candidates[int(rand.random()*len(candidates))]


def compose(Q, S, F=[]):
  # The automaton machine
  # @Q is the set of all states
  # @S is sigma, the input sequence
  # @F is the final states, default empty
  # transitions and q0(initial)  will be computed
  melody = ""
  while S != []:
    
    t = "%s"%S.pop(0)
    if len(t) < 2: t = "0"+t
    print "rythm: "+t, "melody "+melody

    if melody == "":
      melody = randomPick(Q, t)
    else:
      candidates = []
      prev = melody[-NOTE_LEN:]
      for q in Q[prev].keys():
        if q[PITCH_LEN:] == t:
          for i in xrange(Q[prev][q]):
            candidates.append(q)
      rand.shuffle(candidates)
      if candidates == []: melody += randomPick(Q, t)
      else: 
        melody += candidates[int(rand.random()*len(candidates))]
    print "found. now melody: ", melody

  print "\ndone!\n"

  notes_l = []
  for i in xrange(len(melody)/NOTE_LEN):
    # notes_l.append("%3s-%2s"%(int(melody[i*NOTE_LEN:i*NOTE_LEN+PITCH_LEN]), int(melody[i*NOTE_LEN+PITCH_LEN:(i+1)*NOTE_LEN])))
    notes_l.append(melody[i*NOTE_LEN:(i+1)*NOTE_LEN])

  notes_s = " ".join(notes_l)
  print notes_s

  return notes_l
  

"""
Q = importQ("tmp")
print Q.values()
print Q.keys()
"""
