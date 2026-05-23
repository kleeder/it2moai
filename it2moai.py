#!/usr/bin/env python3

"""
it2moai, version 0.6
====================

Python 3 only.

Use the example.it or example.mptm file to do your song. When done, run the script to
generate a .🗿 file usable on thirtydollar.website.

Don't change the samples/instruments (.mptm instrument Alternative Tuning may be changed).

Tempo, Ticks/Row and Global Volume are adjustable. Sample Volume does not do anything
(set to 160 by default so that tracker playback sounds closer to Moai website).

Note volume and pan are supported via the volume column. Pan changes are sticky.
Note Cuts ^ will cut all sounds, no matter where they are placed (i.e., be careful with these).

Supported commands:
* Set Speed (Axx)
* Set Tempo (Txx for xx greater than or equal to 32)
* Fine Portamento (EFx/FFx) and Extra Fine Portamento (EEx/EEx) - only for note triggers
* Set Global Volume (Vxx)
* Fine Global Volume Slide (WFx/WxF)

Version history
---------------

* 0.1: Initial creation of program by kleeder
* 0.2: Added global volume initial setting, note volumes, and updated the soundlist to incorporate the 
       current available sounds (list grows from 131 samples to 191). Samples tuned in example module 
       and appropriate offsets added to the soundlist. Adjusted global/sample volume defaults so that
       tracker playback volume sounds closer to moai playback volume.
* 0.3: Module name is no longer hardcoded and must instead be typed in. Output name remains as is.
       Added ability to xenharmonise files during moai conversion to any tone equal temperament tuning
       system. This may be handy for .mptm files with such a tuning.
* 0.4: Support added for Fine/Extra Fine Portamento Down/Up commands (EFx/FFx/EEx/FEx) to detune notes.
       Use only on rows that also contain a note, otherwise the script will break.
* 0.5: Fixed errors on non-existent patterns and notes
* 0.6: Example modules updated with NNA set to Continue.
       Output file is now placed next to input module by default. Added command line parsing.
       Added support for arbitrary ticks/row, panning, new commands (Axx, Txx, Vxx, WFx/WxF).
       Converter edge case improvements: fixed timing of rows with cuts/effects but no notes,
       fixed handling of notes without an instrument and instrument changes without a note.
       Volume changes are emitted as floating point now.
"""

from argparse import ArgumentParser
from sys import stderr, version_info, argv
from pytrax import impulsetracker
import json

def die(msg):
    print(msg, file=stderr)
    exit(1)


if version_info.major < 3:
    die('python3 only!')

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

def convert(module, filename, soundnamelist, tuninglist, edo = 12, origin_note = 0):
    outfile = open(filename, 'w', encoding="utf8")

    tempo = module['inittempo']
    speed = module['initspeed']
    global_volume = module["globvol"]
    sequence = module["orders"]

    outfile.write(f'!speed@{tempo / (speed / 6) * 4}|')
    outfile.write(f'!volume@{global_volume / 128 * 100}|')

    channel_state = []
    for i in range(127):
        channel_state.append({'pan': 32})

    for pattern_number in sequence:
        if pattern_number == 255:
            continue
        # Skip patterns that don't exist
        if len(module["patterns"]) < pattern_number or len(module["patterns"][pattern_number]) < 1:
            continue
        pattern_data = module["patterns"][pattern_number][0]


        for row in pattern_data:
            # we need to handle tempo/global volume changes before writing notes.
            tempo_speed_changed = False
            global_volume_changed = False
            for channel in row:
                cmd = channel.get('command')
                if not cmd:
                    continue
                elif cmd[0] == 'A': # set speed
                    speed = int(cmd[1], 16) * 16 + int(cmd[2], 16)
                    tempo_speed_changed = True
                elif cmd[0] == 'T': # set tempo
                    xx = int(cmd[1], 16) * 16 + int(cmd[2], 16)
                    if xx > 0x20:
                        tempo = xx
                        tempo_speed_changed = True
                elif cmd[0] == 'V': # set global volume
                    xx = int(cmd[1], 16) * 16 + int(cmd[2], 16)
                    if xx <= 128:
                        global_volume = xx
                        global_volume_changed = True
                elif cmd[0] == 'W': # global volume slide
                    if cmd[1] == 'F' and cmd[2] != 'F' and cmd[2] != '0':
                        global_volume = max(0, global_volume - int(cmd[2], 16))
                        global_volume_changed = True
                    if cmd[2] == 'F' and cmd[1] != 'F' and cmd[1] != '0':
                        global_volume = min(128, global_volume + int(cmd[1], 16))
                        global_volume_changed = True

            if global_volume_changed:
                outfile.write(f'!volume@{global_volume / 128 * 100}|')
            if tempo_speed_changed:
                outfile.write(f'!speed@{tempo / (speed / 6) * 4}|')

            note_written = False
            cut_written = False
            for channel in row:
                state = channel_state[channel['channel']]
                note = channel.get("note")
                instrument = channel.get("instrument")
                volpan = channel.get("volpan")

                if note:
                    state['note'] = note

                if instrument:
                    state['instrument'] = instrument
                    state['volume'] = 64 # technically sample default, but the templates all use 64 anyway.
                    # "set pan" sample option unhandled, but we assume the instruments/samples are not modified.
                    if not note: # bare instrument set should cause a retrigger of a previous note.
                        note = state.get('note')
                else:
                    instrument = state.get('instrument')

                if volpan:
                    if volpan <= 64:
                        state['volume'] = volpan
                    elif volpan >= 128 and volpan <= 192:
                        state['pan'] = volpan - 128

                # Skip notes that don't exist
                if not note:
                    continue
                elif note == 254:
                    if not cut_written:
                        outfile.write('!cut|')
                        cut_written = True
                elif instrument:
                    if note_written:
                        outfile.write('!combine|')
                    sample = soundnamelist[instrument-1] # write to the correct instrument as mapped in the soundlist
                    pitch = note-60+tuninglist[instrument-1] # adjust pitch with the offset from the soundlist
                    # if user wants regular tuning, this is skipped, otherwise, the notes are remapped to the new EDO
                    if (edo!=12.0):
                        ratio=12/edo
                        pitch=((pitch-origin_note)*ratio)+origin_note
                    # Checking for Fine/Extra Fine Portamento Down/Up commands (EFx, FFx, EEx, FEx)
                    # Applies a pitch offset (detune) to rows containing both a note and one of these commands
                    # Note that trying to use these commands in a row without a note will break the script
                    if ('command' in channel):
                        if ("EF" in channel["command"]) or ("FF" in channel["command"]) or ("EE" in channel["command"]) or ("FE" in channel["command"]):
                            cmd = channel["command"]
                            pitchoffset = int(cmd[2],16) * 0.0625
                            if (cmd[0]=='F'): pitchoffset = pitchoffset * -1
                            if (cmd[1]=='E'): pitchoffset = pitchoffset / 4
                            pitch = pitch - pitchoffset

                    cur_vol = state['volume'] / 64 * 100
                    cur_pan = (state['pan'] - 32) / 32 * 100

                    outfile.write(sample)
                    # don't bother writing parameters if they are at their default values.
                    if pitch != 0:
                        outfile.write(f'@{pitch}')
                    if cur_vol != 100:
                        outfile.write(f'%{cur_vol}')
                    if cur_pan != 0:
                        outfile.write(f'^{cur_pan}')
                    outfile.write('|')
                    note_written = True

            if not note_written:
                outfile.write('_pause|')

    outfile.close()

if __name__ == '__main__':
    output_path = None
    origin_note = None

    if len(argv) > 1:
        argparser = ArgumentParser()
        argparser.add_argument("input", help="input module (.it or .mptm supported)")
        argparser.add_argument("--output", help="output .🗿 file path, defaults to input filename with moai extension")
        argparser.add_argument("--edo", type=float, default=12, help="equal divisions of the octave, default is 12")
        argparser.add_argument("--origin-note", type=float, help="central semitone to remap all notes around, required if EDO is other than 12")

        args = argparser.parse_args()

        input_path  = args.input
        edo = args.edo
        origin_note = args.origin_note
        output_path = args.output
        if edo != 12 and not origin_note:
            die('origin note must be specified when EDO is not 12')
    else:
        try:
            input_path = input("Enter module name, .it or .mptm file format included: ")
            edo = float(input("Enter desired 'number of equal divisions of the octave': "))
            if edo!=12:
                origin_note = float(input("Enter central semitone to remap all the notes around: "))
        except BaseException as ex:
            die(ex)

    if not output_path:
        if input_path.casefold().endswith('.it'):
            output_path = input_path[:-3] + '.🗿'
        elif input_path.casefold().endswith('.mptm'):
            output_path = input_path[:-5] + '.🗿'
        else:
            output_path = input_path + '.🗿'

    module = impulsetracker.parse_file(input_path, with_patterns=True)
    soundnamelist,tuninglist = get_soundlist("soundlist.json")
    convert(module, output_path, soundnamelist, tuninglist, edo, origin_note)
    print(f"Output written to '{output_path}'", file=stderr)
