# it2moai

version 0.2
----------------------
Python 3 only.

Use the example.it file to do your song.
Don't change the samples/instruments.
Only notes and volume settings are parsed (no commands)
Note Cuts ^ will cut all sounds, no matter where they are placed (i.e., be careful with these)

Initial settings:
Initial Tempo: adjustable
Ticks/Row: 3 (fixed, do not change)
Initial Global Vol: adjustable (template set at 60)
Sample Volume: 160 (this may be adjusted but does not affect the output, it is 
       set so that tracker output during playback sounds closer to Moai website output)

Version history
---------------

* 0.1: Initial creation of program by kleeder
* 0.2: Added global volume initial setting, note volumes, and updated the soundlist 
       to incorporate the        current available sounds (list grows from 131 
       samples to 191). Samples tuned in example module and appropriate offsets 
       added to the soundlist.

soundlist.json contains the listing of samples in order along with their ids 
and name fields. Both of those fields can be ingested by thirtydollar.website, 
but the tool prefers the emoji icons where available. The soundlist also includes 
an order (for readability only) and a tuning offset to account for tuning 
adjustment made in OpenMPT. 

Module file example.it contains all the samples available on thirtydollar.website at time of 
writing (4/20/23). These have been rearranged alphabetically 
by source file name in the module with these naming convention groupings:
c_<samplename> = chords or multi tonal sounds (fifths, etc.)
n_<samplename> = note (single tonal) sounds
perc_<samplename> = percussion sounds
r_<samplename> = riff sounds 
sfx_<samplename> = sound fx or misc. sounds

Required: https://github.com/ramen/pytrax