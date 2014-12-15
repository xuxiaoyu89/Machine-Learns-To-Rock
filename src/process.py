# normalize parameters
FULL_NOTE = 24*4 # full note length in MIDIclock
MIN_NOTE = float(FULL_NOTE)/128 # minimum note length in ms
NOTE_LEN = 5
PITCH_LEN = 3

import os
import math

# Notes processing class
class Process:
  def generateNotes(self, f):
    pitches = []
    intervals = []
    noteSeqs = []
    tempo = 24
    '''
    filename = f.rstrip(".csv")
    print filename
    # file = open(filename+".note", "w")
    i = 0
    '''
    prev = None
    for line in open(f):
      # some lines are empty
      a = line.strip("\n").split(', ')
      if a[2] == "Header": tempo = float(a[5])/10
      if a[2] == "Note_on_c":
	if prev == None:
          prev = [a[0], a[1], a[4]]
	# end of a track
        elif a[0] != prev[0]:
	  prev = [a[0], a[1], a[4]]
          # print a[0], len(intervals)
	  # append noteSeq to noteSeqs
	  if len(intervals) != 0:
	    '''
	    file = open(filename + "-" + str(i) + ".notes", "w")
            i += 1
	    for j in xrange(len(pitches)):
	      file.write(pitches[j] + "\t" + str(intervals[j]) + "\n")
	    file.close()
            '''
            noteSeq = self.normalizeIntervals(pitches, intervals, tempo)
     	    noteSeq.append("0000")
            noteSeqs.append(noteSeq)
          # clear pitches and intervals
          pitches[:] = []
	  intervals[:] = []
        else:
	  # this note has the same time with the prev one, ignore it
	  if a[1] == prev[1]:
	    continue
	  else:
	    # append the prev note
	    if len(prev[2]) == 1: prev[2] = "00" + prev[2]
	    if len(prev[2]) == 2: prev[2] = "0" + prev[2]
	    pitches.append(prev[2])
	    intervals.append((int(a[1])-int(prev[1])))
	    prev = [a[0], a[1], a[4]]
    '''
    for noteSeq in noteSeqs:
      for note in noteSeq:
	 print note
    '''
    return noteSeqs

    #noteseq = self.normalizeIntervals(pitches, intervals)
    #noteseq.append("0000")
    #return notes

  def normalizeIntervals(self, pitches, intervals, tempo):
    '''
    # @ list of intervals, float
    # @convert into normalize 1-4 string list
    max_i, min_i = max(intervals), min(intervals)
    d = (max_i - min_i)/INTERVAL_PACE
    # !!!!!!!!!1
    if d == 0: intervals = list("1" for e in intervals)
    else: intervals = list("%d"%round((e-min_i)/d+1) for e in intervals)
    '''
    pitchL = []
    interL = []
    for i in xrange(len(intervals)):
      logInterval = int(round(math.log((intervals[i]*32/tempo), 2)))
      if logInterval > 0:
	if logInterval >= 10: interL.append(str(10))
        else: interL.append("0"+str(logInterval))
        pitchL.append(pitches[i])
    # each note include its pitch and its duaration
    norm_res = list(pitchL[i] + interL[i] for i in xrange(len(interL)))
    # each note inclued only its pitch
    # norm_res = pitches
    return norm_res

n = Process()
#n.generateNotes("../data/1501gbson1.csv")

'''
path = "../data/"
try: files = os.listdir(path)
except OSError:
  print "Invalid Directory: "+path+"\nExiting...\n"

for f in files:
  if not f.endswith(".csv"): continue
  f = path+f
  noteSeqs = n.generateNotes(f)
'''




