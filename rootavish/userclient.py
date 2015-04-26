import json
import pyaudio
import wave
import urllib2, urllib
import os, base64

CHUNK = 1024
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2
RATE = 44100 #sample rate
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data) # 2 bytes(16 bits) per channel

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

length = os.path.getsize(WAVE_OUTPUT_FILENAME)

testcase = open(WAVE_OUTPUT_FILENAME,'rb').read()
request = urllib2.Request('http://localhost:5000/classify/',json.dumps({WAVE_OUTPUT_FILENAME: base64.b64encode(testcase)}))
#request.add_header('Content-Length', '%d' % length)
request.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(request)

print response
