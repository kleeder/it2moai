#!/usr/bin/env python

# it2moai.py, version 0.1

from sys import stderr, version_info
from pytrax import impulsetracker
import json

def die(msg):
    if isinstance(msg, BaseException):
        msg = str(msg)
    stderr.write(str(msg) + '\n')
    exit(1)


if version_info.major < 3:
    die('python3 only!')


MODULE = "test.it"
SOUNDLIST = "soundlist.json"


def get_soundlist(soundlist_file):
    file = open(file=soundlist_file, encoding="utf8")
    soundlist = json.load(file)
    soundnamelist = []
    for x in soundlist:
        soundnamelist.append(x["name"])

    return soundnamelist


def convert(module, filename, soundnamelist):
    try:
        outfile = open(filename, 'w', encoding="utf8")
    except BaseException as ex:
        die(ex)

    inittempo = (module["inittempo"])*8
    sequence = module["orders"]

    outfile.write('!speed@{}|'.format(inittempo))

    for pattern_number in sequence:
        if pattern_number != 255:
            pattern_data = module["patterns"][pattern_number][0]
            for row in pattern_data:
                channel_amount = len(row)
                if channel_amount > 0:
                    for channel in row:
                        channel_amount = channel_amount - 1
                        note = channel["note"]
                        if note == 254:
                            outfile.write('!cut|')

                        else:
                            instrument = channel["instrument"]
                            sample = soundnamelist[instrument-1]
                            pitch = note-60
                            outfile.write(sample + '@' + str(pitch) + '|')
                            if channel_amount > 0:
                                outfile.write('!combine|')
                else:
                    outfile.write('_pause|')

    outfile.close()


module = impulsetracker.parse_file(MODULE, with_patterns=True)
soundnamelist = get_soundlist(SOUNDLIST)
convert(module, 'output.🗿', soundnamelist)
print("hey i reached the end of the script, the file SHOULD be there now")
