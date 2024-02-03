#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 09:47:56 2024

@author: yarov3so
"""

# PARAMETERS 

# Feel free to experiment with your own values if you are up for it, but save a copy of the default config file!
# In most cases, the vox factors (vox_factor and vox_mod) are the only parameter that will require adjustment. 
# Read the descriptions for each parameter before you attempt to make any changes!

# Audio hardware

ccpt='' # Chosen capture device => Write '' if unspecified.
cplb='' # Chosen playback device => Write '' if unspecified.

# Calibration (baseline noise level)

sensitivity=1.5 # Helps get accurate reading of average noise level. A higher number results in higher sensitivity, but may make baseline calibration difficult. Recommended value: 1 or 2
init_cutoff=1*11025 # The number of bits at the beginning of the calibration sample that are ignored. Default value is 11025 (1/4 second).

# Visualizer

visualizer_sensitivity_detector_refinement=100 # Decrease value for coarser automatic visualizer sensitivity detection, increase for more refined detection.
visualizer_sensitivity='' # Sensitivity of visualizer, can (but need not be) specified manually. It need not be an integer. => Write '' if unspecified. ParrotPeater detects an appropriate sensitivity during calibration. 
visualizer_sensitivity_adj=1 # DAMPING FACTOR: Adjustment to the detected sensitivity of visualizer (default value is 2, but 0.5 or 1 may also work). Has no effect when sensitivity is manually set. Higher values lead to shorter bars.
max_length_bar=60 # Maximum length of visualizer bars (max number of '=' signs)

# Audio capture, processing and retransmission parameters

vox_factor=1.5 # A number larger than or equal to 0. Default value: 1.5, but may need to be increased if your repeater-laptop connection is particularly noisy. Remember to pick a value that is not too high, so as to allow ParrotPeater to start listening as soon as the PTT button is pressed on a distant radio.
vox_mod=1 # Solves the problem where the repeater cues itself after retransmission when vox_factor is too low. Has no effect when equal to 0. Increase as needed.
min_score=1 # Minimum quality score for a captured audio clip to be retransmitted. Should be an integer less than capture_quality_gauge_resolution. Default value: 1
delay=100 # Retransmission delay at the end of admitted signal, in milliseconds (may need to be changed depending on your transceiver for best results)
pretrans_tone_freq=1000 # Pretransmission tone frequency, in Hz (default value: 1000Hz)
pretrans_tone_dur=0.15 # Pretransmission tone duration, in seconds (default value: 0.15s, max value is 1s). Necessary to cue the repeater radio via vox without losing the beginning of the retransmitted signal.
capture_quality_gauge_resolution=100 # Larger values better capture the beginning of desired retransmissions, but are more prone to noise. Low value will cause less delay, but could potentially result in more noise being retransmitted. Default value: 100
sample_length=0.01 # Low sample length more prone to noise! Default sample length: 0.01s

max_msg_length_factor=10 # The factor entering in the calculation of maximum duration of a retransmitted signal. IT IS NOT THE DURATION ITSELF. MUST BE AN INTEGER! Opt for relatively low values to avoid tying up the repeater needlessly.
                         # The maximum duration of a retransmitted signal is ALWAYS equal to the product of max_msg_length_factor, capture_quality_gauge_resolution and sample_length. 
                         # Play around with the numbers and see what works for you.
                         # Defult factor: 10 => This results in the maximum duration of retransmitted signal being 10s, as 10s=10*100*0.01s