#!/usr/bin/env python

# https://rsmith.home.xs4all.nl/miscellaneous/filtering-a-sound-recording.html
# sudo apt-get install pyalsaaudio

import sys
import time
import alsaaudio as aa
import matplotlib.pyplot as plt
import wave
import numpy as np
import getopt
import os

def usage():
    	print 'usage: wave_plot.py -n <num_channels> -f <file>'#, file=sys.stderr
    	file = sys.stderr
	sys.exit(2)

def channel_plot(signal, num_channels):
	
	# assuming 44.1 kHz sampling
	rate = 44100.0

	if num_channels == 1:
	
        	plt.figure(1)
        	x = np.arange(len(signal))
        	plt.plot(x,signal)
        	plt.xlabel('Sample Number')
        	plt.ylabel('Amplitude')
        	plt.title('Mono Mic Data')
	
	if num_channels == 2:
	
        	left = signal[0::2]
        	right = signal[1::2]
	
        	plt.figure(1)
        	plt.subplot(1,2,1)
        	x1 = np.arange(len(left))
        	plt.plot(x1,left)
        	plt.xlabel('Sample Number')
        	plt.ylabel('Amplitude')
        	plt.title('Left Channel')
	
        	plt.subplot(1,2,2)
        	x2 = np.arange(len(right))
        	plt.plot(x2,right)
        	plt.xlabel('Sample Number')
        	plt.ylabel('Amplitude')
        	plt.title('Right Channel')
        	plt.show()
	
        	plt.figure(2)
        	plt.plot(x1/rate,left,x2/rate,right)
        	plt.title('Stereo')
		plt.xlabel('Time (s)')
		plt.ylabel('Amplitude')
		plt.show()
		
	
	if num_channels == 4:	
        	left = signal[0::4]
        	right = signal[1::4]
        	rear_left = signal[2::4]
        	rear_right = signal[3::4]
	
        	plt.figure(1)
        	plt.subplot(2,2,1)
        	x1 = np.arange(len(left))
		plt.plot(x1,left)
        	plt.xlabel('Sample Number')
        	plt.ylabel('Amplitude')
        	plt.title('Front Left Channel')
	
        	plt.subplot(2,2,2)
        	x2 = np.arange(len(right))
        	plt.plot(x2,right)
        	plt.xlabel('Sample Number')
        	plt.ylabel('Amplitude')
        	plt.title('Front Right Channel')
	
        	plt.subplot(2,2,3)
        	x3 = np.arange(len(rear_left))
        	plt.plot(x3, rear_left)
        	plt.xlabel('Sample Number')
        	plt.ylabel('Amplitude')
        	plt.title('Rear Left Channel')

        	plt.subplot(2,2,4)
        	x4 = np.arange(len(rear_right))
        	plt.plot(x4, rear_right)
       		plt.xlabel('Sample Number')
       		plt.ylabel('Amplitude')
        	plt.title('Rear Left Channel')

	        plt.show()

		plt.figure(2)
                ch1, = plt.plot(x1/rate, left, label = 'Front Left')
		ch2, = plt.plot(x2/rate, right, label = 'Front Right')
		ch3, = plt.plot(x3/rate, rear_left, label = 'Rear Left')
		ch4, = plt.plot(x4/rate, rear_right, label = 'Rear Right')
		
		
		plt.title('All Channels')
		plt.ylabel('Amplitude')
		plt.xlabel('Time (s)')

		plt.legend(handles = [ch1, ch2, ch3, ch4])

		
		plt.show()


if __name__ == '__main__':

	opts, args = getopt.getopt(sys.argv[1:], 'n:f:')
    	for o, a in opts:
	      	if o == '-n':
            		num_channels = int(a)
		elif o == '-f':
			filename = os.getcwd() + '/' +a
	if not opts:
		usage()

	data = wave.open(filename, 'rb')

	signal = np.fromstring(data.readframes(-1), dtype=np.int16)
	
	channel_plot(signal, num_channels)
