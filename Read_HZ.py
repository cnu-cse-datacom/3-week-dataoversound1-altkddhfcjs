from __future__ import print_function

import sys
import wave

import alsaaudio
import colorama
import numpy as np

from reedsolo import RSCodec, ReedSolomonError
from termcolor import cprint
from pyfiglet import figlet_format

def dominant(frame_rate, chunk):
    w = np.fft.fft(chunk)
    freqs = np.fft.fftfreq(len(chunk))

    peak_coeff = np.argmax(np.abs(w))
    peak_freq = freqs[peak_coeff]
    return abs(peak_freq * frame_rate) # in Hz

def listen_linux(frame_rate=44100, interval=0.1):
    mic = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
    mic.setchannels(1)
    mic.setrate(44100)
    mic.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    num_frames = int(round((interval / 2) * frame_rate))
    mic.setperiodsize(num_frames)

    in_packet = False
    packet = []

    while True:
        l, data = mic.read()
        if not l:
            continue

        chunk = np.fromstring(data, dtype=np.int16)
        dom = dominant(frame_rate, chunk)
        if dom > 400: print(dom)

if __name__ == '__main__':
    colorama.init(strip=not sys.stdout.isatty())

    #decode_file(sys.argv[1], float(sys.argv[2]))
    listen_linux()
