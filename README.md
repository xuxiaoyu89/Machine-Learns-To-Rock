FML-project
===========

machine learning project - algorithmic composition


To do list
1. write a shell to generate midi files to csv files
2. write a function in process.py to extract notes sequences from csv files, note format: note + duration

----------How To Run
Generate Notes from wav:

sh src/extract_notes.sh  # --> generate from *.wav to *.notes in data/

To Train from notes:

python src/main.py train  # --> generate from data/*.notes to Frequent Pattern Mining data file (1 single file)

To Compose:

python src/main.py automate  # --> generate from FPM 1 single file as Q, run automaton, get melody in midi

