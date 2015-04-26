# Voice-Classification
Gender Classification of voice

Pre-requisite :

1.Aubio
	apt-get install aubio-tools libaubio-dev libaubio-doc

2.sklearn (scikit-learn)
	pip install -U scikit-learn or apt-get install python-sklearn

To run the program :

1. Run server . 
  
  python serverg.py

2. Run Client
  
  python clientg.py

Currently it classify the .wav files send from the client. Make sure before you run this program you already have the  .wav files in your /server/sample folder.

TODO:

Add the record button at the client.
