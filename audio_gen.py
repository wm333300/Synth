## Audio Generator

import numpy as np
from scipy import signal
import pygame as pg

duration = 10
sampling_frequency = 44100

wave_types = {0: "Sin", 1: "Square", 2: "Sawtooth", 3: "Triangle", 4: "Saw+Tri",
              5: "Chirp"}

delay_times = {0: 1/3, 1: 1/4, 3: 1/6, 4 : 1/8}

def time_array_gen(dur=duration, fs=sampling_frequency):
    return np.linspace(0, duration, duration*sampling_frequency)

time_array = time_array_gen()

def sin_wave(f):
    res = np.cos(2*np.pi*f*time_array)
    return res

def square_wave(f):
    res = signal.square(2 * np.pi * f * time_array)
    return res

def sawtooth_wave(f):
    res = signal.sawtooth(2 * np.pi * f * time_array)
    return res

def triangle_wave(f):
    res = signal.sawtooth(2 * np.pi * f * time_array, 0.5)
    return res

def sw_tr(f):
    res = signal.sawtooth(2 * np.pi * f * time_array, 0.5) + signal.sawtooth(2 * np.pi * f * time_array, 0.5)
    return res

def chirp(f):
    res = signal.chirp(time_array, f0=f, f1=f/3, t1=duration)
    return res


def final_array(wave):
    fin_array = []
    fin_array = np.asarray([32767*wave, 32767*wave]).T.astype(np.int16)
    return np.asarray(fin_array)    

def signal_crush(n, s):
    return signal.decimate(s, n) 

def echoes(arr, delay_sec,  a):
    fil = np.zeros(int(delay_sec*sampling_frequency+1))
    fil[0] = 1
    fil[int(delay_sec*sampling_frequency)] = a
    output = np.convolve(arr, fil, 'same')
    return output


def pyg_sound(freq, wave_type, delayed, w = []):    
    init_wave = []
    if wave_type==0:
        init_wave = sin_wave(freq)
    if wave_type==1:
        init_wave = square_wave(freq)
    if wave_type==2:
        init_wave = sawtooth_wave(freq) 
    if wave_type==3:
        init_wave = triangle_wave(freq)
    if wave_type==4:
        init_wave = sw_tr(freq)
    if wave_type==5:
        init_wave = chirp(freq)
    init_wave = init_wave/max(np.abs(init_wave))  
    w = final_array(init_wave)
    sound = pg.sndarray.make_sound(w.copy()) 
    
    
    return sound
    

