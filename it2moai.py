#!/usr/bin/env python

"""
it2moai.py, version 0.2
----------------------

Python 3 only.

Use the example.it file to do your song. When done, run this 
script and it will generate an output.moai file usable by 
thirtydollar.website.

Don't change the samples/instruments.
Only notes and volume settings are parsed (no commands)
Note Cuts ^ will cut all sounds, no matter where they are placed (i.e., be careful with these)

Initial settings:
Initial Tempo: adjustable
Ticks/Row: 3 (fixed, do not change)
Initial Global Vol: adjustable (template set at 60)
Sample Volume: 160 (this may be adjusted but does not affect the output, it is set so that tracker output during playback sounds closer to Moai website output)

Version history
---------------

* 0.1: Initial creation of program by kleeder
* 0.2: Added global volume initial setting, note volumes, and updated the soundlist to incorporate the 
       current available sounds (list grows from 131 samples to 191). Samples tuned in example module 
       and appropriate offsets added to the soundlist. Adjusted global/sample volume defaults so that
       tracker playback volume sounds closer to moai playback volume.
"""

from sys import stderr, version_info
from pytrax import impulsetracker
import json
import math

def die(msg):
    if isinstance(msg, BaseException):
        msg = str(msg)
    stderr.write(str(msg) + '\n')
    exit(1)


if version_info.major < 3:
    die('python3 only!')


MODULE = "example.it"
SOUNDLIST = "soundlist.json"


def get_soundlist(soundlist_file):
    file = open(file=soundlist_file, encoding="utf8")
    soundlist = json.load(file)
    soundnamelist = []
    tuningoffsetlist = []
    # After populating instrument names, 
    # load the file again to get a list of tuning offsets. Samples were tuned to C in the tracker, and offset in the soundlist accordingly to keep them aligned with the tunings 
    # of the source files on thirtydollar.website.
    for x in soundlist:
        soundnamelist.append(x["name"])        
        tuningoffsetlist.append(x["tuningoffset"]) 
    return soundnamelist,tuningoffsetlist

def convert(module, filename, soundnamelist, tuninglist):
    try:
        outfile = open(filename, 'w', encoding="utf8")
    except BaseException as ex:
        die(ex)

    inittempo = (module["inittempo"])*8
    initvol = math.floor((module["globvol"])/128*100) # change global volume to a percentage
    sequence = module["orders"]

    outfile.write('!speed@{}|'.format(inittempo))
    outfile.write('!volume@{}|'.format(initvol))    

    for pattern_number in sequence:
        if pattern_number != 255:
            pattern_data = module["patterns"][pattern_number][0]
            for row in pattern_data:
                channel_amount = len(row)
                if channel_amount > 0:
                    for channel in row:
                        channel_amount = channel_amount - 1
                        note = channel["note"]
                        try:
                            cur_vol = math.floor(channel['volpan']/64*100) # change note volume setting to a floored percentage
                        except:
                            cur_vol = 100
                                                
                        if note == 254:
                            outfile.write('!cut|')
                        else:
                            instrument = channel["instrument"]
                            sample = soundnamelist[instrument-1] # write to the correct instrument as mapped in the soundlist
                            pitch = note-60+tuninglist[instrument-1] # adjust pitch with the offset from the soundlist

                            # If the note is at default sample pitch offset of 0, don't bother writing pitch (for cleaner json)
                            # If the note volume is set to 100%, don't bother writing (for cleaner json + improved readability of volume settings in UI)
                            if (cur_vol==100):
                                if (pitch==0):
                                    outfile.write(sample + '|')
                                else:
                                    outfile.write(sample + '@' + str(pitch) + '|')
                            else:
                                if (pitch==0):
                                    outfile.write(sample + "%" + str(cur_vol) + '|')
                                else:
                                    outfile.write(sample + '@' + str(pitch) + "%" + str(cur_vol) + '|')
                                
                            if channel_amount > 0:
                                outfile.write('!combine|')
                else:
                    outfile.write('_pause|')

    outfile.close()


module = impulsetracker.parse_file(MODULE, with_patterns=True)
soundnamelist,tuninglist = get_soundlist(SOUNDLIST)
convert(module, 'output.🗿', soundnamelist, tuninglist)
