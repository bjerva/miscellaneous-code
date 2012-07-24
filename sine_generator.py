# create a synthetic 'sine wave' wave file with
# set frequency and length
# tested with Python 2.5.4 and Python 3.1.1 by vegaseat
 
import math
import wave
import struct
import random
import copy
 
def make_soundfile(tone_len=10000, fname="test.wav", 
                   pause_len=1000, freq_list=[], final_freq=400, tones=21):
    """create a synthetic 'sine wave' wave file with frequency freq
    file fname has a length of about data_size * 2"""
    frate = 11025.0 # Framerate as a float
    amp = 8000.0 # Multiplier for amplitude

    #Make sine list
    sine_list = []
    for i in freq_list[:tones]: #Random tones
        for x in range(pause_len):
            sine_list.append(0)
        for x in range(tone_len):
            sine_list.append(math.sin(math.pi*i*(x/frate)))
             
    for x in range(pause_len): 
        sine_list.append(0)   
    for x in range(tone_len): #Final tone
        sine_list.append(math.sin(math.pi*final_freq*(x/frate)))

    for x in range(pause_len): #Final pause
        sine_list.append(0)
     
    #Prepare for file saving
    wav_file = wave.open(fname, "w")
    #Give required parameters
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)*2
    nframes = (tone_len*(len(freq_list)+1)) + (pause_len*(len(freq_list)+2))+pause_len
    comptype = "NONE"
    compname = "not compressed"
    #Set all the parameters at once
    wav_file.setparams((nchannels, sampwidth, framerate, nframes,
    comptype, compname))
    #Write to file
    print( "Please wait..." )
    for s in sine_list:
    #Write the audio frames to filea
        wav_file.writeframes(struct.pack('h', int(s*amp/2)))
    wav_file.close()
    print("%s written" % fname)

def freq_bands(min_v=1000, max_v=4000, step=250):
    bands = [(i, i+2000) for i in range(min_v, max_v+step, step)]
    band_dict = {}
    for i in bands:
        freq_list = [i for i in range(i[0], i[1]+50, 50)]
        avg = freq_list[-1]-freq_list[0]
        avg /= 2
        avg += freq_list[0]
        band_dict[str(avg)] = freq_list
        print str(avg)

    return band_dict
    
#Frequency variables
final_freq = 2500.0
freq_step = 250
bands = freq_bands()
#Low: 1300-2300 (m=1800)
#High: 2300-3300 (m=2800)
#Mid - low variance: 1800-2800 (m=2300)
#Mid - high variance: 1300-3300 (m=2300)
#l_min_freq = 1500
#l_max_freq = 2550
#l_freq_list = [i for i in range(l_min_freq, l_max_freq, freq_step)]
#
#m_min_freq = 2000
#m_max_freq = 3050
#m_freq_list = [i for i in range(m_min_freq, m_max_freq, freq_step)]
#
#h_min_freq = 2500
#h_max_freq = 3550
#h_freq_list = [i for i in range(h_min_freq, h_max_freq, freq_step)]
#Duration is about 4 seconds for a tone_len of 40000
#f_lists = {"L":l_freq_list, "M":m_freq_list, "H":h_freq_list}
raw_input()
tone_len = 1550
pause_len = 660
#Randomising
tones = 21
for level, freq_list in bands.items():
#for i in range(20):
    print "Current level:\t"+str(level)+" ("+str(freq_list[0])+" - "+str(freq_list[-1])+")"
    for i in range(20):
        n_freq_list = copy.deepcopy(freq_list)
        random.shuffle(n_freq_list)
        random.shuffle(n_freq_list)
        print freq_list
        print n_freq_list
        fname = "HV_"+level+"_"+str(i+1)+".wav"
        avg = int(level)
        while (sum(n_freq_list[:tones])/tones not in range(avg-25, avg+25)):
            print "Bad average:\t", sum(n_freq_list[:tones])/tones, "("+str(avg)+")"
            random.shuffle(n_freq_list)
            #raw_input()
        print "Using average:\t", sum(n_freq_list[:tones])/tones
        #continue
        #Write the synthetic wave file to ...
        make_soundfile(tone_len, fname, pause_len, n_freq_list, final_freq, tones)
