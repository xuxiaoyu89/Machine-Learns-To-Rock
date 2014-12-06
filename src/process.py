# normalize parameters
INTERVAL_MAX = 2.0
INTERVAL_PACE = 4

# Notes processing class
class Notes:
  def __init__(self, f):
    self.file = f

  def generateNotes(self, upperbound=INTERVAL_MAX):
    pitches = []
    intervals = []
    for line in open(self.file):
      a = line.strip("\n").split()
      interval = float(a[2])-float(a[1])
      if interval < upperbound :
        pitches.append(a[0])
        intervals.append(interval)

    return self.normalizeIntervals(pitches, intervals)

  def normalizeIntervals(self, pitches, intervals):
    # @ list of intervals, float
    # @convert into normalize 1-4 string list

    d = (max(intervals) - min(intervals))/INTERVAL_PACE
    # !!!!!!!!!1

    intervals = list("%d"%round(e/d) for e in intervals)
    norm_res = list(pitches[i] + intervals[i] for i in xrange(len(intervals)))
    return norm_res

notes = Notes("../data/mozart.notes")
x = notes.generateNotes()
print len(x)
print x
