from Tkinter import *
from threading import Thread
from os.path import expanduser
import os
import time
import datetime
import tkFont
import pyaudio
import wave


def recoder():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

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
    
    return WAVE_OUTPUT_FILENAME

def rec():
        # global videoFile
        # mydate = datetime.datetime.now()
        # videoFile = mydate.strftime("%d%b_%Hh%Mm.avi")
        # pathSt=os.getcwd()+"/Videos/"
        # l['text']=os.path.expanduser('~')+"/Videos/"
        # l1['text']=videoFile
        b.config(state=DISABLED)
        b1.config(state=ACTIVE)
        t = Thread(target=recorder)
        file_name=t.start()
        global count_flag, secs, mins
        count_flag = True
        secs=0
        mins=0
        while True:
                if count_flag == False:
                        break
                label['text'] = str("%02dm:%02ds" % (mins,secs))
                if secs == 0:
                        time.sleep(0)
                else:
                        time.sleep(1)
                if(mins==0 and secs==1):
                        b1.config(bg="red")
                        b.config(fg="white")
                        b.config(bg="white")
                if secs==6:
                        label['text'] = str("%02dm:%02ds" % (mins,secs))
                        break
                root.update()
                secs = secs+1
        return file_name
def stop():
 
        b.config(state=ACTIVE)
        b1.config(state=DISABLED)
        b1.config(fg="white")
        b1.config(bg="white")
        b.config(fg="white")
        b.config(bg="green")
        global count_flag
        count_flag = False
        # os.system("pkill -n ffmpeg")
        try:
            t.stop()
        except:
            print("")
 
root = Tk()
fontTime = tkFont.Font(family="Helvetica", size=12)
fontButton = tkFont.Font(family="Monospace", size=11,weight="bold")
label = Label(root, text="00m:00s",fg="blue",font="fontTime")
b = Button(root,text="Record",command=rec,state=ACTIVE,bg="green",font="fontButton")
b1 = Button(root,text=" Stop ",command=stop,state=DISABLED,bg="white",font="fontButton")
l = Label(root, text="")
l1 = Label(root, text="")
label.grid(row=0, column=0, columnspan=2)
b.grid(row=1, column=0, padx=1, pady=5)
b1.grid(row=1, column=1, padx=1)
l.grid(row=2, column=0,columnspan=2)
l1.grid(row=3, column=0,columnspan=2)
root.minsize(160,105)
root.maxsize(160,105)
root.title("Voice Recorder")
root.attributes("-topmost", 1)
root.mainloop()
