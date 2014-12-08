import sys, os

help_doc="""
Missing or Wrong parameter.
Usage:

	python main.py train|compose

Exiting...
"""

if len(sys.argv) < 2:
  print help_doc
  sys.exit()

else:
  import process
  import mining as mine
  import automate as atm
  op = sys.argv[1]
  if op == "train" and len(sys.argv) >3: 
    train(sys.argv[2], sys.argv[3])
  if op == "cocmpose" and len(sys.argv)>3:
    csv = None if len(sys.argv) < 4 else sys.argv[4] 
    compose(sys.argv[2], sys.argv[3], csv)
  else:
    print help_doc
    sys.exit()


def train(path="../data/", minsup=3, out="../freq_samples/freq.notes"):
  n = Notes()

  try: files = os.listdir(path)
  except OSError:
    print "Invalid Directory: "+path+"\nExiting...\n"
    return

  print "Training in "+path+"..."

  freqNotes, mined = {}, 0
  for f in files:
    if !f.endswith(".notes"): continue
    print "now mining: ", f

    notes = n.generateNotes(f)
    m = mine.Mining(notes, 2)
    fnotes = m.mining()
    print len(fnotes), fnotes[0]
    for note in fnotes:
      noteSeq = mine.getNoteSeq(note[0])
      if noteSeq in freqNotes:
	freqNotes[noteSeq] += note[1]
      else:
	freqNotes[noteSeq] = note[1]
  print "...Done!\nSaving to "+out+"\nExit..."
  atm.exportQ(freqNotes, out, minsup)
  return out

def compose(QFile, SFile, CSVFile="../melody.csv"):
  Q = atm.importQ(QFile)
  S = list(int(line.strip("\n")) for line in open(SFile, 'r'))
  print "Composing based on "+QFile+"\n\twith rythm in "+SFile
  melody = atm.compose(Q, S)
  print "...Done!\nExport to csv...\nExit..."
  atm.export2CSV(melody, CSVFile)


