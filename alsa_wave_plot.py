#!/usr/bin/env python

# simple visualization of data recorded from microphone array
# tested with default microphone (PCH) and minidsp USBStreamer
# with 4 I2S microphone array
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
    	print 'usage: alsa_wave_plot.py -n <num_channels> -f <file>'
    	print '-n: number of channels'
	print '-f: file name to read from (expects a .wav)'
	file = sys.stderr
	sys.exit(2)

def get_fft(signal):
	rate = 44100.0

        Ts = len(signal)/(rate)
        n = len(signal)
        k = np.arange(n)
        T = n/rate
        frq = k/T
        frq = frq[range(n/2)]

        Y = np.fft.fft(signal)/n
        Y = abs(Y[range(n/2)])
	return Y,frq


def fft_plot(signal, num_channels):
	rate = 44100.0

        plt.figure()
        Ts = len(signal)/(num_channels*rate)
        n = len(signal)
        k = np.arange(n)
        T = n/rate
        frq = k/T
        frq = frq[range(n/2)]

        Y = np.fft.fft(signal)/n
        Y = Y[range(n/2)]

        plt.plot(frq, abs(Y))
        plt.xlim(0,1000)
	plt.title('Single Channel FFT')
	plt.xlabel('Frequency (Hz)')
	plt.ylabel('Magnitude')
	plt.show()


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
		plt.show()	
			
		#fft_plot(signal, num_channels)
		Y,frq = get_fft(signal)
		plt.figure(2)
		plt.plot(frq, Y)
		plt.xlim(0,1000)
		plt.title('Mono FFT')
		plt.xlabel('Frequency (Hz)')
		plt.ylabel('Magnitude')
		plt.show()


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

		plt.figure(3)
		Y1, frq1 = get_fft(left)
		Y2, frq2  = get_fft(right)

		plt.subplot(1,2,1)
		plt.plot(frq1, Y1)
		plt.xlabel('Frequency (Hz)')
		plt.ylabel('Magnitude')
		plt.title('Left FFT')
		plt.xlim(0,2000)

		plt.subplot(1,2,2)
		plt.plot(frq2, Y2)
		plt.title('Right FFT')
		plt.xlabel('Frequency (Hz)')
		plt.ylabel('Magnitude')
		plt.xlim(0,2000)
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
        	plt.title('Rear Right Channel')

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

		#TODO:
		# add function for FFTs

                plt.figure(3)
                Y1, frq1 = get_fft(left)
                Y2, frq2 = get_fft(right)
		Y3, frq3 = get_fft(rear_left)
		Y4, frq4 = get_fft(rear_right)

                plt.subplot(2,2,1)
                plt.plot(frq1, Y1)
                plt.xlabel('Frequency (Hz)')
                plt.ylabel('Magnitude')
                plt.title('Left FFT')
                plt.xlim(0,2000)

                plt.subplot(2,2,2)
                plt.plot(frq2, Y2)
                plt.title('Right FFT')
                plt.xlabel('Frequency (Hz)')
                plt.ylabel('Magnitude')
                plt.xlim(0,2000)
                
		plt.subplot(2,2,3)
                plt.plot(frq3, Y3)
                plt.xlabel('Frequency (Hz)')
                plt.ylabel('Magnitude')
                plt.title('Rear Left FFT')
                plt.xlim(0,2000)

                plt.subplot(2,2,4)
                plt.plot(frq4, Y4)
                plt.title('Rear Right FFT')
                plt.xlabel('Frequency (Hz)')
                plt.ylabel('Magnitude')
                plt.xlim(0,2000)

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
	
	print(len(signal))
	
	channel_plot(signal, num_channels)
