#! /usr/bin/env python
import re, math
import sys, os
from aubio import source, freqtomidi
from aubio import pitch as Pitch
import numpy
import subprocess
import classifier
from classifier import Classifier

#folder where we store all the training data
foldername = "samples"

# A function with no learning algorithms in it, calculates the average over all pitch and vocal tract length.
# Male above 18 years.
# Male below 18 years.
# Female above 18 years.
# Female below 18 years.
def ageBenchmarks(pitch, vtl):
    avgp = 0
    avgtl = 0

    for i in pitch:
        avgp += i[0]

    for i in vtl:
        avgtl += i.item()

    return avgp / len(pitch), avgtl / len(vtl)


# A function to calculate the vocal tract length of the speaker
#    VTL = c / 4F
def VocalTractLength(formant):
    return (3 * (10**8)) / (4 * formant)

# A list to store all the vocal tract lengths
vtl = []

# Size with which to instantiate numpy array
num_samples = len([name for name in os.listdir(foldername) if os.path.isfile(os.path.join(foldername,name))])

# numpy arrays to store average pitch and gender
trainingpitch = numpy.zeros(shape=(num_samples,1))
targets = numpy.zeros(num_samples)

# A list to store the file which corresponds to the current example
samplelist = []

# An iterator over the numpy array
current = 0

for fname in os.listdir(foldername):
    filename = os.path.join(foldername, fname)
    downsample = 1
    samplerate = 44100 / downsample
    if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

    win_s = 4096 / downsample # fft size
    hop_s = 512  / downsample # hop size

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = Pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("freq")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []
    time_stamp=[]
    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        #pitch = int(round(pitch))
        confidence = pitch_o.get_confidence()
        #if confidence < 0.8: pitch = 0.
        #print "%f %f %f" % (total_frames / float(samplerate), pitch, confidence)
        time_stamp+=[(total_frames/float(samplerate))]
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    if 0: sys.exit(0)

    #print time_stamp
    # Invoking aubiocut to detect when a word of spoken.
    sub = subprocess.Popen(['python', 'aubiocut',  filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = sub.communicate()[0]

    # Importing Regular Expression Modules for extracting the output[timestamp] of Aubiocut

    timestamps=re.findall("\d+.\d+\d+\d+\d+", out)
    #print timestamps

    extracted_voice=[]

    for i in timestamps:
    	i=float(i)
    	for j in range(len(time_stamp)):
            #Using the floor functions the timestamp is extracted when speakers spoke a word.
    		temp1=math.floor(i*10)/10
    		temp2=math.floor((time_stamp[j])*10)/10
    		#print str(temp1)+ " and "+str(temp2)
    		# if pitch >10000 then it is considered Noice in our environment.
    		if temp1==temp2 and pitches[j]<10000.0:
    			#print "True"+str(j)+pitches[j]
    			extracted_voice+=[pitches[j]]

    #print extracted_voice

    vtl.append(VocalTractLength(extracted_voice[0]))

    avg=0.0
    for i in extracted_voice:
    	avg+=i
    avg=avg/(len(extracted_voice))
#    print "Average Pitch of Extracted Voice: "+ str(avg)

    # Store the average pitch in our array
    trainingpitch[current] = [avg]

    samplelist.append(fname)

    labels = fname.split('.')[0].split(' ')

    if labels[2] == 'MALE':
        targets[current] = 1
    elif labels[2] == 'FEMALE':
        targets[current] = 0

    current = current + 1

global clf
clf = Classifier(trainingpitch, targets, samplelist)

global pavg, vtlavg
pavg, vtlavg = ageBenchmarks(trainingpitch.tolist(), vtl)
