# This script extract notes via audiobio from wav files

TMP=../data/_tmp_
WAVFILES=../data/*.wav
for f in $WAVFILES
do
  name="${f%.*}"
  echo "Processing $name ..."
  aubionotes -i $f -v > $TMP 2>&1
  sed '1, 5d' $TMP > $name.notes
  echo "Done"
done

rm $TMP
echo "\n\n"

