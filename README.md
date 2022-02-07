# it2moai

Converter which takes multi-channel ImpulseTracker modules as input and outputs a .🗿 file
which can be played back in the [moai online tool](https://gdcolon.com/%F0%9F%97%BF). The [Pytrax/impulsetracker-parser library](https://github.com/ramen/pytrax) is used and
slightly modified to work with Python 3.

-------

## Features & Limits
- all samples are supported, multi-channel
- the instruments may not be changed, they are used for proper conversion
- no volume, loop or effect support
- please keep in mind the online tool starts lagging quickly with multiple combined notes
- theres a [userscript](https://greasyfork.org/en/scripts/439347-thirty-dollar-rewrite?t=3tAKFxcFgwaQNXTXVB8cww&s=09) which fixes the issue. Directly implemented in [this web version](https://kleeder.de/files/moai/%F0%9F%97%BF.html).
- Note Cuts cut all sounds, no matter where they are placed
- Initial Tempo may be changed, but not the Initial Ticks.
-------

## Installation & Usage
- download/clone repo 
- make sure Python 3 is installed
- write your song using the test.it (follow the limits listed above)
- convert your song with
  ```bash
   python it2moai.py
  ```
- you may not change the name of your .it, because it is hardcoded

-------
## Version history

* 0.1: Initial creation of program.