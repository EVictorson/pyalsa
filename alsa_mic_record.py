#!/usr/bin/env python

# simple recording from alsaaudio to a wave file
# testing done with the built in microphone (PCH)
# and additional sound card (minidsp USBStreamer, using 4 I2S microphones)
# sudo apt-get install pyalsaaudio

import wave
import numpy as np
import getopt
import os
import alsaaudio as aa
import sys

def usage():
        print 'usage: mic_record.py -n <num_channels> -f <file> -c <card> -v (optional)'
	print '-n: number of microphones recording from'
	print '-f: file to save wave file to'
	print '-c: name of audio card, if using USBStreamer use "USBStreamer"'
	print '-v: verbose, print out mean data on channel 1 as being recorded'
	print '-r: data rate, 44100 is nominal'
        file = sys.stderr
        sys.exit(2)

output_enable = False

opts, args = getopt.getopt(sys.argv[1:], 'n:f:c:r:-v')
for o, a in opts:
        if o == '-n':
                num_channels = int(a)
        elif o == '-f':
                file_name = a
	elif o == '-c':
		card_id = a
	elif o == '-r':
		data_rate = int(a)
	elif o == '-v':
		output_enable = True
			
if not opts:
        usage()

# print out the detected audio cards
print 'available cards are indicated after u and inside single quotes: '
print aa.cards()

# set the audio card accordingly
card_info = {}
for device_number, card_name in enumerate(aa.cards()):
    card_info[card_name] = "hw:%s,0" % device_number

device = aa.PCM(device=card_info[card_id])

# setup the alsa audio object
inp = aa.PCM(aa.PCM_CAPTURE)
inp.setchannels(num_channels)
inp.setrate(data_rate)
inp.setformat(aa.PCM_FORMAT_S16_LE)
inp.setperiodsize(512)

w = wave.open(file_name, 'w')
w.setnchannels(num_channels)
w.setsampwidth(2)
w.setframerate(data_rate)

while True:
    l, data = inp.read()
    a = np.fromstring(data, dtype='int16')
    if output_enable:
        print np.abs(a).mean()
    # the below line will show the entire array
    #print numpy.abs(a)
    w.writeframes(data)


