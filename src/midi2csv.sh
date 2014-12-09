# this script converts all midi files in a folder to csv files
# MIDITMP = ../data/midi/_tmp_
# CSVTMP = ../data/csv/_tmp_
MIDIFILES=../data/*.mid
for f in $MIDIFILES
do
  name="${f%.*}"
  echo "Processing $name ..."
  ./midicsv $name.mid $name.csv
  echo "done"
done


 
