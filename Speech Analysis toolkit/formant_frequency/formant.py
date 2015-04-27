#!/usr/bin/env python
import sys
import numpy
import wave
import math
from scipy.signal import lfilter, hamming
from scikits.talkbox import lpc

"""
Estimate formants using LPC.
"""

def get_formants(file_path):

    # Read from file.
    spf = wave.open(file_path, 'r') # http://www.linguistics.ucla.edu/people/hayes/103/Charts/VChart/ae.wav

    # Get file as numpy array.
    x = spf.readframes(-1)
    x = numpy.fromstring(x, 'Int16')

    # Get Hamming window.
    N = len(x)
    w = numpy.hamming(N)

    # Apply window and high pass filter.
    x1 = x * w
    x1 = lfilter([1], [1., 0.63], x1)
    # Get LPC.

    Fs = spf.getframerate()
    ncoeff = 2 + Fs / 1000
    A, e, k = lpc(x1, ncoeff)


    # Get roots.
    rts = numpy.roots(A)
    rts = [r for r in rts if numpy.imag(r) >= 0]

    # Get angles.
    angz = numpy.arctan2(numpy.imag(rts), numpy.real(rts))

    # Get frequencies.
    Fs = spf.getframerate()
    frqs = sorted(angz * (Fs / (2 * math.pi)))

    return frqs

print get_formants(sys.argv[1])
