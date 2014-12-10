# normalize parameters
INTERVAL_MAX = 2.0
INTERVAL_PACE = 4


# Notes processing class
class Process:
  def generateNotes(self, f, upperbound=INTERVAL_MAX):
    pitches = []
    intervals = []
    noteSeqs = []
    filename = f.rstrip(".csv")
    # print filename
    # file = open(filename+".note", "w")
    
    prev = None
    for line in open(f):
      # some lines are empty
      a = line.strip("\n").split(', ')
      if a[2] == "Note_on_c":
	if prev == None:
          prev = [a[0], a[1], a[4]]
	# end of a track
        elif a[0] != prev[0]:
	  prev = [a[0], a[1], a[4]]
          # print a[0], len(intervals)
	  # append noteSeq to noteSeqs
	  if len(intervals) != 0:
	    noteSeq = self.normalizeIntervals(pitches, intervals)
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
	    # print (int(a[1])-int(prev[1]))/1000.0
	    intervals.append((int(a[1])-int(prev[1]))/1000.0)
	    prev = [a[0], a[1], a[4]]
    for noteSeq in noteSeqs:
      for note in noteSeq:
	# print note
    return noteSeqs

    #noteseq = self.normalizeIntervals(pitches, intervals)
    #noteseq.append("0000")
    #return notes

  def normalizeIntervals(self, pitches, intervals):
    # @ list of intervals, float
    # @convert into normalize 1-4 string list
    max_i, min_i = max(intervals), min(intervals)
    d = (max_i - min_i)/INTERVAL_PACE
    # !!!!!!!!!1
    if d == 0: intervals = list("1" for e in intervals)
    else: intervals = list("%d"%round((e-min_i)/d+1) for e in intervals)
    # each note include its pitch and its duaration
    norm_res = list(pitches[i] + intervals[i] for i in xrange(len(intervals)))
    # each note inclued only its pitch
    # norm_res = pitches
    return norm_res
'''
n = Notes()
n.generateNotes("../data/1501gbson1.csv")

path = "../data/"
try: files = os.listdir(path)
  except OSError:
    print "Invalid Directory: "+path+"\nExiting...\n"
    return

  for f in files:
    if not f.endswith(".csv"): continue
    f = path+f
    noteSeqs = n.generateNotes(f)
'''
