0#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 20:19:55 2024

@author: yarov3so
"""
import sounddevice as sd
import numpy as np
import time

from config import delay,ccpt,cplb,sensitivity,vox_factor,capture_quality_gauge_resolution,min_score,max_msg_length_factor,sample_length,visualizer_sensitivity,max_length_bar,visualizer_sensitivity_adj,init_cutoff,pretrans_tone_dur,pretrans_tone_freq,vox_mod,visualizer_sensitivity_detector_refinement

fs=44100
sd.default.samplerate = 44100

samples=np.arange(0,int(44100))
pretrans_tone = (np.sin(2 * np.pi * pretrans_tone_freq *samples/len(samples))).astype(np.float32)

print("ParrotPeater 1.0 alpha")
print('Developer: yarov3so (VA2ZLT)')
print('')
print("ATTENTION: Please make sure that your Pythion interpreter/terminal has been granted access to your microphone prior to running this program. ")
print('')
print("--> macOS users: see note on using 'ttcplus wrapper hotfix' (gslegendre).")
print('')
devicelist=list(sd.query_devices())

if ccpt=='':
    print(sd.query_devices())
    print('')
    ccpt=input('Please select the audio capture device you wish to use from the list above by entering its index: ')
    print('')
    #list(sd.query_devices())
    cpt=devicelist[int(ccpt)]['name']

else:
    cpt=devicelist[int(ccpt)]['name']
    
if cplb=='':
    print('')
    print(sd.query_devices())
    print('')
    cplb=input('Please select the audio playback device you wish to use from the list above by entering its index: ')
    #list(sd.query_devices())
    plb=devicelist[int(cplb)]['name']
    print('')
    
else:
    plb=devicelist[int(cplb)]['name']

sd.default.device = (cpt,plb)
sd.default.channels = (devicelist[int(ccpt)]['max_input_channels'],devicelist[int(ccpt)]['max_output_channels'])

print('Capture device selected:',cpt)
print('Playback device selected:',plb)

vox_factor=10**vox_factor
vox_mod=10**vox_mod
sens_factor=(1-10*np.log10((100-sensitivity)/100))

# We need to establish the baseline noise level for our retransmission protocol

baseline_rec=[]
while True:
    i=3
    print('')
    print('Measuring baseline noise...')
    baseline_rec=sd.rec(int(1*fs))[int(init_cutoff):]
    sd.wait()
    while sens_factor*np.std(abs(baseline_rec))>np.mean(abs(baseline_rec)) and i>0:
        print(f'Excessive noise from the audio capture device detected! Attempting to measure baseline noise again... ({i})')
        baseline_rec=sd.rec(int(1*fs))[int(init_cutoff):]
        sd.wait()
        i-=1
    
    if sens_factor*np.std(abs(baseline_rec))>np.mean(abs(baseline_rec)):
        print('')
        attempt=input("Baseline noise measurement failed! Reduce sensitivity, reduce background noise, increase the squelch setting on your transceiver or restart the program and select a different audio input device. Attempt again? (y/n): ")
        if attempt != 'y':
            break #remember to NOT go into transmission loop
    if sens_factor*np.std(abs(baseline_rec))<=np.mean(abs(baseline_rec)):
        print('Baseline noise level established')
        mean_noise=np.mean(abs(baseline_rec))
        break
    
sd.stop()

if visualizer_sensitivity=='': # crude way to set visualizer sensitivity...
    i=0
    n=visualizer_sensitivity_detector_refinement
    visualizer_sensitivity=0
    while visualizer_sensitivity*mean_noise<1:
        i+=1
        visualizer_sensitivity=10**(i/n)
    visualizer_sensitivity/=10**(2+visualizer_sensitivity_adj)

time.sleep(1)
print('Visualizer sensitivity:',(visualizer_sensitivity))
time.sleep(1)
print('')

time.sleep(0.2)

print('Hooray! ParrotPeater is ACTIVE')
print('')

time.sleep(0.5)

drawing=["     (\\      ","    (  \\  /(o)\\  ","    (   \\/  ()/ /) ","    (   \\/  ()/ /)  ","     (   `;.))'\\\".) ","      `(/////.-'","   =====))=))===() ","     ///'   ","    //   ","   '       "]
for line in drawing:
    print(line)
    time.sleep(0.1)

print('')
time.sleep(0.4)

print('Maximum duration of a retransmitted signal:',max_msg_length_factor*capture_quality_gauge_resolution*sample_length,'seconds','| ( can be adjusted in the config file by choosing a different value for max_msg_length_factor )' )

print('')

time.sleep(1)

tx=False
rx=True
vox_mod_original=vox_mod

def limiter(num):
    return max_length_bar*(1-np.exp(-num))

while True:
    
    while rx==True:
        
        marker=True
        timer=0
        timer_msg=0
        score=0
        msg=[]
        stop_recording=False
        terminate_flag=False
        
        def callback(indata, frames, time, status):
            
            global marker
            global timer
            global score
            global msg
            global min_score
            global transmit
            global terminate_flag
            global timer_msg
            global rx
            global tx
            global vox_mod
            
            
            if timer_msg==max_msg_length_factor:
                terminate_flag=True
                rx=False
                tx=True
                raise sd.CallbackAbort
                
                
            elif np.mean(abs(indata.copy()))>=(vox_factor)*(vox_mod)*mean_noise and marker==True: 
                msg.append(indata.copy())
                print('|'+("="*int(limiter(visualizer_sensitivity*np.mean(abs(indata.copy()))))))
                marker=False
                timer+=1
                score+=1
                
            else:
                if marker==False and np.mean(abs(indata.copy()))>=vox_factor*mean_noise and timer<capture_quality_gauge_resolution:
                    #print("Listening... +1")
                    print('|'+("="*int(limiter((visualizer_sensitivity)*np.mean(abs(indata.copy()))))))
                    timer+=1
                    score+=1
                    msg.append(indata.copy())
                elif marker==False and np.mean(abs(indata.copy()))<vox_factor*mean_noise and timer<capture_quality_gauge_resolution:
                    #print("Listening... +0")
                    print('|'+("="*int(limiter((visualizer_sensitivity)*np.mean(abs(indata.copy()))))))
                    timer+=1
                    msg.append(indata.copy())
                    
                if score>=min_score and timer==capture_quality_gauge_resolution:
                    print('|'+("="*int(limiter((visualizer_sensitivity)*np.mean(abs(indata.copy()))))))
                    timer=0
                    score=0
                    vox_mod=0
                    msg.pop()
                    timer_msg+=1
                    callback(indata, frames, time, status)
                    
                if score<min_score and timer==capture_quality_gauge_resolution:
                    terminate_flag=True
                    rx=False
                    tx=True
                    raise sd.CallbackAbort
                    
                    
             
        sample_rate = 44100
        blocksize = int(44100*sample_length) 
        
        with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate, blocksize=blocksize):
            print('Listening...')
            print('')
            while not terminate_flag:
                sd.sleep(delay) 
                
            vox_mod=vox_mod_original
            msg_rec=np.array([])
            msg_rec=np.concatenate(msg, axis=0) 
            msg_rec=msg_rec[:-int(fs*capture_quality_gauge_resolution*sample_length)+1]
            
            
            print('')
            print('Transmission captured')
            print('')
            print('Retransmitting...')
            print('')
            sd.play(pretrans_tone[0:int(pretrans_tone_dur*len(pretrans_tone))])
            sd.wait()
            sd.play(msg_rec)
            sd.wait()
            
            print(""" 
                  (\           
                (  \  /(o)\     
                (   \/  ()/ /)  
                  (   `;.))'".) 
                  `(/////.-'
                =====))=))===() 
                  ///'       
                //   
                '            
            """)
            
        while tx==True:
            
            
            print('Done!')
            print('')
            
            tx=False
            rx=True