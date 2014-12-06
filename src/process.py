# normalize parameters
INTERVAL_MAX = 2.0
INTERVAL_PACE = 4

# Notes processing class
class Notes:
  def __init__(self, f):
    self.file = f

  def generateNotes(self, f, upperbound=INTERVAL_MAX):
    pitches = []
    intervals = []
    for line in open(f):
      # some lines are empty
      if len(line) < 3:
	continue
      a = line.strip("\n").split()
      interval = float(a[2])-float(a[1])
      if interval < upperbound :
        b = a[0].split('.')
	# if note < 10, add a '0'  
	if len(b[0]) == 1:
	    b[0] = "0" + b[0]
        pitches.append(b[0])
        intervals.append(interval)

    notes = self.normalizeIntervals(pitches, intervals)
    notes.append("000")
    return notes

  def normalizeIntervals(self, pitches, intervals):
    # @ list of intervals, float
    # @convert into normalize 1-4 string list

    d = (max(intervals) - min(intervals))/INTERVAL_PACE
    # !!!!!!!!!1

    intervals = list("%d"%round(e/d+1) for e in intervals)
    
    # each note include its pitch and its duaration
    norm_res = list(pitches[i] + intervals[i] for i in xrange(len(intervals)))
    
    # each note inclued only its pitch
    # norm_res = pitches
    return norm_res

