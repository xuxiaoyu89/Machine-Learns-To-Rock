from process import Notes
import random
import automate
 
# process.generateNotes(filename) return list of notes
# note: a string, consist of note number and duaration

class Mining:
    def __init__(self, n, ms):
	self.notes = n
	self.idx = []
	self.minsup = ms
	for i in xrange(len(n)-1):
            self.idx.append(i)

    # return a list of frequent patterns: list of lists
    def getNotes(self, begin, depth):
        #print len(self.notes), self.idx[begin], depth
        return self.notes[self.idx[begin] + depth]

    def vectorSwap(self, i, j, l):
        while l > 0:
	    self.idx[i], self.idx[j] = self.idx[j], self.idx[i]
	    i += 1
	    j += 1
	    l -= 1

    def doMining(self, begin, end, depth, equal):
        #printList()
        results = []
        count = end - begin
        if count < self.minsup:
            return results
        elif equal:
            # append to the list
            # only append whose length is between 1 and 10
            if depth > 1 and depth < 10:
                results.append([list(self.notes[begin:begin+depth]), count])
        pivot = random.randint(begin, end-1)
        self.idx[begin], self.idx[pivot] = self.idx[pivot], self.idx[begin]
        t = self.getNotes(begin, depth)
        #print "pivot: ", t
        a, c = begin+1, end-1
        b, d = a, c
        r = None
        while True: 
	    while b <= c and (self.getNotes(b, depth) <= t):
	        if self.getNotes(b, depth) == t:
		    self.idx[a], self.idx[b] = self.idx[b], self.idx[a]
		    a += 1
	        b += 1
	    while b <= c and (self.getNotes(c, depth) >= t):
	        if self.getNotes(c, depth) == t:
		    self.idx[c], self.idx[d] = self.idx[d], self.idx[c]
		    d -= 1
	        c -= 1
	    if b > c:
	        break
	    self.idx[b], self.idx[c] = self.idx[c], self.idx[b]
	    b += 1
 	    c -= 1
        range = min(a-begin, b-a)
        self.vectorSwap(begin, b-range, range)
        range = min(d-c, end-d-1)
        self.vectorSwap(b, end-range, range)
        #print "idx: ", idx
        range = b-a
        results += self.doMining(begin, begin+range, depth, False)
        # "000" is the end of the music
        if t != "0000": 
	    #print begin+range, range+a+end-d-1, depth+1
	    results += self.doMining(begin+range, range+a+end-d-1, depth+1, True)
        range = d - c
        results += self.doMining(end-range, end, depth, False)
        return results

    def mining(self):
        return self.doMining(0, len(self.notes)-1, 0, False)


def getNoteSeq(note):
    noteSeq = ""
    for i in xrange(len(note)-1):
	noteSeq += note[i] + ","
    noteSeq += note[-1]
    return noteSeq

"""
n = Notes()
freqNotes = {}
minsup = 3
for i in xrange(10):
    print "now mining: ", i
    filename = "../data/" + str(i) + ".notes"
    notes = n.generateNotes(filename)
    m = Mining(notes, 2)
    fnotes = m.mining()
    print len(fnotes)
    print fnotes[0]
    for note in fnotes:
        noteSeq = getNoteSeq(note[0])
	if noteSeq in freqNotes:
	    freqNotes[noteSeq] += note[1]
	else:
	    freqNotes[noteSeq] = note[1]
#output to a file: ../freq_samples
QFile = "../freq_samples/freq.notes"
fo = open(QFile, "w+")
for key in freqNotes:
    if freqNotes[key] >= minsup:
	print key
        fo.write(key + "\t" + str(freqNotes[key]) + "\n")
fo.close()

Q = automate.importQ(QFile)
S = [1,1,1,1,1,1,1,1,1,1]
melody = automate.compose(Q, S)

automate.export2CSV(melody, "../out.csv")
"""
