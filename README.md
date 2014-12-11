FML-project
===========

machine learning project - algorithmic composition


To do list

1. write a shell to generate midi files to csv files

2. write a function in process.py to extract notes sequences from csv files, note format: note + duration


----------format:
1. midi clock: A MIDI timing reference signal used to synchronize pieces of 
equipment together. MIDI clock runs at a rate of 24 ppqn (pulses per quarter
note).

2. csv structure: 
column 1: track num
colume 2: midi clock
colume 5: midi note (0-127)

3. Distribution of notes length
h is loged notes length, length 1 here is a 1/128 notes

> h$breaks
 [1]  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18
> h$counts
 [1] 46550  3260  3945 18666 35722 49710 56351 51277 32116 10395  2852   864
[13]   491   402   188    39     6     5

round all >10 to 10 -- 4-full notes
8 is full note

there are 3064 equals to  after floor operation, we discard those equals to 0 after ROUND in the program

4. Notes struct:

a string[5] = pitch[0:3] + length[3:5]
pitch 0~127
length (log2) 0-18 --> 1-10


----------How To Run
Generate Notes from wav:

sh src/extract_notes.sh  # --> generate from *.wav to *.notes in data/

To Train from notes:

python src/main.py train  # --> generate from data/*.notes to Frequent Pattern Mining data file (1 single file)

To Compose:

python src/main.py automate  # --> generate from FPM 1 single file as Q, run automaton, get melody in midi

