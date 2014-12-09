# normalize parameters
INTERVAL_MAX = 2.0
INTERVAL_PACE = 4


# Notes processing class
class Notes:
  def generateNotes(self, f, upperbound=INTERVAL_MAX):
    pitches = []
    intervals = []
    noteSeqs = []
    prev = None
    for line in open(f):
      # some lines are empty
      a = line.strip("\n").split(', ')
      print a[2] 
      if a[2] == "Note_on_c":
        print "!!!!!"
	if prev == None:
          prev = [a[0], a[1], a[4]]
	# end of a track
        elif a[0] != prev[0]:
	  prev = [a[0], a[1], a[4]]
	  # append noteSeq to noteSeqs
	  noteSeq = self.normalizeIntervals(pitches, intervals)
          print "noteSeq len: ", len(noteSeq)
          noteSeqs.append(noteSeq)
          # clear pitches and intervals
          pitches[:] = []
	  intervals[:] = []
        else:
	  # this note has the same time with the prev one, ignore it
	  if a[1] == prev[0]:
	    continue
	  else:
	    # append the prev note
	    pitches.append(prev[4])
	    intervals.append(int(a[1])-int(prev[1]))
    print len(noteSeqs)
    print len(noteSeqs[0])
    return noteSeqs

    #noteseq = self.normalizeIntervals(pitches, intervals)
    #noteseq.append("000")
    #return notes

  def normalizeIntervals(self, pitches, intervals):
    # @ list of intervals, float
    # @convert into normalize 1-4 string list
    max_i, min_i = max(intervals), min(intervals)
    d = (max_i - min_i)/INTERVAL_PACE
    # !!!!!!!!!1
    intervals = list("%d"%round((e-min_i)/d+1) for e in intervals)
    # each note include its pitch and its duaration
    norm_res = list(pitches[i] + intervals[i] for i in xrange(len(intervals)))
    # each note inclued only its pitch
    # norm_res = pitches
    return norm_res

n = Notes()
n.generateNotes("../data/supr_mch.csv")



