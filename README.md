            Welcome to ParrotPeater! 
    -- your personal HAM radio companion --
              by yarov3so (VA2ZLT)


                  (\           
                (  \  /(o)\     
                (   \/  ()/ /)  
                  (   `;.))'".) 
                  `(/////.-'
                =====))=))===() 
                  ///'       
                //   
                '            

ParrotPeater allows you to turn a single handheld amateur radio transceiver into a repeater. 
To run this applicaton, you need to have a working Python IDE instealled, along with the libraries NumPy and sounddevice. 
You will also need an APRS cable to connect your radio to your computer's sound card (APRS-K1 if you are using a Baofeng UV 17 Pro).

QUICK DEMONSTRATION (video): https://drive.google.com/file/d/1TmtDIhJIyx5-4ljhzfINe1OYly3Yv8nu/view?usp=share_link

INSTRUCTIONS 

# Default configurtion values are suitable for running ParrotPeater with the following hardware and software setup:
    
Macbook Air M1 (2020) with a Baofeng UV 17 Pro connected to the laptop's headphone jack with an APRS-K1 cable  
Recommended Python IDE: Spyder  
Recommended output volume setting on the laptop: maximum (100%)  
Recommended input volume setting on the laptop: maximum (100%)  
Recommended volume setting on the repeater radio: 1/2 turn of the volume knob (50%)  

MACOS USERS: you will most likely need to apply the ttcplus wrapper hotfix (by gslegendre) to your Python IDE in order to grant it access to your microphone. Please see: https://github.com/jslegendre/tccplus.

*** The following configurations are primarily suited for Baofeng UV 17 Pro HTs, but can be readily generalized to other devices with similar features. ***

# In order to successfully use ParrotPeater, you will need to ensure that the settings on your radio match the following values:
    
       Repeater radio: 
    
       SQL: 1
       SAVE: OFF (battery saving mode must be off on ALL radios!)
       VOX: 1
       TDR: OFF 
       R-CTCS: OFF 
       R-DCS: OFF
       T-CTCS: OFF
       T-DCS: OFF
       BCL: ON 
    ** OFFSET: 0.6-1Mhz recommended, but can be any non-zero value
       VOX DELAY: 0.5 (use lowest value possible)
       ACTIVE FREQUENCY: Only ONE active frequency will be used during the repeater's operation. VFO mode is assumed.
                         Choose an unoccupied frequency and write it down (henceforth referred to as F)
     * SFT-D: ON(+ or -) Make sure that SFT-D is active for the chosen frequency!

       Distant radios (those that talk to the repeater):
    
       SQL: 1
       SAVE: OFF (Battery saving mode must be off on ALL radios!)
       VOX: OFF (Reduce spurious signals! Do NOT use VOX on distant radios!)
       TDR: OFF 
       R-DCS: OFF
       T-CTCS: OFF
       T-DCS: OFF
       BCL: ON 
    ** OFFSET: THE SAME as that of the repeater 
       VOX DELAY: 0.5 (use lowest value possible)
       ACTIVE FREQUENCIES: BOTH active frequencies will be used in this setup.

                          Set the top active frequency to ( F - OFFSET ) if the repeater's SFT-D is negative, or set it to ( F + OFFSET ) if the repeater's SFT-D is positive
                        * SFT-D: OFF for top active frequency
                          R-CTCS: OFF

                          Set the bottom active frequency to the SAME frequency as the top channel
                        * SFT-D: ON with sign OPPOSITE to that of the repeater!
                          R-CTCS: ON (choose any tone - this is meant to block the repeater's signal as soon as you are done transmitting, so that you do not hear your own voice retransmitted back to you) 

The following steps should help you get familiar with the proper opertion of your radios when using ParrotPeater.
In following these instructions, it is assumed that you have configured all of your devices according to the information provided above.

# Running ParrotPeater:

1. Adjust the settings on your computer so that it stays awake during ParrotPeater's operation.
2. Turn on your radio (turn the volume knob halfway) and connect it to your computer BEFORE starting your Python IDE and running ParrotPeater.
3. Go to your settings and make sure that the microphone port is selected as audio input device and that it is at maximum volume.
4. Also, make sure that the headphone port is selected as audio output device and that it is at maximum volume as well.
5. If you run into the problem of ParrotPeater cueing itself repeatedly even with high vox_factor/vox_mod parameters, then you should keep the Settings window open during ParrotPeater's operation, with your chosen audio input device selected. If you are using a mac, you should be seeing a yellow/orange microphone icon in the menu bar at all times.
6. Make sure that the 'config.py' file is in the same folder as 'ParrotPeater.py'.
7. Start ParrotPeater by running 'ParrotPeater.py' inside your Python interpreter and select your computer's audio i/o devices that will be interacting with the repeater radio. 
   In the case of an M1 Macbook Air (2020), those devices will usually be:
   
       0 External Microphone, Core Audio (1 in, 0 out)
       1 External Headphones, Core Audio (0 in, 2 out)
   
8. Wait a brief moment for ParrotPeater to calibrate itself.
9. As soon as you see "Listening..." appear on the screen, you may begin communicating using your repeater.

# Strategy for communicating using ParrotPeater:
    
Assuming that you have configured your radios as per the instructions provided, you may be wondering why the distant radios require the use of both of the active frequencies.
The reason for this is that (in most cases), we do not want to hear our signal retransmitted back to us, though we would like to know when ParrotPeater is done retransmitting it.
As such, each person using a distant radio will need to be switching between the active frequencies.

1. The top active frequency is known as the listening and monitoring frequency. Your radio must be set to it at all times when you are not actively trying to communicate.
2. The bottom active frequency is known as the transmitting frequency. You will use the blue button (Baofeng UV 17 Pro) to switch to it in order to transmit to the repeater.
3. When you are done transmitting, you should watch the green LED on top of your radio light up to indicate that ParrotPeater is retransmitting your signal. 
4. At this point, you should not be hearing your voice (this is the reason we turned on R-CTCS for the bottom active channel).
5. When the green light goes out, press the blue button to switch back to the top active channel as you await a reply.
6. Bear in mind that there will be a significant delay before you hear a reply, as ParrotPeater cannot receive and transmit simultaneously.
7. Once a reply is heard, repeat steps 1 through 5 to transmit again. 
8. PRACTICE, PRACTICE, PRATICE! Switching between the two active frequencies correctly will take some getting used to, but I am sure you will become a master Parroteer in no time. ^^

Feel free to experiment with different parameter values in the 'config.py' file and tweak them to your liking. The amateur radio hobby is, after all, firmly grounded in experimentation. 

Cheers!  
yarov3so (VA2ZLT)
