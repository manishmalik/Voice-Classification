# In Case Of Emergency


### This application needs the following to run:
* scikit-learn
* pyaudio
* aubio
* flask


### How to run the program:
* Start the server:  
```bash
$python flaskserv.py
```
**Wait** for the classifier to finish training, this may take a while depending on your machine.

* Start the client
```bash
$python userclient.py
```
At this point record your five second clip, it will be recorded locally into a file called `output.wav` and also transmitted over the network to the server for analysis where another file called `output.wav` shall be created. Note that since the server is constantly running, we shall only need to train the classifier once. *You don't need to touch anything or send any arguments.*

The gender output is currently printed on the server side, and the graph is also seen on the server, and the client is sent a `{200: OK}` response.

As usual, we do not tell age.<br/>
I haven't tested it with the entire sample set right now.
