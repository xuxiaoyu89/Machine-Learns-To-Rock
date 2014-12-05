import process
import random
# process.generateNotes(filename) return list of notes
# note: a string, consist of note number and duaration

notes = []
idx = []
minsup = 0

# return a list of frequent patterns: list of lists
def getNotes(begin, depth):
    #print len(notes), idx[begin], depth
    return notes[idx[begin] + depth]

def vectorSwap(i, j, l):
    while l > 0:
	idx[i], idx[j] = idx[j], idx[i]
	i += 1
	j += 1
	l -= 1

def printList():
    l = []
    for i in xrange(len(idx)):
	l += notes[idx[i]]
    print l

def doMining(begin, end, depth, equal, results):
    #printList()
    count = end - begin
    if count < minsup:
        return
    elif equal:
        #append to the list
        print notes[idx[begin]:idx[begin]+depth], count
        results.append(list(notes[begin:begin+depth]))
    pivot = random.randint(begin, end-1)
    idx[begin], idx[pivot] = idx[pivot], idx[begin]
    t = getNotes(begin, depth)
    #print "pivot: ", t
    a, c = begin+1, end-1
    b, d = a, c
    r = None
    while True: 
	while b <= c and (getNotes(b, depth) <= t):
	    if getNotes(b, depth) == t:
		idx[a], idx[b] = idx[b], idx[a]
		a += 1
	    b += 1
	while b <= c and (getNotes(c, depth) >= t):
	    if getNotes(c, depth) == t:
		idx[c], idx[d] = idx[d], idx[c]
		d -= 1
	    c -= 1
	if b > c:
	    break
	idx[b], idx[c] = idx[c], idx[b]
	b += 1
	c -= 1
    range = min(a-begin, b-a)
    vectorSwap(begin, b-range, range)
    range = min(d-c, end-d-1)
    vectorSwap(b, end-range, range)
    #print "idx: ", idx
    range = b-a
    doMining(begin, begin+range, depth, False, results)
    # "000" is the end of the music
    if t != "0": 
	#print begin+range, range+a+end-d-1, depth+1
	doMining(begin+range, range+a+end-d-1, depth+1, True, results)
    range = d - c
    doMining(end-range, end, depth, False, results)
    
def mining(notes, minsup):
    for i in xrange(len(notes)-1):
        idx.append(i)
    results = []
    return doMining(0, len(notes)-1, 0, False, results)

notes = ["1", "1", "2", "2", "1", "1", "2", "0"]
minsup = 2
print mining(notes, minsup)



