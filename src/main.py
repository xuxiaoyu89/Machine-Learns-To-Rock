import sys, os


def train(path="../data/", minsup=3, out="../freq_samples/freq.notes"):
  n = process.Notes()

  try: files = os.listdir(path)
  except OSError:
    print "Invalid Directory: "+path+"\nExiting...\n"
    return

  print "Training in "+path+"..."

  freqNotes, mined = {}, 0
  for f in files:
    if not f.endswith(".csv"): continue
    f = path+f
    print "now mining: ", f

    noteSeqs = n.generateNotes(f)
    if len(noteSeqs) == 0:
      continue
    for noteSeq in noteSeqs:
      m = mine.Mining(noteSeq, 2)
      fnotes = m.mining()
      # print len(fnotes), fnotes[0]
      if len(fnotes) == 0:
	continue
      for note in fnotes:
        noteSeq = mine.getNoteSeq(note[0])
        if noteSeq in freqNotes:
	  freqNotes[noteSeq] += note[1]
        else:
	  freqNotes[noteSeq] = note[1]
  print "...Done!\nSaving to "+out+"\nExit..."
  print "len of Q: ", len(freqNotes)
  atm.exportQ(freqNotes, out, minsup)
  return out

def compose(QFile, SFile, CSVFile):
  Q = atm.importQ(QFile)
  S = []
  for line in open(SFile, 'r'):
    line.strip("\n").strip(" ")
    if line != "":
      print line
      S.append(int(line))

  print "Composing based on "+QFile+"\n\twith rythm in "+SFile, len(S)
  melody = atm.compose(Q, S)
  print "...Done!\nExport to csv...\nExit..."
  atm.export2CSV(melody, CSVFile)

help_doc="""
Missing or Wrong parameter.
Usage:
  Train data:
	python main.py train \ \n
               "path_for_*.notes_dir" \ \n
               int_minsup

  Compose melody:
        python main.py compose \ \n
               "freq_notes_dir" \ \n
               "input_rythm_dir" \ \n
               "output_csv_dir" (optional, for midi)

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
    train(sys.argv[2], int(sys.argv[3]))
  elif op == "compose" and len(sys.argv)>4:
    compose(sys.argv[2], sys.argv[3], sys.argv[4])
  else:
    print help_doc
    sys.exit()



