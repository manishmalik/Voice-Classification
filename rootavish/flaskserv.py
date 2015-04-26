#! /usr/bin/env python
import classifier_pitch
from flask import Flask, jsonify, request
import base64, re
import sys
from aubio import source,freqtomidi
from aubio import pitch as p1
from classifier_pitch import clf
import subprocess
from numpy import array, ma
import matplotlib.pyplot as plt
from demo_waveform_plot import get_waveform_plot, set_xlabels_sample2time

#from classifier_pitch import clf

app = Flask(__name__)

@app.route('/classify/', methods=['POST'])
def pitchpy():

	filename = ""
	for i in request.json:
		with open(i,'wb') as f:
			filename = i
			f.write(base64.b64decode(request.json[i]))

		downsample = 1
		samplerate = 44100 / downsample

	win_s = 4096 / downsample # fft size
	hop_s = 512  / downsample # hop size

	s = source(filename, samplerate, hop_s)
	samplerate = s.samplerate

	tolerance = 0.8

        pitch_o = p1("yin", win_s, hop_s, samplerate)
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
	    print "%f %f %f" % (total_frames / float(samplerate), pitch, confidence)
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

	timestamps=re.findall("\d+.\d+\d+\d+\d+", out)
	print timestamps

	extracted_voice=[]

	import math

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

	print extracted_voice
	avg=0.0
	for i in extracted_voice:
		avg+=i
	avg=avg/(len(extracted_voice))
	print "Average Pitch of Extracted Voice: "+ str(avg)
	clf.classify([avg])
	skip = 1

	pitches = array(pitches[skip:])
	confidences = array(confidences[skip:])
	times = [t * hop_s for t in range(len(pitches))]

	fig = plt.figure()

	ax1 = fig.add_subplot(311)
	ax1 = get_waveform_plot(filename, samplerate = samplerate, block_size = hop_s, ax = ax1)
	plt.setp(ax1.get_xticklabels(), visible = False)
	ax1.set_xlabel('')

	def array_from_text_file(filename, dtype = 'float'):
	    import os.path
	    from numpy import array
	    filename = os.path.join(os.path.dirname(__file__), filename)
	    return array([line.split() for line in open(filename).readlines()],
	        dtype = dtype)

	ax2 = fig.add_subplot(312, sharex = ax1)
	import sys, os.path
	ground_truth = os.path.splitext(filename)[0] + '.f0.Corrected'
	if os.path.isfile(ground_truth):
	    ground_truth = array_from_text_file(ground_truth)
	    true_freqs = ground_truth[:,2]
	    true_freqs = ma.masked_where(true_freqs < 2, true_freqs)
	    true_times = float(samplerate) * ground_truth[:,0]
	    ax2.plot(true_times, true_freqs, 'r')
	    ax2.axis( ymin = 0.9 * true_freqs.min(), ymax = 1.1 * true_freqs.max() )
	# plot raw pitches
	ax2.plot(times, pitches, '--g')
	# plot cleaned up pitches
	cleaned_pitches = pitches
	#cleaned_pitches = ma.masked_where(cleaned_pitches < 0, cleaned_pitches)
	#cleaned_pitches = ma.masked_where(cleaned_pitches > 120, cleaned_pitches)
	cleaned_pitches = ma.masked_where(confidences < tolerance, cleaned_pitches)
	ax2.plot(times, cleaned_pitches, '.-')
	#ax2.axis( ymin = 0.9 * cleaned_pitches.min(), ymax = 1.1 * cleaned_pitches.max() )
	#ax2.axis( ymin = 55, ymax = 70 )
	plt.setp(ax2.get_xticklabels(), visible = False)
	ax2.set_ylabel('f0 (Hz)')

	# plot confidence
	ax3 = fig.add_subplot(313, sharex = ax1)
	# plot the confidence
	ax3.plot(times, confidences)
	# draw a line at tolerance
	ax3.plot(times, [tolerance]*len(confidences))
	ax3.axis( xmin = times[0], xmax = times[-1])
	ax3.set_ylabel('condidence')
	set_xlabels_sample2time(ax3, times[-1], samplerate)
	plt.show()

	return jsonify(result={"status": 200})


if __name__ == '__main__':
	app.run(debug=True)
