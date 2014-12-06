import numpy
import wave
import sys

wav = wave.open(sys.argv[1])
#print "sample width: ", wav.getsampwidth()
datatype = numpy.dtype('<i' + str(wav.getsampwidth()))  # Little endian
#print "datatype: ",  datatype
raw_data = numpy.fromstring(wav.readframes(wav.getnframes()), datatype)
#print "raw_data: ", raw_data
channels_data = [raw_data[i::wav.getnchannels()] for i in xrange(wav.getnchannels())]
#print channels_data
#print "nchannels: ", wav.getnchannels()
#nframe = wav.getnframes()
#print nframe


def tune(data):
    fft_data = numpy.fft.rfft(data)
    new_fft = [fft_data[round(i/1.25)] for i in xrange(len(fft_data))]
    return numpy.fft.irfft(new_fft)

def tuneChannel(data):
    ret = []
    chunksize = wav.getframerate() / 8
    for i in xrange(0, len(data), chunksize):
        print i
        chunk = data[i:i+chunksize]
        ret += list(tune(chunk))
    return ret

for i in xrange(len(channels_data)):
    channels_data[i] = tuneChannel(channels_data[i])

final_data = []
for j in xrange(len(channels_data[0])):
    for i in xrange(len(channels_data)):
        final_data += [channels_data[i][j]]
final_data = numpy.array(final_data, dtype=datatype).tostring()

new_wav = wave.open('out.wav', 'w')
new_wav.setparams(wav.getparams())
new_wav.writeframes(final_data)
new_wav.close()
